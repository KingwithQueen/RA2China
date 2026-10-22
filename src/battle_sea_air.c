#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

/* 飞行物不借用桥面占格；舰船只走水面，两栖运输工具继续使用岸坡边检查。 */
bool battle_type_passable(const ra_battle *b, uint32_t cell, const ra_battle_type *t)
{
    if (!b || !t || cell >= 2 * b->width * b->height) return false;
    if (t->flying) return cell < b->width * b->height && b->tiles[cell].land != 255;
    if (t->naval && !t->amphibious) return cell < b->width * b->height && !b->tiles[cell].blocked && b->tiles[cell].land == 2;
    return ra_battle_passable(b, cell) || (t->amphibious && cell < b->width * b->height && !b->tiles[cell].blocked && b->tiles[cell].land == 2);
}

void battle_sea_air_move(ra_battle *b, ra_battle_unit *u)
{
    const ra_battle_type *t = &b->types[u->type];
    if (!u->health || (u->traits & RA_UNIT_LIMBO)) return;
    if (u->unloading && u->cell == u->next) return;
    if (u->next == u->cell)
    {
        if (u->goal == u->cell) return;
        if (u->retry)
        {
            --u->retry;
            return;
        }
        if (t->flying) u->next = u->goal;
        else
        {
            if (u->path_cursor >= u->path_count && !ra_battle_route(b, u->id, u->goal))
            {
                u->retry = RA_BATTLE_HZ;
                return;
            }
            if (u->path_cursor >= u->path_count) return;
            uint32_t next = u->path[u->path_cursor];
            if (!ra_battle_edge(b, u->cell, next, u->id))
            {
                u->path_count = u->path_cursor = 0;
                u->retry = 5;
                return;
            }
            ++u->path_cursor;
            u->next = next;
            b->occupied[next] = u->id;
        }
    }
    int32_t tx = (int32_t)(u->next % b->width * RA_BATTLE_CELL), ty = (int32_t)(ra_battle_cell_y(b, u->next) * RA_BATTLE_CELL);
    int64_t dx = (int64_t)tx - u->x, dy = (int64_t)ty - u->y;
    uint32_t distance = battle_sqrt((uint64_t)(dx * dx + dy * dy));
    uint32_t direction = battle_direction(dx, dy);
    ra_battle_turn_start(&u->body, direction, t->rot, b->tick);
    if (!t->flying && b->tick - u->body.started < u->body.duration) return;
    uint32_t rate = t->step;
    if (!distance || rate >= distance)
    {
        if (!t->flying && b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
        u->cell = u->next;
        u->x = tx;
        u->y = ty;
    }
    else
    {
        u->x += (int32_t)(dx * rate / distance);
        u->y += (int32_t)(dy * rate / distance);
        if (t->flying) u->cell = (uint32_t)((u->y + RA_BATTLE_CELL / 2) / RA_BATTLE_CELL) * b->width + (uint32_t)((u->x + RA_BATTLE_CELL / 2) / RA_BATTLE_CELL);
    }
}

uint32_t battle_transport_count(const ra_battle *b, uint32_t carrier)
{
    uint32_t count = 0;
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].carrier == carrier) ++count;
    return count;
}
bool battle_transport_load(ra_battle *b, ra_battle_unit *u, ra_battle_unit *v)
{
    const ra_battle_type *t = &b->types[u->type], *transport = &b->types[v->type];
    if (u == v || !u->health || !v->health || !ra_battle_allied(b, u->team, v->team) || t->structure || t->flying || t->passengers || u->carrier ||
        (v->traits & RA_UNIT_LIMBO) || !transport->passengers || t->size > transport->size_limit)
        return false;
    uint32_t used = 0;
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].carrier == v->id) used += b->types[b->units[i].type].size;
    if (t->size > transport->passengers - used) return false;
    battle_reservations_clear(b, u);
    if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
    if (b->occupied[u->next] == u->id) b->occupied[u->next] = 0;
    u->carrier = v->id;
    u->traits |= RA_UNIT_LIMBO;
    u->cell = u->next = u->goal = u->destination = v->cell;
    u->x = v->x;
    u->y = v->y;
    u->target = u->path_count = u->path_cursor = u->track_active = 0;
    u->order = RA_ORDER_STOP;
    return true;
}

bool battle_transport_spawn(ra_battle *b, uint32_t type, uint32_t team, uint32_t carrier, ra_error *error)
{
    if (type >= b->type_count || !carrier || carrier > b->count || b->count == RA_BATTLE_UNITS)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid transported reinforcement");
    ra_battle_unit *u = &b->units[b->count];
    memset(u, 0, sizeof(*u));
    u->id = b->count + 1;
    u->type = type;
    u->team = team;
    u->health = b->types[type].strength;
    u->ammunition = b->types[type].ammo;
    u->speed_factor = 10000;
    u->motion_factor = BATTLE_ONE;
    if (!battle_transport_load(b, u, &b->units[carrier - 1]))
    {
        memset(u, 0, sizeof(*u));
        return ra_fail(error, RA_ARGUMENT, 0, "transport capacity or passenger type rejected");
    }
    ++b->count;
    return true;
}

static bool unload_one(ra_battle *b, ra_battle_unit *v, ra_battle_unit *u)
{
    /* 只向相邻可达地面卸载；整圈受阻时保留乘员，下一固定步继续，不丢弃也不传送。 */
    for (int radius = 1; radius <= 1; ++radius)
        for (int y = (int)ra_battle_cell_y(b, v->cell) - radius; y <= (int)ra_battle_cell_y(b, v->cell) + radius; ++y)
            for (int x = (int)(v->cell % b->width) - radius; x <= (int)(v->cell % b->width) + radius; ++x)
            {
                if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
                if (x == (int)(v->cell % b->width) && y == (int)ra_battle_cell_y(b, v->cell)) continue;
                uint32_t cell = (uint32_t)y * b->width + (uint32_t)x;
                if (!battle_cell_available(b, cell, u->id) || !ra_battle_slope_edge(&b->tiles[v->cell], &b->tiles[cell])) continue;
                uint32_t used = 0;
                for (uint32_t i = 0; i < b->count; ++i)
                    if (b->units[i].health && !(b->units[i].traits & RA_UNIT_LIMBO) && b->types[b->units[i].type].infantry &&
                        (b->units[i].cell == cell || b->units[i].next == cell))
                        used |= 1u << b->units[i].subcell;
                u->carrier = 0;
                u->traits &= ~RA_UNIT_LIMBO;
                u->cell = u->next = u->goal = u->destination = u->anchor = cell;
                u->x = x * (int32_t)RA_BATTLE_CELL;
                u->y = y * (int32_t)RA_BATTLE_CELL;
                u->order = RA_ORDER_GUARD;
                for (u->subcell = 0; u->subcell < 5 && (used & (1u << u->subcell)); ++u->subcell)
                {
                }
                if (!b->types[u->type].infantry) b->occupied[cell] = u->id;
                return true;
            }
    return false;
}
void battle_transport_step(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        if (!u->health || (u->traits & RA_UNIT_LIMBO)) continue;
        if (u->order == RA_ORDER_LOAD && u->target && u->target <= b->count)
        {
            ra_battle_unit *v = &b->units[u->target - 1];
            if (!v->health)
            {
                u->order = RA_ORDER_STOP;
                continue;
            }
            if (b->types[v->type].flying && v->altitude > 0)
            {
                u->order = RA_ORDER_STOP;
                continue;
            }
            if (u->cell == u->next && battle_distance_squared(u, v) <= (uint64_t)2 * RA_BATTLE_CELL * RA_BATTLE_CELL)
            {
                if (battle_transport_load(b, u, v)) continue;
                u->order = RA_ORDER_STOP;
            }
            else if (u->cell == u->next && b->tick % 15 == 0) battle_route_range(b, u->id, v, RA_BATTLE_CELL);
        }
        if (!u->unloading || u->cell != u->next || b->tick < u->unload_tick) continue;
        if (b->types[u->type].flying && u->altitude > 0)
        {
            u->altitude -= u->altitude > 40 ? 40 : u->altitude;
            if (!u->altitude) u->traits &= ~RA_UNIT_AIRBORNE;
            continue;
        }
        bool remaining = false;
        for (uint32_t j = 0; j < b->count; ++j)
            if (b->units[j].health && b->units[j].carrier == u->id)
            {
                remaining = true;
                if (unload_one(b, u, &b->units[j])) u->unload_tick = b->tick + 5;
                break;
            }
        if (!remaining) u->unloading = 0;
    }
}

void battle_gates_step(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *gate = &b->units[i];
        const ra_battle_type *t = &b->types[gate->type];
        if (!gate->health || !t->gate) continue;
        bool nearby = false, occupied = false;
        int left = (int)(gate->cell % b->width), top = (int)(gate->cell / b->width);
        for (uint32_t j = 0; j < b->count; ++j)
        {
            const ra_battle_unit *u = &b->units[j];
            if (!u->health || b->types[u->type].structure || (u->traits & (RA_UNIT_LIMBO | RA_UNIT_AIRBORNE))) continue;
            int x = (int)(u->cell % b->width), y = (int)ra_battle_cell_y(b, u->cell);
            if (x >= left - 3 && y >= top - 3 && x <= left + (int)t->foundation_width + 2 && y <= top + (int)t->foundation_height + 2 &&
                ra_battle_allied(b, u->team, gate->team))
                nearby = true;
            if (x >= left && y >= top && x < left + (int)t->foundation_width && y < top + (int)t->foundation_height) occupied = true;
        }
        if (nearby)
        {
            gate->gate_open_until = b->tick + 30;
            battle_structure_release(b, gate);
        }
        else if (gate->gate_open_until && b->tick >= gate->gate_open_until && !occupied)
        {
            bool free = true;
            for (uint32_t y = 0; y < t->foundation_height; ++y)
                for (uint32_t x = 0; x < t->foundation_width; ++x)
                    if (b->occupied[gate->cell + y * b->width + x]) free = false;
            if (free)
            {
                for (uint32_t y = 0; y < t->foundation_height; ++y)
                    for (uint32_t x = 0; x < t->foundation_width; ++x) b->occupied[gate->cell + y * b->width + x] = gate->id;
                gate->gate_open_until = 0;
            }
        }
    }
}
