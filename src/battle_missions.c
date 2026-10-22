#include "internal.h"
#include "battle_internal.h"
#include <string.h>

int32_t battle_guard_range(int32_t guard, int32_t primary, int32_t secondary, int32_t kind, bool special)
{
    int32_t range;
    if (kind == -1) return -1;
    if (!kind) return special ? 0 : guard;
    range = guard ? guard : primary > secondary ? primary : secondary;
    range *= 2;
    if (kind == 2 && range < 7 * 256) return 7 * 256;
    if (range < 0) return 0;
    return range > 16 * 256 ? 16 * 256 : range;
}

bool battle_command_target(const ra_battle *b, uint32_t unit, uint32_t kind, uint32_t target)
{
    if (!b) return false;
    if (kind == RA_ORDER_UNLOAD) return unit && unit <= b->count && b->types[b->units[unit - 1].type].passengers && !target;
    if (kind == RA_ORDER_LOAD)
        return unit && unit <= b->count && target && target <= b->count && unit != target && b->types[b->units[target - 1].type].passengers &&
               !b->types[b->units[unit - 1].type].structure && ra_battle_allied(b, b->units[unit - 1].team, b->units[target - 1].team);
    if (kind >= RA_ORDER_DEPLOY) return battle_people_target(b, unit, kind, target);
    if (kind >= RA_ECON_QUEUE) return battle_economy_target(b, unit, kind, target);
    if (kind >= RA_EVENT_BRIDGE_HIT && kind <= RA_EVENT_BRIDGE_REPAIR) return !unit && target < b->width * b->height && b->bridge_at[target];
    if (!unit || unit > b->count) return false;
    if (b->types[b->units[unit - 1].type].structure && kind != RA_ORDER_STOP) return false;
    switch (kind)
    {
    case RA_ORDER_MOVE:
    case RA_ORDER_ATTACK_MOVE:
    case RA_ORDER_WAYPOINT:
    case RA_ORDER_WAYPOINT_APPEND:
        if (target >= 2 * b->width * b->height) return false;
        const ra_battle_tile *tiles = b->terrain_sealed ? b->initial_tiles : b->tiles;
        if (b->types[b->units[unit - 1].type].flying || b->types[b->units[unit - 1].type].naval)
            return battle_type_passable(b, target, &b->types[b->units[unit - 1].type]);
        return (!tiles[target].blocked && (tiles[target].track || (b->types[b->units[unit - 1].type].amphibious && tiles[target].land == 2))) ||
               b->bridge_at[target % (b->width * b->height)];
    case RA_ORDER_FORCE_GROUND:
        return target < b->width * b->height || ra_battle_passable(b, target) ||
               (target < 2 * b->width * b->height && b->bridge_at[target % (b->width * b->height)]);
    case RA_ORDER_ATTACK:
        return target <= b->count && (!target || !ra_battle_allied(b, b->units[unit - 1].team, b->units[target - 1].team));
    case RA_ORDER_FORCE_UNIT:
        return target && target <= b->count;
    case RA_ORDER_STOP:
    case RA_ORDER_GUARD:
    case RA_ORDER_SCATTER:
        return target == 0;
    case RA_ORDER_WAYPOINT_LOOP:
        return target < RA_BATTLE_WAYPOINTS;
    default:
        return false;
    }
}

static bool command_room(const ra_battle *b, uint32_t tick, uint32_t unit, uint32_t count)
{
    return b && b->tiles && tick > b->tick && tick <= 10000000 && unit && unit <= b->count && b->units[unit - 1].health &&
           !(b->units[unit - 1].traits & RA_UNIT_LIMBO) && count <= RA_BATTLE_COMMANDS - b->command_count &&
           (!b->command_count || tick >= b->commands[b->command_count - 1].tick);
}
static void append(ra_battle *b, uint32_t tick, uint32_t unit, uint32_t kind, uint32_t target)
{
    b->commands[b->command_count] = (ra_battle_command){tick, b->command_count + 1, unit, target, kind};
    ++b->command_count;
}
bool ra_battle_order_add(ra_battle *b, uint32_t tick, uint32_t unit, ra_battle_order kind, uint32_t target, ra_error *error)
{
    if (!command_room(b, tick, unit, 1) || (kind >= RA_ORDER_WAYPOINT && kind < RA_ORDER_DEPLOY) || !battle_command_target(b, unit, kind, target) ||
        ((kind == RA_ORDER_MOVE || kind == RA_ORDER_ATTACK_MOVE) && !battle_cell_passable(b, target, unit)) ||
        ((kind == RA_ORDER_ATTACK || kind == RA_ORDER_FORCE_UNIT) && target && !b->units[target - 1].health))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid mission command, target or command order");
    append(b, tick, unit, kind, target);
    return true;
}
bool ra_battle_attack_add(ra_battle *b, uint32_t tick, uint32_t unit, uint32_t target, ra_error *error)
{
    return ra_battle_order_add(b, tick, unit, RA_ORDER_ATTACK, target, error);
}
bool ra_battle_stop_add(ra_battle *b, uint32_t tick, uint32_t unit, ra_error *error)
{
    return ra_battle_order_add(b, tick, unit, RA_ORDER_STOP, 0, error);
}
bool ra_battle_waypoints_add(ra_battle *b, uint32_t tick, uint32_t unit, const uint32_t *cells, uint32_t count, uint32_t loop_from, ra_error *error)
{
    if (!cells || !count || count > RA_BATTLE_WAYPOINTS || (loop_from != UINT32_MAX && loop_from >= count) ||
        !command_room(b, tick, unit, count + (loop_from != UINT32_MAX)))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid waypoint batch or insufficient command capacity");
    for (uint32_t i = 0; i < count; ++i)
        if (!ra_battle_passable(b, cells[i])) return ra_fail(error, RA_ARGUMENT, i, "waypoint is not passable");
    /* 批次不可部分入队；调用方可在同一模拟步提交多个单位的完整路线。 */
    for (uint32_t i = 0; i < count; ++i) append(b, tick, unit, i ? RA_ORDER_WAYPOINT_APPEND : RA_ORDER_WAYPOINT, cells[i]);
    if (loop_from != UINT32_MAX) append(b, tick, unit, RA_ORDER_WAYPOINT_LOOP, loop_from);
    return true;
}

static void destination(ra_battle_unit *u, uint32_t cell)
{
    if (u->goal == cell) return;
    u->goal = cell;
    u->path_count = u->path_cursor = u->retry = 0;
}
static void scatter(ra_battle *b, ra_battle_unit *u)
{
    static const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1}, dy[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
    uint32_t chosen = u->next;
    uint64_t best = 0;
    /* 暂用稳定编号打破平局；它是确定性参考行为，尚未宣称与原版散开随机算法一致。 */
    for (uint32_t n = 0; n < 8; ++n)
    {
        uint32_t direction = (n + u->id) % 8;
        int x = (int)(u->next % b->width) + dx[direction], y = (int)(ra_battle_cell_y(b, u->next)) + dy[direction];
        uint64_t score = 1;
        bool reserved = false;
        if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
        uint32_t cell = (uint32_t)y * b->width + (uint32_t)x + u->next / (b->width * b->height) * b->width * b->height;
        if (!ra_battle_edge(b, u->next, cell, u->id)) continue;
        for (uint32_t i = 0; i < b->count; ++i)
        {
            const ra_battle_unit *v = &b->units[i];
            if (v->id == u->id || !v->health) continue;
            if (v->order == RA_ORDER_SCATTER && v->destination == cell) reserved = true;
            int64_t vx = (int64_t)x * RA_BATTLE_CELL - v->x, vy = (int64_t)y * RA_BATTLE_CELL - v->y;
            if (battle_distance_squared(u, v) <= (uint64_t)4 * RA_BATTLE_CELL * RA_BATTLE_CELL) score += (uint64_t)(vx * vx + vy * vy);
        }
        if (!reserved && (chosen == u->next || score > best))
        {
            best = score;
            chosen = cell;
        }
    }
    u->destination = chosen;
    destination(u, chosen);
    if (chosen == u->next) ++b->rejected;
}
void battle_command_apply(ra_battle *b, const ra_battle_command *c)
{
    if (c->kind == RA_ORDER_UNLOAD || c->kind == RA_ORDER_LOAD ||
        (c->kind == RA_ORDER_DEPLOY && c->unit && c->unit <= b->count && b->types[b->units[c->unit - 1].type].passengers))
    {
        if (!c->unit || c->unit > b->count || !b->units[c->unit - 1].health || (b->units[c->unit - 1].traits & RA_UNIT_LIMBO) ||
            (c->kind != RA_ORDER_DEPLOY && !battle_command_target(b, c->unit, c->kind, c->target)))
        {
            ++b->rejected;
            return;
        }
        ra_battle_unit *u = &b->units[c->unit - 1];
        u->script_team = 0;
        if (c->kind == RA_ORDER_LOAD)
        {
            u->order = RA_ORDER_LOAD;
            u->target = c->target;
        }
        else
        {
            u->unloading = 1;
            u->goal = u->destination = u->next;
            u->path_count = u->path_cursor = 0;
            u->order = RA_ORDER_STOP;
        }
        return;
    }
    if (c->kind >= RA_ORDER_DEPLOY)
    {
        battle_people_apply(b, c);
        return;
    }
    if (c->kind >= RA_ECON_QUEUE)
    {
        battle_economy_apply(b, c);
        return;
    }
    if (c->kind >= RA_EVENT_BRIDGE_HIT && c->kind <= RA_EVENT_BRIDGE_REPAIR)
    {
        battle_bridge_event(b, c);
        return;
    }
    if (!c->unit || c->unit > b->count || !battle_command_target(b, c->unit, c->kind, c->target))
    {
        ++b->rejected;
        return;
    }
    ra_battle_unit *u = &b->units[c->unit - 1];
    if (!u->health || (u->traits & RA_UNIT_LIMBO)) return;
    if (b->economy) b->economy->state.miners[c->unit - 1].active = 0;
    if (c->kind == RA_ORDER_WAYPOINT)
    {
        uint32_t end = b->command_cursor;
        bool valid = ra_battle_passable(b, c->target);
        /* 地形可在排队后改变；整批再次验证，拒绝时不能把后续追加挂到旧任务上。 */
        while (end < b->command_count)
        {
            const ra_battle_command *next = &b->commands[end];
            if (next->tick != c->tick || next->unit != c->unit || (next->kind != RA_ORDER_WAYPOINT_APPEND && next->kind != RA_ORDER_WAYPOINT_LOOP)) break;
            if (next->kind == RA_ORDER_WAYPOINT_APPEND && !ra_battle_passable(b, next->target)) valid = false;
            ++end;
        }
        if (!valid)
        {
            ++b->rejected;
            b->command_cursor = end;
            return;
        }
    }
    if ((c->kind == RA_ORDER_MOVE || c->kind == RA_ORDER_ATTACK_MOVE || c->kind == RA_ORDER_WAYPOINT || c->kind == RA_ORDER_WAYPOINT_APPEND) &&
        !battle_cell_passable(b, c->target, c->unit))
    {
        ++b->rejected;
        return;
    }
    if (c->kind == RA_ORDER_WAYPOINT_APPEND)
    {
        if (u->order == RA_ORDER_WAYPOINT && u->waypoint_count < RA_BATTLE_WAYPOINTS) u->waypoints[u->waypoint_count++] = c->target;
        return;
    }
    if (c->kind == RA_ORDER_WAYPOINT_LOOP)
    {
        if (u->order == RA_ORDER_WAYPOINT && c->target < u->waypoint_count) u->waypoint_loop = c->target + 1;
        return;
    }
    u->unloading = 0;
    if (b->types[u->type].flying)
    {
        u->altitude = (int32_t)b->types[u->type].flight_height;
        u->traits |= RA_UNIT_AIRBORNE;
    }
    u->script_team = 0;
    u->action_tick = 0;
    u->order = c->kind;
    u->target = 0;
    u->path_count = u->path_cursor = u->retry = 0;
    u->waypoint_count = u->waypoint_cursor = u->waypoint_loop = 0;
    u->anchor = u->destination = u->goal = u->next;
    if (c->kind == RA_ORDER_MOVE || c->kind == RA_ORDER_ATTACK_MOVE) u->destination = u->goal = c->target;
    else if (c->kind == RA_ORDER_ATTACK || c->kind == RA_ORDER_FORCE_UNIT) u->target = c->target ? c->target : ra_battle_nearest(b, u->id);
    else if (c->kind == RA_ORDER_FORCE_GROUND) u->fire_cell = c->target;
    else if (c->kind == RA_ORDER_SCATTER) scatter(b, u);
    else if (c->kind == RA_ORDER_WAYPOINT)
    {
        u->waypoints[0] = u->destination = u->goal = c->target;
        u->waypoint_count = 1;
    }
}

bool battle_aim(const ra_battle *b, const ra_battle_unit *u, ra_battle_unit *aim)
{
    if (u->order == RA_ORDER_FORCE_GROUND)
    {
        memset(aim, 0, sizeof(*aim));
        aim->cell = u->fire_cell;
        aim->x = (int32_t)(aim->cell % b->width * RA_BATTLE_CELL);
        aim->y = (int32_t)(ra_battle_cell_y(b, aim->cell) * RA_BATTLE_CELL);
        return true;
    }
    if (!u->target || u->target > b->count) return false;
    const ra_battle_unit *v = &b->units[u->target - 1];
    if (!ra_battle_targetable(b, u, v, false, u->order == RA_ORDER_FORCE_UNIT)) return false;
    /* 建筑瞄准最近的占地格；只复制瞄准字段，避免复制大型路径数组。 */
    battle_target_point(b, u, v, aim);
    return true;
}
static bool candidate(const ra_battle *b, const ra_battle_unit *u, const ra_battle_unit *v)
{
    const ra_battle_type *t = &b->types[u->type];
    uint32_t range = (uint32_t)battle_guard_range((int32_t)(t->guard_range / 256), (int32_t)(t->weapon.range / 256), 0, 1, false) * 256;
    if (t->structure) range = t->weapon.range;
    if (!ra_battle_targetable(b, u, v, true, false) || battle_distance_squared(u, v) > (uint64_t)range * range) return false;
    if (u->order == RA_ORDER_GUARD)
    {
        int64_t dx = (int64_t)(u->anchor % b->width) * RA_BATTLE_CELL - v->x, dy = (int64_t)(ra_battle_cell_y(b, u->anchor)) * RA_BATTLE_CELL - v->y;
        if ((uint64_t)(dx * dx + dy * dy) > (uint64_t)range * range) return false;
    }
    return true;
}
void battle_missions(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        bool automatic = u->order == RA_ORDER_ATTACK_MOVE || u->order == RA_ORDER_GUARD || (u->order == RA_ORDER_WAYPOINT && u->waypoint_loop);
        if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->order == RA_ORDER_ENTER || u->order == RA_ORDER_LOAD) continue;
        if (u->target && (!ra_battle_targetable(b, u, &b->units[u->target - 1], automatic, u->order == RA_ORDER_FORCE_UNIT) ||
                          (automatic && !candidate(b, u, &b->units[u->target - 1]))))
        {
            u->target = 0;
            destination(u, u->next);
        }
        if (automatic && !u->target)
        {
            int32_t best = INT32_MIN;
            for (uint32_t j = 0; j < b->count; ++j)
                if (candidate(b, u, &b->units[j]))
                {
                    int32_t score = battle_threat_score(b, u, &b->units[j]);
                    if (score > best)
                    {
                        best = score;
                        u->target = j + 1;
                    }
                }
        }
        if (u->target || u->order == RA_ORDER_FORCE_GROUND) continue;
        if (u->order == RA_ORDER_WAYPOINT && u->waypoint_count)
        {
            /* 重合路径点也须有界处理；完整绕一圈仍在原格时留到下一步。 */
            for (uint32_t n = 0; n < u->waypoint_count && u->cell == u->next && u->cell == u->waypoints[u->waypoint_cursor]; ++n)
            {
                if (++u->waypoint_cursor < u->waypoint_count) continue;
                if (u->waypoint_loop) u->waypoint_cursor = u->waypoint_loop - 1;
                else
                {
                    u->waypoint_count = u->waypoint_cursor = 0;
                    u->order = RA_ORDER_MOVE;
                    break;
                }
            }
            if (u->waypoint_count) u->destination = u->waypoints[u->waypoint_cursor];
        }
        if (u->order == RA_ORDER_GUARD) destination(u, u->anchor);
        else if (u->order == RA_ORDER_MOVE || u->order == RA_ORDER_ATTACK_MOVE || u->order == RA_ORDER_SCATTER || u->order == RA_ORDER_WAYPOINT)
            destination(u, u->destination);
    }
}
