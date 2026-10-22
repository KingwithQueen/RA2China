#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>
static battle_scene scene;
static int run(int argc, char **argv)
{
    if (argc < 4) return 2;
    ra_error error = {0};
    scene.scenario = scene.campaign_mode = true;
    uint32_t ticks = argc > 4 ? (uint32_t)strtoul(argv[4], NULL, 10) : 900;
    if (!ticks || ticks > 10000) return 2;
    if (!battle_scene_open(&scene, argv[1], &error)) goto fail;
    size_t map;
    for (map = 0; map < scene.maps.source_count; ++map)
        if (ra_equal(scene.maps.sources[map].name, argv[2])) break;
    if (map == scene.maps.source_count || !battle_scene_map(&scene, map, false, &error)) goto fail;
    fprintf(stderr, "loaded %s: %u objects, %zu pending, %u triggers\n", argv[2], scene.battle.count, scene.issue_count, scene.battle.campaign->trigger_count);
    uint8_t (*trace)[20] = calloc(ticks, 20), expected[20], actual[20], *replay = NULL;
    size_t size = 0;
    uint32_t end = 0, failures = 0;
    if (!trace) goto fail;
    for (uint32_t i = 0; i < ticks; ++i)
    {
        ra_battle_step(&scene.battle);
        ra_battle_hash(&scene.battle, trace[i]);
        if (!(i % 300))
        {
            fprintf(stderr, "step %u\n", i + 1);
            fflush(stderr);
        }
    }
    if (!battle_scene_campaign_report(&scene, argv[3], &error) || !ra_battle_replay_write(&scene.battle, &replay, &size, &error) ||
        !ra_battle_replay_read(&scene.battle, (ra_view){replay, size}, &end, expected, &error))
    {
        free(trace);
        free(replay);
        goto fail;
    }
    for (uint32_t i = 0; i < end; ++i)
    {
        ra_battle_step(&scene.battle);
        ra_battle_hash(&scene.battle, actual);
        if (memcmp(actual, trace[i], 20))
        {
            ++failures;
            fprintf(stderr, "state mismatch at %u\n", i + 1);
            break;
        }
    }
    if (memcmp(actual, expected, 20)) ++failures;
    char hex[41];
    ra_hex(actual, 20, hex);
    printf("{\"paired_steps\":%u,\"failures\":%u,\"state_sha1\":\"%s\",\"complete_original_mission\":false}\n", end, failures, hex);
    free(trace);
    free(replay);
    battle_scene_close(&scene);
    return failures ? 1 : 0;
fail:
    fprintf(stderr, "campaign load/check failed: %s (line %zu)\n", error.message, error.line);
    battle_scene_close(&scene);
    return 1;
}
#define app_main run
#include "entry.h"
