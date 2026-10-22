#include "internal.h"
#include "battle_internal.h"
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

static void continuous_boundary(void)
{
    ra_battle_type type = {0};
    battle_real factor = BATTLE_ONE;
    type.step = 15 * 256;
    type.slowdown = 500;
    type.deceleration = 20;
    type.acceleration = 300;
    for (unsigned step = 0; step < 20; ++step) factor = battle_motion_factor(&type, 499, factor, BATTLE_ONE);
    /* 原版连续第 20 步的独立金值；万分比四舍五入会把速度误算成 6。 */
    CHECK(factor == UINT64_C(0x3fd9999999999990));
    CHECK(battle_motion_rate(&type, factor) == 5 * 256);
    for (unsigned step = 0; step < 15; ++step) factor = battle_motion_factor(&type, 499, factor, BATTLE_ONE);
    CHECK(factor == UINT64_C(0x3fd3333340000000) && battle_motion_rate(&type, factor) == 4 * 256);
    factor = battle_motion_factor(&type, 500, factor, BATTLE_ONE);
    CHECK(factor == UINT64_C(0x3fd51eb85eb851eb));
    CHECK(battle_real_compare(battle_motion_factor(&type, 501, factor, BATTLE_ONE), factor) > 0);
}

static void ramp_planes(void)
{
    ra_battle_tile tile = {100, 2, 1, 0, 0};
    CHECK(ra_battle_tile_height(&tile, 0, 128) == 208);
    CHECK(ra_battle_tile_height(&tile, 128, 128) == 260);
    CHECK(ra_battle_tile_height(&tile, 255, 128) == 311);
    tile.ramp = 5;
    CHECK(ra_battle_tile_height(&tile, 128, 128) == 208);
    CHECK(ra_battle_tile_height(&tile, 255, 255) == 311);
    tile.ramp = 13;
    CHECK(ra_battle_tile_height(&tile, 128, 128) == 312);
    CHECK(ra_battle_tile_height(&tile, 255, 255) == 415);
    for (tile.ramp = 17; tile.ramp <= 20; ++tile.ramp) CHECK(ra_battle_tile_height(&tile, 128, 128) == 260);
}

static void projectile_goldens(void)
{
    ra_battle_weapon weapon = {0};
    battle_real velocity[3];
    int32_t position[3] = {3000, 4000, 100};
    weapon.gravity = 6 * 256;
    /* 原版完整初始化片段及重力、坐标片段产生的金值，包含重复取整的累积影响。 */
    CHECK(battle_projectile_launch(&weapon, 1024, 0, -104, velocity));
    CHECK(velocity[0] == UINT64_C(0x4053cec9576ed480));
    CHECK(velocity[2] == UINT64_C(0x403ec57684125500));
    battle_projectile_step(position, velocity, battle_real_int(6));
    CHECK(position[0] == 3079 && position[1] == 4000 && position[2] == 124);
    for (unsigned step = 1; step < 20; ++step) battle_projectile_step(position, velocity, battle_real_int(6));
    CHECK(position[0] == 4580 && position[1] == 4000 && position[2] == -551);
    CHECK(velocity[2] == UINT64_C(0xc0564ea25efb6ac0));
    CHECK(battle_projectile_speed(1024, battle_real_int(6)) == 85);
    CHECK(!battle_projectile_launch(&weapon, 0, 0, 0, velocity));
}

static void fixture(ra_battle *battle)
{
    ra_battle_tile tiles[16 * 16];
    ra_error error = {0};
    for (unsigned y = 0; y < 16; ++y)
        for (unsigned x = 0; x < 16; ++x) tiles[y * 16 + x] = (ra_battle_tile){x >= 10 ? 70 : 100, x >= 8 ? 1 : 0, x == 7 ? 1 : 0, 0, 0};
    CHECK(ra_battle_create(battle, 16, 16, tiles, NULL, &error));
    CHECK(ra_battle_type_add(battle, "MTNK", "ra2.allied", 17 * 256, &error));
    battle->types[0].rot = 5;
    battle->types[0].slowdown = 500;
    battle->types[0].deceleration = 20;
    battle->types[0].downhill = 12000;
    CHECK(ra_battle_spawn(battle, 0, 4, 4, &error));
    CHECK(ra_battle_ground_height(battle, 7 * RA_BATTLE_CELL, 4 * RA_BATTLE_CELL) == 52);
}

static void step_replay(void)
{
    const unsigned end_tick = 1200;
    const uint64_t intervals[] = {1000, 100000, 17333, 250000, 33333, 63001};
    ra_battle a = {0}, b = {0};
    ra_error error = {0};
    uint8_t states[1200][20], expected[20], digest[20], before[20], *bytes = NULL;
    uint32_t end = 0, groups = 0;
    size_t size = 0;
    uint64_t phase = 0;
    fixture(&a);
    fixture(&b);
    CHECK(ra_battle_command_add(&a, 1, 1, 4 * 16 + 8, &error));
    CHECK(ra_battle_command_add(&a, 201, 1, 8 * 16 + 8, &error));
    CHECK(ra_battle_command_add(&a, 401, 1, 8 * 16 + 4, &error));
    CHECK(ra_battle_command_add(&a, 601, 1, 4 * 16 + 4, &error));
    CHECK(ra_battle_command_add(&a, 801, 1, 4 * 16 + 12, &error));
    CHECK(ra_battle_stop_add(&a, 1001, 1, &error));
    for (unsigned i = 0; i < end_tick; ++i)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, states[i]);
    }
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error) && end == end_tick);
    while (b.tick < end_tick)
    {
        uint32_t count = ra_battle_clock(&phase, intervals[groups++ % 6]);
        while (count-- && b.tick < end_tick)
        {
            ra_battle_step(&b);
            ra_battle_hash(&b, digest);
            CHECK(!memcmp(digest, states[b.tick - 1], 20));
        }
    }
    CHECK(!memcmp(digest, expected, 20) && groups > 6);
    ra_battle_hash(&b, before);
    b.units[0].motion_factor ^= 1;
    ra_battle_hash(&b, digest);
    CHECK(memcmp(before, digest, 20));
    b.units[0].motion_factor ^= 1;
    b.shots[0].active = 1;
    b.shots[0].velocity[0] = BATTLE_ONE;
    ra_battle_hash(&b, before);
    b.shots[0].velocity[0] ^= 1;
    ra_battle_hash(&b, digest);
    CHECK(memcmp(before, digest, 20));
    b.shots[0] = (ra_battle_shot){0};
    ra_battle_hash(&b, before);
    bytes[8] = bytes[36] = 3;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    ra_battle_hash(&b, digest);
    CHECK(!memcmp(before, digest, 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}

static void acquisition(void)
{
    ra_battle battle = {0};
    ra_error error = {0};
    fixture(&battle);
    ra_battle_close(&battle);
    ra_battle_tile tiles[16 * 16];
    for (unsigned i = 0; i < 16 * 16; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(&battle, 16, 16, tiles, NULL, &error));
    CHECK(ra_battle_type_add(&battle, "MTNK", "ra2.allied", 17 * 256, &error));
    battle.types[0].sight = RA_BATTLE_CELL;
    battle.types[0].weapon.damage = 65;
    battle.types[0].weapon.verses[0] = 10000;
    battle.types[0].weapon.range = 5 * RA_BATTLE_CELL;
    CHECK(ra_battle_spawn_team(&battle, 0, 1, 1, 4, &error));
    CHECK(ra_battle_spawn_team(&battle, 0, 2, 10, 4, &error));
    CHECK(ra_battle_order_add(&battle, 1, 1, RA_ORDER_GUARD, 0, &error));
    ra_battle_step(&battle);
    CHECK(battle.units[0].target == 2);
    CHECK(battle_guard_range(0, 1280, 0, 1, false) == 2560);
    CHECK(battle_guard_range(0, 256, 0, 2, false) == 1792);
    CHECK(battle_guard_range(3000, 1280, 0, 1, false) == 4096);
    CHECK(!ra_battle_factions[2].enabled && !strcmp(ra_battle_factions[2].id, "future.china"));
    ra_battle_close(&battle);
}

static void nominal_projectile_speed(void)
{
    ra_battle battle = {0};
    ra_battle_tile tiles[16 * 16];
    ra_error error = {0};
    for (unsigned i = 0; i < 16 * 16; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(&battle, 16, 16, tiles, NULL, &error));
    CHECK(ra_battle_type_add(&battle, "SHOOTER", "ra2.allied", 17 * 256, &error));
    CHECK(ra_battle_type_add(&battle, "TARGET", "ra2.soviet", 17 * 256, &error));
    ra_battle_weapon *weapon = &battle.types[0].weapon;
    weapon->damage = 65;
    weapon->rof = 60;
    weapon->range = 5 * RA_BATTLE_CELL;
    weapon->speed = 1;
    weapon->gravity = 6 * 256;
    weapon->arcing = true;
    weapon->spread = 19660;
    weapon->percent_at_max = 5000;
    weapon->verses[0] = 10000;
    CHECK(ra_battle_spawn_team(&battle, 0, 1, 1, 4, &error));
    CHECK(ra_battle_spawn_team(&battle, 1, 2, 5, 4, &error));
    CHECK(ra_battle_attack_add(&battle, 1, 1, 2, &error));
    for (unsigned i = 0; i < 32; ++i) ra_battle_step(&battle);
    /* 即使名义速度只有一，原版无制导初速仍由距离计算，不应被当作超时而拒绝。 */
    CHECK(battle.fired == 1 && battle.impacts == 1 && !battle.dropped_shots);
    CHECK(battle.units[1].health == 35);
    ra_battle_close(&battle);
}

int main(void)
{
    continuous_boundary();
    ramp_planes();
    projectile_goldens();
    step_replay();
    acquisition();
    nominal_projectile_speed();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"physics\",\"paired_steps\":1200}\n", checks, failures);
    return failures ? 1 : 0;
}
