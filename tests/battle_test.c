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
static void fixture(ra_battle *b, ra_battle_tile *tiles)
{
    ra_error e = {0};
    size_t i;
    for (i = 0; i < 256; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 16, 16, tiles, NULL, &e));
    CHECK(ra_battle_type_add(b, "MTNK", "ra2.allied", 28672, &e));
    CHECK(ra_battle_spawn(b, 0, 1, 1, &e));
}
static void seal(uint8_t *bytes, size_t size)
{
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
}
static void movement(void)
{
    ra_battle b = {0};
    ra_battle_tile tiles[256];
    ra_error e = {0};
    uint32_t i;
    fixture(&b, tiles);
    CHECK(ra_battle_land(9) == 2 && ra_battle_land(10) == 6 && ra_battle_land(15) == 3);
    CHECK(ra_battle_land(0) == 0 && ra_battle_land(11) == 1 && ra_battle_land(12) == 1);
    CHECK(ra_battle_land(16) == 255 && ra_battle_land(255) == 255);
    CHECK(!ra_battle_type_add(&b, "CHINA", "future.china", 1, &e));
    CHECK(!ra_battle_spawn(&b, 0, 1, 1, &e));
    CHECK(!ra_battle_command_add(&b, 0, 1, 34, &e));
    CHECK(!ra_battle_command_add(&b, 1, 0, 34, &e));
    CHECK(!ra_battle_edge(&b, 15, 16, 1));
    b.tiles[18].blocked = 1;
    b.tiles[33].blocked = 1;
    CHECK(!ra_battle_edge(&b, 17, 34, 1));
    b.tiles[18].blocked = b.tiles[33].blocked = 0;
    b.tiles[18].height = 1;
    CHECK(!ra_battle_edge(&b, 17, 18, 1));
    b.tiles[17].ramp = 1;
    CHECK(ra_battle_edge(&b, 17, 18, 1));
    b.tiles[18].height = 2;
    CHECK(!ra_battle_edge(&b, 17, 18, 1));
    b.tiles[18].height = 0;
    for (i = 0; i < 15; ++i) b.tiles[i * 16 + 5].blocked = 1;
    CHECK(ra_battle_command_add(&b, 1, 1, 30, &e));
    for (i = 0; i < 200; ++i)
    {
        ra_battle_step(&b);
        CHECK(ra_battle_passable(&b, b.units[0].cell));
        CHECK(b.occupied[b.units[0].cell] == 1);
    }
    CHECK(b.units[0].cell == 30 && b.units[0].x == 14 * (int32_t)RA_BATTLE_CELL);
    ra_battle_reset(&b);
    b.command_count = 0;
    for (i = 0; i < 16; ++i) b.tiles[i * 16 + 5].blocked = 1;
    CHECK(ra_battle_command_add(&b, 1, 1, 30, &e));
    for (i = 0; i < 50; ++i) ra_battle_step(&b);
    CHECK(b.units[0].cell == 17 && b.rejected > 0);
    ra_battle_close(&b);
}
static void replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_battle_tile tiles[256];
    ra_error e = {0};
    uint8_t *bytes = NULL, expected[20], hash[20], other[20];
    size_t size = 0, i;
    uint32_t end = 0;
    fixture(&a, tiles);
    fixture(&b, tiles);
    CHECK(ra_battle_command_add(&a, 1, 1, 238, &e));
    CHECK(ra_battle_command_add(&a, 8, 1, 33, &e));
    for (i = 0; i < 160; ++i) ra_battle_step(&a);
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &e));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    CHECK(end == 160);
    ra_battle_reset(&a);
    for (i = 0; i < 160; ++i)
    {
        ra_battle_step(&a);
        ra_battle_step(&b);
        ra_battle_hash(&a, hash);
        ra_battle_hash(&b, other);
        CHECK(!memcmp(hash, other, 20));
    }
    CHECK(!memcmp(hash, expected, 20));
    for (i = 0; i < size; ++i) CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, i}, &end, expected, &e));
    bytes[0] ^= 1;
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    bytes[0] ^= 1;
    bytes[size - 1] ^= 1;
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    bytes[size - 1] ^= 1;
    bytes[12] = 30;
    seal(bytes, size);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    bytes[12] = 15;
    bytes[120] = 0;
    seal(bytes, size);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    bytes[120] = 1;
    seal(bytes, size);
    CHECK(b.tick == 160);
    b.tiles[0].track = 90;
    /* 当前地形属于可重置的模拟状态；初始地图指纹才是回放兼容性边界。 */
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    CHECK(b.tiles[0].track == b.initial_tiles[0].track && b.tiles[0].track != 90);
    b.initial_tiles[0].track = 90;
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}
static void timing_and_occupancy(void)
{
    ra_battle a = {0}, b = {0};
    ra_battle_tile tiles[256];
    ra_error e = {0};
    uint64_t p = 0, total = 0;
    uint8_t x[20], y[20];
    uint32_t ticks = 0, i;
    fixture(&a, tiles);
    fixture(&b, tiles);
    CHECK(ra_battle_spawn(&a, 0, 3, 1, &e));
    CHECK(ra_battle_spawn(&b, 0, 3, 1, &e));
    CHECK(ra_battle_command_add(&a, 1, 1, 30, &e));
    CHECK(ra_battle_command_add(&a, 1, 2, 17, &e));
    CHECK(ra_battle_command_add(&b, 1, 1, 30, &e));
    CHECK(ra_battle_command_add(&b, 1, 2, 17, &e));
    for (i = 0; i < 300; ++i) ra_battle_step(&a);
    while (total < 20000000)
    {
        uint64_t us = (total % 5 + 1) * 7331;
        uint32_t count;
        if (us > 20000000 - total) us = 20000000 - total;
        total += us;
        count = ra_battle_clock(&p, us);
        ticks += count;
        while (count--) ra_battle_step(&b);
        CHECK(b.units[0].cell != b.units[1].cell && b.units[0].next != b.units[1].next);
    }
    CHECK(ticks == 300 && p == 0);
    ra_battle_hash(&a, x);
    ra_battle_hash(&b, y);
    CHECK(!memcmp(x, y, 20));
    ra_battle_close(&a);
    ra_battle_close(&b);
}
static void terrain_speed(void)
{
    ra_battle fast = {0}, slow = {0}, empty = {0};
    ra_battle_tile tiles[256];
    ra_error e = {0};
    uint32_t fast_ticks = 0, slow_ticks = 0;
    uint64_t phase = 0;
    fixture(&fast, tiles);
    fixture(&slow, tiles);
    for (unsigned i = 0; i < 256; ++i) slow.tiles[i].track = 50;
    /* 地面目标速度通过减速器逐步生效；零减速量不会改变连续系数。 */
    slow.types[0].deceleration = 20;
    CHECK(ra_battle_command_add(&fast, 1, 1, 20, &e));
    CHECK(ra_battle_command_add(&slow, 1, 1, 20, &e));
    while (fast.units[0].cell != 20 && fast_ticks < 200)
    {
        ra_battle_step(&fast);
        ++fast_ticks;
    }
    while (slow.units[0].cell != 20 && slow_ticks < 200)
    {
        ra_battle_step(&slow);
        ++slow_ticks;
    }
    CHECK(slow_ticks > fast_ticks && slow_ticks < 200);
    slow.tiles[21].track = 0;
    CHECK(!ra_battle_command_add(&slow, slow.tick + 1, 1, 21, &e));
    CHECK(ra_battle_clock(&phase, 1000000) == 15 && phase == 0);
    CHECK(ra_battle_clock(&phase, 0) == 0 && phase == 0);
    CHECK(ra_battle_clock(&phase, UINT64_MAX) == 0 && phase == 0);
    CHECK(ra_battle_create(&empty, 16, 16, tiles, NULL, &e));
    CHECK(!ra_battle_type_add(&empty, "CN", "future.china", 1, &e));
    CHECK(ra_battle_type_add(&empty, "A", "ra2.allied", 1, &e));
    CHECK(!ra_battle_type_add(&empty, "A", "ra2.allied", 1, &e));
    ra_battle_close(&fast);
    ra_battle_close(&slow);
    ra_battle_close(&empty);
}
static int app_main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    movement();
    replay();
    timing_and_occupancy();
    terrain_speed();
    printf("{\"checks\":%u,\"failures\":%u}\n", checks, failures);
    return failures ? 1 : 0;
}
#include "entry.h"
