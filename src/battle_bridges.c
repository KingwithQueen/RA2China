#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

void battle_terrain_seal(ra_battle *b)
{
    if (b->terrain_sealed) return;
    b->initial_count = b->count;
    battle_economy_seal(b);
    battle_campaign_seal(b);
    memcpy(b->initial_tiles, b->tiles, (size_t)2 * b->width * b->height * sizeof(*b->tiles));
    memcpy(b->initial_bridges, b->bridges, (size_t)b->width * b->height);
    memcpy(b->initial_parts, b->bridge_parts, b->bridge_count * sizeof(*b->bridge_parts));
    b->terrain_sealed = true;
}

static bool present(const ra_battle_bridge *p)
{
    return p->kind < 2 ? p->frame < 18 : p->frame < 27;
}

static void surface(ra_battle *b, const ra_battle_bridge *p)
{
    uint32_t n = b->width * b->height;
    if (p->kind >= 2)
    {
        b->tiles[p->cell] = p->under;
        if (present(p))
        {
            b->tiles[p->cell].land = 1;
            b->tiles[p->cell].track = 100;
        }
        else b->tiles[p->cell].blocked = 1;
        return;
    }
    for (int side = -1; side <= 1; ++side)
    {
        int x = (int)(p->cell % b->width) + (p->axis == 2 ? side : 0), y = (int)(p->cell / b->width) + (p->axis == 1 ? side : 0);
        if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
        uint32_t c = (uint32_t)y * b->width + (uint32_t)x;
        b->bridges[c] = (uint8_t)(p->axis | (present(p) ? 4u : 0u));
        b->tiles[n + c] = (ra_battle_tile){100, (uint8_t)(b->tiles[p->cell].height + 4), 0, (uint8_t)!present(p), 1};
    }
}

bool ra_battle_bridge_segment_add(ra_battle *b, uint32_t cell, uint32_t axis, uint32_t kind, uint32_t frame, ra_error *error)
{
    if (!b || !b->tiles || b->terrain_sealed || b->count || b->tick || cell >= b->width * b->height || b->bridge_count == RA_BATTLE_BRIDGES || axis < 1 ||
        axis > 2 || kind > 3 || (kind < 2 ? frame >= 18 && frame != 255 : !frame || frame > 28) || b->tiles[cell].height > 123)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid bridge segment");
    for (int side = kind < 2 ? -1 : 0; side <= (kind < 2 ? 1 : 0); ++side)
    {
        int x = (int)(cell % b->width) + (axis == 2 ? side : 0), y = (int)(cell / b->width) + (axis == 1 ? side : 0);
        if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
        if (b->bridge_at[(uint32_t)y * b->width + (uint32_t)x]) return ra_fail(error, RA_FORMAT, 0, "overlapping bridge segments");
    }
    ra_battle_bridge *p = &b->bridge_parts[b->bridge_count++];
    *p = (ra_battle_bridge){cell, axis, kind, frame, frame, 0, b->tiles[cell]};
    /* 初始地表是桥下原有的 TMP；低桥修复不能把水格永久改成道路。 */
    surface(b, p);
    for (int side = kind < 2 ? -1 : 0; side <= (kind < 2 ? 1 : 0); ++side)
    {
        int x = (int)(cell % b->width) + (axis == 2 ? side : 0), y = (int)(cell / b->width) + (axis == 1 ? side : 0);
        if (x >= 0 && y >= 0 && x < (int)b->width && y < (int)b->height) b->bridge_at[(uint32_t)y * b->width + (uint32_t)x] = b->bridge_count;
    }
    return true;
}

uint32_t battle_bridge_frame(uint32_t frame, bool first, bool removal)
{
    if (frame >= 18) return frame;
    uint32_t base = frame >= 9 ? 9u : 0u, f = frame - base;
    if (base) first = !first;
    /* 原版 554750/554850 与 554960/554d00：两端损坏合并，断口向相邻残段传播。 */
    if (removal)
    {
        if (f <= 6) return base + (first ? 7u : 8u);
        if (f == (first ? 8u : 7u)) return 255;
    }
    else
    {
        if (f <= 3) return base + (first ? 4u : 5u);
        if (f == (first ? 5u : 4u)) return base + 6;
    }
    return frame;
}

static void changed(ra_battle *b, uint32_t index, uint32_t frame, uint32_t killer)
{
    ra_battle_bridge *p = &b->bridge_parts[index];
    if (p->frame == frame) return;
    bool removed = present(p) && (p->kind < 2 ? frame == 255 : frame >= 27);
    /* 先按实际轨迹采样格判定在桥上的对象，不能拿未来预占格当作当前位置。 */
    if (removed)
        for (uint32_t i = 0; i < b->count; ++i)
        {
            ra_battle_unit *u = &b->units[i];
            if (!u->health || (u->traits & (RA_UNIT_LIMBO | RA_UNIT_AIRBORNE))) continue;
            int64_t x = (int64_t)u->x + RA_BATTLE_CELL / 2, y = (int64_t)u->y + RA_BATTLE_CELL / 2;
            if (x < 0 || y < 0 || x >= (int64_t)b->width * RA_BATTLE_CELL || y >= (int64_t)b->height * RA_BATTLE_CELL) continue;
            uint32_t c = (uint32_t)(y / RA_BATTLE_CELL) * b->width + (uint32_t)(x / RA_BATTLE_CELL);
            if (b->bridge_at[c] != index + 1 || ra_battle_unit_layer(b, u) != (p->kind < 2 ? 1u : 0u)) continue;
            u->fall_cell = c;
            u->fall_height = ra_battle_unit_height(b, u);
            u->traits |= RA_UNIT_FALLEN;
            battle_kill(b, u, killer);
            ++b->bridge_falls;
        }
    p->frame = frame;
    p->changed_tick = b->tick;
    ++b->topology_revision;
    if (removed) ++b->bridge_destroyed;
    surface(b, p);
    /* 已提交的曲线也会预占将要消失的格；撤销后从当前实际格重新规划。 */
    for (uint32_t i = 0; removed && i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        bool invalid = false;
        for (uint32_t j = 0; j < u->reserved_count; ++j)
            if (!ra_battle_passable(b, u->reserved[j])) invalid = true;
        u->path_count = u->path_cursor = u->retry = 0;
        if (!u->health || !invalid) continue;
        uint32_t n = b->width * b->height, layer = ra_battle_unit_layer(b, u);
        uint32_t c = (uint32_t)((u->y + (int32_t)RA_BATTLE_CELL / 2) / (int32_t)RA_BATTLE_CELL) * b->width +
                     (uint32_t)((u->x + (int32_t)RA_BATTLE_CELL / 2) / (int32_t)RA_BATTLE_CELL) + layer * n;
        battle_reservations_clear(b, u);
        if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
        if (b->occupied[u->next] == u->id) b->occupied[u->next] = 0;
        u->cell = u->next = c;
        u->x = (int32_t)(c % b->width * RA_BATTLE_CELL);
        u->y = (int32_t)(ra_battle_cell_y(b, c) * RA_BATTLE_CELL);
        u->track_active = u->track_index = u->track_remainder = u->progress = 0;
        u->motion_factor = 0;
        u->speed_factor = 0;
        b->occupied[c] = u->id;
    }
}

static uint32_t neighbor(const ra_battle *b, const ra_battle_bridge *p, int direction)
{
    int x = (int)(p->cell % b->width) + (p->axis == 1 ? direction : 0), y = (int)(p->cell / b->width) + (p->axis == 2 ? direction : 0);
    if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) return 0;
    uint32_t id = b->bridge_at[(uint32_t)y * b->width + (uint32_t)x];
    if (!id) return 0;
    const ra_battle_bridge *q = &b->bridge_parts[id - 1];
    return q->axis == p->axis && q->kind == p->kind && b->tiles[q->cell].height == b->tiles[p->cell].height ? id : 0;
}

static void hit(ra_battle *b, uint32_t id, bool demolish, uint32_t killer)
{
    ra_battle_bridge *p = &b->bridge_parts[id - 1];
    if (!present(p)) return;
    ++b->bridge_hits;
    if (p->kind >= 2)
    {
        uint32_t f = p->frame, frame = f;
        if (f <= 9) frame = demolish || f >= 7 ? 27 : 7;
        else if (f <= 18) frame = demolish || f >= 16 ? 28 : 16;
        else if (f <= 26 && (f & 1)) frame = f + 1;
        /* 低桥横向三格属于同一截面，原版 55def0/55e410 同时更新三格。 */
        for (int side = -2; side <= 2; ++side)
        {
            int x = (int)(p->cell % b->width) + (p->axis == 2 ? side : 0), y = (int)(p->cell / b->width) + (p->axis == 1 ? side : 0);
            if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
            uint32_t other = b->bridge_at[(uint32_t)y * b->width + (uint32_t)x];
            if (!other) continue;
            const ra_battle_bridge *q = &b->bridge_parts[other - 1];
            if (q->kind == p->kind && q->axis == p->axis && q->frame == f) changed(b, other - 1, frame, killer);
        }
        return;
    }
    bool remove = demolish || p->frame % 9 >= 6;
    changed(b, id - 1, remove ? 255 : p->axis == 1 ? 6u : 15u, killer);
    for (int direction = 1; direction >= -1; direction -= 2)
    {
        uint32_t next = neighbor(b, p, direction);
        for (uint32_t limit = 0; next && limit < b->bridge_count; ++limit)
        {
            ra_battle_bridge *q = &b->bridge_parts[next - 1];
            if (!present(q)) break;
            uint32_t frame = battle_bridge_frame(q->frame, direction > 0, remove);
            changed(b, next - 1, frame, killer);
            if (frame != 255) break;
            next = neighbor(b, q, direction);
        }
    }
}

static void repair(ra_battle *b, uint32_t id)
{
    uint32_t queue[RA_BATTLE_BRIDGES], count = 1;
    uint8_t visited[RA_BATTLE_BRIDGES] = {0};
    queue[0] = id;
    visited[id - 1] = 1;
    for (uint32_t cursor = 0; cursor < count; ++cursor)
    {
        ra_battle_bridge *p = &b->bridge_parts[queue[cursor] - 1];
        for (uint32_t j = 0; j < b->bridge_count; ++j)
        {
            const ra_battle_bridge *q = &b->bridge_parts[j];
            if (visited[j] || q->axis != p->axis || q->kind != p->kind || b->tiles[q->cell].height != b->tiles[p->cell].height) continue;
            int dx = abs((int)(p->cell % b->width) - (int)(q->cell % b->width)), dy = abs((int)(p->cell / b->width) - (int)(q->cell / b->width));
            if (dx + dy != 1 || (p->kind < 2 && (p->axis == 1 ? dy : dx))) continue;
            visited[j] = 1;
            queue[count++] = j + 1;
        }
    }
    for (uint32_t i = 0; i < count; ++i)
    {
        ra_battle_bridge *p = &b->bridge_parts[queue[i] - 1];
        uint32_t frame = p->kind < 2 ? (p->axis == 1 ? 0u : 9u) : (p->axis == 1 ? 1u : 10u);
        if (p->kind >= 2 && ((p->original_frame >= 1 && p->original_frame <= 4) || (p->original_frame >= 10 && p->original_frame <= 13)))
            frame = p->original_frame;
        if (p->kind >= 2 && p->original_frame >= 19 && p->original_frame <= 26) frame = (p->original_frame & 1) ? p->original_frame : p->original_frame - 1;
        if (p->frame != frame)
        {
            changed(b, queue[i] - 1, frame, 0);
            ++b->bridge_repaired;
        }
    }
}

bool ra_battle_bridge_event_add(ra_battle *b, uint32_t tick, ra_battle_order kind, uint32_t cell, ra_error *error)
{
    if (!b || tick <= b->tick || tick > 10000000 || kind < RA_EVENT_BRIDGE_HIT || kind > RA_EVENT_BRIDGE_REPAIR || !battle_command_target(b, 0, kind, cell) ||
        b->command_count == RA_BATTLE_COMMANDS || (b->command_count && tick < b->commands[b->command_count - 1].tick))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid bridge scenario event");
    b->commands[b->command_count] = (ra_battle_command){tick, b->command_count + 1, 0, cell, kind};
    ++b->command_count;
    return true;
}

void battle_bridge_event(ra_battle *b, const ra_battle_command *c)
{
    uint32_t id = b->bridge_at[c->target];
    if (c->kind == RA_EVENT_BRIDGE_REPAIR) repair(b, id);
    else hit(b, id, c->kind == RA_EVENT_BRIDGE_DEMOLISH, 0);
}

bool battle_bridge_damage_test(int32_t height, int32_t z, bool low, bool wall, bool demolition, uint32_t damage, uint32_t roll)
{
    if (!low && (!wall || z <= height * 104 + 208 || z > height * 104 + 520)) return false;
    return demolition || roll < damage;
}

void battle_bridge_impact(ra_battle *b, const ra_battle_shot *s)
{
    const ra_battle_weapon *w = &b->types[s->type].weapon;
    int64_t x = (int64_t)s->x + RA_BATTLE_CELL / 2, y = (int64_t)s->y + RA_BATTLE_CELL / 2;
    if (x < 0 || y < 0 || x >= (int64_t)b->width * RA_BATTLE_CELL || y >= (int64_t)b->height * RA_BATTLE_CELL) return;
    uint32_t cell = (uint32_t)(y / RA_BATTLE_CELL) * b->width + (uint32_t)(x / RA_BATTLE_CELL), id = b->bridge_at[cell];
    if (!id || !present(&b->bridge_parts[id - 1])) return;
    const ra_battle_bridge *p = &b->bridge_parts[id - 1];
    int32_t height = b->tiles[p->cell].height, z = s->z / 256;
    /* 先过滤几何和弹头资格，再消耗随机数；严格小于 Damage 才成功。 */
    if (!battle_bridge_damage_test(height, z, p->kind >= 2, w->wall, true, w->damage, 0)) return;
    uint32_t roll = w->bridge_forced ? 0 : battle_random_range(b, 1, b->bridge_strength);
    if (battle_bridge_damage_test(height, z, p->kind >= 2, w->wall, w->bridge_forced, w->damage, roll)) hit(b, id, false, s->owner);
}
