#define _CRT_SECURE_NO_WARNINGS
#include "battle_number.h"
#include "battle_internal.h"
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

/* 数值夹具由独立参考程序输入；此工具只执行产品中的整数数值运算。 */
static int numbers(void)
{
    uint64_t a, b, result;
    char operation;
    while (scanf(" %c %" SCNx64 " %" SCNx64, &operation, &a, &b) == 3)
    {
        switch (operation)
        {
        case '+':
            result = battle_real_add(a, b);
            break;
        case '-':
            result = battle_real_sub(a, b);
            break;
        case '*':
            result = battle_real_mul(a, b);
            break;
        case '/':
            result = battle_real_div(a, b);
            break;
        case 's':
            result = battle_real_sqrt(a);
            break;
        case 'r':
            result = battle_real_ratio((uint32_t)a, (uint32_t)b);
            break;
        default:
            return 2;
        }
        printf("%016" PRIx64 "\n", result);
    }
    return ferror(stdin) ? 1 : 0;
}

static int motion(void)
{
    ra_battle_type type = {0};
    uint32_t base, terrain, distance;
    int slope;
    uint64_t current;
    type.uphill = 10000;
    type.downhill = 12000;
    while (scanf("%u %u %u %u %u %u %d %" SCNx64, &base, &type.slowdown, &type.deceleration, &type.acceleration, &distance, &terrain, &slope, &current) == 8)
    {
        type.step = base * 256;
        battle_real target = battle_motion_target(&type, terrain, slope), value = battle_motion_factor(&type, distance, current, target);
        printf("%016" PRIx64 " %016" PRIx64 " %u\n", target, value, battle_motion_rate(&type, value) / 256);
    }
    return ferror(stdin) ? 1 : 0;
}

static int turns(void)
{
    ra_battle_turn turn = {0};
    uint32_t reset, initial, rot, target, tick;
    while (scanf("%u %u %u %u %u", &reset, &initial, &rot, &target, &tick) == 5)
    {
        if (reset) turn = (ra_battle_turn){initial, initial, 100, 0};
        ra_battle_turn_start(&turn, target, rot, tick);
        printf("%u %u %u %u %u\n", turn.initial, turn.target, turn.started, turn.duration, ra_battle_turn_value(&turn, tick));
    }
    return ferror(stdin) ? 1 : 0;
}

static int legacy(void)
{
    uint64_t a, b, result;
    char operation;
    while (scanf(" %c %" SCNx64 " %" SCNx64, &operation, &a, &b) == 3)
    {
        switch (operation)
        {
        case 's':
            result = battle_legacy_sqrt(a);
            break;
        case 'c':
            result = battle_legacy_trig(a, true);
            break;
        case 'i':
            result = battle_legacy_trig(a, false);
            break;
        case 'a':
            result = battle_legacy_acos(a);
            break;
        case 't':
            result = battle_legacy_atan(a, b);
            break;
        default:
            return 2;
        }
        printf("%016" PRIx64 "\n", result);
    }
    return ferror(stdin) ? 1 : 0;
}

static int arcs(void)
{
    uint32_t distance, speed, high, direction;
    int32_t height;
    uint64_t gravity, angle;
    while (scanf("%u %d %u %" SCNx64 " %u", &distance, &height, &speed, &gravity, &high) == 5)
    {
        bool valid = battle_arc_angle(distance, height, speed, gravity, high != 0, &angle);
        bool directed = battle_arc_direction(distance, height, speed, gravity, high != 0, &direction);
        printf("%u %016" PRIx64 " %u %u %u\n", valid, valid ? angle : 0, directed, directed ? direction : 0, battle_projectile_speed(distance, gravity));
    }
    return ferror(stdin) ? 1 : 0;
}

static int heights(void)
{
    uint32_t height, ramp, x, y;
    while (scanf("%u %u %u %u", &height, &ramp, &x, &y) == 4)
    {
        ra_battle_tile tile = {100, (uint8_t)height, (uint8_t)ramp, 0, 0};
        printf("%d\n", ra_battle_tile_height(&tile, x, y));
    }
    return ferror(stdin) ? 1 : 0;
}
static int guards(void)
{
    int32_t guard, primary, secondary, kind, special;
    while (scanf("%d %d %d %d %d", &guard, &primary, &secondary, &kind, &special) == 5)
        printf("%d\n", battle_guard_range(guard, primary, secondary, kind, special != 0));
    return ferror(stdin) ? 1 : 0;
}
static uint64_t canonical(uint64_t value)
{
    return value & UINT64_C(0x7fffffffffffffff) ? value : 0;
}
static int launches(void)
{
    int32_t dx, dy, height;
    uint32_t gravity, high, floater;
    while (scanf("%d %d %d %u %u %u", &dx, &dy, &height, &gravity, &high, &floater) == 6)
    {
        ra_battle_weapon weapon = {0};
        battle_real velocity[3];
        int32_t position[3] = {3000, 4000, 100};
        weapon.gravity = gravity * 256;
        weapon.high = high != 0;
        weapon.floater = floater != 0;
        bool valid = battle_projectile_launch(&weapon, dx, dy, height, velocity);
        printf("%u", valid);
        if (valid)
        {
            for (unsigned i = 0; i < 3; ++i) printf(" %016" PRIx64, canonical(velocity[i]));
            for (unsigned step = 0; step < 20; ++step)
            {
                battle_projectile_step(position, velocity, battle_real_ratio(gravity, floater ? 2 : 1));
                printf(" %d %d %d %016" PRIx64, position[0], position[1], position[2], canonical(velocity[2]));
            }
        }
        puts("");
    }
    return ferror(stdin) ? 1 : 0;
}

static int tracks(void)
{
    uint32_t control, index, direction;
    int32_t x, y;
    while (scanf("%u %u", &control, &index) == 2)
    {
        bool valid = battle_track_sample(control, index, &x, &y, &direction);
        printf("%u", valid);
        if (valid) printf(" %d %d %u", x, y, direction);
        puts("");
    }
    return ferror(stdin) ? 1 : 0;
}
static int slopes(void)
{
    unsigned a, b, c, d;
    while (scanf("%u %u %u %u", &a, &b, &c, &d) == 4)
    {
        ra_battle_tile from = {100, (uint8_t)a, (uint8_t)b, 0, 0}, to = {100, (uint8_t)c, (uint8_t)d, 0, 0};
        printf("%u\n", ra_battle_slope_edge(&from, &to));
    }
    return ferror(stdin) ? 1 : 0;
}
static int partial(void)
{
    int32_t delta;
    uint32_t remainder;
    while (scanf("%d %u", &delta, &remainder) == 2) printf("%d\n", battle_track_partial(delta, remainder));
    return ferror(stdin) ? 1 : 0;
}
static int muzzle(void)
{
    ra_battle_type type = {0};
    uint32_t facing;
    while (scanf("%u %d %d %d", &facing, &type.flh[0], &type.flh[1], &type.flh[2]) == 4)
    {
        int32_t position[3] = {0};
        battle_muzzle(&type, facing, position);
        printf("%d %d %d\n", position[0], position[1], position[2]);
    }
    return ferror(stdin) ? 1 : 0;
}
static int damage(void)
{
    ra_battle_weapon weapon = {0};
    uint32_t distance;
    while (scanf("%u %u %u %x %u %u", &weapon.damage, &weapon.spread, &distance, &weapon.percent_bits, &weapon.verses[0], &weapon.max_damage) == 6)
        printf("%u\n", battle_damage(&weapon, 0, distance));
    return ferror(stdin) ? 1 : 0;
}
static int threat(void)
{
    ra_battle_type types[2] = {0};
    ra_battle battle = {0};
    battle.types = types;
    ra_battle_unit own = {0}, other = {0};
    uint32_t distance, health, strength, verses, enemy_verses, attacking, range;
    own.id = 1;
    other.type = 1;
    other.id = 2;
    battle.types[1].weapon.damage = 65;
    while (scanf("%u %u %u %u %u %u %u %d", &distance, &health, &strength, &verses, &enemy_verses, &attacking, &range, &battle.types[1].special_threat) == 8)
    {
        own.x = own.y = other.y = 0;
        other.x = (int32_t)(distance * 256);
        other.health = health;
        other.target = attacking;
        battle.types[0].weapon.range = range * 256;
        battle.types[0].weapon.verses[0] = verses;
        battle.types[1].weapon.verses[0] = enemy_verses;
        battle.types[1].strength = strength;
        for (unsigned i = 0; i < 5; ++i) battle.types[0].threat_coefficients[i] = i == 4 ? -10000 : 2000000;
        printf("%d\n", battle_threat_score(&battle, &own, &other));
    }
    return ferror(stdin) ? 1 : 0;
}
static int chassis(void)
{
    uint32_t ramp, facing, matrix[12];
    while (scanf("%u %u", &ramp, &facing) == 2)
    {
        if (!ra_battle_chassis(ramp, facing, matrix)) return 1;
        for (unsigned i = 0; i < 12; ++i) printf(i ? " %08x" : "%08x", matrix[i] & 0x7fffffff ? matrix[i] : 0);
        puts("");
    }
    return ferror(stdin) ? 1 : 0;
}
static int chassis_muzzle(void)
{
    ra_battle_type type = {0};
    uint32_t ramp, body, turret;
    while (scanf("%u %u %u %d %d %d %d", &ramp, &body, &turret, &type.turret_offset, &type.flh[0], &type.flh[1], &type.flh[2]) == 7)
    {
        int32_t position[3] = {0};
        battle_chassis_muzzle(&type, ramp, body, turret, position);
        printf("%d %d %d\n", position[0], position[1], position[2]);
    }
    return ferror(stdin) ? 1 : 0;
}
static int bridges(void)
{
    uint32_t a, ar, c, cr, ff, tf, initial;
    int32_t level;
    while (scanf("%u %u %u %u %u %u %d %u", &a, &ar, &c, &cr, &ff, &tf, &level, &initial) == 8)
    {
        ra_battle_tile from = {100, (uint8_t)a, (uint8_t)ar, 0, 0}, to = {100, (uint8_t)c, (uint8_t)cr, 0, 0};
        bool transition = false;
        uint32_t result = battle_bridge_test(&from, &to, ff, tf, &level, &transition, initial != 0);
        printf("%u %d %u\n", result, level, transition);
    }
    return ferror(stdin) ? 1 : 0;
}
static int surfaces(void)
{
    int32_t oldz, z, ground, deck;
    uint32_t bridge;
    while (scanf("%d %d %d %d %u", &oldz, &z, &ground, &deck, &bridge) == 5) printf("%u\n", battle_surface_collision(oldz, z, ground, deck, bridge != 0));
    return ferror(stdin) ? 1 : 0;
}
static int fuses(void)
{
    int32_t x, y, z;
    uint32_t previous;
    while (scanf("%d %d %d %u", &x, &y, &z, &previous) == 4)
    {
        uint32_t result = battle_fuse(x, y, z, &previous);
        printf("%u %u\n", result, previous);
    }
    return ferror(stdin) ? 1 : 0;
}
static int hitpoints(void)
{
    int32_t x, y, z;
    uint32_t vx, vy, vz;
    ra_battle battle = {0};
    ra_battle_type type = {0};
    battle.types = &type;
    ra_battle_unit target = {0};
    ra_battle_tile tiles[2] = {{100, 0, 0, 0, 0}, {0, 0, 0, 1, 0}};
    battle.width = battle.height = battle.count = target.health = 1;
    battle.units = &target;
    battle.tiles = tiles;
    while (scanf("%d %d %d %u %u %u", &x, &y, &z, &vx, &vy, &vz) == 6)
    {
        ra_battle_shot shot = {0};
        shot.target = 1;
        shot.x = x * 256;
        shot.y = y * 256;
        shot.z = z * 256;
        shot.velocity[0] = battle_real_int((int32_t)vx);
        shot.velocity[1] = battle_real_int((int32_t)vy);
        shot.velocity[2] = battle_real_int((int32_t)vz);
        bool result = battle_projectile_snap(&battle, &shot);
        printf("%u %d %d %d\n", result, shot.x / 256, shot.y / 256, shot.z / 256);
    }
    return ferror(stdin) ? 1 : 0;
}
static int candidates(void)
{
    ra_battle b = {0};
    ra_battle_type type = {0};
    b.types = &type;
    ra_battle_unit own = {0}, target = {0};
    uint32_t traits, hidden, detected, friendly, health;
    uint8_t bridge = 0;
    b.width = b.height = b.type_count = 1;
    b.bridges = &bridge;
    own.id = own.team = own.health = 1;
    b.types[0].weapon.damage = 65;
    b.types[0].weapon.verses[0] = 10000;
    while (scanf("%u %u %u %u %u", &traits, &hidden, &detected, &friendly, &health) == 5)
    {
        target.traits = traits;
        target.hidden_from = hidden;
        target.detected_by = detected;
        target.team = friendly ? 1 : 2;
        target.health = health;
        printf("%u\n", ra_battle_targetable(&b, &own, &target, false, true));
    }
    return ferror(stdin) ? 1 : 0;
}
static int bridge_gates(void)
{
    int32_t height, z;
    uint32_t low, wall, demolition, damage, roll;
    while (scanf("%d %d %u %u %u %u %u", &height, &z, &low, &wall, &demolition, &damage, &roll) == 7)
        printf("%u\n", battle_bridge_damage_test(height, z, low != 0, wall != 0, demolition != 0, damage, roll));
    return ferror(stdin) ? 1 : 0;
}
static int bridge_frames(void)
{
    uint32_t frame, first, removal;
    while (scanf("%u %u %u", &frame, &first, &removal) == 3) printf("%u\n", battle_bridge_frame(frame, first != 0, removal != 0));
    return ferror(stdin) ? 1 : 0;
}
static int bridge_damage(void)
{
    uint32_t frame;
    while (scanf("%u", &frame) == 1)
    {
        ra_battle b = {0};
        ra_error e = {0};
        ra_battle_tile tiles[16] = {0};
        if (!ra_battle_create(&b, 4, 4, tiles, NULL, &e) || !ra_battle_bridge_segment_add(&b, 5, frame < 9 ? 1u : 2u, 0, frame, &e) ||
            !ra_battle_bridge_event_add(&b, 1, RA_EVENT_BRIDGE_HIT, 5, &e))
            return 1;
        ra_battle_step(&b);
        printf("%u\n", b.bridge_parts[0].frame);
        ra_battle_close(&b);
    }
    return ferror(stdin) ? 1 : 0;
}
static int random_ranges(void)
{
    ra_battle b = {0};
    uint32_t low, high;
    battle_random_reset(&b);
    while (scanf("%u %u", &low, &high) == 2)
    {
        uint32_t value = battle_random_range(&b, low, high);
        printf("%u %u %u\n", value, b.random_a, b.random_b);
    }
    return ferror(stdin) ? 1 : 0;
}
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "--bridge-gates")) return bridge_gates();
    if (!strcmp(argv[1], "--bridge-frames")) return bridge_frames();
    if (!strcmp(argv[1], "--bridge-damage")) return bridge_damage();
    if (!strcmp(argv[1], "--random-ranges")) return random_ranges();
    if (!strcmp(argv[1], "--candidates")) return candidates();
    if (!strcmp(argv[1], "--surfaces")) return surfaces();
    if (!strcmp(argv[1], "--fuses")) return fuses();
    if (!strcmp(argv[1], "--hitpoints")) return hitpoints();
    if (!strcmp(argv[1], "--chassis")) return chassis();
    if (!strcmp(argv[1], "--chassis-muzzle")) return chassis_muzzle();
    if (!strcmp(argv[1], "--bridges")) return bridges();
    if (!strcmp(argv[1], "--numbers")) return numbers();
    if (!strcmp(argv[1], "--motion")) return motion();
    if (!strcmp(argv[1], "--turns")) return turns();
    if (!strcmp(argv[1], "--legacy")) return legacy();
    if (!strcmp(argv[1], "--arcs")) return arcs();
    if (!strcmp(argv[1], "--heights")) return heights();
    if (!strcmp(argv[1], "--guards")) return guards();
    if (!strcmp(argv[1], "--launches")) return launches();
    if (!strcmp(argv[1], "--tracks")) return tracks();
    if (!strcmp(argv[1], "--slopes")) return slopes();
    if (!strcmp(argv[1], "--partial")) return partial();
    if (!strcmp(argv[1], "--muzzle")) return muzzle();
    if (!strcmp(argv[1], "--damage")) return damage();
    if (!strcmp(argv[1], "--threat")) return threat();
    return 2;
}
