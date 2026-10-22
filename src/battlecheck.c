#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

static int app_main(int argc, char **argv)
{
    battle_scene scene = {0};
    ra_error e = {0};
    const char *original = "H:/开发/运行版本/原版1.006", *replay = NULL, *output = NULL, *name = "MP05MW.map";
    bool corpus = false, combat = false, missions = false, trace = false, layers = false, bridge_life = false, bridge_repair = false;
    int result = 1;
    size_t maps = 0, cells = 0, missing = 0;
    uint32_t goal = 0, bridge_cell = 0, end = 360, requested_steps = 0;
    uint8_t expected[20], digest[20], chain[40] = {0};
    char hex[41], trace_hex[41];
    for (int i = 1; i < argc; ++i)
    {
        if (i + 1 < argc && !strcmp(argv[i], "--original")) original = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--replay")) replay = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--output")) output = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--map")) name = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--steps"))
        {
            char *tail;
            unsigned long value = strtoul(argv[++i], &tail, 10);
            if (!*argv[i] || *tail || !value || value > 10000000) return 2;
            requested_steps = (uint32_t)value;
        }
        else if (!strcmp(argv[i], "--corpus")) corpus = true;
        else if (!strcmp(argv[i], "--combat")) combat = true;
        else if (!strcmp(argv[i], "--missions")) missions = trace = true;
        else if (!strcmp(argv[i], "--trace")) trace = true;
        else if (!strcmp(argv[i], "--bridge-repair")) bridge_repair = trace = true;
        else if (!strcmp(argv[i], "--bridge-life")) bridge_life = trace = true;
        else if (!strcmp(argv[i], "--layers")) layers = trace = true;
        else return 2;
    }
    if (!battle_scene_open(&scene, original, &e)) goto done;
    if (corpus)
    {
        puts("{\"navigation\":[");
        for (size_t i = 0; i < scene.maps.source_count; ++i)
        {
            size_t passable = 0, water = 0, coast = 0, cliffs = 0, decks = 0;
            if (!battle_scene_map(&scene, i, false, &e)) goto done;
            for (uint32_t j = 0; j < 512 * 512; ++j)
            {
                if (ra_battle_passable(&scene.battle, j)) ++passable;
                if (ra_battle_passable(&scene.battle, j + 512 * 512)) ++decks;
                if (scene.battle.tiles[j].land == 2) ++water;
                if (scene.battle.tiles[j].land == 6) ++coast;
                if (scene.battle.tiles[j].land == 3) ++cliffs;
                if ((scene.battle.tiles[j].land == 2 || scene.battle.tiles[j].land == 6 || scene.battle.tiles[j].land == 3) &&
                    ra_battle_passable(&scene.battle, j))
                {
                    ra_fail(&e, RA_FORMAT, 0, "water, beach or cliff was incorrectly walkable");
                    goto done;
                }
            }
            printf("%s{\"name\":\"%s\",\"theater\":\"%s\",\"cells\":%zu,\"passable\":%zu,\"missing\":%zu,\"bridges\":%zu,\"obstacles\":%zu,\"unknown_"
                   "foundation\":%zu,\"water\":%zu,\"coast\":%zu,\"cliffs\":%zu",
                   maps ? ",\n" : "", scene.maps.sources[i].name, scene.map.theater, scene.map.cell_count, passable, scene.missing, scene.bridges,
                   scene.obstacles, scene.unsupported_foundations, water, coast, cliffs);
            uint32_t missing_spans = 0, damaged_parts = 0;
            for (uint32_t part = 0; part < scene.battle.bridge_count; ++part)
            {
                const ra_battle_bridge *p = &scene.battle.bridge_parts[part];
                if (p->frame == 255) ++missing_spans;
                if (p->kind < 2 ? p->frame != (p->axis == 1 ? 0u : 9u)
                                : (p->frame >= 5 && p->frame <= 9) || (p->frame >= 14 && p->frame <= 18) || p->frame >= 27)
                    ++damaged_parts;
            }
            printf(",\"bridge_parts\":%u,\"missing_spans\":%u,\"damaged_parts\":%u", scene.battle.bridge_count, missing_spans, damaged_parts);
            printf(",\"decks\":%zu,\"low_bridges\":%zu,\"pending_bridges\":%zu", decks, scene.low_bridges, scene.pending_bridges);
            putchar('}');
            ++maps;
            cells += scene.map.cell_count;
            missing += scene.missing;
        }
        printf("],\"maps\":%zu,\"cells\":%zu,\"missing\":%zu,\"active_factions\":2,\"china_enabled\":false}\n", maps, cells, missing);
        result = 0;
        goto done;
    }
    for (size_t i = 0; i < scene.maps.source_count; ++i)
        if (ra_equal(scene.maps.sources[i].name, name))
        {
            if (!battle_scene_map(&scene, i, false, &e)) goto done;
            break;
        }
    if (!scene.battle.tiles)
    {
        ra_fail(&e, RA_NOT_FOUND, 0, "map not found");
        goto done;
    }
    if (bridge_life && !battle_scene_bridge_lifecycle_fixture(&scene, &bridge_cell, &goal, &e)) goto done;
    if (layers && !battle_scene_bridge_fixture(&scene, &goal, &e)) goto done;
    if (bridge_repair)
    {
        for (uint32_t i = 0; i < scene.battle.bridge_count; ++i)
            if (scene.battle.bridge_parts[i].frame == 255 || (scene.battle.bridge_parts[i].kind >= 2 && scene.battle.bridge_parts[i].frame >= 27))
            {
                bridge_cell = scene.battle.bridge_parts[i].cell;
                break;
            }
        if (!bridge_cell)
        {
            ra_fail(&e, RA_NOT_FOUND, 0, "map has no registered missing bridge segment");
            goto done;
        }
    }
    if (replay)
    {
        ra_file file = {0};
        bool ok = ra_file_open(&file, replay, &e) && ra_battle_replay_read(&scene.battle, file.view, &end, expected, &e);
        ra_file_close(&file);
        if (!ok) goto done;
    }
    else if (bridge_repair)
    {
        end = 360;
        if (!ra_battle_bridge_event_add(&scene.battle, 60, RA_EVENT_BRIDGE_REPAIR, bridge_cell, &e)) goto done;
    }
    else if (bridge_life)
    {
        end = 900;
        if (!ra_battle_command_add(&scene.battle, 1, 1, goal, &e) || !ra_battle_bridge_event_add(&scene.battle, 5, RA_EVENT_BRIDGE_HIT, bridge_cell, &e) ||
            !ra_battle_bridge_event_add(&scene.battle, 12, RA_EVENT_BRIDGE_HIT, bridge_cell, &e) ||
            !ra_battle_bridge_event_add(&scene.battle, 120, RA_EVENT_BRIDGE_REPAIR, bridge_cell, &e) || !ra_battle_command_add(&scene.battle, 121, 1, goal, &e))
            goto done;
    }
    else if (layers)
    {
        end = 900;
        if (!ra_battle_command_add(&scene.battle, 1, 1, goal, &e)) goto done;
    }
    else if (missions)
    {
        uint32_t points[3];
        end = 900;
        if (!battle_scene_goal(&scene, 1, 5, &points[0]) || !battle_scene_goal(&scene, 1, 3, &points[1]) || !battle_scene_goal(&scene, 2, 6, &points[2]) ||
            !ra_battle_order_add(&scene.battle, 1, 1, RA_ORDER_FORCE_GROUND, points[0], &e) ||
            !ra_battle_order_add(&scene.battle, 80, 1, RA_ORDER_GUARD, 0, &e) || !ra_battle_order_add(&scene.battle, 120, 1, RA_ORDER_SCATTER, 0, &e) ||
            !ra_battle_order_add(&scene.battle, 180, 2, RA_ORDER_ATTACK_MOVE, scene.battle.units[2].cell, &e) ||
            !ra_battle_waypoints_add(&scene.battle, 360, 1, points, 3, 0, &e))
            goto done;
    }
    else if (combat)
    {
        end = 900;
        if (!ra_battle_attack_add(&scene.battle, 1, 2, 3, &e)) goto done;
    }
    else
    {
        if (!battle_scene_goal(&scene, 1, 8, &goal) || !ra_battle_command_add(&scene.battle, 1, 1, goal, &e)) goto done;
        if (!battle_scene_goal(&scene, 2, 6, &goal) || !ra_battle_command_add(&scene.battle, 40, 2, goal, &e)) goto done;
        if (!battle_scene_goal(&scene, 3, 4, &goal) || !ra_battle_command_add(&scene.battle, 80, 3, goal, &e)) goto done;
    }
    if (requested_steps)
    {
        if ((replay && requested_steps != end) || (scene.battle.command_count && requested_steps < scene.battle.commands[scene.battle.command_count - 1].tick))
        {
            ra_fail(&e, RA_ARGUMENT, 0, "step limit differs from replay or precedes a pending command");
            goto done;
        }
        end = requested_steps;
    }
    /* 选测试目的地会使用寻路工作区，生成命令后恢复初始现场，避免把夹具查询写进逐步摘要。 */
    ra_battle_reset(&scene.battle);
    while (scene.battle.tick < end)
    {
        ra_battle_step(&scene.battle);
        if (trace)
        {
            ra_battle_hash(&scene.battle, chain + 20);
            ra_sha1((ra_view){chain, sizeof(chain)}, digest);
            memcpy(chain, digest, 20);
        }
    }
    ra_hex(chain, 20, trace_hex);
    ra_battle_hash(&scene.battle, digest);
    ra_hex(digest, 20, hex);
    if (replay && memcmp(digest, expected, 20))
    {
        ra_fail(&e, RA_FORMAT, 0, "replayed state checksum mismatch");
        goto done;
    }
    if (output)
    {
        uint8_t *bytes = NULL;
        size_t size = 0;
        bool ok = ra_battle_replay_write(&scene.battle, &bytes, &size, &e) && battle_file_write(output, bytes, size, &e);
        free(bytes);
        if (!ok) goto done;
    }
    printf("{\"map\":\"%s\",\"tick\":%u,\"commands\":%u,\"sha1\":\"%s\",\"replay_verified\":%s,\"fired\":%u,\"impacts\":%u,\"kills\":%u,\"dropped_shots\":%u,"
           "\"simulation_version\":%u,\"trace_enabled\":%s,\"trace_sha1\":\"%s\"",
           name, scene.battle.tick, scene.battle.command_count, hex, replay ? "true" : "false", scene.battle.fired, scene.battle.impacts, scene.battle.kills,
           scene.battle.dropped_shots, RA_BATTLE_VERSION, trace ? "true" : "false", trace_hex);
    printf(",\"bridge_parts\":%u,\"bridge_hits\":%u,\"destroyed_segments\":%u,\"repaired_segments\":%u,\"bridge_falls\":%u,\"units\":[",
           scene.battle.bridge_count, scene.battle.bridge_hits, scene.battle.bridge_destroyed, scene.battle.bridge_repaired, scene.battle.bridge_falls);
    for (uint32_t i = 0; i < scene.battle.count; ++i)
    {
        const ra_battle_unit *u = &scene.battle.units[i];
        printf("%s{\"id\":%u,\"type\":\"%s\",\"cell\":%u,\"goal\":%u,\"x\":%d,\"y\":%d,\"team\":%u,\"health\":%u,\"shots\":%u,\"kills\":%u}", i ? "," : "",
               u->id, scene.battle.types[u->type].id, u->cell, u->goal, u->x, u->y, u->team, u->health, u->shots, u->kills);
    }
    puts("]}");
    result = 0;
done:
    if (result) fprintf(stderr, "%s: %s\n", ra_status_name(e.code), e.message);
    battle_scene_close(&scene);
    return result;
}
#include "entry.h"
