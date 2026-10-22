#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>

void battle_random_reset(ra_battle *b)
{
    uint32_t seed = 0x1badf00d;
    /* 初始化是本项目回放协议的一部分；抽取使用与原版核对过的 R250 路径。 */
    for (uint32_t i = 0; i < 250; ++i)
    {
        seed = seed * 1664525u + 1013904223u;
        b->random[i] = seed;
    }
    b->random_a = 0;
    b->random_b = 103;
}
uint32_t battle_random_range(ra_battle *b, uint32_t low, uint32_t high)
{
    uint32_t range = high - low, mask = range, value;
    if (!range) return low;
    mask |= mask >> 1;
    mask |= mask >> 2;
    mask |= mask >> 4;
    mask |= mask >> 8;
    mask |= mask >> 16;
    do
    {
        value = b->random[b->random_a] ^ b->random[b->random_b];
        b->random[b->random_a] = value;
        b->random_a = (b->random_a + 1) % 250;
        b->random_b = (b->random_b + 1) % 250;
        value &= mask;
    } while (value > range);
    return low + value;
}
uint32_t battle_random_delay(ra_battle *b)
{
    return battle_random_range(b, 0, 2);
}

uint64_t battle_distance_squared(const ra_battle_unit *a, const ra_battle_unit *b)
{
    int64_t dx = (int64_t)a->x - b->x, dy = (int64_t)a->y - b->y;
    return (uint64_t)(dx * dx + dy * dy);
}

uint32_t ra_battle_nearest(const ra_battle *b, uint32_t unit)
{
    uint64_t best = UINT64_MAX;
    uint32_t target = 0;
    if (!b || !unit || unit > b->count || !b->units[unit - 1].health) return 0;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        uint64_t distance;
        if (!ra_battle_targetable(b, &b->units[unit - 1], &b->units[i], true, false)) continue;
        distance = battle_distance_squared(&b->units[unit - 1], &b->units[i]);
        if (distance < best)
        {
            best = distance;
            target = i + 1;
        }
    }
    return target;
}

static bool in_range(const ra_battle_unit *u, const ra_battle_unit *v, uint32_t range)
{
    return battle_distance_squared(u, v) <= (uint64_t)range * range;
}

void battle_attack_orders(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i], aim, *v = &aim;
        const ra_battle_weapon *w = &b->types[u->type].weapon;
        if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->order == RA_ORDER_ENTER || u->order == RA_ORDER_LOAD || !w->damage || !battle_aim(b, u, v))
            continue;
        if (in_range(u, v, w->range))
        {
            u->goal = u->next;
            u->path_count = u->path_cursor = 0;
        }
        else if (u->cell == u->next && (b->tick % RA_BATTLE_HZ == 0 || u->goal == u->cell))
        {
            /* 直接搜索可到达的射程圈，避免选择隔墙但无法到达的几何近点。 */
            if (b->types[u->type].flying) u->goal = v->cell % (b->width * b->height);
            else if (u->retry) --u->retry;
            else if (!battle_route_range(b, u->id, v, w->range))
            {
                u->goal = u->cell;
                u->retry = RA_BATTLE_HZ;
                ++b->rejected;
            }
        }
        ra_battle_turn_start(&u->turret, battle_direction((int64_t)v->x - u->x, (int64_t)v->y - u->y), b->types[u->type].rot, b->tick);
    }
}

void battle_kill(ra_battle *b, ra_battle_unit *u, uint32_t killer)
{
    if (!u->health) return;
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].carrier == u->id) battle_kill(b, &b->units[i], killer);
    u->health = 0;
    u->killer = killer;
    battle_structure_release(b, u);
    u->destroyed_tick = b->tick;
    battle_reservations_clear(b, u);
    u->track_active = u->track_index = u->track_remainder = 0;
    u->target = 0;
    u->goal = u->cell;
    if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
    if (b->occupied[u->next] == u->id) b->occupied[u->next] = 0;
    u->next = u->cell;
    u->path_count = u->path_cursor = u->progress = 0;
    u->waypoint_count = u->waypoint_cursor = u->waypoint_loop = 0;
    ++b->kills;
    if (killer && killer <= b->count) ++b->units[killer - 1].kills;
}

static void impact(ra_battle *b, ra_battle_shot *shot)
{
    const ra_battle_weapon *w = &b->types[shot->type].weapon;
    if (shot->active != 1) return;
    shot->active = 2;
    shot->impact_tick = b->tick;
    ++b->impacts;
    battle_bridge_impact(b, shot);
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        int64_t dx = (int64_t)u->x - shot->x, dy = (int64_t)u->y - shot->y;
        int64_t dz = (int64_t)ra_battle_unit_height(b, u) * 256 - shot->z;
        uint32_t distance = battle_sqrt((uint64_t)(dx * dx + dy * dy + dz * dz)) / 256;
        if (b->types[u->type].structure) distance = battle_structure_distance(b, u, shot->x, shot->y, shot->z);
        if (!u->health || (u->traits & (RA_UNIT_LIMBO | RA_UNIT_IMMUNE))) continue;
        uint32_t damage = battle_damage(w, b->types[u->type].armor, distance);
        if (!damage) continue;
        shot->hit = u->id;
        if (damage >= u->health) battle_kill(b, u, shot->owner);
        else
        {
            u->health -= damage;
            /* 受击还击保留警戒、移动攻击和路径任务，交战结束后恢复原任务。 */
            if (!u->target && u->order != RA_ORDER_FORCE_GROUND && u->order != RA_ORDER_FORCE_UNIT && shot->owner && b->units[shot->owner - 1].health &&
                !ra_battle_allied(b, u->team, shot->team) && ra_battle_targetable(b, u, &b->units[shot->owner - 1], false, false) &&
                b->types[u->type].weapon.verses[b->types[b->units[shot->owner - 1].type].armor] > 100)
            {
                u->target = shot->owner;
                if (u->order != RA_ORDER_GUARD && u->order != RA_ORDER_ATTACK_MOVE && u->order != RA_ORDER_WAYPOINT) u->order = RA_ORDER_ATTACK;
                u->goal = u->next;
                u->path_count = u->path_cursor = 0;
            }
        }
    }
}

static bool position_cell(const ra_battle *b, int32_t x, int32_t y, uint32_t *cell)
{
    int64_t px = (int64_t)x + RA_BATTLE_CELL / 2, py = (int64_t)y + RA_BATTLE_CELL / 2;
    if (px < 0 || py < 0 || px >= (int64_t)b->width * RA_BATTLE_CELL || py >= (int64_t)b->height * RA_BATTLE_CELL) return false;
    *cell = (uint32_t)(py / RA_BATTLE_CELL) * b->width + (uint32_t)(px / RA_BATTLE_CELL);
    return true;
}
static void retire(ra_battle *b, ra_battle_shot *s, uint32_t reason)
{
    if (b->types[s->type].weapon.missile && s->owner && s->owner <= b->count)
    {
        uint32_t ready = b->tick + b->types[s->type].weapon.regeneration;
        if (ready > b->units[s->owner - 1].spawn_ready) b->units[s->owner - 1].spawn_ready = ready;
    }
    s->active = 3;
    s->retired_tick = b->tick;
    if (reason) s->collision = reason;
}
static void collide(ra_battle *b, ra_battle_shot *s, uint32_t reason)
{
    s->collision = reason;
    impact(b, s);
}
bool battle_projectile_snap(const ra_battle *b, ra_battle_shot *s)
{
    if (!s->target || s->target > b->count) return false;
    const ra_battle_unit *target = &b->units[s->target - 1];
    if (!target->health || (target->traits & (RA_UNIT_LIMBO | RA_UNIT_SINKING))) return false;
    if (b->types[target->type].structure)
    {
        s->x = s->end_x;
        s->y = s->end_y;
        s->z = s->end_z;
        return true;
    }
    int32_t dx = (s->x - target->x) / 256, dy = (s->y - target->y) / 256;
    int32_t dz = (s->z / 256 + ra_battle_unit_height(b, target)) / 2 - ra_battle_unit_height(b, target);
    battle_real vx = battle_real_int(dx), vy = battle_real_int(dy), vz = battle_real_int(dz);
    battle_real distance = battle_legacy_sqrt(battle_real_add(battle_real_add(battle_real_mul(vx, vx), battle_real_mul(vy, vy)), battle_real_mul(vz, vz)));
    uint32_t third = (uint32_t)battle_real_integer(distance) / 3;
    battle_real square = battle_real_add(battle_real_mul(s->velocity[0], s->velocity[0]), battle_real_mul(s->velocity[1], s->velocity[1]));
    square = battle_real_add(square, battle_real_mul(s->velocity[2], s->velocity[2]));
    battle_real reach = battle_real_mul(battle_legacy_sqrt(square), battle_real_int(2));
    if (battle_real_compare(reach, battle_real_int(128)) < 0) reach = battle_real_int(128);
    if (battle_real_compare(battle_real_int((int32_t)third), reach) > 0) return false;
    /* 原版 460cee..460e98：近目标格命中可修正到仍有效的目标坐标。 */
    s->x = target->x;
    s->y = target->y;
    s->z = ra_battle_unit_height(b, target) * 256;
    return true;
}
/* 导弹采用整数分段飞行参考：起竖、爬升、巡航和俯冲。轨迹参数仍需原版实机校准。 */
static void missile_advance(ra_battle *b, ra_battle_shot *s)
{
    if (!s->health)
    {
        retire(b, s, RA_COLLISION_OBJECT);
        return;
    }
    ++s->age;
    if (s->age <= s->launch_delay)
    {
        s->z = s->start_z + (int32_t)((uint64_t)s->cruise_height * 256 * s->age / (s->launch_delay ? s->launch_delay : 1));
        return;
    }
    uint32_t elapsed = s->age - s->launch_delay, duration = s->duration ? s->duration : 1;
    if (elapsed > duration) elapsed = duration;
    s->x = s->start_x + (int32_t)((int64_t)(s->end_x - s->start_x) * elapsed / duration);
    s->y = s->start_y + (int32_t)((int64_t)(s->end_y - s->start_y) * elapsed / duration);
    int32_t cruise = s->start_z + (int32_t)s->cruise_height * 256;
    s->z = elapsed * 2 < duration ? cruise : cruise + (int32_t)((int64_t)(s->end_z - cruise) * (elapsed * 2 - duration) / duration);
    if (elapsed == duration)
    {
        s->z = s->end_z;
        collide(b, s, RA_COLLISION_TARGET_CELL);
    }
}

static void advance(ra_battle *b, ra_battle_shot *s)
{
    const ra_battle_weapon *w = &b->types[s->type].weapon;
    int32_t oldx = s->x, oldy = s->y, oldz = s->z;
    uint32_t cell, previous = 0, destination;
    if (s->active == 3)
    {
        if (b->tick > s->retired_tick) *s = (ra_battle_shot){0};
        return;
    }
    if (s->active == 2)
    {
        if (b->tick - s->impact_tick > 12) retire(b, s, 0);
        return;
    }
    if (s->active != 1) return;
    if (w->missile)
    {
        missile_advance(b, s);
        return;
    }
    if (w->projectile_rot && !w->arcing)
    {
        ++s->age;
        if (s->target && s->target <= b->count && b->units[s->target - 1].health && !(b->units[s->target - 1].traits & RA_UNIT_LIMBO))
        {
            const ra_battle_unit *target = &b->units[s->target - 1];
            s->end_x = target->x;
            s->end_y = target->y;
            s->end_z = ra_battle_unit_height(b, target) * 256;
        }
        int64_t dx = (int64_t)s->end_x - s->x, dy = (int64_t)s->end_y - s->y, dz = (int64_t)s->end_z - s->z;
        uint32_t distance = battle_sqrt((uint64_t)(dx * dx + dy * dy + dz * dz)), rate = w->speed * 256;
        if (distance <= rate)
        {
            s->x = s->end_x;
            s->y = s->end_y;
            s->z = s->end_z;
            collide(b, s, RA_COLLISION_TARGET_CELL);
        }
        else
        {
            s->x += (int32_t)(dx * rate / distance);
            s->y += (int32_t)(dy * rate / distance);
            s->z += (int32_t)(dz * rate / distance);
            if (s->age > 4096) retire(b, s, RA_COLLISION_EXPIRED);
        }
        return;
    }
    ++s->age;
    if (w->arcing)
    {
        int32_t position[3] = {s->x / 256, s->y / 256, s->z / 256};
        battle_projectile_step(position, s->velocity, battle_real_ratio(w->gravity, w->floater ? 512 : 256));
        s->x = position[0] * 256;
        s->y = position[1] * 256;
        s->z = position[2] * 256;
    }
    else
    {
        uint32_t duration = s->duration ? s->duration : 1;
        s->x = s->start_x + (int32_t)((int64_t)(s->end_x - s->start_x) * s->age / duration);
        s->y = s->start_y + (int32_t)((int64_t)(s->end_y - s->start_y) * s->age / duration);
        s->z = s->start_z + (int32_t)((int64_t)(s->end_z - s->start_z) * s->age / duration);
    }
    if (!position_cell(b, s->x, s->y, &cell))
    {
        retire(b, s, RA_COLLISION_OUTSIDE);
        return;
    }
    position_cell(b, oldx, oldy, &previous);
    int32_t ground = ra_battle_ground_height(b, s->x, s->y), deck = ground + 4 * 104;
    bool bridge = (b->bridges[cell] & 4) || (b->bridges[previous] & 4);
    uint32_t surface = battle_surface_collision(oldz / 256, s->z / 256, ground, deck, bridge);
    if (surface && (w->arcing || w->elevation))
    {
        s->z = (surface == RA_COLLISION_BRIDGE_UP ? deck - 20 : surface == RA_COLLISION_BRIDGE_DOWN ? deck : ground) * 256;
    }
    else surface = RA_COLLISION_NONE;
    /* 墙体扫格用于防止高速穿墙，使用原版近地 150 lepton 门限；不发明悬崖附加高度。 */
    uint32_t subdivisions = (uint32_t)(abs(s->x - oldx) + abs(s->y - oldy)) / (RA_BATTLE_CELL / 8) + 1;
    for (uint32_t i = 1; i <= subdivisions && (w->walls || w->cliffs); ++i)
    {
        int32_t x = oldx + (int32_t)((int64_t)(s->x - oldx) * i / subdivisions), y = oldy + (int32_t)((int64_t)(s->y - oldy) * i / subdivisions);
        int32_t z = oldz + (int32_t)((int64_t)(s->z - oldz) * i / subdivisions);
        uint32_t at;
        if (!position_cell(b, x, y, &at)) continue;
        bool wall = w->walls && b->tiles[at].land == 4 && z / 256 < ra_battle_ground_height(b, x, y) + 150;
        bool cliff = w->cliffs && b->tiles[at].land == 3 && z / 256 < ra_battle_ground_height(b, x, y);
        if (wall || cliff)
        {
            s->x = x;
            s->y = y;
            s->z = z;
            collide(b, s, wall ? RA_COLLISION_WALL : RA_COLLISION_CLIFF);
            return;
        }
    }
    if (position_cell(b, s->end_x, s->end_y, &destination) && cell == destination && s->z / 256 - ground < 2 * 104)
    {
        battle_projectile_snap(b, s);
        collide(b, s, surface ? surface : RA_COLLISION_TARGET_CELL);
        return;
    }
    if (surface)
    {
        collide(b, s, surface);
        return;
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!u->health || u->id == s->owner || ra_battle_allied(b, u->team, s->team) || (u->traits & (RA_UNIT_LIMBO | RA_UNIT_SINKING))) continue;
        int64_t dx = ((int64_t)s->x - u->x) / 256, dy = ((int64_t)s->y - u->y) / 256, dz = (int64_t)s->z / 256 - ra_battle_unit_height(b, u);
        if (b->types[u->type].structure ? battle_structure_distance(b, u, s->x, s->y, s->z) == 0 : dx * dx + dy * dy + dz * dz < 128 * 128)
        {
            collide(b, s, RA_COLLISION_OBJECT);
            return;
        }
    }
    if ((w->arm || w->proximity) && s->age >= w->arm)
    {
        uint32_t fuse = battle_fuse((s->x - s->end_x) / 256, (s->y - s->end_y) / 256, (s->z - s->end_z) / 256, &s->fuse_distance);
        if (fuse && (w->ranged || fuse == 1))
        {
            if (fuse == 1) battle_projectile_snap(b, s);
            collide(b, s, RA_COLLISION_TARGET_CELL);
            return;
        }
    }
    if (!w->arcing && s->age >= s->duration) collide(b, s, RA_COLLISION_TARGET_CELL);
    else if (s->age >= 256) retire(b, s, RA_COLLISION_EXPIRED);
}

void battle_combat(ra_battle *b)
{
    /* 先按固定槽号推进既有弹体，再按单位编号发射；同一输入始终使用相同顺序。 */
    for (uint32_t i = 0; i < RA_BATTLE_SHOTS; ++i) advance(b, &b->shots[i]);
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i], aim, *v = &aim;
        const ra_battle_weapon *w = &b->types[u->type].weapon;
        ra_battle_shot *shot = NULL;
        if (!u->health || (u->traits & RA_UNIT_LIMBO)) continue;
        if (b->types[u->type].powered)
        {
            uint32_t output, drain;
            ra_battle_power(b, u->team, &output, &drain);
            if (output < drain) continue;
        }
        if (u->cooldown) --u->cooldown;
        if (w->aa && w->damage && !u->cooldown)
        {
            for (uint32_t j = 0; j < RA_BATTLE_SHOTS; ++j)
            {
                ra_battle_shot *missile = &b->shots[j];
                if (missile->active != 1 || !missile->health || ra_battle_allied(b, u->team, missile->team)) continue;
                int64_t dx = (int64_t)missile->x - u->x, dy = (int64_t)missile->y - u->y;
                if ((uint64_t)(dx * dx + dy * dy) > (uint64_t)w->range * w->range) continue;
                uint32_t damage = battle_damage(w, 10, 0);
                if (!damage) continue;
                missile->health = damage >= missile->health ? 0 : missile->health - damage;
                u->cooldown = w->rof;
                ++u->shots;
                ++b->fired;
                break;
            }
        }
        if (u->order == RA_ORDER_ENTER || u->order == RA_ORDER_LOAD || !w->damage || !w->speed || u->cooldown || !battle_aim(b, u, v)) continue;
        if (w->missile && !u->burst_left)
        {
            bool in_flight = false;
            for (uint32_t j = 0; j < RA_BATTLE_SHOTS; ++j)
                if (b->shots[j].active == 1 && b->shots[j].owner == u->id) in_flight = true;
            if (in_flight || b->tick < u->spawn_ready) continue;
        }
        if ((b->types[u->type].ammo && !u->ammunition) || !in_range(u, v, w->range) || battle_distance_squared(u, v) < (uint64_t)w->minimum * w->minimum ||
            b->tick - u->turret.started < u->turret.duration)
            continue;
        if (b->types[u->type].instant_weapon && v->id && v->id <= b->count)
        {
            ra_battle_unit *target = &b->units[v->id - 1];
            uint32_t damage = battle_damage(w, b->types[target->type].armor, 0);
            if (damage >= target->health) battle_kill(b, target, u->id);
            else target->health -= damage;
            if (!u->burst_left) u->burst_left = w->burst ? w->burst : 1;
            --u->burst_left;
            u->cooldown = u->burst_left ? 3 : (w->regeneration > w->rof ? w->regeneration : w->rof) + battle_random_delay(b);
            if (b->types[u->type].ammo && !u->burst_left && u->ammunition) --u->ammunition;
            ++u->shots;
            ++b->fired;
            ++b->impacts;
            continue;
        }
        for (uint32_t j = 0; j < RA_BATTLE_SHOTS; ++j)
            if (!b->shots[j].active)
            {
                shot = &b->shots[j];
                break;
            }
        if (!shot)
        {
            ++b->dropped_shots;
            continue;
        }
        uint32_t duration = (battle_sqrt(battle_distance_squared(u, v)) + w->speed * 256 - 1) / (w->speed * 256);
        if (!duration) duration = 1;
        /* 弧线按独立速度推进；名义 Speed 不能触发直线弹体的时间上限而拒绝发射。 */
        if (w->arcing && duration > 256) duration = 256;
        if (duration > (w->missile ? 4096u : 256u))
        {
            ++b->dropped_shots;
            continue;
        }
        *shot = (ra_battle_shot){0};
        shot->id = ++b->next_shot;
        shot->active = 1;
        shot->owner = u->id;
        shot->target = v->id;
        shot->type = u->type;
        shot->team = u->team;
        int32_t muzzle[3] = {u->x / 256, u->y / 256, ra_battle_unit_height(b, u)};
        uint32_t ramp = ra_battle_unit_ramp(b, u);
        battle_chassis_muzzle(&b->types[u->type], ramp, ra_battle_turn_value(&u->body, b->tick), ra_battle_turn_value(&u->turret, b->tick), muzzle);
        shot->x = shot->start_x = muzzle[0] * 256;
        shot->y = shot->start_y = muzzle[1] * 256;
        shot->z = shot->start_z = muzzle[2] * 256;
        shot->end_x = v->x;
        shot->end_y = v->y;
        shot->end_z = ra_battle_unit_height(b, v) * 256;
        shot->duration = duration;
        shot->fuse_distance = INT32_MAX;
        shot->health = w->missile ? w->missile_health : 0;
        shot->launch_delay = w->launch_delay;
        shot->cruise_height = w->altitude;
        if (w->arcing &&
            !battle_projectile_launch(w, (shot->end_x - shot->x) / 256, (shot->end_y - shot->y) / 256, (shot->end_z - shot->z) / 256, shot->velocity))
        {
            *shot = (ra_battle_shot){0};
            --b->next_shot;
            ++b->dropped_shots;
            continue;
        }
        if (!u->burst_left) u->burst_left = w->burst ? w->burst : 1;
        --u->burst_left;
        u->cooldown = u->burst_left ? 3 : (w->regeneration > w->rof ? w->regeneration : w->rof) + battle_random_delay(b);
        if (b->types[u->type].ammo && !u->burst_left && u->ammunition) --u->ammunition;
        ++u->shots;
        ++b->fired;
    }
}
