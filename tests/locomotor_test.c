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

static void fixture(ra_battle *b)
{
    ra_error error = {0};
    ra_battle_tile tiles[16 * 16];
    for (unsigned i = 0; i < 16 * 16; ++i) tiles[i] = (ra_battle_tile){100, 0, 0, 0, 0};
    CHECK(ra_battle_create(b, 16, 16, tiles, NULL, &error));
    CHECK(ra_battle_type_add(b, "MTNK", "ra2.allied", 17 * 256, &error));
    b->types[0].rot = 5;
    CHECK(ra_battle_spawn(b, 0, 7, 7, &error));
}

static void every_curve(void)
{
    static const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1}, dy[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
    for (unsigned incoming = 0; incoming < 8; ++incoming)
        for (unsigned outgoing = 0; outgoing < 8; ++outgoing)
        {
            int32_t px, py;
            uint32_t d;
            if (!battle_track_sample(incoming * 8 + outgoing, 0, &px, &py, &d)) continue;
            ra_battle b = {0};
            fixture(&b);
            ra_battle_unit *u = &b.units[0];
            uint32_t via = (uint32_t)(7 + dy[incoming]) * 16 + (uint32_t)(7 + dx[incoming]);
            uint32_t end = (uint32_t)(7 + dy[incoming] + dy[outgoing]) * 16 + (uint32_t)(7 + dx[incoming] + dx[outgoing]);
            u->goal = u->destination = end;
            u->path[0] = via;
            u->path[1] = end;
            u->path_count = 2;
            u->body = (ra_battle_turn){incoming * 8192, incoming * 8192, 0, 0};
            bool moving_turn = false;
            for (unsigned step = 0; step < 160 && u->cell != end; ++step)
            {
                int32_t x = u->x, y = u->y;
                uint32_t angle = ra_battle_turn_value(&u->body, b.tick);
                ra_battle_step(&b);
                if ((u->x != x || u->y != y) && ra_battle_turn_value(&u->body, b.tick) != angle) moving_turn = true;
                CHECK(b.occupied[u->cell] == u->id && b.occupied[u->next] == u->id);
                CHECK(abs(u->x - x) < 64 * 256 && abs(u->y - y) < 64 * 256);
                for (unsigned i = 0; i < u->reserved_count; ++i) CHECK(b.occupied[u->reserved[i]] == u->id);
            }
            CHECK(u->cell == end && !u->track_active && !u->reserved_count);
            CHECK(u->x == (int32_t)(end % 16 * RA_BATTLE_CELL) && u->y == (int32_t)(end / 16 * RA_BATTLE_CELL));
            CHECK(ra_battle_turn_value(&u->body, b.tick) == outgoing * 8192);
            if (incoming != outgoing) CHECK(moving_turn);
            unsigned occupied = 0;
            for (unsigned i = 0; i < 256; ++i) occupied += b.occupied[i] != 0;
            CHECK(occupied == 1);
            ra_battle_close(&b);
        }
}

static void continuous_and_stop(void)
{
    ra_battle b = {0};
    fixture(&b);
    ra_battle_unit *u = &b.units[0];
    const uint32_t path[] = {6 * 16 + 7, 6 * 16 + 8, 7 * 16 + 8, 7 * 16 + 9, 8 * 16 + 9, 8 * 16 + 10, 9 * 16 + 10};
    memcpy(u->path, path, sizeof(path));
    u->path_count = 7;
    u->goal = u->destination = path[6];
    for (unsigned i = 0; i < 600 && u->cell != path[6]; ++i) ra_battle_step(&b);
    CHECK(u->curve_joins >= 3 && u->cell == path[6] && !u->reserved_count);
    ra_battle_close(&b);
    fixture(&b);
    u = &b.units[0];
    memcpy(u->path, path, sizeof(path));
    u->path_count = 7;
    u->goal = u->destination = path[6];
    for (unsigned i = 0; i < 8; ++i) ra_battle_step(&b);
    CHECK(u->track_active && u->reserved_count >= 2);
    uint32_t dock = u->next;
    ra_error error = {0};
    CHECK(ra_battle_stop_add(&b, b.tick + 1, 1, &error));
    for (unsigned i = 0; i < 300; ++i) ra_battle_step(&b);
    CHECK(u->cell == dock && u->next == dock && !u->track_active && !u->reserved_count && !u->curve_joins);
    unsigned occupied = 0;
    for (unsigned i = 0; i < 256; ++i) occupied += b.occupied[i] != 0;
    CHECK(occupied == 1);
    ra_battle_close(&b);
}

static void slopes(void)
{
    ra_battle b = {0};
    fixture(&b);
    uint32_t start = 7 * 16 + 7;
    for (unsigned ramp = 1; ramp <= 20; ++ramp)
        for (int dy = -1; dy <= 1; ++dy)
            for (int dx = -1; dx <= 1; ++dx)
            {
                if (!dx && !dy) continue;
                uint32_t end = (uint32_t)(7 + dy) * 16 + (uint32_t)(7 + dx);
                for (unsigned i = 0; i < 256; ++i) b.tiles[i] = (ra_battle_tile){100, 4, (uint8_t)ramp, 0, 0};
                b.tiles[end].height = 5;
                b.tiles[end].ramp = 0;
                CHECK(ra_battle_edge(&b, start, end, 1));
                CHECK(ra_battle_edge(&b, end, start, 1));
                for (unsigned i = 0; i < 256; ++i) b.tiles[i] = (ra_battle_tile){100, 4, 0, 0, 0};
                b.tiles[end].height = 5;
                b.tiles[end].ramp = (uint8_t)ramp;
                CHECK(!ra_battle_edge(&b, start, end, 1));
                CHECK(!ra_battle_edge(&b, end, start, 1));
            }
    ra_battle_close(&b);
}

static void damage_and_priority(void)
{
    ra_battle_weapon w = {0};
    w.max_damage = 10000;
    w.damage = 65;
    w.spread = 19660;
    w.percent_at_max = 5000;
    w.verses[0] = 10000;
    CHECK(battle_damage(&w, 0, 0) == 65 && battle_damage(&w, 0, 1) == 64);
    CHECK(battle_damage(&w, 0, 75) == 32 && battle_damage(&w, 0, 76) == 32 && !battle_damage(&w, 0, 77));
    w.damage = 1;
    w.verses[0] = 2500;
    CHECK(!battle_damage(&w, 0, 0));
    w.damage = 100000;
    w.verses[0] = 10000;
    w.max_damage = 10000;
    CHECK(battle_damage(&w, 0, 0) == 10000);
    w.max_damage = 0;
    CHECK(!battle_damage(&w, 0, 0));
    ra_battle_type type = {0};
    type.flh[0] = 150;
    type.flh[2] = 100;
    int32_t p[3] = {0};
    battle_muzzle(&type, 0, p);
    CHECK(p[0] == 0 && p[1] == -150 && p[2] == 100);
    memset(p, 0, sizeof(p));
    battle_muzzle(&type, 16384, p);
    CHECK(p[0] == 150 && p[1] == 0 && p[2] == 100);
    ra_battle b = {0};
    fixture(&b);
    ra_error e = {0};
    b.types[0].weapon.damage = 65;
    b.types[0].weapon.range = 5 * RA_BATTLE_CELL;
    b.types[0].weapon.verses[0] = 10000;
    CHECK(ra_battle_spawn_team(&b, 0, 2, 8, 7, &e));
    CHECK(ra_battle_spawn_team(&b, 0, 2, 11, 7, &e));
    b.units[1].health = 1;
    CHECK(ra_battle_order_add(&b, 1, 1, RA_ORDER_GUARD, 0, &e));
    ra_battle_step(&b);
    CHECK(b.units[0].target == 3);
    ra_battle_close(&b);
}

static void hash_coverage(void)
{
    ra_battle b = {0};
    fixture(&b);
    ra_error error = {0};
    CHECK(ra_battle_command_add(&b, 1, 1, 3 * 16 + 10, &error));
    for (unsigned i = 0; i < 15; ++i) ra_battle_step(&b);
    ra_battle_unit *u = &b.units[0];
    CHECK(u->track_active);
    uint32_t *fields[] = {&u->track_control, &u->track_index, &u->track_remainder, &u->track_active, &u->track_via, &u->curve_joins, &u->reserved[0]};
    uint8_t before[20], after[20];
    for (unsigned i = 0; i < sizeof(fields) / sizeof(fields[0]); ++i)
    {
        ra_battle_hash(&b, before);
        *fields[i] ^= 1;
        ra_battle_hash(&b, after);
        CHECK(memcmp(before, after, 20));
        *fields[i] ^= 1;
    }
    ra_battle_close(&b);
}

static void destruction_releases_curve(void)
{
    ra_battle b = {0};
    fixture(&b);
    ra_error error = {0};
    CHECK(ra_battle_spawn_team(&b, 0, 2, 12, 12, &error));
    ra_battle_unit *u = &b.units[0];
    u->path[0] = 6 * 16 + 7;
    u->path[1] = 6 * 16 + 8;
    u->path_count = 2;
    u->goal = u->destination = u->path[1];
    for (unsigned i = 0; i < 8; ++i) ra_battle_step(&b);
    CHECK(u->track_active && u->reserved_count >= 2);
    b.types[0].weapon.damage = 1000;
    b.types[0].weapon.spread = RA_BATTLE_CELL;
    b.types[0].weapon.percent_at_max = 10000;
    b.types[0].weapon.verses[0] = 10000;
    ra_battle_shot *shot = &b.shots[0];
    shot->active = 1;
    shot->owner = 2;
    shot->duration = 1;
    shot->start_x = shot->end_x = u->x;
    shot->start_y = shot->end_y = u->y;
    ra_battle_step(&b);
    CHECK(!u->health && !u->track_active && !u->reserved_count);
    for (unsigned i = 0; i < 256; ++i) CHECK(b.occupied[i] != 1);
    ra_battle_close(&b);
}

static void replay_curves(void)
{
    ra_battle a = {0}, b = {0};
    fixture(&a);
    fixture(&b);
    ra_error error = {0};
    uint8_t states[600][20], digest[20], expected[20], *bytes = NULL;
    size_t size = 0;
    uint32_t end = 0, curved = 0;
    CHECK(ra_battle_command_add(&a, 1, 1, 3 * 16 + 12, &error));
    CHECK(ra_battle_stop_add(&a, 45, 1, &error));
    CHECK(ra_battle_command_add(&a, 120, 1, 12 * 16 + 3, &error));
    CHECK(ra_battle_command_add(&a, 220, 1, 3 * 16 + 12, &error));
    CHECK(ra_battle_stop_add(&a, 350, 1, &error));
    for (unsigned i = 0; i < 600; ++i)
    {
        ra_battle_step(&a);
        ra_battle_hash(&a, states[i]);
        if (a.units[0].track_active && a.units[0].track_control % 9) ++curved;
    }
    CHECK(curved > 0 && ra_battle_replay_write(&a, &bytes, &size, &error));
    CHECK(ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error) && end == 600);
    uint64_t phase = 0;
    unsigned batches = 0;
    const uint64_t groups[] = {50000, 120000, 1000, 33333, 200000};
    while (b.tick < 600)
    {
        uint32_t count = ra_battle_clock(&phase, groups[batches++ % 5]);
        while (count-- && b.tick < 600)
        {
            ra_battle_step(&b);
            ra_battle_hash(&b, digest);
            CHECK(!memcmp(digest, states[b.tick - 1], 20));
        }
    }
    CHECK(!memcmp(digest, expected, 20));
    bytes[8] = bytes[36] = 4;
    ra_sha1((ra_view){bytes, size - 20}, bytes + size - 20);
    CHECK(!ra_battle_replay_read(&b, (ra_view){bytes, size}, &end, expected, &error));
    free(bytes);
    ra_battle_close(&a);
    ra_battle_close(&b);
}

int main(void)
{
    every_curve();
    continuous_and_stop();
    slopes();
    damage_and_priority();
    hash_coverage();
    destruction_releases_curve();
    replay_curves();
    printf("{\"checks\":%u,\"failures\":%u,\"suite\":\"locomotor\"}\n", checks, failures);
    return failures ? 1 : 0;
}
