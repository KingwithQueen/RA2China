#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>
static unsigned checks, failures;
#define CHECK(x)                                                                                                                                               \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(x))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "economy line %d: %s\n", __LINE__, #x);                                                                                            \
            return false;                                                                                                                                      \
        }                                                                                                                                                      \
    } while (0)
static const char rules_text[] = "[General]\nBuildSpeed=.1\nPrerequisitePower=POWER\nPrerequisiteFactory=FACTORY\nPrerequisiteProc=REF\n"
                                 "[YARD]\nCost=1000\nTechLevel=-1\nFactory=BuildingType\n"
                                 "[POWER]\nCost=100\nTechLevel=1\nOwner=Russians\nPrerequisite=YARD\n"
                                 "[REF]\nCost=200\nTechLevel=1\nOwner=Russians\nPrerequisite=POWER,YARD\nRefinery=yes\nFreeUnit=MINER\n"
                                 "[FACTORY]\nCost=200\nTechLevel=2\nOwner=Russians\nPrerequisite=PROC,YARD\nFactory=UnitType\n"
                                 "[TANK]\nCost=100\nTechLevel=2\nOwner=Russians\nPrerequisite=FACTORY\n"
                                 "[MINER]\nCost=100\nTechLevel=1\nOwner=Russians\nPrerequisite=FACTORY,PROC\nHarvester=yes\nStorage=4\nDock=REF\n"
                                 "[TECH]\nCost=300\nTechLevel=8\nOwner=Russians\nPrerequisite=FACTORY\n"
                                 "[Riparius]\nValue=25\n[Cruentus]\nValue=50\n";
static bool setup(ra_battle *b, bool base)
{
    ra_error error = {0};
    ra_ini rules = {0};
    ra_battle_tile tiles[32 * 32];
    for (uint32_t i = 0; i < 32 * 32; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 32, 32, tiles, NULL, &error));
    const char *ids[] = {"YARD", "POWER", "REF", "FACTORY", "TANK", "MINER", "TECH"};
    for (uint32_t i = 0; i < 7; ++i)
    {
        CHECK(ra_battle_type_add(b, ids[i], "ra2.soviet", 8192, &error));
        if (i < 4 || i == 6)
        {
            b->types[i].structure = true;
            b->types[i].foundation_width = b->types[i].foundation_height = 2;
        }
    }
    b->types[1].power = 100;
    b->types[2].power = -50;
    b->types[3].power = -25;
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)rules_text, strlen(rules_text)}, "economy-test", &error));
    CHECK(ra_economy_open(b, &rules, &error));
    ra_ini_close(&rules);
    CHECK(ra_economy_house(b, 1, "Russians", 1000, 10, &error));
    CHECK(ra_battle_spawn_structure(b, 0, 1, 5, 5, &error));
    if (base)
    {
        CHECK(ra_battle_spawn_structure(b, 1, 1, 8, 5, &error));
        CHECK(ra_battle_spawn_structure(b, 2, 1, 11, 5, &error));
        CHECK(ra_battle_spawn_structure(b, 3, 1, 14, 5, &error));
    }
    return true;
}
static bool building(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    uint8_t before[20], after[20];
    CHECK(setup(&b, false));
    ra_battle_hash(&b, before);
    ra_battle_reset(&b);
    ra_battle_hash(&b, after);
    CHECK(!memcmp(before, after, 20) && b.economy->state.houses[0].credits == 1000);
    CHECK(ra_economy_available(&b, 1, 1));
    CHECK(!ra_economy_available(&b, 1, 2));
    CHECK(!ra_economy_available(&b, 1, 4));
    CHECK(!ra_economy_available(&b, 2, 1));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 1, &error));
    ra_battle_step(&b);
    ra_econ_house *h = &b.economy->state.houses[0];
    CHECK(h->queues[0].paid > 0 && h->credits + h->spent == 1000);
    CHECK(ra_economy_command(&b, 2, 1, RA_ECON_PAUSE, 0, &error));
    ra_battle_step(&b);
    uint32_t progress = h->queues[0].progress;
    for (uint32_t i = 0; i < 20; ++i) ra_battle_step(&b);
    CHECK(h->queues[0].progress == progress);
    CHECK(ra_economy_command(&b, b.tick + 1, 1, RA_ECON_CANCEL, 0, &error));
    ra_battle_step(&b);
    CHECK(!h->queues[0].count && h->credits == 1000 && !h->spent);
    CHECK(ra_economy_command(&b, b.tick + 1, 1, RA_ECON_QUEUE, 1, &error));
    for (uint32_t i = 0; i < 10; ++i) ra_battle_step(&b);
    CHECK(h->queues[0].paid == 100 && h->credits == 900);
    CHECK(!ra_economy_placeable(&b, 1, 1, 5 * 32 + 5));
    CHECK(!ra_economy_placeable(&b, 1, 1, 30 * 32 + 30));
    CHECK(ra_economy_placeable(&b, 1, 1, 5 * 32 + 8));
    CHECK(ra_economy_command(&b, b.tick + 1, 1, RA_ECON_PLACE, (5 * 32 + 8) * RA_BATTLE_TYPES + 1, &error));
    ra_battle_step(&b);
    CHECK(b.count == 2 && b.initial_count == 1 && h->built == 1 && !h->queues[0].count && ra_economy_available(&b, 1, 2));
    ra_battle_hash(&b, before);
    uint8_t *bytes = NULL, expected[20];
    size_t size = 0;
    uint32_t end = 0;
    CHECK(ra_battle_replay_write(&b, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    CHECK(b.count == 1 && b.economy->state.houses[0].credits == 1000);
    while (b.tick < end) ra_battle_step(&b);
    ra_battle_hash(&b, after);
    CHECK(!memcmp(before, after, 20) && !memcmp(after, expected, 20));
    free(bytes);
    ra_battle_close(&b);
    return true;
}
static bool production_and_money(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b, true));
    b.economy->state.houses[0].tech = 2;
    CHECK(!ra_economy_available(&b, 1, 6));
    CHECK(ra_economy_available(&b, 1, 4));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 4, &error));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 4, &error));
    for (uint32_t i = 0; i < 20; ++i) ra_battle_step(&b);
    CHECK(b.count == 6 && b.economy->state.houses[0].produced == 2 && b.economy->state.houses[0].credits == 800);
    CHECK(ra_battle_command_add(&b, b.tick + 1, 5, 12 * 32 + 14, &error));
    uint8_t trace[200][20], digest[20], expected[20], *bytes = NULL;
    uint32_t end;
    size_t size;
    for (uint32_t i = 0; i < 200; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(ra_battle_replay_write(&b, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    while (b.tick < end)
    {
        ra_battle_step(&b);
        if (b.tick > 20)
        {
            ra_battle_hash(&b, digest);
            CHECK(!memcmp(digest, trace[b.tick - 21], 20));
        }
    }
    CHECK(!memcmp(digest, expected, 20));
    free(bytes);
    ra_battle_reset(&b);
    b.command_count = 0;
    b.economy->state.houses[0].credits = 0;
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 4, &error));
    for (uint32_t i = 0; i < 20; ++i) ra_battle_step(&b);
    CHECK(b.count == 4 && b.economy->state.houses[0].queues[1].paid == 0);
    b.economy->state.houses[0].credits = 100;
    for (uint32_t i = 0; i < 20; ++i) ra_battle_step(&b);
    CHECK(b.count == 5 && b.economy->state.houses[0].credits == 0);
    ra_battle_close(&b);
    return true;
}
static bool harvesting(bool chrono)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b, true));
    CHECK(ra_battle_spawn_team(&b, 5, 1, 11, 9, &error));
    b.economy->types[5].chrono = chrono;
    CHECK(ra_economy_ore(&b, 11 * 32 + 11, 1, 4, &error));
    CHECK(ra_economy_ore(&b, 11 * 32 + 12, 2, 4, &error));
    CHECK(ra_economy_command(&b, 1, 5, RA_ECON_HARVEST, 11 * 32 + 11, &error));
    uint8_t (*trace)[20] = malloc(1200 * 20), digest[20], expected[20], *bytes = NULL;
    CHECK(trace != NULL);
    for (uint32_t i = 0; i < 1200; ++i)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, trace[i]);
    }
    CHECK(b.economy->state.houses[0].earned == 300 && b.economy->state.houses[0].credits == 1300);
    CHECK(!b.economy->ore[11 * 32 + 11] && !b.economy->ore[11 * 32 + 12]);
    uint32_t end;
    size_t size;
    CHECK(ra_battle_replay_write(&b, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    while (b.tick < end)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, digest);
        CHECK(!memcmp(digest, trace[b.tick - 1], 20));
    }
    CHECK(!memcmp(digest, expected, 20));
    free(bytes);
    free(trace);
    ra_battle_close(&b);
    return true;
}
static bool blocked_exit_and_low_power(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b, true));
    for (uint32_t y = 4; y <= 7; ++y)
        for (uint32_t x = 13; x <= 16; ++x)
            if (x == 13 || x == 16 || y == 4 || y == 7) b.tiles[y * 32 + x].blocked = 1;
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 4, &error));
    for (uint32_t i = 0; i < 30; ++i) ra_battle_step(&b);
    CHECK(b.count == 4 && b.economy->state.houses[0].queues[1].paid == 100 && b.economy->state.houses[0].credits == 900);
    b.tiles[7 * 32 + 14].blocked = 0;
    ra_battle_step(&b);
    CHECK(b.count == 5 && !b.economy->state.houses[0].queues[1].count);
    battle_kill(&b, &b.units[1], 0);
    CHECK(ra_economy_command(&b, b.tick + 1, 1, RA_ECON_QUEUE, 4, &error));
    ra_battle_step(&b);
    CHECK(b.economy->state.houses[0].queues[1].progress == 500);
    battle_kill(&b, &b.units[3], 0);
    uint32_t progress = b.economy->state.houses[0].queues[1].progress;
    for (uint32_t i = 0; i < 10; ++i) ra_battle_step(&b);
    CHECK(b.economy->state.houses[0].queues[1].progress == progress);
    ra_battle_close(&b);
    return true;
}
static bool free_miner_and_requested_refinery(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(setup(&b, true));
    CHECK(ra_battle_spawn_structure(&b, 2, 1, 20, 5, &error));
    CHECK(ra_battle_spawn_team(&b, 5, 1, 11, 9, &error));
    b.economy->types[5].storage = 40;
    b.types[5].rot = 5;
    b.types[5].step = ra_battle_native_speed(4) * 256;
    b.types[5].slowdown = 500;
    b.types[5].deceleration = 20;
    CHECK(ra_economy_ore(&b, 9 * 32 + 11, 1, 12, &error));
    CHECK(ra_economy_command(&b, 1, 6, RA_ECON_HARVEST, 9 * 32 + 11, &error));
    for (uint32_t i = 0; i < 10; ++i) ra_battle_step(&b);
    CHECK(b.economy->state.miners[5].ore == 2);
    CHECK(ra_battle_stop_add(&b, b.tick + 1, 6, &error));
    ra_battle_step(&b);
    CHECK(!b.economy->state.miners[5].active && b.economy->state.miners[5].ore == 2);
    CHECK(ra_economy_command(&b, b.tick + 1, 6, RA_ECON_RETURN, 5, &error));
    ra_battle_step(&b);
    CHECK(b.economy->state.miners[5].refinery == 5);
    for (uint32_t i = 0; i < 1500 && !b.economy->state.houses[0].earned; ++i) ra_battle_step(&b);
    CHECK(b.economy->state.houses[0].earned == 50 && !b.economy->state.miners[5].ore);
    ra_battle_close(&b);
    CHECK(setup(&b, true));
    CHECK(ra_economy_command(&b, 1, 1, RA_ECON_QUEUE, 2, &error));
    for (uint32_t i = 0; i < 40; ++i) ra_battle_step(&b);
    CHECK(ra_economy_placeable(&b, 1, 2, 8 * 32 + 11));
    CHECK(ra_economy_command(&b, b.tick + 1, 1, RA_ECON_PLACE, (8 * 32 + 11) * RA_BATTLE_TYPES + 2, &error));
    ra_battle_step(&b);
    CHECK(b.count == 6 && b.types[b.units[4].type].structure && b.economy->state.miners[5].active);
    CHECK(b.economy->state.houses[0].credits == 800 && b.economy->state.houses[0].produced == 1);
    uint8_t *bytes = NULL, expected[20], before[20], after[20];
    size_t size;
    uint32_t end;
    CHECK(ra_battle_replay_write(&b, &bytes, &size, &error));
    ra_battle_hash(&b, before);
    memcpy(bytes, "RA2RPL10", 8);
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    ra_battle_hash(&b, after);
    CHECK(!memcmp(before, after, 20));
    free(bytes);
    ra_battle_close(&b);
    return true;
}
int main(void)
{
    building();
    production_and_money();
    harvesting(false);
    harvesting(true);
    blocked_exit_and_low_power();
    free_miner_and_requested_refinery();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"economy\",\"paired_steps\":2600}\n", checks, failures);
    return failures ? 1 : 0;
}
