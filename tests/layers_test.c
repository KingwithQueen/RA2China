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

static void fixture(ra_battle *b)
{
    ra_battle_tile tiles[16 * 16];
    ra_error e = {0};
    for (unsigned i = 0; i < 256; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    tiles[8 * 16 + 4].height = tiles[8 * 16 + 11].height = 4;
    CHECK(ra_battle_create(b, 16, 16, tiles, NULL, &e));
    for (unsigned x = 5; x <= 10; ++x) CHECK(ra_battle_bridge_add(b, 8 * 16 + x, 1, true, &e));
    CHECK(ra_battle_type_add(b, "MTNK", "ra2.allied", 17 * 256, &e));
    b->types[0].rot = 5;
    b->types[0].weapon.damage = 65;
    b->types[0].weapon.range = 5 * RA_BATTLE_CELL;
    b->types[0].weapon.verses[0] = 10000;
    b->types[0].weapon.spread = 19660;
    b->types[0].weapon.percent_at_max = 5000;
}

static void layers(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    CHECK(ra_battle_spawn_layer(&b, 0, 1, 7, 8, 1, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 2, 7, 8, &e));
    CHECK(b.occupied[8 * 16 + 7] == 2 && b.occupied[256 + 8 * 16 + 7] == 1);
    CHECK(ra_battle_unit_height(&b, &b.units[0]) == 416 && ra_battle_unit_height(&b, &b.units[1]) == 0);
    CHECK(!ra_battle_targetable(&b, &b.units[0], &b.units[1], true, false));
    CHECK(!ra_battle_edge(&b, 8 * 16 + 7, 256 + 8 * 16 + 7, 2));
    CHECK(!ra_battle_edge(&b, 7 * 16 + 7, 256 + 8 * 16 + 7, 2));
    CHECK(ra_battle_command_add(&b, 1, 1, 256 + 8 * 16 + 9, &e));
    CHECK(ra_battle_command_add(&b, 1, 2, 8 * 16 + 9, &e));
    for (unsigned step = 0; step < 160; ++step)
    {
        ra_battle_step(&b);
        CHECK(b.units[0].cell >= 256 && b.units[1].cell < 256);
        CHECK(b.occupied[b.units[0].cell] == 1 && b.occupied[b.units[1].cell] == 2);
        for (unsigned i = 0; i < 2; ++i)
            for (unsigned j = 0; j < b.units[i].reserved_count; ++j) CHECK(b.occupied[b.units[i].reserved[j]] == i + 1);
    }
    CHECK(b.units[0].cell == 256 + 8 * 16 + 9 && b.units[1].cell == 8 * 16 + 9);
    CHECK(!ra_battle_bridge_add(&b, 0, 1, true, &e));
    ra_battle_reset(&b);
    CHECK(b.occupied[256 + 8 * 16 + 7] == 1 && b.occupied[8 * 16 + 7] == 2);
    ra_battle_close(&b);
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 4, 8, &e));
    CHECK(ra_battle_route(&b, 1, 8 * 16 + 11));
    CHECK(b.units[0].path_count == 7);
    for (unsigned i = 0; i < 6; ++i) CHECK(b.units[0].path[i] >= 256);
    CHECK(ra_battle_command_add(&b, 1, 1, 8 * 16 + 11, &e));
    bool crossed = false;
    for (unsigned step = 0; step < 260; ++step)
    {
        ra_battle_step(&b);
        if (b.units[0].cell >= 256) crossed = true;
        CHECK(ra_battle_unit_height(&b, &b.units[0]) == 416);
        CHECK(b.occupied[b.units[0].cell] == 1);
    }
    CHECK(crossed && b.units[0].cell == 8 * 16 + 11 && !b.units[0].reserved_count);
    ra_battle_close(&b);
}

static void filters(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 2, 2, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 2, 3, 2, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 2, 4, 2, &e));
    ra_battle_unit *u = &b.units[0], *v = &b.units[1];
    CHECK(ra_battle_targetable(&b, u, v, true, false));
    const uint32_t blocked[] = {RA_UNIT_LIMBO, RA_UNIT_SINKING, RA_UNIT_UNTARGETABLE, RA_UNIT_IMMUNE, RA_UNIT_SUBMERGED};
    for (unsigned i = 0; i < sizeof(blocked) / sizeof(*blocked); ++i)
    {
        v->traits = blocked[i];
        CHECK(!ra_battle_targetable(&b, u, v, true, false));
        CHECK(ra_battle_nearest(&b, 1) == 3);
    }
    v->traits = RA_UNIT_CLOAKED;
    CHECK(!ra_battle_targetable(&b, u, v, true, false));
    v->detected_by = 1;
    CHECK(ra_battle_targetable(&b, u, v, true, false));
    v->hidden_from = 1;
    CHECK(!ra_battle_targetable(&b, u, v, true, true));
    v->hidden_from = v->traits = 0;
    v->traits = RA_UNIT_AIRBORNE;
    CHECK(!ra_battle_targetable(&b, u, v, true, false));
    b.types[0].weapon.aa = true;
    CHECK(ra_battle_targetable(&b, u, v, true, false));
    v->traits = 0;
    b.types[0].weapon.no_ground = true;
    CHECK(!ra_battle_targetable(&b, u, v, true, false));
    b.types[0].weapon.no_ground = false;
    for (unsigned verses = 0; verses <= 300; verses += 100)
    {
        b.types[0].weapon.verses[0] = verses;
        CHECK(ra_battle_targetable(&b, u, v, true, false) == (verses > 200));
        CHECK(ra_battle_targetable(&b, u, v, false, true) == (verses != 0));
    }
    b.types[0].weapon.verses[0] = 10000;
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_GUARD, 0, &e));
    ra_battle_step(&b);
    CHECK(u->target == 2);
    v->traits = RA_UNIT_LIMBO;
    ra_battle_step(&b);
    CHECK(u->target == 3);
    CHECK(!battle_aim(&b, v, &(ra_battle_unit){0}));
    ra_battle_close(&b);
}

static void shot(ra_battle *b, int old_z, int next_z)
{
    ra_battle_shot *s = &b->shots[0];
    *s = (ra_battle_shot){0};
    s->active = s->id = s->owner = 1;
    s->duration = 20;
    s->x = s->start_x = 7 * RA_BATTLE_CELL;
    s->y = s->start_y = 8 * RA_BATTLE_CELL;
    s->z = old_z * 256;
    s->end_x = 12 * RA_BATTLE_CELL;
    s->end_y = s->y;
    s->velocity[2] = battle_real_int(next_z - old_z + 6);
    b->types[0].weapon.arcing = true;
    b->types[0].weapon.gravity = 6 * 256;
}
static void lifecycle(void)
{
    ra_battle b = {0};
    ra_error e = {0};
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 2, 2, &e));
    CHECK(ra_battle_spawn_layer(&b, 0, 2, 7, 8, 1, &e));
    shot(&b, 417, 415);
    ra_battle_step(&b);
    CHECK(b.shots[0].active == 2 && b.shots[0].collision == RA_COLLISION_BRIDGE_DOWN && b.shots[0].z == 416 * 256);
    CHECK(b.impacts == 1 && b.units[1].health == 35);
    for (unsigned step = 0; step < 13; ++step) ra_battle_step(&b);
    CHECK(b.shots[0].active == 3 && b.shots[0].retired_tick == b.tick && b.impacts == 1);
    ra_battle_step(&b);
    CHECK(!b.shots[0].active && !b.shots[0].id && b.impacts == 1);
    shot(&b, 415, 416);
    ra_battle_step(&b);
    CHECK(b.shots[0].active == 2 && b.shots[0].collision == RA_COLLISION_BRIDGE_UP && b.shots[0].z == 396 * 256);
    CHECK(b.impacts == 2 && !b.units[1].health && !b.occupied[256 + 8 * 16 + 7]);
    ra_battle_close(&b);
    fixture(&b);
    CHECK(ra_battle_spawn_team(&b, 0, 1, 2, 2, &e));
    shot(&b, 10, -1);
    b.units[0].health = 0;
    ra_battle_step(&b);
    CHECK(b.impacts == 1 && b.shots[0].collision == RA_COLLISION_GROUND && b.shots[0].z == 0);
    shot(&b, 100, 100);
    b.shots[0].x = 15 * RA_BATTLE_CELL;
    b.shots[0].velocity[0] = battle_real_int(512);
    ra_battle_step(&b);
    CHECK(b.shots[0].active == 3 && b.shots[0].collision == RA_COLLISION_OUTSIDE && b.impacts == 1);
    ra_battle_step(&b);
    CHECK(!b.shots[0].active);
    ra_battle_close(&b);
}

static void replay(void)
{
    ra_battle a = {0}, b = {0};
    ra_error e = {0};
    fixture(&a);
    fixture(&b);
    CHECK(ra_battle_spawn_team(&a, 0, 1, 4, 8, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 1, 4, 8, &e));
    CHECK(ra_battle_spawn_layer(&a, 0, 2, 9, 8, 1, &e));
    CHECK(ra_battle_spawn_layer(&b, 0, 2, 9, 8, 1, &e));
    CHECK(ra_battle_command_add(&a, 1, 2, 256 + 8 * 16 + 10, &e));
    CHECK(ra_battle_command_add(&a, 1, 1, 256 + 8 * 16 + 8, &e));
    CHECK(ra_battle_stop_add(&a, 100, 1, &e));
    CHECK(ra_battle_command_add(&a, 180, 1, 8 * 16 + 4, &e));
    uint8_t states[700][20], expected[20], digest[20], *bytes = NULL;
    size_t size = 0;
    uint32_t end = 0;
    for (unsigned i = 0; i < 700; ++i)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, states[i]);
    }
    CHECK(ra_battle_replay_write(&a, &bytes, &size, &e));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e) && end == 700);
    uint64_t clock = 0;
    unsigned step = 0;
    while (step < end)
    {
        uint32_t count = ra_battle_clock(&clock, step % 2 ? 175000 : 13000);
        while (count-- && step < end)
        {
            ra_battle_step(&b);
            ra_battle_hash(&b, digest);
            CHECK(!memcmp(digest, states[step++], 20));
        }
    }
    CHECK(!memcmp(digest, expected, 20));
    uint32_t *fields[] = {&b.units[0].traits, &b.units[0].hidden_from, &b.units[0].detected_by};
    for (unsigned i = 0; i < sizeof(fields) / sizeof(*fields); ++i)
    {
        ra_battle_hash(&b, digest);
        *fields[i] ^= 1;
        ra_battle_hash(&b, expected);
        CHECK(memcmp(digest, expected, 20));
        *fields[i] ^= 1;
    }
    ra_battle_hash(&b, digest);
    b.bridges[8 * 16 + 7] ^= 4;
    ra_battle_hash(&b, expected);
    CHECK(memcmp(digest, expected, 20));
    b.bridges[8 * 16 + 7] ^= 4;
    bytes[8] = bytes[36] = 5;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &e));
    ra_battle_hash(&b, expected);
    CHECK(!memcmp(digest, expected, 20));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}
int main(void)
{
    layers();
    filters();
    lifecycle();
    replay();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"layers\",\"paired_steps\":700}\n", checks, failures);
    return failures ? 1 : 0;
}
