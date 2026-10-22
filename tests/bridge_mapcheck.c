#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

/* 只重新布置本程序的坦克，核对原始断桥在修复后确实能够穿越缺失段。 */
static int app_main(int argc, char **argv)
{
    battle_scene *s = calloc(1, sizeof(*s));
    ra_error e = {0};
    uint32_t start = 0, goal = 0, target = 0, missing = 0, total_missing = 0, checks = 0, failures = 0;
    uint8_t states[600][20], digest[20], expected[20], *bytes = NULL;
    size_t size = 0;
    int result = 1;
#define CHECK(v)                                                                                                                                               \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(v))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "line %d: %s\n", __LINE__, #v);                                                                                                    \
            goto done;                                                                                                                                         \
        }                                                                                                                                                      \
    } while (0)
    CHECK(argc == 2 && s && battle_scene_open(s, "H:/开发/运行版本/原版1.006", &e));
    for (size_t m = 0; m < s->maps.source_count; ++m)
        if (ra_equal(s->maps.sources[m].name, "MP09DU.map"))
        {
            CHECK(battle_scene_map(s, m, false, &e));
            break;
        }
    ra_battle *b = &s->battle;
    CHECK(b->tiles);
    for (uint32_t i = 0; i < b->bridge_count && !target; ++i)
    {
        const ra_battle_bridge *p = &b->bridge_parts[i];
        if (p->frame != 255) continue;
        uint32_t stride = p->axis == 1 ? 1u : 512u, a = p->cell, c = a;
        while (a >= stride && b->bridge_at[a - stride]) a -= stride;
        while (c + stride < 512 * 512 && b->bridge_at[c + stride]) c += stride;
        if (a < stride || c + stride >= 512 * 512) continue;
        for (int side = -1; side <= 1 && !target; ++side)
        {
            int offset = side * (p->axis == 1 ? 512 : 1);
            uint32_t from = (uint32_t)((int)(a - stride) + offset), to = (uint32_t)((int)(c + stride) + offset);
            if (!ra_battle_passable(b, from) || !ra_battle_passable(b, to) || b->tiles[from].height != b->tiles[p->cell + 512 * 512].height ||
                b->tiles[to].height != b->tiles[from].height)
                continue;
            start = from;
            goal = to;
            target = p->cell;
            for (uint32_t c2 = a; c2 <= c; c2 += stride)
                if (b->bridge_parts[b->bridge_at[c2] - 1].original_frame == 255) ++missing;
        }
    }
    CHECK(target);
    for (uint32_t i = 0; i < b->bridge_count; ++i)
        if (b->bridge_parts[i].frame == 255) ++total_missing;
    b->count = 0;
    memset(b->units, 0, RA_BATTLE_UNITS * sizeof(*b->units));
    memset(b->initial, 0, RA_BATTLE_UNITS * sizeof(*b->initial));
    memset(b->occupied, 0, 2 * 512 * 512 * sizeof(*b->occupied));
    CHECK(ra_battle_spawn_team(b, 0, 1, start % 512, start / 512, &e));
    CHECK(ra_battle_bridge_event_add(b, 60, RA_EVENT_BRIDGE_REPAIR, target, &e));
    CHECK(ra_battle_command_add(b, 61, 1, goal, &e));
    bool crossed = false;
    for (unsigned tick = 0; tick < 600; ++tick)
    {
        ra_battle_step(b);
        ra_battle_hash(b, states[tick]);
        const ra_battle_unit *u = &b->units[0];
        uint32_t id = b->bridge_at[u->cell % (512 * 512)];
        if (id && u->cell >= 512 * 512 && b->bridge_parts[id - 1].original_frame == 255) crossed = true;
        CHECK(u->health && b->occupied[u->cell] == u->id);
    }
    CHECK(crossed && b->units[0].cell == goal && b->bridge_repaired == 9 && missing == 7);
    CHECK(ra_battle_replay_write(b, &bytes, &size, &e) && battle_file_write(argv[1], bytes, size, &e));
    uint32_t end = 0;
    CHECK(ra_battle_replay_read(b, (ra_view){bytes, size}, &end, expected, &e) && end == 600);
    for (unsigned tick = 0; tick < end; ++tick)
    {
        ra_battle_step(b);
        ra_battle_hash(b, digest);
        CHECK(!memcmp(digest, states[tick], 20));
    }
    CHECK(!memcmp(digest, expected, 20));
    char hex[41];
    ra_hex(digest, 20, hex);
    printf("{\"checks\":%u,\"failures\":%u,\"map\":\"MP09DU.map\",\"total_missing_segments\":%u,\"missing_segments\":%u,\"repaired_segments\":%u,\"crossed_"
           "original_gap\":true,\"paired_"
           "steps\":600,\"sha1\":\"%s\"}\n",
           checks, failures, total_missing, missing, b->bridge_repaired, hex);
    result = 0;
done:
    if (result) fprintf(stderr, "%s\n", e.message);
    free(bytes);
    if (s)
    {
        battle_scene_close(s);
        free(s);
    }
    return result;
}
#include "entry.h"
