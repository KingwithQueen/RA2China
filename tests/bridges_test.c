#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

static unsigned checks, failures;
#define CHECK(value)                                                                                                                                           \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "line %d: %s\n", __LINE__, #value);                                                                                                \
        }                                                                                                                                                      \
    } while (0)

static void fixture(ra_battle *b, uint32_t kind, uint32_t axis, uint32_t frame)
{
    ra_error e = {0};
    ra_battle_tile tiles[256];
    for (unsigned i = 0; i < 256; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    for (unsigned a = 5; a <= 10; ++a)
        for (unsigned side = 7; side <= 9; ++side)
        {
            uint32_t c = axis == 1 ? side * 16 + a : a * 16 + side;
            tiles[c] = (ra_battle_tile){0, 0, 0, 0, 2};
        }
    if (kind < 2)
        for (unsigned side = 7; side <= 9; ++side)
        {
            tiles[axis == 1 ? side * 16 + 4 : 4 * 16 + side].height = 4;
            tiles[axis == 1 ? side * 16 + 11 : 11 * 16 + side].height = 4;
        }
    CHECK(ra_battle_create(b, 16, 16, tiles, NULL, &e));
    for (unsigned a = 5; a <= 10; ++a)
        for (unsigned side = kind < 2 ? 8u : 7u; side <= (kind < 2 ? 8u : 9u); ++side)
            CHECK(ra_battle_bridge_segment_add(b, axis == 1 ? side * 16 + a : a * 16 + side, axis, kind, frame, &e));
    CHECK(ra_battle_type_add(b, "MTNK", "ra2.allied", 17 * 256, &e));
    b->types[0].rot = 5;
}

static void occupancy(const ra_battle *b)
{
    for (uint32_t c = 0; c < 2 * b->width * b->height; ++c)
    {
        if (!b->occupied[c]) continue;
        uint32_t id = b->occupied[c];
        CHECK(id <= b->count && b->units[id - 1].health && ra_battle_passable(b, c));
        const ra_battle_unit *u = &b->units[id - 1];
        bool owned = u->cell == c || u->next == c;
        for (uint32_t j = 0; j < u->reserved_count; ++j) owned |= u->reserved[j] == c;
        CHECK(owned);
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!u->health) CHECK(!u->reserved_count && !u->track_active);
        else CHECK(b->occupied[u->cell] == u->id);
    }
}

static void lifecycle(void)
{
    for (uint32_t kind = 0; kind < 4; ++kind)
        for (uint32_t axis = 1; axis <= 2; ++axis)
        {
            ra_battle b = {0};
            ra_error e = {0};
            fixture(&b, kind, axis, kind < 2 ? (axis == 1 ? 0u : 9u) : (axis == 1 ? 1u : 10u));
            uint32_t cell = axis == 1 ? 8 * 16 + 7 : 7 * 16 + 8;
            CHECK(ra_battle_spawn_layer(&b, 0, 1, cell % 16, cell / 16, kind < 2 ? 1u : 0u, &e));
            CHECK(ra_battle_bridge_event_add(&b, 1, RA_EVENT_BRIDGE_HIT, cell, &e));
            CHECK(ra_battle_bridge_event_add(&b, 2, RA_EVENT_BRIDGE_HIT, cell, &e));
            CHECK(ra_battle_bridge_event_add(&b, 3, RA_EVENT_BRIDGE_REPAIR, cell, &e));
            ra_battle_step(&b);
            CHECK(b.units[0].health && !b.bridge_falls && b.bridge_hits == 1);
            occupancy(&b);
            ra_battle_step(&b);
            CHECK(!b.units[0].health && (b.units[0].traits & RA_UNIT_FALLEN) && b.bridge_falls == 1 && b.kills == 1);
            CHECK(b.units[0].fall_cell == cell && b.units[0].fall_height == (kind < 2 ? 416 : 0));
            CHECK(!ra_battle_passable(&b, cell + (kind < 2 ? 256u : 0u)));
            occupancy(&b);
            ra_battle_step(&b);
            CHECK(ra_battle_passable(&b, cell + (kind < 2 ? 256u : 0u)) && b.bridge_repaired > 0);
            CHECK(!b.units[0].health && b.bridge_falls == 1 && b.kills == 1);
            ra_battle_reset(&b);
            CHECK(b.units[0].health && !b.bridge_falls && !b.topology_revision);
            CHECK(b.bridge_parts[b.bridge_at[cell] - 1].frame == (kind < 2 ? (axis == 1 ? 0u : 9u) : (axis == 1 ? 1u : 10u)));
            occupancy(&b);
            ra_battle_close(&b);
        }
}

static void layers_and_reservations(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, 0, 1, 0);
    b.tiles[8 * 16 + 7].track = 100;
    b.tiles[8 * 16 + 7].land = 0;
    CHECK(ra_battle_spawn_layer(&b, 0, 1, 7, 8, 1, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 2, 7, 8, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 4, 8, &e));
    CHECK(ra_battle_command_add(&b, 1, 3, 8 * 16 + 11, &e));
    CHECK(ra_battle_bridge_event_add(&b, 2, RA_EVENT_BRIDGE_DEMOLISH, 8 * 16 + 5, &e));
    CHECK(ra_battle_bridge_event_add(&b, 3, RA_EVENT_BRIDGE_DEMOLISH, 8 * 16 + 7, &e));
    CHECK(ra_battle_bridge_event_add(&b, 80, RA_EVENT_BRIDGE_REPAIR, 8 * 16 + 7, &e));
    CHECK(ra_battle_command_add(&b, 81, 3, 8 * 16 + 11, &e));
    for (unsigned i = 0; i < 500; ++i)
    {
        ra_battle_step(&b);
        occupancy(&b);
        if (b.tick == 2) CHECK(b.units[2].health && b.units[2].cell == 8 * 16 + 4 && !b.units[2].reserved_count);
        if (b.tick >= 3) CHECK(!b.units[0].health && b.units[1].health && b.units[2].health);
    }
    CHECK(b.units[2].cell == 8 * 16 + 11 && b.bridge_falls == 1);
    ra_battle_close(&b);
}

static void impact_boundaries(void)
{
    static const int heights[] = {207, 208, 209, 415, 416, 520, 521};
    for (unsigned i = 0; i < sizeof(heights) / sizeof(*heights); ++i)
        for (unsigned side = 0; side < 2; ++side)
        {
            ra_battle b = {0};
            fixture(&b, 0, 1, 0);
            battle_terrain_seal(&b);
            b.tick = 1;
            b.types[0].weapon.wall = true;
            b.types[0].weapon.bridge_forced = true;
            ra_battle_shot shot = {0};
            shot.x = 7 * RA_BATTLE_CELL;
            /* 正半格属于下一格；桥宽三格的外侧不能击中桥面。 */
            shot.y = (int32_t)(9 * RA_BATTLE_CELL + RA_BATTLE_CELL / 2 - (side ? 0 : 1));
            shot.z = heights[i] * 256;
            battle_bridge_impact(&b, &shot);
            CHECK(b.bridge_hits == (!side && heights[i] > 208 && heights[i] <= 520 ? 1u : 0u));
            ra_battle_close(&b);
        }
}

static void replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_error e = {0};
    fixture(&a, 1, 2, 9);
    fixture(&b, 1, 2, 9);
    CHECK(ra_battle_spawn_team(&a, 0, 1, 8, 4, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 8, 4, &e));
    CHECK(ra_battle_command_add(&a, 1, 1, 11 * 16 + 8, &e));
    CHECK(ra_battle_bridge_event_add(&a, 35, RA_EVENT_BRIDGE_HIT, 7 * 16 + 8, &e));
    CHECK(ra_battle_bridge_event_add(&a, 40, RA_EVENT_BRIDGE_DEMOLISH, 7 * 16 + 8, &e));
    CHECK(ra_battle_bridge_event_add(&a, 200, RA_EVENT_BRIDGE_REPAIR, 7 * 16 + 8, &e));
    CHECK(ra_battle_command_add(&a, 210, 1, 11 * 16 + 8, &e));
    CHECK(ra_battle_bridge_event_add(&a, 500, RA_EVENT_BRIDGE_DEMOLISH, 8 * 16 + 8, &e));
    uint8_t states[700][20], expected[20], digest[20], *bytes = NULL;
    size_t size = 0;
    uint32_t end = 0;
    for (unsigned i = 0; i < 700; ++i)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, states[i]);
        occupancy(&a);
    }
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &e));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e) && end == 700);
    uint64_t phase = 0;
    while (b.tick < end)
    {
        uint32_t ticks = ra_battle_clock(&phase, b.tick & 1 ? 170000 : 51000);
        while (ticks-- && b.tick < end)
        {
            ra_battle_step(&b);
            ra_battle_hash(&b, digest);
            CHECK(!memcmp(digest, states[b.tick - 1], 20));
        }
    }
    CHECK(!memcmp(digest, expected, 20));
    /* 从已毁桥的终局读取自己的回放，也必须验证初始地图而非终局地形。 */
    CHECK(ra_battle_replay_read(&a, (ra_view){bytes, size}, &end, expected, &e));
    for (unsigned i = 0; i < end; ++i)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, digest);
        CHECK(!memcmp(digest, states[i], 20));
    }
    ra_battle_hash(&a, digest);
    bytes[6] = '8';
    CHECK(!ra_battle_replay_read(&a, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_hash(&a, expected);
    CHECK(!memcmp(expected, digest, 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}

static void broken_low_and_ballistics(void)
{
    for (uint32_t axis = 1; axis <= 2; ++axis)
    {
        ra_battle b = {0};
        ra_error e = {0};
        fixture(&b, 2, axis, axis == 1 ? 27u : 28u);
        uint32_t cell = axis == 1 ? 8 * 16 + 7 : 7 * 16 + 8;
        CHECK(!ra_battle_passable(&b, cell));
        CHECK(ra_battle_bridge_event_add(&b, 1, RA_EVENT_BRIDGE_REPAIR, cell, &e));
        CHECK(ra_battle_bridge_event_add(&b, 2, RA_EVENT_BRIDGE_DEMOLISH, cell, &e));
        ra_battle_step(&b);
        CHECK(ra_battle_passable(&b, cell) && b.bridge_repaired == 18);
        ra_battle_step(&b);
        CHECK(!ra_battle_passable(&b, cell) && b.bridge_destroyed == 3);
        ra_battle_reset(&b);
        CHECK(!ra_battle_passable(&b, cell) && b.bridge_parts[b.bridge_at[cell] - 1].frame == (axis == 1 ? 27u : 28u));
        ra_battle_close(&b);
    }
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, 0, 1, 0);
    ra_battle_weapon *w = &b.types[0].weapon;
    w->damage = 65;
    w->rof = 45;
    w->range = 6 * RA_BATTLE_CELL;
    w->speed = 40;
    w->gravity = 1536;
    w->spread = 19660;
    w->percent_at_max = 5000;
    w->arcing = w->wall = w->bridge_forced = true;
    CHECK(ra_battle_spawn_team(&b, 0, 1, 4, 8, &e));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_FORCE_GROUND, 256 + 8 * 16 + 7, &e));
    for (unsigned i = 0; i < 400; ++i)
    {
        ra_battle_step(&b);
        occupancy(&b);
    }
    CHECK(b.fired >= 2 && b.impacts >= 2 && b.bridge_hits >= 2 && b.bridge_destroyed >= 1 && !b.dropped_shots);
    CHECK(!ra_battle_passable(&b, 256 + 8 * 16 + 7));
    ra_battle_close(&b);
}

static void topology_missions(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, 0, 1, 0);
    b.tiles[8 * 16 + 7].track = 100;
    b.types[0].weapon.damage = 65;
    b.types[0].weapon.range = 5 * RA_BATTLE_CELL;
    b.types[0].weapon.verses[0] = 10000;
    CHECK(ra_battle_spawn_team(&b, 0, 1, 7, 8, &e));
    CHECK(ra_battle_spawn_layer(&b, 0, 2, 9, 8, 1, &e));
    CHECK(!ra_battle_targetable(&b, &b.units[0], &b.units[1], true, false));
    CHECK(ra_battle_bridge_event_add(&b, 1, RA_EVENT_BRIDGE_DEMOLISH, 8 * 16 + 7, &e));
    CHECK(ra_battle_bridge_event_add(&b, 2, RA_EVENT_BRIDGE_REPAIR, 8 * 16 + 7, &e));
    ra_battle_step(&b);
    CHECK(b.units[0].health && b.units[1].health && !b.bridge_falls);
    CHECK(ra_battle_targetable(&b, &b.units[0], &b.units[1], true, false) && ra_battle_nearest(&b, 1) == 2);
    ra_battle_step(&b);
    CHECK(!ra_battle_targetable(&b, &b.units[0], &b.units[1], true, false));
    ra_battle_close(&b);
    for (unsigned blocked_head = 0; blocked_head < 2; ++blocked_head)
    {
        fixture(&b, 0, 1, 0);
        CHECK(ra_battle_spawn_team(&b, 0, 1, 4, 8, &e));
        uint32_t old = 7 * 16 + 4, points[2] = {blocked_head ? 256 + 8 * 16 + 5 : 9 * 16 + 4, blocked_head ? 9 * 16 + 4 : 256 + 8 * 16 + 5};
        CHECK(ra_battle_waypoints_add(&b, 1, 1, &old, 1, UINT32_MAX, &e));
        CHECK(ra_battle_bridge_event_add(&b, 9, RA_EVENT_BRIDGE_DEMOLISH, 8 * 16 + 5, &e));
        CHECK(ra_battle_waypoints_add(&b, 10, 1, points, 2, 0, &e));
        for (unsigned i = 0; i < 10; ++i) ra_battle_step(&b);
        CHECK(b.rejected == 1 && b.command_cursor == b.command_count);
        CHECK(b.units[0].order == RA_ORDER_WAYPOINT && b.units[0].waypoint_count == 1 && b.units[0].waypoints[0] == old && !b.units[0].waypoint_loop);
        occupancy(&b);
        ra_battle_close(&b);
    }
}

int main(void)
{
    lifecycle();
    layers_and_reservations();
    impact_boundaries();
    replay();
    broken_low_and_ballistics();
    topology_missions();
    printf("{\"suite\":\"bridges\",\"checks\":%u,\"failures\":%u,\"paired_steps\":1400}\n", checks, failures);
    return failures ? 1 : 0;
}
