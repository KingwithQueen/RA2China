#include "internal.h"
#include "ra2/battle.h"
#include <stdlib.h>
#include <string.h>

static unsigned checks, failures;
#define CHECK(c)                                                                                                                                               \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(c))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "line %d: %s\n", __LINE__, #c);                                                                                                    \
        }                                                                                                                                                      \
    } while (0)

static void fixture(ra_battle *b)
{
    ra_battle_tile tiles[24 * 16];
    ra_error e = {0};
    for (unsigned i = 0; i < 24 * 16; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 24, 16, tiles, NULL, &e));
    CHECK(ra_battle_type_add(b, "TEST", "ra2.allied", RA_BATTLE_CELL, &e));
    CHECK(ra_battle_type_add(b, "TARGET", "ra2.soviet", RA_BATTLE_CELL, &e));
    b->types[0].strength = b->types[1].strength = 300;
    b->types[0].sight = 8 * RA_BATTLE_CELL;
    /* 本任务夹具明确要求八格索敌；普通查询会把 GuardRange 扩为两倍。 */
    b->types[0].guard_range = 4 * RA_BATTLE_CELL;
    b->types[0].weapon = (ra_battle_weapon){0};
    b->types[0].weapon.damage = 100;
    b->types[0].weapon.rof = 8;
    b->types[0].weapon.range = 2 * RA_BATTLE_CELL;
    b->types[0].weapon.speed = 256;
    b->types[0].weapon.percent_at_max = 10000;
    b->types[0].weapon.max_damage = 10000;
    b->types[0].weapon.verses[0] = 10000;
}
static void run(ra_battle *b, unsigned ticks)
{
    while (ticks--) ra_battle_step(b);
}
static void force_fire(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 1, 4, &e));
    CHECK(ra_battle_spawn_team(&b, 1, 1, 8, 4, &e));
    CHECK(!ra_battle_attack_add(&b, 1, 1, 2, &e));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_FORCE_UNIT, 2, &e));
    run(&b, 100);
    CHECK(b.kills == 1 && !b.units[1].health && b.units[0].cell != 97);
    CHECK(!ra_battle_order_add(&b, 101, 1, RA_ORDER_FORCE_UNIT, 2, &e));
    CHECK(ra_battle_order_add(&b, 101, 1, RA_ORDER_FORCE_GROUND, 4 * 24 + 10, &e));
    run(&b, 60);
    CHECK(b.units[0].order == RA_ORDER_FORCE_GROUND && b.units[0].target == 0 && b.impacts > 3);
    bool ground = false;
    for (unsigned i = 0; i < RA_BATTLE_SHOTS; ++i)
        if (b.shots[i].active && !b.shots[i].target && b.shots[i].end_x == 10 * (int32_t)RA_BATTLE_CELL && b.shots[i].end_z == 0) ground = true;
    CHECK(ground);
    CHECK(ra_battle_stop_add(&b, b.tick + 1, 1, &e));
    run(&b, 30);
    uint32_t fired = b.fired;
    run(&b, 50);
    CHECK(b.fired == fired && b.units[0].order == RA_ORDER_STOP);
    b.tiles[6 * 24 + 10].blocked = 1;
    CHECK(ra_battle_order_add(&b, b.tick + 1, 1, RA_ORDER_FORCE_GROUND, 6 * 24 + 10, &e));
    CHECK(!ra_battle_order_add(&b, b.tick + 1, 1, RA_ORDER_FORCE_GROUND, 24 * 16, &e));
    run(&b, 50);
    CHECK(b.fired > fired);
    ra_battle_close(&b);
}
static void attack_move_and_guard(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 1, 4, &e));
    CHECK(ra_battle_spawn_team(&b, 1, 2, 8, 4, &e));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ATTACK_MOVE, 4 * 24 + 20, &e));
    run(&b, 120);
    CHECK(b.kills == 1 && b.units[0].cell == 4 * 24 + 20 && b.units[0].destination == 4 * 24 + 20);
    ra_battle_reset(&b);
    b.command_count = 0;
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_GUARD, 0, &e));
    bool pursued = false;
    for (unsigned i = 0; i < 120; ++i)
    {
        ra_battle_step(&b);
        if (b.units[0].cell != 97) pursued = true;
    }
    CHECK(pursued && b.kills == 1 && b.units[0].cell == 97 && b.units[0].anchor == 97 && b.units[0].order == RA_ORDER_GUARD);
    ra_battle_reset(&b);
    b.command_count = 0;
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_GUARD, 0, &e));
    CHECK(ra_battle_command_add(&b, 2, 2, 14 * 24 + 22, &e));
    run(&b, 150);
    CHECK(b.units[1].health && b.units[0].cell == 97 && !b.units[0].target);
    ra_battle_close(&b);
}
static void waypoints_and_patrol(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    uint32_t cells[] = {4 * 24 + 5, 8 * 24 + 5, 8 * 24 + 1};
    fixture(&b);
    CHECK(ra_battle_spawn(&b, 0, 1, 4, &e));
    CHECK(ra_battle_waypoints_add(&b, 1, 1, cells, 3, UINT32_MAX, &e));
    unsigned visited = 0;
    for (unsigned i = 0; i < 100; ++i)
    {
        ra_battle_step(&b);
        if (visited < 3 && b.units[0].cell == cells[visited]) ++visited;
    }
    CHECK(visited == 3 && b.units[0].cell == cells[2] && !b.units[0].waypoint_count);
    ra_battle_reset(&b);
    b.command_count = 0;
    CHECK(ra_battle_waypoints_add(&b, 1, 1, cells, 3, 1, &e));
    unsigned loops = 0;
    uint32_t previous = UINT32_MAX;
    for (unsigned i = 0; i < 100; ++i)
    {
        ra_battle_step(&b);
        if (previous == 2 && b.units[0].waypoint_cursor == 1) ++loops;
        previous = b.units[0].waypoint_cursor;
    }
    CHECK(loops > 3 && b.units[0].waypoint_loop == 2 && b.units[0].waypoint_count == 3);
    CHECK(ra_battle_stop_add(&b, b.tick + 1, 1, &e));
    run(&b, 10);
    CHECK(!b.units[0].waypoint_count && !b.units[0].waypoint_loop && !b.units[0].target);
    CHECK(ra_battle_waypoints_add(&b, b.tick + 1, 1, cells, 3, 0, &e));
    CHECK(ra_battle_command_add(&b, b.tick + 2, 1, 3 * 24 + 2, &e));
    run(&b, 50);
    CHECK(b.units[0].cell == 3 * 24 + 2 && !b.units[0].waypoint_count);
    ra_battle_close(&b);

    fixture(&b);
    CHECK(ra_battle_spawn(&b, 0, 1, 4, &e));
    CHECK(ra_battle_spawn(&b, 1, 5, 8, &e));
    CHECK(ra_battle_waypoints_add(&b, 1, 1, cells, 3, UINT32_MAX, &e));
    run(&b, 80);
    CHECK(b.units[0].waypoint_cursor == 1 && b.units[0].waypoint_count == 3 && b.units[0].cell == cells[0]);
    CHECK(ra_battle_command_add(&b, b.tick + 1, 2, 10 * 24 + 9, &e));
    run(&b, 80);
    CHECK(!b.units[0].waypoint_count && b.units[0].cell == cells[2]);
    ra_battle_close(&b);
}
static void scatter_and_capacity(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    for (uint32_t i = 0; i < 3; ++i) CHECK(ra_battle_spawn(&b, 0, 5 + i, 5, &e));
    for (uint32_t i = 0; i < 3; ++i) CHECK(ra_battle_order_add(&b, 1, i + 1, RA_ORDER_SCATTER, 0, &e));
    run(&b, 20);
    for (uint32_t i = 0; i < 3; ++i)
    {
        CHECK(b.units[i].cell == b.units[i].destination && b.units[i].cell != b.initial[i].cell);
        for (uint32_t j = i + 1; j < 3; ++j) CHECK(b.units[i].cell != b.units[j].cell);
    }
    uint32_t before = b.command_count, cells[RA_BATTLE_WAYPOINTS + 1];
    for (unsigned i = 0; i < RA_BATTLE_WAYPOINTS + 1; ++i) cells[i] = 30;
    CHECK(!ra_battle_waypoints_add(&b, 21, 1, cells, 33, UINT32_MAX, &e));
    CHECK(!ra_battle_waypoints_add(&b, 21, 1, cells, 0, UINT32_MAX, &e));
    CHECK(!ra_battle_waypoints_add(&b, 21, 1, cells, 1, 1, &e));
    cells[2] = 24 * 16;
    CHECK(!ra_battle_waypoints_add(&b, 21, 1, cells, 3, UINT32_MAX, &e));
    CHECK(b.command_count == before);
    b.command_count = RA_BATTLE_COMMANDS - 1;
    CHECK(!ra_battle_waypoints_add(&b, 21, 1, cells, 2, UINT32_MAX, &e));
    CHECK(b.command_count == RA_BATTLE_COMMANDS - 1);
    b.command_count = before;
    ra_battle_close(&b);
}
static void replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_error e = {0};
    uint32_t cells[] = {100, 196, 200}, end = 0;
    uint8_t *bytes = NULL, expected[20], hash[20], other[20];
    size_t size = 0;
    fixture(&a);
    fixture(&b);
    for (unsigned i = 0; i < 2; ++i)
    {
        ra_battle *p = i ? &b : &a;
        CHECK(ra_battle_spawn_team(p, 0, 1, 1, 4, &e));
        CHECK(ra_battle_spawn_team(p, 1, 1, 8, 4, &e));
        CHECK(ra_battle_spawn_team(p, 1, 2, 15, 8, &e));
    }
    CHECK(ra_battle_order_add(&a, 1, 1, RA_ORDER_FORCE_GROUND, 102, &e));
    CHECK(ra_battle_order_add(&a, 30, 1, RA_ORDER_FORCE_UNIT, 2, &e));
    CHECK(ra_battle_order_add(&a, 60, 1, RA_ORDER_GUARD, 0, &e));
    CHECK(ra_battle_order_add(&a, 100, 1, RA_ORDER_SCATTER, 0, &e));
    CHECK(ra_battle_order_add(&a, 120, 1, RA_ORDER_ATTACK_MOVE, 9 * 24 + 20, &e));
    CHECK(ra_battle_waypoints_add(&a, 200, 1, cells, 3, 1, &e));
    run(&a, 300);
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &e));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_reset(&a);
    for (unsigned i = 0; i < end; ++i)
    {
        ra_battle_step(&a);
        ra_battle_step(&b);
        ra_battle_hash(&a, hash);
        ra_battle_hash(&b, other);
        CHECK(!memcmp(hash, other, 20));
    }
    CHECK(!memcmp(hash, expected, 20) && b.units[0].waypoint_loop == 2);
    ++b.units[0].destination;
    ra_battle_hash(&b, other);
    CHECK(memcmp(hash, other, 20));
    --b.units[0].destination;
    ++b.units[0].waypoints[0];
    ra_battle_hash(&b, other);
    CHECK(memcmp(hash, other, 20));
    --b.units[0].waypoints[0];
    uint8_t saved = bytes[8];
    bytes[8] = 2;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    bytes[8] = saved;
    /* 改成孤立追加后重新签名，必须拒绝且保持当前战场完整。 */
    size_t command = 104 + 3 * 20;
    bytes[command + 16] = RA_ORDER_WAYPOINT_APPEND;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_hash(&b, other);
    CHECK(!memcmp(hash, other, 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}
static void zero_damage_lifecycle(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    b.types[0].weapon.max_damage = 0;
    CHECK(ra_battle_spawn_team(&b, 0, 1, 1, 4, &e));
    CHECK(ra_battle_spawn_team(&b, 1, 1, 8, 4, &e));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_FORCE_UNIT, 2, &e));
    run(&b, 100);
    CHECK(b.fired > 0 && !b.kills && b.units[1].health == 300);
    CHECK(ra_battle_order_add(&b, 101, 1, RA_ORDER_FORCE_GROUND, 4 * 24 + 10, &e));
    run(&b, 60);
    CHECK(b.units[1].health == 300 && b.units[0].health == 300);
    CHECK(ra_battle_stop_add(&b, 161, 1, &e));
    run(&b, 60);
    CHECK(!b.kills && !b.units[0].track_active && b.units[0].cell == b.units[0].next);
    ra_battle_close(&b);
}
int main(void)
{
    force_fire();
    attack_move_and_guard();
    waypoints_and_patrol();
    scatter_and_capacity();
    replay();
    zero_damage_lifecycle();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"missions\"}\n", checks, failures);
    return failures ? 1 : 0;
}
