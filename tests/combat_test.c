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
/* 夹具采用原版两种坦克的原始规则值；每项改变都在生成初始单位前完成。 */
static const char rules_text[] = "[General]\nTrackedUphill=1.0\nTrackedDownhill=1.2\nGravity=6\n"
                                 "[MTNK]\nSpeed=7\nROT=5\nStrength=300\nArmor=heavy\nPrimary=105mm\nImage=GTNK\n"
                                 "[HTNK]\nSpeed=6\nROT=5\nStrength=400\nArmor=heavy\nPrimary=120mm\n"
                                 "[105mm]\nDamage=65\nROF=60\nRange=5\nProjectile=Cannon\nSpeed=40\nWarhead=AP\n"
                                 "[120mm]\nDamage=90\nROF=65\nRange=5.75\nProjectile=Cannon\nSpeed=40\nWarhead=AP\n"
                                 "[Cannon]\nArcing=true\nSubjectToCliffs=yes\nSubjectToElevation=yes\nSubjectToWalls=yes\n"
                                 "[AP]\nCellSpread=.3\nPercentAtMax=.5\nVerses=25%,25%,25%,75%,100%,100%,65%,45%,60%,60%,100%\n";

static void fixture(ra_battle *b, bool retaliation)
{
    ra_battle_tile tiles[24 * 16];
    ra_ini rules = {0}, art = {0};
    ra_error e = {0};
    for (unsigned i = 0; i < 24 * 16; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 24, 16, tiles, NULL, &e));
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)rules_text, strlen(rules_text)}, "原版规则夹具.ini", &e));
    CHECK(ra_battle_type_add(b, "MTNK", "ra2.allied", 4352, &e));
    CHECK(ra_battle_type_add(b, "HTNK", "ra2.soviet", 3840, &e));
    CHECK(ra_battle_type_rules(b, 0, &rules, &e));
    CHECK(ra_battle_type_rules(b, 1, &rules, &e));
    const char art_text[] = "[GTNK]\nPrimaryFireFLH=150,0,100\n[HTNK]\nPrimaryFireFLH=150,0,100\n";
    CHECK(ra_ini_parse(&art, (ra_view){(const uint8_t *)art_text, strlen(art_text)}, "原版炮口夹具.ini", &e));
    CHECK(ra_battle_type_art(b, 0, &rules, &art, &e));
    CHECK(ra_battle_type_art(b, 1, &rules, &art, &e));
    CHECK(b->types[0].step == 4352 && b->types[1].step == 3840 && b->types[0].weapon.range == 5 * RA_BATTLE_CELL);
    CHECK(b->types[1].weapon.range == 376832 && b->types[0].weapon.verses[3] == 7500 && b->types[0].weapon.spread == 19660);
    if (!retaliation) b->types[1].weapon.damage = 0;
    ra_ini_close(&rules);
    ra_ini_close(&art);
}
static void spawn_pair(ra_battle *b, uint32_t distance)
{
    ra_error e = {0};
    CHECK(ra_battle_spawn_team(b, 0, 1, 1, 4, &e));
    CHECK(ra_battle_spawn_team(b, 1, 2, 1 + distance, 4, &e));
}
static void shooting(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    uint32_t fired = 0, last = 0, first = 0, first_hit = 0;
    fixture(&b, false);
    spawn_pair(&b, 4);
    CHECK(ra_battle_nearest(&b, 1) == 2);
    CHECK(!ra_battle_attack_add(&b, 1, 1, 1, &e));
    CHECK(ra_battle_attack_add(&b, 1, 1, 0, &e));
    while (b.tick < 700 && b.units[1].health)
    {
        ra_battle_step(&b);
        if (b.fired != fired)
        {
            if (last) CHECK(b.tick - last >= 60 && b.tick - last <= 62);
            else first = b.tick;
            last = b.tick;
            fired = b.fired;
        }
        if (!first_hit && b.impacts)
        {
            first_hit = b.tick;
            /* 原版近目标格修正后落点位于目标坐标，AP 对重甲结算 65 点。 */
            CHECK(b.units[1].health == 335 && b.shots[0].hit == 2);
        }
        CHECK(b.units[0].health == 300);
    }
    CHECK(first >= 12 && first_hit - first == 11 && b.fired == 7 && b.impacts == 7);
    CHECK(!b.units[1].health && b.kills == 1 && b.units[0].kills == 1 && b.units[1].destroyed_tick == b.tick);
    CHECK(!b.occupied[b.units[1].cell] && b.occupied[b.units[0].cell] == 1);
    CHECK(!ra_battle_attack_add(&b, b.tick + 1, 1, 2, &e));
    CHECK(!ra_battle_command_add(&b, b.tick + 1, 2, 50, &e));
    ra_battle_step(&b);
    CHECK(!b.units[0].target);
    ra_battle_close(&b);
}
static void armor_and_miss(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, false);
    b.types[1].armor = 3;
    spawn_pair(&b, 4);
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    while (!b.impacts && b.tick < 100) ra_battle_step(&b);
    CHECK(b.units[1].health == 352);
    ra_battle_close(&b);
    fixture(&b, false);
    b.types[1].step = RA_BATTLE_CELL;
    b.types[1].rot = b.types[1].slowdown = 0;
    spawn_pair(&b, 4);
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    while (!b.fired && b.tick < 100) ra_battle_step(&b);
    CHECK(ra_battle_command_add(&b, b.tick + 1, 2, 12 * 24 + 20, &e));
    while (!b.impacts && b.tick < 100) ra_battle_step(&b);
    CHECK(b.impacts == 1 && b.units[1].health == 400 && !b.shots[0].hit);
    ra_battle_close(&b);
}
static void obstacles_and_range(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, false);
    spawn_pair(&b, 5);
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    for (unsigned i = 0; i < 40; ++i) ra_battle_step(&b);
    CHECK(b.fired == 1 && b.units[0].cell == 4 * 24 + 1);
    ra_battle_close(&b);
    fixture(&b, false);
    /* 非弧线炮弹用于隔离墙体与悬崖碰撞，不把此夹具当成原版 Cannon 的轨迹校准。 */
    b.types[0].weapon.arcing = false;
    spawn_pair(&b, 4);
    b.tiles[4 * 24 + 4].land = 4;
    b.tiles[4 * 24 + 4].blocked = 1;
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    for (unsigned i = 0; i < 55; ++i) ra_battle_step(&b);
    CHECK(b.impacts == 1 && b.units[1].health == 400 && b.shots[0].x < 5 * (int32_t)RA_BATTLE_CELL);
    ra_battle_close(&b);
    fixture(&b, false);
    spawn_pair(&b, 11);
    /* 开口位于远处，攻击寻路必须找到可到达的射程圈。 */
    for (unsigned y = 0; y < 14; ++y) b.tiles[y * 24 + 5].blocked = 1;
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    for (unsigned i = 0; i < 1800 && !b.fired; ++i) ra_battle_step(&b);
    CHECK(b.fired > 0 && b.units[0].cell % 24 > 5);
    ra_battle_close(&b);
}
static void stopping_and_slopes(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, false);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 1, 4, &e));
    CHECK(ra_battle_command_add(&b, 1, 1, 4 * 24 + 10, &e));
    while (!b.units[0].progress && b.tick < 100) ra_battle_step(&b);
    uint32_t dock = b.units[0].next;
    CHECK(ra_battle_stop_add(&b, b.tick + 1, 1, &e));
    for (unsigned i = 0; i < 150; ++i) ra_battle_step(&b);
    CHECK(b.units[0].cell == dock && b.units[0].cell == b.units[0].next && !b.units[0].progress);
    CHECK(b.units[0].x == (int32_t)(dock % 24 * RA_BATTLE_CELL) && b.units[0].speed_factor >= 3000 && b.units[0].speed_factor < 10000);
    ra_battle_type *t = &b.types[0];
    CHECK(ra_battle_motion_rate(t, 100, 0, 10000) == 17 * 256 && ra_battle_motion_rate(t, 70, 0, 10000) == 11 * 256);
    CHECK(ra_battle_motion_rate(t, 100, -1, 10000) == 20 * 256 && ra_battle_motion_rate(t, 70, -1, 10000) == 14 * 256);
    CHECK(ra_battle_slowdown(t, 499, 10000) == 9660 && ra_battle_slowdown(t, 500, 9660) == 9960);
    uint32_t factor = 10000;
    for (unsigned i = 0; i < 100; ++i) factor = ra_battle_slowdown(t, 10, factor);
    CHECK(factor == 3000);
    ra_battle_close(&b);
}
static void replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_error e = {0};
    uint8_t *bytes = NULL, expected[20], x[20], y[20];
    size_t size = 0;
    uint32_t end = 0;
    fixture(&a, true);
    fixture(&b, true);
    spawn_pair(&a, 4);
    spawn_pair(&b, 4);
    CHECK(ra_battle_attack_add(&a, 1, 1, 2, &e));
    for (unsigned i = 0; i < 480; ++i) ra_battle_step(&a);
    CHECK(a.fired > 5 && a.kills > 0 && a.units[1].shots > 0);
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &e));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_reset(&a);
    for (uint32_t i = 0; i < end; ++i)
    {
        ra_battle_step(&a);
        ra_battle_step(&b);
        ra_battle_hash(&a, x);
        ra_battle_hash(&b, y);
        CHECK(!memcmp(x, y, 20));
    }
    CHECK(!memcmp(x, expected, 20));
    ra_battle_reset(&b);
    uint64_t phase = 0, elapsed = 0, total = (uint64_t)end * 1000000 / RA_BATTLE_HZ;
    while (elapsed < total)
    {
        uint64_t delta = 7301 + elapsed % 17003;
        if (delta > total - elapsed) delta = total - elapsed;
        elapsed += delta;
        uint32_t ticks = ra_battle_clock(&phase, delta);
        while (ticks--) ra_battle_step(&b);
    }
    ra_battle_hash(&b, y);
    CHECK(b.tick == end && !memcmp(x, y, 20));
    uint32_t occupied = b.occupied[b.units[1].cell];
    b.occupied[b.units[1].cell] = occupied + 10;
    ra_battle_hash(&b, y);
    CHECK(memcmp(x, y, 20) != 0);
    b.occupied[b.units[1].cell] = occupied;
    /* 修改命令种类后重新签摘要，验证语义拒绝而非仅检查损坏尾部。 */
    bytes[104 + 2 * 20 + 16] = 99;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_hash(&b, y);
    CHECK(!memcmp(x, y, 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}
static void simultaneous_destruction(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b, true);
    b.types[0].weapon.damage = b.types[1].weapon.damage = 1000;
    spawn_pair(&b, 4);
    CHECK(ra_battle_attack_add(&b, 1, 1, 2, &e));
    CHECK(ra_battle_attack_add(&b, 1, 2, 1, &e));
    for (unsigned i = 0; i < 60; ++i) ra_battle_step(&b);
    CHECK(!b.units[0].health && !b.units[1].health && b.kills == 2 && b.impacts == 2);
    CHECK(!b.occupied[b.units[0].cell] && !b.occupied[b.units[1].cell]);
    CHECK(b.units[0].kills == 1 && b.units[1].kills == 1);
    ra_battle_close(&b);
}
static void oversized_rule(void)
{
    ra_battle b = {0};
    ra_ini rules = {0};
    ra_error e = {0};
    char text[sizeof(rules_text) + 64];
    const char *range = strstr(rules_text, "Range=5\n");
    fixture(&b, false);
    snprintf(text, sizeof(text), "%.*sRange=2814754.76710656\n%s", (int)(range - rules_text), rules_text, range + strlen("Range=5\n"));
    CHECK(ra_ini_parse(&rules, (ra_view){(const uint8_t *)text, strlen(text)}, "超大射程夹具.ini", &e));
    CHECK(!ra_battle_type_rules(&b, 0, &rules, &e));
    CHECK(b.types[0].weapon.range == 5 * RA_BATTLE_CELL);
    ra_ini_close(&rules);
    ra_battle_close(&b);
}
int main(void)
{
    shooting();
    armor_and_miss();
    obstacles_and_range();
    stopping_and_slopes();
    replay();
    simultaneous_destruction();
    oversized_rule();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"combat\"}\n", checks, failures);
    return failures ? 1 : 0;
}
