#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

static void put(uint8_t **p, uint32_t value)
{
    for (unsigned i = 0; i < 4; ++i) *(*p)++ = (uint8_t)(value >> (i * 8));
}
static void turn_put(uint8_t **p, const ra_battle_turn *t)
{
    put(p, t->initial);
    put(p, t->target);
    put(p, t->started);
    put(p, t->duration);
}
static void state_hash(const ra_battle *b, uint8_t digest[20], bool initial_economy)
{
    uint8_t *start = ((battle_search *)b->search)->canonical, *p = start;
    uint32_t i, j;
    memcpy(p, b->content, 20);
    p += 20;
    put(&p, RA_BATTLE_VERSION);
    put(&p, RA_BATTLE_HZ);
    put(&p, b->width);
    put(&p, b->height);
    put(&p, b->tick);
    put(&p, b->count);
    put(&p, b->type_count);
    battle_economy_hash(b, initial_economy, &p);
    battle_campaign_hash(b, initial_economy, &p);
    for (i = 0; i < RA_BATTLE_TEAMS; ++i) put(&p, b->allies[i]);
    put(&p, b->command_cursor);
    put(&p, b->rejected);
    put(&p, b->next_shot);
    put(&p, b->fired);
    put(&p, b->impacts);
    put(&p, b->kills);
    put(&p, b->dropped_shots);
    put(&p, b->bridge_count);
    put(&p, b->bridge_strength);
    put(&p, b->topology_revision);
    put(&p, b->bridge_hits);
    put(&p, b->bridge_destroyed);
    put(&p, b->bridge_repaired);
    put(&p, b->bridge_falls);
    for (i = 0; i < b->bridge_count; ++i)
    {
        const ra_battle_bridge *part = &b->bridge_parts[i];
        put(&p, part->cell);
        put(&p, part->axis);
        put(&p, part->kind);
        put(&p, part->frame);
        put(&p, part->original_frame);
        put(&p, part->changed_tick);
        put(&p, part->under.track);
        put(&p, part->under.height | (uint32_t)part->under.ramp << 8 | (uint32_t)part->under.blocked << 16 | (uint32_t)part->under.land << 24);
    }
    put(&p, b->random_a);
    put(&p, b->random_b);
    for (i = 0; i < 250; ++i) put(&p, b->random[i]);
    for (i = 0; i < 2 * b->width * b->height; ++i)
    {
        const ra_battle_tile *t = &b->tiles[i];
        *p++ = (uint8_t)t->track;
        *p++ = (uint8_t)(t->track >> 8);
        *p++ = t->height;
        *p++ = t->ramp;
        *p++ = t->blocked;
        *p++ = t->land;
        put(&p, b->occupied[i]);
        if (i < b->width * b->height) *p++ = b->bridges[i];
    }
    for (i = 0; i < b->type_count; ++i)
    {
        const ra_battle_type *t = &b->types[i];
        const ra_battle_weapon *w = &t->weapon;
        memcpy(p, t->id, 32);
        p += 32;
        memcpy(p, t->faction, 32);
        p += 32;
        put(&p, t->step);
        put(&p, t->rot);
        put(&p, t->strength);
        put(&p, t->armor);
        put(&p, t->uphill);
        put(&p, t->downhill);
        put(&p, t->slowdown);
        put(&p, t->deceleration);
        put(&p, t->acceleration);
        put(&p, t->sight);
        put(&p, t->guard_range);
        for (j = 0; j < 3; ++j) put(&p, (uint32_t)t->flh[j]);
        for (j = 0; j < 5; ++j) put(&p, (uint32_t)t->threat_coefficients[j]);
        put(&p, (uint32_t)t->special_threat);
        put(&p, (uint32_t)t->turret_offset);
        put(&p, t->gate);
        put(&p, t->powered);
        put(&p, t->naval);
        put(&p, t->flying);
        put(&p, t->passive_acquire);
        put(&p, t->passengers);
        put(&p, t->size);
        put(&p, t->size_limit);
        put(&p, t->flight_height);
        put(&p, t->ammo);
        put(&p, t->amphibious);
        put(&p, t->infantry);
        put(&p, t->engineer);
        put(&p, t->c4);
        put(&p, t->capturable);
        put(&p, t->bridge_hut);
        put(&p, t->insignificant);
        put(&p, t->instant_weapon);
        put(&p, t->deploy_type);
        put(&p, t->c4_ticks);
        put(&p, t->structure);
        put(&p, t->foundation_width);
        put(&p, t->foundation_height);
        put(&p, t->height);
        put(&p, (uint32_t)t->power);
        memcpy(p, w->id, 32);
        p += 32;
        memcpy(p, w->projectile, 32);
        p += 32;
        memcpy(p, w->warhead, 32);
        p += 32;
        put(&p, w->minimum);
        put(&p, w->burst);
        put(&p, w->missile);
        put(&p, w->launch_delay);
        put(&p, w->missile_health);
        put(&p, w->altitude);
        put(&p, w->regeneration);
        put(&p, w->damage);
        put(&p, w->rof);
        put(&p, w->range);
        put(&p, w->speed);
        put(&p, w->gravity);
        put(&p, w->spread);
        put(&p, w->percent_at_max);
        put(&p, w->projectile_rot);
        put(&p, w->max_damage);
        put(&p, w->percent_bits);
        for (j = 0; j < 11; ++j) put(&p, w->verses[j]);
        put(&p, w->arcing);
        put(&p, w->cliffs);
        put(&p, w->walls);
        put(&p, w->elevation);
        put(&p, w->high);
        put(&p, w->floater);
        put(&p, w->aa);
        put(&p, w->no_ground);
        put(&p, w->proximity);
        put(&p, w->ranged);
        put(&p, w->arm);
        put(&p, w->wall);
        put(&p, w->bridge_forced);
    }
    for (i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        put(&p, u->carrier);
        put(&p, u->unloading);
        put(&p, u->unload_tick);
        put(&p, u->ammunition);
        put(&p, u->burst_left);
        put(&p, u->flash_until);
        put(&p, u->spawn_ready);
        put(&p, u->gate_open_until);
        put(&p, (uint32_t)u->altitude);
        put(&p, u->subcell);
        put(&p, u->tag);
        put(&p, u->script_team);
        put(&p, u->action_tick);
        put(&p, u->selected_tick);
        put(&p, u->c4_owner);
        put(&p, u->id);
        put(&p, u->type);
        put(&p, u->cell);
        put(&p, u->next);
        put(&p, u->goal);
        put(&p, u->progress);
        put(&p, u->retry);
        put(&p, u->facing);
        put(&p, (uint32_t)u->x);
        put(&p, (uint32_t)u->y);
        put(&p, u->path_count);
        put(&p, u->path_cursor);
        put(&p, u->team);
        put(&p, u->health);
        put(&p, u->target);
        put(&p, u->order);
        put(&p, u->cooldown);
        put(&p, u->speed_factor);
        put(&p, (uint32_t)u->motion_factor);
        put(&p, (uint32_t)(u->motion_factor >> 32));
        put(&p, u->track_control);
        put(&p, u->track_index);
        put(&p, u->track_remainder);
        put(&p, u->track_active);
        put(&p, u->track_via);
        put(&p, u->reserved_count);
        put(&p, u->curve_joins);
        for (j = 0; j < u->reserved_count; ++j) put(&p, u->reserved[j]);
        put(&p, u->shots);
        put(&p, u->kills);
        put(&p, u->destroyed_tick);
        put(&p, u->fall_cell);
        put(&p, u->killer);
        put(&p, (uint32_t)u->fall_height);
        put(&p, u->traits);
        put(&p, u->hidden_from);
        put(&p, u->detected_by);
        put(&p, u->destination);
        put(&p, u->anchor);
        put(&p, u->fire_cell);
        put(&p, u->waypoint_count);
        put(&p, u->waypoint_cursor);
        put(&p, u->waypoint_loop);
        for (j = 0; j < u->waypoint_count; ++j) put(&p, u->waypoints[j]);
        turn_put(&p, &u->body);
        turn_put(&p, &u->turret);
        for (j = 0; j < u->path_count; ++j) put(&p, u->path[j]);
    }
    for (i = 0; i < RA_BATTLE_SHOTS; ++i)
    {
        const ra_battle_shot *s = b->shots ? &b->shots[i] : NULL;
        put(&p, s ? s->active : 0);
        if (!s || !s->active) continue;
        put(&p, s->health);
        put(&p, s->launch_delay);
        put(&p, s->cruise_height);
        put(&p, s->id);
        put(&p, s->owner);
        put(&p, s->target);
        put(&p, s->type);
        put(&p, s->team);
        put(&p, s->age);
        put(&p, s->duration);
        put(&p, s->impact_tick);
        put(&p, s->hit);
        put(&p, s->collision);
        put(&p, s->retired_tick);
        put(&p, s->fuse_distance);
        put(&p, (uint32_t)s->x);
        put(&p, (uint32_t)s->y);
        put(&p, (uint32_t)s->z);
        put(&p, (uint32_t)s->start_x);
        put(&p, (uint32_t)s->start_y);
        put(&p, (uint32_t)s->start_z);
        put(&p, (uint32_t)s->end_x);
        put(&p, (uint32_t)s->end_y);
        put(&p, (uint32_t)s->end_z);
        for (j = 0; j < 3; ++j)
        {
            put(&p, (uint32_t)s->velocity[j]);
            put(&p, (uint32_t)(s->velocity[j] >> 32));
        }
    }
    ra_sha1((ra_view){start, (size_t)(p - start)}, digest);
}
void ra_battle_hash(const ra_battle *b, uint8_t digest[20])
{
    state_hash(b, digest, false);
}
static void initial_hash(const ra_battle *b, uint8_t digest[20])
{
    ra_battle initial = *b;
    initial.tiles = b->terrain_sealed ? b->initial_tiles : b->tiles;
    initial.bridges = b->terrain_sealed ? b->initial_bridges : b->bridges;
    initial.bridge_parts = b->terrain_sealed ? b->initial_parts : b->bridge_parts;
    initial.topology_revision = initial.bridge_hits = initial.bridge_destroyed = initial.bridge_repaired = initial.bridge_falls = 0;
    initial.tick = initial.command_cursor = initial.rejected = 0;
    initial.units = b->initial;
    initial.count = b->terrain_sealed ? b->initial_count : b->count;
    /* 初始占格在寻路临时区重建，不能引用已结束战斗的当前占格。 */
    initial.occupied = ((battle_search *)b->search)->position;
    memset(initial.occupied, 0, (size_t)2 * b->width * b->height * sizeof(*initial.occupied));
    battle_initial_occupancy(&initial, initial.occupied);
    initial.shots = NULL;
    initial.next_shot = initial.fired = initial.impacts = initial.kills = initial.dropped_shots = 0;
    battle_random_reset(&initial);
    if (b->campaign && b->terrain_sealed) memcpy(initial.allies, b->campaign->initial.allies, sizeof(initial.allies));
    state_hash(&initial, digest, b->terrain_sealed);
}
bool ra_battle_replay_write(ra_battle *b, uint8_t **bytes, size_t *size, ra_error *error)
{
    uint8_t *data, *p, digest[20];
    size_t length;
    if (!b || !b->tiles || !bytes || !size || b->command_cursor != b->command_count)
        return ra_fail(error, RA_ARGUMENT, 0, "apply pending commands before saving replay");
    battle_terrain_seal(b);
    length = 124 + (size_t)(b->initial_count + b->command_count) * 20;
    data = calloc(length, 1);
    if (!data) return ra_fail(error, RA_MEMORY, 0, "replay allocation failed");
    memcpy(data, RA_BATTLE_REPLAY_MAGIC, 8);
    p = data + 8;
    put(&p, RA_BATTLE_VERSION);
    put(&p, RA_BATTLE_HZ);
    put(&p, b->width);
    put(&p, b->height);
    put(&p, b->initial_count);
    put(&p, b->command_count);
    put(&p, b->tick);
    put(&p, RA_BATTLE_VERSION);
    initial_hash(b, data + 40);
    ra_battle_hash(b, data + 60);
    memcpy(data + 80, b->content, 20);
    p = data + 104;
    for (uint32_t i = 0; i < b->initial_count; ++i)
    {
        const ra_battle_unit *u = &b->initial[i];
        put(&p, u->type);
        put(&p, u->cell % (b->width * b->height));
        put(&p, u->cell / (b->width * b->height));
        put(&p, u->id);
        put(&p, u->team);
    }
    for (uint32_t i = 0; i < b->command_count; ++i)
    {
        const ra_battle_command *c = &b->commands[i];
        put(&p, c->tick);
        put(&p, c->sequence);
        put(&p, c->unit);
        put(&p, c->target);
        put(&p, c->kind);
    }
    ra_sha1((ra_view){data, length - 20}, digest);
    memcpy(p, digest, 20);
    *bytes = data;
    *size = length;
    return true;
}
bool ra_battle_replay_read(ra_battle *b, ra_view bytes, uint32_t *end_tick, uint8_t expected[20], ra_error *error)
{
    const uint8_t *d = bytes.data, *p;
    uint8_t digest[20];
    uint32_t count, commands, end, waypoint_counts[RA_BATTLE_UNITS] = {0};
    size_t length;
    if (!b || !b->tiles || !d || bytes.size < 124 || !end_tick || !expected) return ra_fail(error, RA_ARGUMENT, 0, "invalid replay arguments");
    if (memcmp(d, RA_BATTLE_REPLAY_MAGIC, 8) || ra_le32(d + 8) != RA_BATTLE_VERSION || ra_le32(d + 12) != RA_BATTLE_HZ ||
        ra_le32(d + 36) != RA_BATTLE_VERSION || ra_le32(d + 100))
        return ra_fail(error, RA_FORMAT, 0, "unsupported replay format or simulation version");
    count = ra_le32(d + 24);
    commands = ra_le32(d + 28);
    end = ra_le32(d + 32);
    if (count > RA_BATTLE_UNITS || commands > RA_BATTLE_COMMANDS || end > 10000000) return ra_fail(error, RA_RANGE, 0, "replay limits exceeded");
    length = 124 + (size_t)(count + commands) * 20;
    if (bytes.size != length) return ra_fail(error, RA_FORMAT, 0, "replay length mismatch");
    ra_sha1((ra_view){d, length - 20}, digest);
    if (memcmp(digest, d + length - 20, 20)) return ra_fail(error, RA_FORMAT, 0, "replay checksum mismatch");
    initial_hash(b, digest);
    if (ra_le32(d + 16) != b->width || ra_le32(d + 20) != b->height || count != (b->terrain_sealed ? b->initial_count : b->count) ||
        memcmp(d + 40, digest, 20) || memcmp(d + 80, b->content, 20))
        return ra_fail(error, RA_FORMAT, 0, "replay map, content, types or initial units differ");
    p = d + 104;
    for (uint32_t i = 0; i < count; ++i, p += 20)
    {
        const ra_battle_unit *u = &b->initial[i];
        if (ra_le32(p) != u->type || ra_le32(p + 4) != u->cell % (b->width * b->height) || ra_le32(p + 8) != u->cell / (b->width * b->height) ||
            ra_le32(p + 12) != u->id || ra_le32(p + 16) != u->team)
            return ra_fail(error, RA_FORMAT, 0, "replay initial unit mismatch");
    }
    for (uint32_t i = 0; i < commands; ++i)
    {
        const uint8_t *c = p + (size_t)i * 20;
        uint32_t tick = ra_le32(c), unit = ra_le32(c + 8), target = ra_le32(c + 12), kind = ra_le32(c + 16);
        bool valid = battle_command_target(b, unit, kind, target);
        /* 经济回放可能引用尚未生产的编号；先检查协议边界，执行时再检查对象及所有权。 */
        if ((b->economy || b->campaign) && kind < RA_EVENT_BRIDGE_HIT && unit && unit <= RA_BATTLE_UNITS)
        {
            if (kind == RA_ORDER_ATTACK || kind == RA_ORDER_FORCE_UNIT) valid = target <= RA_BATTLE_UNITS && (kind != RA_ORDER_FORCE_UNIT || target);
            else if (kind == RA_ORDER_STOP || kind == RA_ORDER_GUARD || kind == RA_ORDER_SCATTER) valid = !target;
            else if (kind == RA_ORDER_WAYPOINT_LOOP) valid = target < RA_BATTLE_WAYPOINTS;
            else valid = target < 2 * b->width * b->height;
        }
        if (unit && unit <= RA_BATTLE_UNITS && kind >= RA_ORDER_DEPLOY)
            valid = (kind == RA_ORDER_ENTER || kind == RA_ORDER_LOAD)
                        ? target && target <= RA_BATTLE_UNITS
                        : (kind == RA_ORDER_DEPLOY || (kind == RA_EVENT_SELECT || kind == RA_ORDER_UNLOAD)) && !target;
        if (!tick || tick > end || (i && tick < ra_le32(c - 20)) || ra_le32(c + 4) != i + 1 || !valid)
            return ra_fail(error, RA_FORMAT, i + 1, "invalid replay command");
        if (kind == RA_ORDER_WAYPOINT_APPEND)
        {
            /* 路线追加和闭环必须属于同单位、同一步的连续批次，拒绝孤立或超长队列。 */
            if (!i || !waypoint_counts[unit - 1] || waypoint_counts[unit - 1] >= RA_BATTLE_WAYPOINTS || ra_le32(c - 20) != tick || ra_le32(c - 12) != unit ||
                (ra_le32(c - 4) != RA_ORDER_WAYPOINT && ra_le32(c - 4) != RA_ORDER_WAYPOINT_APPEND))
                return ra_fail(error, RA_FORMAT, i + 1, "invalid waypoint append batch");
            ++waypoint_counts[unit - 1];
        }
        else if (kind == RA_ORDER_WAYPOINT_LOOP)
        {
            if (!i || target >= waypoint_counts[unit - 1] || ra_le32(c - 20) != tick || ra_le32(c - 12) != unit ||
                (ra_le32(c - 4) != RA_ORDER_WAYPOINT && ra_le32(c - 4) != RA_ORDER_WAYPOINT_APPEND))
                return ra_fail(error, RA_FORMAT, i + 1, "invalid patrol loop batch");
        }
        else if (unit) waypoint_counts[unit - 1] = kind == RA_ORDER_WAYPOINT ? 1 : 0;
    }
    /* 先完整验证，再替换现场；旧版回放不会被误当作新命令解释。 */
    battle_terrain_seal(b);
    ra_battle_reset(b);
    b->command_count = commands;
    for (uint32_t i = 0; i < commands; ++i, p += 20)
        b->commands[i] = (ra_battle_command){ra_le32(p), ra_le32(p + 4), ra_le32(p + 8), ra_le32(p + 12), ra_le32(p + 16)};
    *end_tick = end;
    memcpy(expected, d + 60, 20);
    return true;
}
