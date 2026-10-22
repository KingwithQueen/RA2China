#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

static uint32_t checks, failures;
#define CHECK(x)                                                                                                                                               \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(x))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "sea/air test %d: %s\n", __LINE__, #x);                                                                                            \
        }                                                                                                                                                      \
    } while (0)
static bool setup(ra_battle *b)
{
    ra_battle_tile tiles[20 * 20];
    ra_error error = {0};
    for (uint32_t i = 0; i < 400; ++i) tiles[i] = (ra_battle_tile){i / 20 < 10 ? 0 : 100, 0, 0, 0, i / 20 < 10 ? 2 : 0};
    if (!ra_battle_create(b, 20, 20, tiles, NULL, &error)) return false;
    const char *names[] = {"SHIP", "CRAFT", "FOOT", "JET", "V3", "TARGET", "AA"};
    for (uint32_t i = 0; i < 7; ++i)
        if (!ra_battle_type_add(b, names[i], "ra2.allied", 16384, &error)) return false;
    b->types[0].naval = true;
    b->types[1].naval = b->types[1].amphibious = true;
    b->types[1].passengers = 2;
    b->types[1].size_limit = 1;
    b->types[2].infantry = true;
    b->types[3].flying = true;
    b->types[3].flight_height = 600;
    for (uint32_t i = 0; i < 7; ++i) b->types[i].rot = 127;
    return true;
}
static void paired(ra_battle *b, const uint8_t *trace, uint32_t ticks)
{
    ra_error error = {0};
    uint8_t *bytes = NULL, expected[20], actual[20];
    size_t size = 0;
    uint32_t end = 0;
    CHECK(ra_battle_replay_write(b, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(b, (ra_view){bytes, size}, &end, expected, &error));
    CHECK(end == ticks);
    for (uint32_t i = 0; i < end; ++i)
    {
        ra_battle_step(b);
        ra_battle_hash(b, actual);
        CHECK(!memcmp(actual, trace + (size_t)i * 20, 20));
    }
    CHECK(!memcmp(actual, expected, 20));
    free(bytes);
}
static void transport(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[180][20];
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 1, 1, 5, 10, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 5, 11, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 6, 11, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 7, 11, &error));
    CHECK(ra_battle_order_add(&b, 1, 2, RA_ORDER_LOAD, 1, &error));
    CHECK(ra_battle_order_add(&b, 1, 3, RA_ORDER_LOAD, 1, &error));
    CHECK(ra_battle_order_add(&b, 1, 4, RA_ORDER_LOAD, 1, &error));
    CHECK(ra_battle_order_add(&b, 3, 1, RA_ORDER_MOVE, 5 * 20 + 5, &error));
    CHECK(ra_battle_order_add(&b, 25, 1, RA_ORDER_UNLOAD, 0, &error));
    CHECK(ra_battle_order_add(&b, 75, 1, RA_ORDER_UNLOAD, 0, &error));
    CHECK(ra_battle_order_add(&b, 100, 1, RA_ORDER_MOVE, 10 * 20 + 5, &error));
    CHECK(ra_battle_order_add(&b, 150, 1, RA_ORDER_DEPLOY, 0, &error));
    for (uint32_t i = 0; i < 180; ++i)
    {
        ra_battle_step(&b);
        if (i == 1) CHECK(battle_transport_count(&b, 1) == 2);
        if (i == 90) CHECK(battle_transport_count(&b, 1) == 2 && b.units[0].unloading);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(!battle_transport_count(&b, 1));
    CHECK(!(b.units[1].traits & RA_UNIT_LIMBO) && !(b.units[2].traits & RA_UNIT_LIMBO));
    CHECK(b.units[3].health && !b.units[3].carrier);
    paired(&b, trace[0], 180);
    ra_battle_reset(&b);
    CHECK(battle_transport_load(&b, &b.units[1], &b.units[0]));
    battle_kill(&b, &b.units[0], 0);
    CHECK(!b.units[1].health && b.units[1].destroyed_tick == b.tick);
    ra_battle_close(&b);
}
static void flight(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[160][20];
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 3, 3, &error));
    CHECK(!ra_battle_spawn_team(&b, 0, 1, 3, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 3, 1, 3, 3, &error));
    CHECK(b.occupied[3 * 20 + 3] == 1);
    CHECK(ra_battle_unit_height(&b, &b.units[1]) == 600);
    CHECK(ra_battle_order_add(&b, 1, 2, RA_ORDER_MOVE, 12 * 20 + 12, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_MOVE, 6 * 20 + 6, &error));
    CHECK(!ra_battle_order_add(&b, 1, 1, RA_ORDER_MOVE, 12 * 20 + 6, &error));
    for (uint32_t i = 0; i < 160; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(b.units[0].cell == 6 * 20 + 6);
    CHECK(b.units[1].cell == 12 * 20 + 12);
    paired(&b, trace[0], 160);
    CHECK(b.occupied[12 * 20 + 12] == 0);
    ra_battle_close(&b);
}
static void missile(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[100][20];
    CHECK(setup(&b));
    ra_battle_weapon *w = &b.types[4].weapon;
    w->damage = 120;
    w->rof = w->regeneration = 60;
    w->speed = 30;
    w->range = 15 * RA_BATTLE_CELL;
    w->minimum = 3 * RA_BATTLE_CELL;
    w->burst = 2;
    w->missile = 1;
    w->missile_health = 50;
    w->launch_delay = 5;
    w->altitude = 768;
    w->max_damage = 10000;
    w->percent_at_max = 10000;
    for (uint32_t i = 0; i < 11; ++i) w->verses[i] = 10000;
    b.types[5].strength = 200;
    CHECK(ra_battle_spawn_team(&b, 4, 1, 2, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 5, 2, 12, 12, &error));
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &error));
    for (uint32_t i = 0; i < 100; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(!b.units[1].health && b.units[0].shots == 2 && b.impacts == 2);
    paired(&b, trace[0], 100);
    ra_battle_close(&b);
}
static void interception(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b));
    ra_battle_weapon *w = &b.types[4].weapon;
    w->damage = 120;
    w->rof = w->regeneration = 60;
    w->speed = 30;
    w->range = 15 * RA_BATTLE_CELL;
    w->minimum = 3 * RA_BATTLE_CELL;
    w->missile = 1;
    w->missile_health = 50;
    w->launch_delay = 5;
    w->altitude = 768;
    w->max_damage = 10000;
    w->percent_at_max = 10000;
    for (uint32_t i = 0; i < 11; ++i) w->verses[i] = 10000;
    b.types[6].weapon = *w;
    b.types[6].weapon.missile = 0;
    b.types[6].weapon.aa = true;
    CHECK(ra_battle_spawn_team(&b, 4, 1, 2, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 5, 2, 4, 12, &error));
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &error));
    for (uint32_t i = 0; i < 60; ++i) ra_battle_step(&b);
    CHECK(b.fired == 0 && b.units[1].health == 100);
    ra_battle_close(&b);
    CHECK(setup(&b));
    w = &b.types[4].weapon;
    *w = (ra_battle_weapon){0};
    w->damage = 120;
    w->rof = 500;
    w->speed = 30;
    w->range = 15 * RA_BATTLE_CELL;
    w->missile = 1;
    w->missile_health = 50;
    w->launch_delay = 5;
    w->altitude = 768;
    w->max_damage = 10000;
    for (uint32_t i = 0; i < 11; ++i) w->verses[i] = 10000;
    b.types[6].weapon = *w;
    b.types[6].weapon.missile = 0;
    b.types[6].weapon.aa = true;
    CHECK(ra_battle_spawn_team(&b, 4, 1, 2, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 5, 2, 12, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 6, 2, 12, 13, &error));
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &error));
    for (uint32_t i = 0; i < 160; ++i) ra_battle_step(&b);
    CHECK(b.units[1].health == 100 && b.units[2].shots > 0 && b.impacts == 0);
    ra_battle_close(&b);
}
static void gates(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[180][20];
    CHECK(setup(&b));
    b.types[5].structure = b.types[5].gate = true;
    b.types[5].foundation_width = b.types[5].foundation_height = 1;
    for (uint32_t y = 10; y < 20; ++y)
        if (y != 15) b.tiles[y * 20 + 10].blocked = 1;
    CHECK(ra_battle_spawn_structure(&b, 5, 1, 10, 15, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 7, 15, &error));
    CHECK(ra_battle_order_add(&b, 1, 2, RA_ORDER_MOVE, 15 * 20 + 14, &error));
    bool opened = false;
    for (uint32_t i = 0; i < 180; ++i)
    {
        ra_battle_step(&b);
        if (b.units[0].gate_open_until) opened = true;
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(opened && b.units[1].cell == 15 * 20 + 14);
    paired(&b, trace[0], 180);
    ra_battle_close(&b);
}
static void sea_air_production(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    ra_ini rules = {0};
    const char *text = "[TARGET]\nFactory=UnitType\nNaval=yes\n[AA]\nFactory=AircraftType\n[SHIP]\nCost=100\nTechLevel=1\nOwner=Americans\n"
                       "[JET]\nCost=200\nTechLevel=1\nOwner=Americans\nAirportBound=yes\n";
    uint8_t trace[400][20];
    CHECK(setup(&b));
    b.types[5].structure = b.types[6].structure = true;
    b.types[5].foundation_width = b.types[5].foundation_height = b.types[6].foundation_width = b.types[6].foundation_height = 1;
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)text, strlen(text)}, "factories", &error));
    CHECK(ra_economy_open(&b, &rules, &error));
    CHECK(ra_economy_house(&b, 1, "Americans", 1000, 10, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 1, 8, 10, &error));
    CHECK(ra_battle_spawn_structure(&b, 6, 1, 13, 12, &error));
    CHECK(ra_economy_available(&b, 1, 0) && ra_economy_available(&b, 1, 3));
    CHECK(ra_economy_category(&b, 0) == 4 && ra_economy_category(&b, 3) == 3);
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 0, &error));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 3, &error));
    for (uint32_t i = 0; i < 400; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(b.count == 4 && b.economy->state.houses[0].produced == 2 && b.economy->state.houses[0].credits == 700);
    paired(&b, trace[0], 400);
    ra_ini_close(&rules);
    ra_battle_close(&b);
}
static void standoff(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    ra_battle_tile *tiles = calloc(10000, sizeof(*tiles));
    CHECK(tiles != NULL);
    if (!tiles) return;
    for (uint32_t i = 0; i < 10000; ++i) tiles[i].track = 100;
    CHECK(ra_battle_create(&b, 100, 100, tiles, NULL, &error));
    free(tiles);
    CHECK(ra_battle_type_add(&b, "RIFLE", "ra2.allied", 3840, &error));
    CHECK(ra_battle_type_add(&b, "TOWER", "ra2.soviet", 1, &error));
    b.types[0].infantry = b.types[0].instant_weapon = true;
    b.types[0].strength = 250;
    b.types[0].rot = 127;
    b.types[0].weapon.damage = 125;
    b.types[0].weapon.rof = 10;
    b.types[0].weapon.range = 6 * RA_BATTLE_CELL;
    b.types[0].weapon.speed = 100;
    for (uint32_t i = 0; i < 11; ++i) b.types[0].weapon.verses[i] = 10000;
    b.types[1] = b.types[0];
    b.types[1].infantry = false;
    b.types[1].structure = true;
    b.types[1].foundation_width = b.types[1].foundation_height = 1;
    b.types[1].strength = 400;
    b.types[1].weapon.damage = 100;
    b.types[1].weapon.range = 11 * RA_BATTLE_CELL / 2;
    CHECK(ra_battle_spawn_team(&b, 0, 1, 82, 35, &error));
    CHECK(ra_battle_spawn_structure(&b, 1, 2, 93, 63, &error));
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &error));
    for (uint32_t i = 0; i < 1600 && b.units[1].health; ++i) ra_battle_step(&b);
    CHECK(!b.units[1].health && b.units[0].health == 250 && b.units[1].shots == 0);
    ra_battle_close(&b);
}
int main(void)
{
    transport();
    flight();
    missile();
    interception();
    gates();
    sea_air_production();
    standoff();
    printf("%u checks, %u failures\n", checks, failures);
    return failures ? 1 : 0;
}
