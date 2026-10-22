#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

const ra_battle_faction ra_battle_factions[3] = {{"ra2.allied", true}, {"ra2.soviet", true}, {"future.china", false}};
uint8_t ra_battle_land(uint8_t tmp_land)
{
    static const uint8_t mapping[16] = {0, 8, 8, 8, 8, 10, 9, 3, 3, 2, 6, 1, 1, 0, 7, 3};
    return tmp_land < 16 ? mapping[tmp_land] : 255;
}

bool ra_battle_passable(const ra_battle *b, uint32_t cell)
{
    return b && b->tiles && cell < 2 * b->width * b->height && !b->tiles[cell].blocked && b->tiles[cell].track > 0;
}

static bool free_cell(const ra_battle *b, uint32_t cell, uint32_t unit)
{
    return battle_cell_available(b, cell, unit);
}

bool ra_battle_edge(const ra_battle *b, uint32_t from, uint32_t to, uint32_t unit)
{
    int dx, dy;
    if (!battle_cell_passable(b, from, unit) || !free_cell(b, to, unit)) return false;
    dx = (int)(to % b->width) - (int)(from % b->width);
    dy = (int)ra_battle_cell_y(b, to) - (int)ra_battle_cell_y(b, from);
    if (abs(dx) > 1 || abs(dy) > 1 || (!dx && !dy)) return false;
    if (!battle_bridge_edge(b, from, to)) return false;
    /* 斜向移动必须同时通过两个正交边，防止穿过墙角或跨越悬崖。 */
    if (dx && dy)
    {
        if (from / (b->width * b->height) != to / (b->width * b->height)) return false;
        uint32_t a = (uint32_t)((int)from + dx), c = (uint32_t)((int)from + dy * (int)b->width);
        return ra_battle_edge(b, from, a, unit) && ra_battle_edge(b, from, c, unit) && ra_battle_edge(b, a, to, unit) && ra_battle_edge(b, c, to, unit);
    }
    return true;
}

void ra_battle_close(ra_battle *b)
{
    battle_search *s;
    if (!b) return;
    s = b->search;
    if (s)
    {
        free(s->cost);
        free(s->parent);
        free(s->heap);
        free(s->position);
        free(s->closed);
        free(s->canonical);
        free(s);
    }
    free(b->tiles);
    free(b->bridges);
    free(b->initial_tiles);
    free(b->initial_bridges);
    free(b->bridge_parts);
    free(b->initial_parts);
    free(b->bridge_at);
    free(b->occupied);
    free(b->units);
    free(b->initial);
    free(b->commands);
    free(b->shots);
    free(b->types);
    battle_economy_close(b);
    battle_campaign_close(b);
    memset(b, 0, sizeof(*b));
}

bool ra_battle_create(ra_battle *b, uint32_t width, uint32_t height, const ra_battle_tile *tiles, const uint8_t content[20], ra_error *error)
{
    ra_battle r = {0};
    battle_search *s;
    size_t n, i;
    if (!b || !tiles || !width || !height || width > 512 || height > 512) return ra_fail(error, RA_ARGUMENT, 0, "invalid battlefield dimensions");
    n = (size_t)width * height;
    for (i = 0; i < n; ++i)
        if (tiles[i].track > 1000) return ra_fail(error, RA_RANGE, 0, "terrain multiplier exceeds 1000 percent");
    r.width = width;
    r.height = height;
    r.types = calloc(RA_BATTLE_TYPES, sizeof(*r.types));
    r.tiles = calloc(2 * n, sizeof(*r.tiles));
    r.bridges = calloc(n, 1);
    r.initial_tiles = calloc(2 * n, sizeof(*r.tiles));
    r.initial_bridges = calloc(n, 1);
    r.bridge_parts = calloc(RA_BATTLE_BRIDGES, sizeof(*r.bridge_parts));
    r.initial_parts = calloc(RA_BATTLE_BRIDGES, sizeof(*r.initial_parts));
    r.bridge_at = calloc(n, sizeof(*r.bridge_at));
    r.bridge_strength = 1500;
    r.occupied = calloc(2 * n, sizeof(*r.occupied));
    r.units = calloc(RA_BATTLE_UNITS, sizeof(*r.units));
    r.initial = calloc(RA_BATTLE_UNITS, sizeof(*r.initial));
    r.commands = calloc(RA_BATTLE_COMMANDS, sizeof(*r.commands));
    r.shots = calloc(RA_BATTLE_SHOTS, sizeof(*r.shots));
    r.search = s = calloc(1, sizeof(*s));
    if (s)
    {
        s->cost = malloc(2 * n * sizeof(uint64_t));
        s->parent = malloc(2 * n * sizeof(uint32_t));
        s->heap = malloc(2 * n * sizeof(uint32_t));
        s->position = malloc(2 * n * sizeof(uint32_t));
        s->closed = malloc(2 * n);
        s->canonical = malloc(n * 21 + RA_BATTLE_BRIDGES * 32 + RA_BATTLE_UNITS * (RA_BATTLE_PATH * 4 + RA_BATTLE_WAYPOINTS * 4 + 512) + RA_BATTLE_SHOTS * 128 +
                              RA_BATTLE_TYPES * 2048 + n + 2097152);
    }
    if (!r.types || !r.initial_tiles || !r.initial_bridges || !r.bridge_parts || !r.initial_parts || !r.bridge_at || !r.tiles || !r.bridges || !r.occupied ||
        !r.units || !r.initial || !r.commands || !r.shots || !s || !s->cost || !s->parent || !s->heap || !s->position || !s->closed || !s->canonical)
    {
        ra_battle_close(&r);
        return ra_fail(error, RA_MEMORY, 0, "battlefield allocation failed");
    }
    memcpy(r.tiles, tiles, n * sizeof(*tiles));
    for (i = n; i < 2 * n; ++i) r.tiles[i].blocked = 1;
    if (content) memcpy(r.content, content, 20);
    battle_random_reset(&r);
    *b = r;
    return true;
}

bool ra_battle_type_add(ra_battle *b, const char *id, const char *faction, uint32_t step, ra_error *error)
{
    size_t i;
    if (!b || !b->tiles || b->economy || b->tick || b->count || b->type_count == RA_BATTLE_TYPES || !id || !faction || !*id || strlen(id) >= 32 ||
        strlen(faction) >= 32 || !step || step > 65536)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid type registration");
    for (i = 0; i < 3; ++i)
        if (!strcmp(faction, ra_battle_factions[i].id) && !ra_battle_factions[i].enabled)
            return ra_fail(error, RA_ARGUMENT, 0, "faction content is reserved and inactive");
    for (i = 0; i < b->type_count; ++i)
        if (!strcmp(id, b->types[i].id)) return ra_fail(error, RA_ARGUMENT, 0, "duplicate type identifier");
    strcpy(b->types[b->type_count].id, id);
    strcpy(b->types[b->type_count].faction, faction);
    b->types[b->type_count++].step = step;
    b->types[b->type_count - 1].strength = 100;
    b->types[b->type_count - 1].passive_acquire = true;
    b->types[b->type_count - 1].size = b->types[b->type_count - 1].size_limit = 1;
    b->types[b->type_count - 1].uphill = b->types[b->type_count - 1].downhill = 10000;
    b->types[b->type_count - 1].acceleration = 300;
    b->types[b->type_count - 1].sight = 8 * RA_BATTLE_CELL;
    for (unsigned k = 0; k < 5; ++k) b->types[b->type_count - 1].threat_coefficients[k] = k == 4 ? -10000 : 2000000;
    b->types[b->type_count - 1].flh[2] = 100;
    b->types[b->type_count - 1].weapon.max_damage = 10000;
    return true;
}

bool ra_battle_spawn(ra_battle *b, uint32_t type, uint32_t x, uint32_t y, ra_error *error)
{
    return ra_battle_spawn_team(b, type, 1, x, y, error);
}

bool ra_battle_spawn_team(ra_battle *b, uint32_t type, uint32_t team, uint32_t x, uint32_t y, ra_error *error)
{
    return ra_battle_spawn_layer(b, type, team, x, y, 0, error);
}

bool ra_battle_spawn_layer(ra_battle *b, uint32_t type, uint32_t team, uint32_t x, uint32_t y, uint32_t layer, ra_error *error)
{
    return battle_spawn_mobile(b, type, team, x, y, layer, false, error);
}
bool battle_spawn_mobile(ra_battle *b, uint32_t type, uint32_t team, uint32_t x, uint32_t y, uint32_t layer, bool runtime, ra_error *error)
{
    ra_battle_unit *u;
    uint32_t cell;
    if (!b || layer > 1 || (!runtime && (b->tick || b->command_count)) || !team || team > RA_BATTLE_TEAMS || type >= b->type_count ||
        b->count == RA_BATTLE_UNITS || x >= b->width || y >= b->height)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial unit");
    cell = y * b->width + x + layer * b->width * b->height;
    if (b->types[type].structure) return ra_fail(error, RA_ARGUMENT, 0, "use the structure constructor for building types");
    if ((!battle_type_passable(b, cell, &b->types[type]) || (!b->types[type].flying && !b->types[type].infantry && b->occupied[cell])))
        return ra_fail(error, RA_ARGUMENT, 0, "spawn cell is blocked");
    if (!b->types[type].infantry && !b->types[type].flying)
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && !(b->units[i].traits & RA_UNIT_LIMBO) && b->types[b->units[i].type].infantry &&
                (b->units[i].cell == cell || b->units[i].next == cell))
                return ra_fail(error, RA_ARGUMENT, 0, "vehicle spawn overlaps infantry");
    if (b->types[type].infantry)
    {
        uint32_t feet = 0;
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && b->types[b->units[i].type].infantry && !(b->units[i].traits & RA_UNIT_LIMBO) &&
                (b->units[i].cell == cell || b->units[i].next == cell))
                ++feet;
        if (!battle_type_passable(b, cell, &b->types[type]) || b->occupied[cell] || feet >= 5) return ra_fail(error, RA_ARGUMENT, 0, "infantry cell is full");
    }
    u = &b->units[b->count];
    memset(u, 0, sizeof(*u));
    u->id = b->count + 1;
    u->type = type;
    u->team = team;
    u->health = b->types[type].strength;
    u->speed_factor = 10000;
    u->motion_factor = BATTLE_ONE;
    u->cell = u->next = u->goal = cell;
    u->destination = u->anchor = u->fire_cell = cell;
    u->x = (int32_t)(x * RA_BATTLE_CELL);
    u->y = (int32_t)(y * RA_BATTLE_CELL);
    if (b->types[type].infantry)
    {
        uint32_t used = 0;
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && b->types[b->units[i].type].infantry && b->units[i].cell == cell) used |= 1u << b->units[i].subcell;
        for (u->subcell = 0; u->subcell < 5 && (used & (1u << u->subcell)); ++u->subcell)
        {
        }
    }
    else if (!b->types[type].flying) b->occupied[cell] = u->id;
    u->ammunition = b->types[type].ammo;
    if (b->types[type].flying)
    {
        u->traits |= RA_UNIT_AIRBORNE;
        u->altitude = (int32_t)b->types[type].flight_height;
    }
    ++b->count;
    if (!runtime)
    {
        b->initial[b->count - 1] = *u;
        b->initial_count = b->count;
    }
    return true;
}

bool ra_battle_command_add(ra_battle *b, uint32_t tick, uint32_t unit, uint32_t target, ra_error *error)
{
    return ra_battle_order_add(b, tick, unit, RA_ORDER_MOVE, target, error);
}

static bool before(const battle_search *s, uint32_t a, uint32_t c)
{
    return s->cost[a] < s->cost[c] || (s->cost[a] == s->cost[c] && a < c);
}

static void heap_up(battle_search *s, uint32_t at)
{
    uint32_t value = s->heap[at];
    while (at)
    {
        uint32_t parent = (at - 1) / 2, other = s->heap[parent];
        if (!before(s, value, other)) break;
        s->heap[at] = other;
        s->position[other] = at;
        at = parent;
    }
    s->heap[at] = value;
    s->position[value] = at;
}

static uint32_t heap_pop(battle_search *s)
{
    uint32_t result = s->heap[0], value = s->heap[--s->count], at = 0;
    while (at * 2 + 1 < s->count)
    {
        uint32_t child = at * 2 + 1;
        if (child + 1 < s->count && before(s, s->heap[child + 1], s->heap[child])) ++child;
        if (!before(s, s->heap[child], value)) break;
        s->heap[at] = s->heap[child];
        s->position[s->heap[at]] = at;
        at = child;
    }
    s->heap[at] = value;
    s->position[value] = at;
    return result;
}

static bool route(ra_battle *b, uint32_t unit, uint32_t target, const ra_battle_unit *enemy, uint32_t range)
{
    battle_search *s;
    ra_battle_unit *u;
    uint32_t current, n, i;
    bool found = false;
    static const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1}, dy[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
    if (!b || !unit || unit > b->count || (!enemy && !free_cell(b, target, unit))) return false;
    if (b->types[b->units[unit - 1].type].structure) return false;
    s = b->search;
    u = &b->units[unit - 1];
    n = 2 * b->width * b->height;
    u->path_count = u->path_cursor = 0;
    uint32_t origin = u->next;
    if (!enemy && origin == target) return true;
    memset(s->cost, 255, n * sizeof(uint64_t));
    memset(s->closed, 0, n);
    s->count = 1;
    s->heap[0] = origin;
    s->position[origin] = 0;
    s->cost[origin] = 0;
    /* 有权 Dijkstra 使用稳定格号打破平局，是后续并行寻路的单线程参考。 */
    while (s->count)
    {
        current = heap_pop(s);
        s->closed[current] = 1;
        if (enemy)
        {
            int64_t vx = (int64_t)(current % b->width) * RA_BATTLE_CELL - enemy->x;
            int64_t vy = (int64_t)ra_battle_cell_y(b, current) * RA_BATTLE_CELL - enemy->y;
            if ((uint64_t)(vx * vx + vy * vy) <= (uint64_t)range * range)
            {
                target = current;
                found = true;
                break;
            }
        }
        else if (current == target)
        {
            found = true;
            break;
        }
        for (i = 0; i < 16; ++i)
        {
            int x = (int)(current % b->width) + dx[i % 8], y = (int)ra_battle_cell_y(b, current) + dy[i % 8];
            uint32_t next;
            uint64_t cost;
            if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
            next = (uint32_t)y * b->width + (uint32_t)x + (i / 8) * (n / 2);
            if (s->closed[next] || !ra_battle_edge(b, current, next, unit)) continue;
            cost = s->cost[current] + ((dx[i % 8] && dy[i % 8]) ? 141420u : 100000u) /
                                          ((b->types[u->type].amphibious || b->types[u->type].naval) && b->tiles[next].land == 2 ? 100u : b->tiles[next].track);
            if (cost >= s->cost[next]) continue;
            if (s->cost[next] == UINT64_MAX)
            {
                s->position[next] = s->count;
                s->heap[s->count++] = next;
            }
            s->cost[next] = cost;
            s->parent[next] = current;
            heap_up(s, s->position[next]);
        }
    }
    if (!found) return false;
    current = target;
    while (current != origin)
    {
        if (u->path_count == RA_BATTLE_PATH)
        {
            u->path_count = 0;
            return false;
        }
        u->path[u->path_count++] = current;
        current = s->parent[current];
    }
    for (i = 0; i < u->path_count / 2; ++i)
    {
        uint32_t swap = u->path[i];
        u->path[i] = u->path[u->path_count - i - 1];
        u->path[u->path_count - i - 1] = swap;
    }
    if (enemy) u->goal = target;
    return true;
}

bool ra_battle_route(ra_battle *b, uint32_t unit, uint32_t target)
{
    return route(b, unit, target, NULL, 0);
}
bool battle_route_range(ra_battle *b, uint32_t unit, const ra_battle_unit *enemy, uint32_t range)
{
    return enemy && route(b, unit, 0, enemy, range);
}

void ra_battle_step(ra_battle *b)
{
    if (!b || !b->tiles || b->tick >= 10000000) return;
    battle_terrain_seal(b);
    ++b->tick;
    while (b->command_cursor < b->command_count && b->commands[b->command_cursor].tick == b->tick)
    {
        const ra_battle_command *c = &b->commands[b->command_cursor++];
        battle_command_apply(b, c);
    }
    battle_economy_step(b);
    battle_gates_step(b);
    battle_missions(b);
    battle_attack_orders(b);
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].traits & RA_UNIT_LIMBO) continue;
        else if (b->types[b->units[i].type].flying || b->types[b->units[i].type].naval) battle_sea_air_move(b, &b->units[i]);
        else if (b->types[b->units[i].type].infantry) battle_people_move(b, &b->units[i]);
        else battle_move(b, &b->units[i]);
    battle_people_step(b);
    battle_transport_step(b);
    battle_combat(b);
    battle_campaign_step(b);
}
void ra_battle_reset(ra_battle *b)
{
    if (!b || !b->tiles) return;
    if (b->terrain_sealed)
    {
        memcpy(b->tiles, b->initial_tiles, (size_t)2 * b->width * b->height * sizeof(*b->tiles));
        memcpy(b->bridges, b->initial_bridges, (size_t)b->width * b->height);
        memcpy(b->bridge_parts, b->initial_parts, b->bridge_count * sizeof(*b->bridge_parts));
    }
    b->topology_revision = b->bridge_hits = b->bridge_destroyed = b->bridge_repaired = b->bridge_falls = 0;
    if (b->terrain_sealed) b->count = b->initial_count;
    memset(b->units, 0, RA_BATTLE_UNITS * sizeof(*b->units));
    memcpy(b->units, b->initial, b->count * sizeof(*b->units));
    if (b->economy && b->terrain_sealed)
    {
        b->economy->state = b->economy->initial;
        memcpy(b->economy->ore, b->economy->initial_ore, (size_t)b->width * b->height);
    }
    battle_campaign_reset(b);
    memset(b->occupied, 0, (size_t)2 * b->width * b->height * sizeof(*b->occupied));
    battle_initial_occupancy(b, b->occupied);
    b->tick = b->command_cursor = b->rejected = 0;
    memset(b->shots, 0, RA_BATTLE_SHOTS * sizeof(*b->shots));
    b->next_shot = b->fired = b->impacts = b->kills = b->dropped_shots = 0;
    battle_random_reset(b);
}

uint32_t ra_battle_clock(uint64_t *phase, uint64_t microseconds)
{
    uint64_t total, ticks;
    if (!phase || *phase >= 1000000 || microseconds > UINT64_MAX / RA_BATTLE_HZ - 1000000) return 0;
    total = *phase + microseconds * RA_BATTLE_HZ;
    ticks = total / 1000000;
    if (ticks > UINT32_MAX) return 0;
    *phase = total % 1000000;
    return (uint32_t)ticks;
}
