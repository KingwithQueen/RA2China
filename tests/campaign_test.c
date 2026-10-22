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
            fprintf(stderr, "campaign test %d: %s\n", __LINE__, #x);                                                                                           \
        }                                                                                                                                                      \
    } while (0)
static bool setup(ra_battle *b)
{
    ra_battle_tile tiles[24 * 24];
    ra_error error = {0};
    for (uint32_t i = 0; i < 24 * 24; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    if (!ra_battle_create(b, 24, 24, tiles, NULL, &error)) return false;
    const char *names[] = {"MCV", "YARD", "FOOT", "ENG", "TANY", "ENEMY"};
    for (uint32_t i = 0; i < 6; ++i)
        if (!ra_battle_type_add(b, names[i], "ra2.allied", 8192, &error)) return false;
    b->types[0].deploy_type = 2;
    for (uint32_t i = 0; i < 6; ++i)
    {
        b->types[i].strength = 100;
        if (i == 1 || i == 5)
        {
            b->types[i].structure = true;
            b->types[i].foundation_width = b->types[i].foundation_height = 3;
            b->types[i].capturable = true;
        }
        if (i >= 2 && i <= 4) b->types[i].infantry = true;
    }
    b->types[1].strength = 1000;
    b->types[3].engineer = true;
    b->types[4].c4 = true;
    b->types[4].c4_ticks = 4;
    return true;
}
static void replay(ra_battle *b, const uint8_t *trace, uint32_t ticks)
{
    ra_error error = {0};
    uint8_t *bytes = NULL, digest[20], expected[20];
    size_t size = 0;
    uint32_t end = 0;
    CHECK(ra_battle_replay_write(b, &bytes, &size, &error));
    CHECK(bytes && !memcmp(bytes, "RA2RPL13", 8));
    CHECK(ra_battle_replay_read(b, (ra_view){bytes, size}, &end, expected, &error));
    CHECK(end == ticks);
    for (uint32_t i = 0; i < end; ++i)
    {
        ra_battle_step(b);
        ra_battle_hash(b, digest);
        CHECK(!memcmp(digest, trace + i * 20, 20));
    }
    CHECK(!memcmp(digest, expected, 20));
    free(bytes);
}
static void people(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[160][20];
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 5, 5, &error));
    CHECK(ra_battle_spawn_team(&b, 3, 1, 10, 10, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 2, 13, 10, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_DEPLOY, 0, &error));
    CHECK(ra_battle_order_add(&b, 2, 2, RA_ORDER_ENTER, 3, &error));
    for (uint32_t i = 0; i < 160; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(b.units[0].type == 1 && b.units[0].id == 1 && b.units[0].health == 1000);
    CHECK(b.count == 3 && b.units[2].team == 1 && !b.units[1].health && !b.kills);
    CHECK(b.occupied[4 * b.width + 4] == 1 && b.occupied[6 * b.width + 6] == 1);
    replay(&b, &trace[0][0], 160);
    ra_battle_reset(&b);
    CHECK(b.units[0].type == 0 && b.units[1].health && b.units[2].team == 2);
    ra_battle_close(&b);
    CHECK(setup(&b));
    for (uint32_t i = 0; i < 5; ++i) CHECK(ra_battle_spawn_team(&b, 2, 1, 5, 5, &error));
    CHECK(!ra_battle_spawn_team(&b, 2, 1, 5, 5, &error));
    CHECK(!ra_battle_spawn_team(&b, 0, 1, 5, 5, &error));
    CHECK(!ra_battle_spawn_structure(&b, 1, 1, 5, 5, &error));
    CHECK(ra_battle_command_add(&b, 1, 1, 5 * b.width + 9, &error));
    for (uint32_t i = 0; i < 100; ++i) ra_battle_step(&b);
    CHECK(b.units[0].cell == 5 * b.width + 9 && b.units[0].cell == b.units[0].next);
    CHECK(b.units[1].cell == 5 * b.width + 5 && !b.occupied[5 * b.width + 5]);
    ra_battle_close(&b);
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 4, 1, 8, 8, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 2, 10, 8, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ENTER, 2, &error));
    for (uint32_t i = 0; i < 100; ++i) ra_battle_step(&b);
    CHECK(!b.units[1].health && b.units[0].health && b.kills == 1 && !b.occupied[8 * b.width + 10]);
    ra_battle_close(&b);
}

static void edges(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 5, 5, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 4, 4, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_DEPLOY, 0, &error));
    ra_battle_step(&b);
    CHECK(b.units[0].type == 0 && b.units[0].health == 100 && b.rejected == 1 && b.count == 2);
    ra_battle_close(&b);
    CHECK(setup(&b));
    CHECK(ra_battle_bridge_segment_add(&b, 5 * b.width + 5, 1, 0, 255, &error));
    b.types[5].bridge_hut = true;
    CHECK(ra_battle_spawn_team(&b, 3, 1, 4, 7, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 2, 5, 7, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ENTER, 2, &error));
    ra_battle_step(&b);
    CHECK(!b.units[0].health && b.bridge_repaired == 1 && !b.kills && b.units[1].team == 2);
    ra_battle_close(&b);
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 3, 1, 4, 7, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 1, 5, 7, &error));
    b.units[1].health = 20;
    b.initial[1] = b.units[1];
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ENTER, 2, &error));
    ra_battle_step(&b);
    CHECK(!b.units[0].health && b.units[1].health == 100 && !b.kills);
    ra_battle_close(&b);
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 3, 1, 4, 7, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 2, 5, 7, &error));
    b.types[5].capturable = false;
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ENTER, 2, &error));
    ra_battle_step(&b);
    CHECK(b.units[0].health && b.units[1].team == 2);
    ra_battle_close(&b);
}

static void amphibious(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t trace[140][20];
    CHECK(setup(&b));
    b.types[4].amphibious = true;
    for (uint32_t y = 0; y < b.height; ++y)
    {
        b.tiles[y * b.width + 7].track = 0;
        b.tiles[y * b.width + 7].land = 2;
    }
    CHECK(ra_battle_spawn_team(&b, 4, 1, 6, 7, &error));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 6, 8, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 2, 9, 7, &error));
    CHECK(!ra_battle_route(&b, 2, 8 * b.width + 8));
    CHECK(ra_battle_route(&b, 1, 7 * b.width + 8));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_ENTER, 3, &error));
    bool planted = false;
    for (uint32_t i = 0; i < 140; ++i)
    {
        ra_battle_step(&b);
        if (!planted && b.units[2].c4_owner)
        {
            planted = true;
            CHECK(ra_battle_order_add(&b, b.tick + 1, 1, RA_ORDER_MOVE, 5 * b.width + 8, &error));
        }
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(planted && !b.units[2].health && b.units[0].health && b.units[0].cell == 5 * b.width + 8);
    replay(&b, &trace[0][0], 140);
    ra_battle_close(&b);
}
static void production(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    ra_ini rules = {0};
    const char *text = "[YARD]\nFactory=BuildingType\n[ENEMY]\nFactory=InfantryType\n[FOOT]\nCost=100\nTechLevel=1\nOwner=Americans,Russians\nForbiddenHouses="
                       "Russians\nPrerequisite=ENEMY\n";
    CHECK(setup(&b));
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)text, strlen(text)}, "test", &error));
    CHECK(ra_economy_open(&b, &rules, &error));
    CHECK(ra_economy_house(&b, 1, "Americans", 1000, 10, &error));
    CHECK(ra_battle_spawn_structure(&b, 1, 1, 3, 3, &error));
    CHECK(ra_battle_spawn_structure(&b, 5, 1, 8, 3, &error));
    CHECK(ra_economy_house(&b, 2, "Russians", 1000, 10, &error));
    CHECK(ra_economy_owner_allowed(&b, 1, 2) && !ra_economy_owner_allowed(&b, 2, 2));
    CHECK(ra_economy_available(&b, 1, 2));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 2, &error));
    for (uint32_t i = 0; i < 100; ++i) ra_battle_step(&b);
    CHECK(b.count == 3 && b.units[2].type == 2 && b.economy->state.houses[0].credits == 900);
    CHECK(!b.economy->state.houses[0].queues[2].count && !b.economy->state.houses[0].queues[1].count);
    ra_ini_close(&rules);
    ra_battle_close(&b);
}
static const char map_text[] = "[Countries]\n0=Player\n1=Enemy\n[BuildingTypes]\n0=YARD\n1=ENEMY\n[Waypoints]\n0=5005\n"
                               "[Triggers]\nstart=Player,<none>,Start,0,1,1,1,0\ncell=Player,<none>,Cell,0,1,1,1,0\nwin=Player,<none>,Victory,1,1,1,1,0\n"
                               "bad=Player,<none>,Unsupported,0,1,1,1,0\n[Events]\nstart=1,13,0,1\ncell=1,1,0,13\nwin=1,36,0,7\nbad=1,99,0,0\n"
                               "[Actions]\nstart=2,11,4,MISSION:HELLO,0,0,0,0,A,53,2,win,0,0,0,0,A\n"
                               "cell=1,56,0,7,0,0,0,0,A\nwin=1,1,0,13,0,0,0,0,A\nbad=1,2,0,13,0,0,0,0,A\n"
                               "[Tags]\ntag=0,Cell,cell\n[CellTags]\n5007=tag\n";
static void triggers(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    ra_ini map = {0};
    uint8_t trace[120][20];
    const char *houses[] = {"Player House", "Enemy House"}, *countries[] = {"Player", "Enemy"};
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_team(&b, 2, 1, 5, 5, &error));
    CHECK(ra_ini_parse(&map, (ra_view){(const uint8_t *)map_text, strlen(map_text)}, "test-map", &error));
    CHECK(ra_campaign_open(&b, &map, houses, countries, 2, &error));
    CHECK(b.campaign && b.campaign->trigger_count == 4 && b.campaign->unsupported_events[99] == 1);
    CHECK(ra_battle_command_add(&b, 20, 1, 5 * b.width + 7, &error));
    for (uint32_t i = 0; i < 120; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(b.campaign->state.outcome == 1 && b.campaign->state.local[7]);
    CHECK(b.campaign->state.triggers[0].fired == 1 && b.campaign->state.triggers[3].fired == 0);
    CHECK(!strcmp(b.campaign->state.message, "MISSION:HELLO"));
    replay(&b, &trace[0][0], 120);
    ra_battle_reset(&b);
    CHECK(!b.campaign->state.outcome && !b.campaign->state.local[7]);
    ra_ini_close(&map);
    ra_battle_close(&b);
}
static void ordinal_types(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    ra_ini map = {0};
    const char *houses[] = {"Player House", "Enemy House"}, *countries[] = {"Player", "Enemy"};
    const char *text = "[Countries]\n0=Player\n1=Enemy\n[BuildingTypes]\n41=YARD\n7=ENEMY\n[Triggers]\n"
                       "present=Player,<none>,Present,0,1,1,1,0\n[Events]\npresent=1,32,0,0\n[Actions]\npresent=1,11,4,FOUND,0,0,0,0,A\n"
                       "[TeamTypes]\n0=team\n[team]\nHouse=Player\nScript=script\nTaskForce=task\n[task]\n0=1,FOOT\n[script]\n0=46,131073\n";
    CHECK(setup(&b));
    CHECK(ra_battle_spawn_structure(&b, 1, 1, 3, 3, &error));
    CHECK(ra_ini_parse(&map, (ra_view){(const uint8_t *)text, strlen(text)}, "ordinal", &error));
    CHECK(ra_campaign_open(&b, &map, houses, countries, 2, &error));
    CHECK(b.campaign->triggers[0].events[0].argument == 1);
    CHECK(b.campaign->teams[0].script[0].argument == 131077);
    ra_battle_step(&b);
    CHECK(b.campaign->state.triggers[0].fired == 1 && !strcmp(b.campaign->state.message, "FOUND"));
    ra_ini_close(&map);
    ra_battle_close(&b);
}
int main(void)
{
    amphibious();
    edges();
    production();
    people();
    triggers();
    ordinal_types();
    printf("{\"checks\":%u,\"failures\":%u,\"simulation\":%u}\n", checks, failures, RA_BATTLE_VERSION);
    return failures ? 1 : 0;
}
