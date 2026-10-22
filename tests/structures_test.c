#define _CRT_SECURE_NO_WARNINGS
#include "battle_internal.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned checks, failures;
#define CHECK(expression)                                                                                                                                      \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(expression))                                                                                                                                     \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "structure line %d: %s\n", __LINE__, #expression);                                                                                 \
            return false;                                                                                                                                      \
        }                                                                                                                                                      \
    } while (0)
static const char rules_text[] = "[PLANT]\nStrength=300\nArmor=wood\nPower=120\n[FACTORY]\nStrength=600\nArmor=steel\nPower=-50\n";
static const char art_text[] = "[PLANT]\nFoundation=3x2\nHeight=4\n[FACTORY]\nFoundation=2x2\nHeight=3\n";
static bool create(ra_battle *b)
{
    ra_error error = {0};
    ra_battle_tile tiles[32 * 32];
    for (size_t i = 0; i < 32 * 32; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 32, 32, tiles, NULL, &error));
    CHECK(ra_battle_type_add(b, "TANK", "ra2.allied", 4096, &error));
    ra_battle_type *tank = &b->types[0];
    tank->weapon.damage = 65;
    tank->weapon.range = 6 * RA_BATTLE_CELL;
    tank->weapon.rof = 10;
    tank->weapon.speed = 60;
    for (size_t i = 0; i < 11; ++i) tank->weapon.verses[i] = 10000;
    ra_ini rules = {0}, art = {0};
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)rules_text, strlen(rules_text)}, "test-rules", &error));
    CHECK(ra_ini_parse(&art, (ra_view){(const uint8_t *)art_text, strlen(art_text)}, "test-art", &error));
    CHECK(ra_battle_type_add(b, "PLANT", "ra2.soviet", 1, &error));
    CHECK(ra_battle_structure_rules(b, 1, &rules, NULL, &art, &error));
    CHECK(ra_battle_type_add(b, "FACTORY", "ra2.soviet", 1, &error));
    CHECK(ra_battle_structure_rules(b, 2, &rules, NULL, &art, &error));
    ra_ini_close(&rules);
    ra_ini_close(&art);
    return true;
}
static bool foundations(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(create(&b));
    CHECK(ra_battle_spawn_structure(&b, 1, 2, 12, 12, &error));
    CHECK(b.units[0].x == 13 * RA_BATTLE_CELL && b.units[0].y == 12 * RA_BATTLE_CELL + RA_BATTLE_CELL / 2);
    CHECK(b.types[1].height == 416);
    CHECK(!ra_battle_route(&b, 1, 20 * 32 + 20));
    for (uint32_t y = 12; y < 14; ++y)
        for (uint32_t x = 12; x < 15; ++x) CHECK(b.occupied[y * 32 + x] == 1);
    uint8_t before[20], after[20];
    ra_battle_hash(&b, before);
    CHECK(!ra_battle_spawn_structure(&b, 2, 2, 14, 13, &error));
    CHECK(!ra_battle_spawn_structure(&b, 1, 2, 31, 31, &error));
    CHECK(!ra_battle_spawn_team(&b, 1, 2, 20, 20, &error));
    ra_battle_hash(&b, after);
    CHECK(!memcmp(before, after, 20));
    CHECK(!ra_battle_command_add(&b, 1, 1, 20 * 32 + 20, &error));
    uint32_t output, drain;
    ra_battle_power(&b, 2, &output, &drain);
    CHECK(output == 120 && !drain);
    b.units[0].health = 150;
    ra_battle_power(&b, 2, &output, &drain);
    CHECK(output == 60 && !drain);
    CHECK(ra_battle_spawn_structure(&b, 2, 2, 20, 20, &error));
    ra_battle_power(&b, 2, &output, &drain);
    CHECK(output == 60 && drain == 50);
    ra_battle_reset(&b);
    CHECK(b.units[0].health == 300 && b.occupied[13 * 32 + 14] == 1);
    CHECK(battle_structure_distance(&b, &b.units[0], 14 * RA_BATTLE_CELL, 13 * RA_BATTLE_CELL, 100 * 256) == 0);
    CHECK(battle_structure_distance(&b, &b.units[0], 16 * RA_BATTLE_CELL, 13 * RA_BATTLE_CELL, 100 * 256) > 0);
    battle_kill(&b, &b.units[0], 0);
    for (uint32_t y = 12; y < 14; ++y)
        for (uint32_t x = 12; x < 15; ++x) CHECK(!b.occupied[y * 32 + x]);
    ra_battle_power(&b, 2, &output, &drain);
    CHECK(!output && drain == 50);
    ra_battle_close(&b);
    return true;
}
static bool combat_replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_error error = {0};
    CHECK(create(&a) && create(&b));
    CHECK(ra_battle_spawn_team(&a, 0, 1, 8, 12, &error) && ra_battle_spawn_structure(&a, 1, 2, 13, 12, &error));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 8, 12, &error) && ra_battle_spawn_structure(&b, 1, 2, 13, 12, &error));
    CHECK(ra_battle_attack_add(&a, 1, 1, 2, &error));
    uint8_t traces[300][20], digest[20];
    for (uint32_t tick = 0; tick < 300; ++tick)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, traces[tick]);
    }
    CHECK(!a.units[1].health && a.units[0].health && a.units[0].shots >= 5 && !a.occupied[13 * 32 + 15]);
    uint8_t *bytes;
    size_t size;
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &error));
    uint32_t end;
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, digest, &error) && end == 300);
    for (uint32_t tick = 0; tick < end; ++tick)
    {
        ra_battle_step(&b);
        ra_battle_hash(&b, digest);
        CHECK(!memcmp(digest, traces[tick], 20));
    }
    CHECK(ra_battle_command_add(&b, 301, 1, 12 * 32 + 14, &error));
    for (uint32_t tick = 0; tick < 200; ++tick) ra_battle_step(&b);
    CHECK(b.units[0].cell == 12 * 32 + 14);
    ra_battle_reset(&b);
    CHECK(b.occupied[12 * 32 + 14] == 2 && b.units[1].health == 300);
    /* 失败回放必须不改现场，旧协议显式拒绝，不能误解释为新增建筑状态。 */
    ra_battle_hash(&b, digest);
    memcpy(bytes, "RA2RPL9", 8);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, traces[0], &error));
    ra_battle_hash(&b, traces[0]);
    CHECK(!memcmp(digest, traces[0], 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
    return true;
}
static bool alliances_and_overrides(void)
{
    ra_battle b = {0};
    ra_error error = {0};
    CHECK(create(&b));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 10, 10, &error));
    CHECK(ra_battle_spawn_structure(&b, 1, 32, 13, 10, &error));
    b.allies[0] = 1u << 31;
    CHECK(ra_battle_allied(&b, 1, 32) && !ra_battle_allied(&b, 1, 33));
    CHECK(!ra_battle_attack_add(&b, 1, 1, 2, &error));
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_FORCE_UNIT, 2, &error));
    CHECK(!ra_battle_targetable(&b, &b.units[0], &b.units[1], true, false));
    CHECK(ra_battle_targetable(&b, &b.units[0], &b.units[1], false, true));
    ra_battle_close(&b);
    CHECK(create(&b));
    ra_ini local = {0}, art = {0}, rules = {0};
    static const char local_text[] = "[PLANT]\nImage=FACTORY\nStrength=900\nArmor=steel\nPower=250\n";
    static const char fractional_art[] = "[FACTORY]\nFoundation=2x2\nHeight=1.5\n";
    CHECK(ra_ini_parse(&local, (ra_view){(const uint8_t *)local_text, strlen(local_text)}, "map-override", &error));
    CHECK(ra_ini_parse(&art, (ra_view){(const uint8_t *)fractional_art, strlen(fractional_art)}, "fractional-art", &error));
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)rules_text, strlen(rules_text)}, "global-rules", &error));
    CHECK(ra_battle_structure_rules(&b, 1, &rules, &local, &art, &error));
    CHECK(b.types[1].strength == 900 && b.types[1].armor == 7 && b.types[1].power == 250 && b.types[1].height == 156 && b.types[1].foundation_width == 2);
    ra_ini_close(&local);
    ra_ini_close(&art);
    ra_ini_close(&rules);
    ra_battle_close(&b);
    return true;
}
int main(void)
{
    foundations();
    combat_replay();
    alliances_and_overrides();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"structures\",\"paired_steps\":300}\n", checks, failures);
    return failures ? 1 : 0;
}
