#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

/* 步兵五个站位单独保留，不覆盖车辆和建筑的整格占用。站位竞争按稳定编号处理。 */
bool battle_cell_passable(const ra_battle *b, uint32_t cell, uint32_t unit)
{
    if (b && unit && unit <= b->count) return battle_type_passable(b, cell, &b->types[b->units[unit - 1].type]);
    return ra_battle_passable(b, cell);
}
bool battle_cell_available(const ra_battle *b, uint32_t cell, uint32_t unit)
{
    if (!battle_cell_passable(b, cell, unit)) return false;
    if (b->occupied[cell] && b->occupied[cell] != unit)
    {
        const ra_battle_unit *gate = &b->units[b->occupied[cell] - 1];
        if (!unit || unit > b->count || !b->types[gate->type].gate || !ra_battle_allied(b, b->units[unit - 1].team, gate->team)) return false;
    }
    bool infantry = unit && unit <= b->count && b->types[b->units[unit - 1].type].infantry;
    uint32_t feet = 0;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->id == unit || !b->types[u->type].infantry) continue;
        if (u->cell == cell || u->next == cell) ++feet;
    }
    return infantry ? feet < 5 : feet == 0;
}

void battle_people_move(ra_battle *b, ra_battle_unit *u)
{
    if (!u->health) return;
    if (u->next == u->cell)
    {
        if (u->cell == u->goal) return;
        if (u->retry)
        {
            --u->retry;
            return;
        }
        if (u->path_cursor >= u->path_count && !ra_battle_route(b, u->id, u->goal))
        {
            u->retry = RA_BATTLE_HZ;
            return;
        }
        if (u->path_cursor >= u->path_count) return;
        uint32_t next = u->path[u->path_cursor++];
        if (!ra_battle_edge(b, u->cell, next, u->id))
        {
            u->path_count = u->path_cursor = 0;
            u->retry = 5;
            return;
        }
        uint32_t used = 0;
        for (uint32_t i = 0; i < b->count; ++i)
        {
            const ra_battle_unit *v = &b->units[i];
            if (v->health && !(v->traits & RA_UNIT_LIMBO) && v->id != u->id && b->types[v->type].infantry && (v->cell == next || v->next == next))
                used |= 1u << v->subcell;
        }
        for (u->subcell = 0; u->subcell < 5 && (used & (1u << u->subcell)); ++u->subcell)
        {
        }
        if (u->subcell >= 5)
        {
            u->subcell = 0;
            u->path_count = u->path_cursor = 0;
            return;
        }
        u->next = next;
    }
    int32_t tx = (int32_t)(u->next % b->width * RA_BATTLE_CELL), ty = (int32_t)(ra_battle_cell_y(b, u->next) * RA_BATTLE_CELL);
    int64_t dx = (int64_t)tx - u->x, dy = (int64_t)ty - u->y;
    uint32_t distance = battle_sqrt((uint64_t)(dx * dx + dy * dy));
    uint32_t rate = b->types[u->type].step;
    if (rate > distance || !distance)
    {
        u->x = tx;
        u->y = ty;
        u->cell = u->next;
    }
    else
    {
        u->x += (int32_t)(dx * rate / distance);
        u->y += (int32_t)(dy * rate / distance);
    }
    uint32_t direction = battle_direction(dx, dy);
    u->facing = direction;
    u->body = (ra_battle_turn){direction, direction, b->tick, 0};
}

bool battle_people_target(const ra_battle *b, uint32_t actor, uint32_t kind, uint32_t target)
{
    if (!b || !actor || actor > b->count) return false;
    const ra_battle_type *t = &b->types[b->units[actor - 1].type];
    if (kind == RA_EVENT_SELECT) return target == 0;
    if (kind == RA_ORDER_DEPLOY) return !target && (t->passengers || (t->deploy_type && t->deploy_type <= b->type_count));
    return kind == RA_ORDER_ENTER && (t->engineer || t->c4) && target && target <= b->count &&
           (b->types[b->units[target - 1].type].structure || (t->c4 && b->types[b->units[target - 1].type].naval));
}

static bool deploy(ra_battle *b, ra_battle_unit *u)
{
    const ra_battle_type *old = &b->types[u->type], *t = &b->types[old->deploy_type - 1];
    if (!t->structure || u->cell != u->next || u->track_active || u->cell >= b->width * b->height) return false;
    uint32_t x = u->cell % b->width, y = u->cell / b->width;
    uint32_t dx = (t->foundation_width - 1) / 2, dy = (t->foundation_height - 1) / 2;
    if (x < dx || y < dy) return false;
    x -= dx;
    y -= dy;
    if (t->foundation_width > b->width - x || t->foundation_height > b->height - y) return false;
    uint32_t origin = y * b->width + x;
    for (uint32_t row = 0; row < t->foundation_height; ++row)
        for (uint32_t col = 0; col < t->foundation_width; ++col)
        {
            uint32_t at = origin + row * b->width + col;
            if (!battle_cell_available(b, at, u->id) || b->tiles[at].ramp || b->tiles[at].height != b->tiles[origin].height || b->bridges[at] ||
                (b->economy && b->economy->ore[at]))
                return false;
        }
    uint32_t health = (uint32_t)(((uint64_t)u->health * t->strength + old->strength - 1) / old->strength);
    battle_reservations_clear(b, u);
    if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
    u->type = old->deploy_type - 1;
    u->health = health;
    u->cell = u->next = u->goal = u->destination = u->anchor = origin;
    u->x = (int32_t)(x * RA_BATTLE_CELL + (t->foundation_width - 1) * RA_BATTLE_CELL / 2);
    u->y = (int32_t)(y * RA_BATTLE_CELL + (t->foundation_height - 1) * RA_BATTLE_CELL / 2);
    u->target = u->path_count = u->path_cursor = u->waypoint_count = u->waypoint_cursor = u->waypoint_loop = 0;
    u->order = RA_ORDER_STOP;
    for (uint32_t row = 0; row < t->foundation_height; ++row)
        for (uint32_t col = 0; col < t->foundation_width; ++col) b->occupied[origin + row * b->width + col] = u->id;
    return true;
}

void battle_people_apply(ra_battle *b, const ra_battle_command *c)
{
    if (!battle_people_target(b, c->unit, c->kind, c->target) || !b->units[c->unit - 1].health)
    {
        ++b->rejected;
        return;
    }
    ra_battle_unit *u = &b->units[c->unit - 1];
    if (c->kind == RA_EVENT_SELECT)
    {
        u->selected_tick = b->tick;
        return;
    }
    if (c->kind == RA_ORDER_DEPLOY)
    {
        if (!deploy(b, u)) ++b->rejected;
        return;
    }
    u->order = RA_ORDER_ENTER;
    u->target = c->target;
    u->action_tick = 0;
    u->goal = u->next;
    u->path_count = u->path_cursor = u->waypoint_count = u->waypoint_cursor = u->waypoint_loop = 0;
}

static bool adjacent(const ra_battle *b, const ra_battle_unit *u, const ra_battle_unit *v)
{
    int x = (int)(u->cell % b->width), y = (int)ra_battle_cell_y(b, u->cell);
    int left = (int)(v->cell % b->width), top = (int)(v->cell / b->width);
    const ra_battle_type *t = &b->types[v->type];
    return u->next == u->cell && x >= left - 1 && y >= top - 1 && x <= left + (int)(t->foundation_width ? t->foundation_width : 1) &&
           y <= top + (int)(t->foundation_height ? t->foundation_height : 1) && ra_battle_unit_layer(b, u) == 0;
}
static bool repair_bridge(ra_battle *b, const ra_battle_unit *hut)
{
    uint32_t chosen = UINT32_MAX, distance = UINT32_MAX;
    for (uint32_t i = 0; i < b->bridge_count; ++i)
    {
        uint32_t cell = b->bridge_parts[i].cell;
        int dx = (int)(cell % b->width) - (int)(hut->cell % b->width), dy = (int)(cell / b->width) - (int)(hut->cell / b->width);
        uint32_t score = (uint32_t)(dx * dx + dy * dy);
        if (score < distance)
        {
            distance = score;
            chosen = cell;
        }
    }
    if (chosen == UINT32_MAX || distance > 64) return false;
    uint32_t repaired = b->bridge_repaired;
    ra_battle_command command = {b->tick, 0, 0, chosen, RA_EVENT_BRIDGE_REPAIR};
    battle_bridge_event(b, &command);
    return b->bridge_repaired != repaired;
}
void battle_people_step(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        if (u->health && u->c4_owner && u->action_tick && b->tick >= u->action_tick)
        {
            battle_kill(b, u, u->c4_owner);
            u->c4_owner = u->action_tick = 0;
        }
        if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->order != RA_ORDER_ENTER || !u->target || u->target > b->count) continue;
        ra_battle_unit *v = &b->units[u->target - 1];
        const ra_battle_type *t = &b->types[u->type], *target = &b->types[v->type];
        bool allied = ra_battle_allied(b, u->team, v->team);
        bool valid = v->health && (target->structure || (t->c4 && target->naval)) &&
                     (t->engineer ? target->bridge_hut || (allied ? v->health < target->strength : target->capturable)
                                  : t->c4 && !allied && !(v->traits & RA_UNIT_IMMUNE));
        if (!valid)
        {
            u->order = RA_ORDER_STOP;
            u->target = u->action_tick = 0;
            u->goal = u->next;
            continue;
        }
        if (!adjacent(b, u, v))
        {
            u->action_tick = 0;
            if (u->cell == u->next && (!u->path_count || b->tick % RA_BATTLE_HZ == 0))
            {
                ra_battle_unit aim = {0};
                battle_target_point(b, u, v, &aim);
                if (!battle_route_range(b, u->id, &aim, RA_BATTLE_CELL * 3 / 2)) u->goal = u->next;
            }
            continue;
        }
        if (t->c4)
        {
            v->action_tick = b->tick + t->c4_ticks;
            v->c4_owner = u->id;
        }
        else
        {
            if (target->bridge_hut && !repair_bridge(b, v))
            {
                u->order = RA_ORDER_STOP;
                u->target = 0;
                continue;
            }
            if (!target->bridge_hut)
            {
                v->team = allied ? v->team : u->team;
                v->health = target->strength;
            }
            /* 进入建筑消耗工程师；不记作战斗死亡，不增加击杀数。 */
            u->health = 0;
            u->traits |= RA_UNIT_LIMBO;
        }
        u->order = RA_ORDER_STOP;
        u->target = u->action_tick = 0;
        u->goal = u->next;
    }
}
