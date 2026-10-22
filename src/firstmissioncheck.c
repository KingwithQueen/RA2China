#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>

static battle_scene scene;
static uint32_t find(const ra_battle *b, const char *type, uint32_t team)
{
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && (!team || b->units[i].team == team) && ra_equal(b->types[b->units[i].type].id, type)) return i + 1;
    return 0;
}
static uint32_t fired(const ra_battle *b, const char *id)
{
    for (uint32_t i = 0; i < b->campaign->trigger_count; ++i)
        if (ra_equal(b->campaign->triggers[i].id, id)) return b->campaign->state.triggers[i].fired;
    return 0;
}
static bool order(ra_battle *b, uint32_t id, ra_battle_order kind, uint32_t target)
{
    ra_error error = {0};
    if (!id || id > b->count || !b->units[id - 1].health || b->units[id - 1].team != 1) return false;
    if (!ra_battle_order_add(b, b->tick + 1, id, kind, target, &error))
    {
        fprintf(stderr, "command %u/%u/%u rejected: %s\n", id, kind, target, error.message);
        return false;
    }
    return true;
}
static bool building(ra_battle *b, const char *name)
{
    if (find(b, name, 1)) return true;
    uint32_t type = ra_economy_type(b, name), yard = find(b, "GACNST", 1);
    if (type == UINT32_MAX || !yard) return false;
    ra_econ_queue *q = &b->economy->state.houses[0].queues[0];
    ra_error error = {0};
    if (!q->count && ra_economy_available(b, 1, type)) ra_economy_command(b, b->tick + 1, 1, RA_ECON_QUEUE, type, &error);
    if (!q->count || q->types[0] != type || q->progress != b->economy->types[type].ticks * 1000) return false;
    int cx = (int)(b->units[yard - 1].cell % b->width), cy = (int)ra_battle_cell_y(b, b->units[yard - 1].cell);
    for (int radius = 0; radius < 18; ++radius)
        for (int y = cy - radius; y <= cy + radius; ++y)
            for (int x = cx - radius; x <= cx + radius; ++x)
            {
                if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
                uint32_t cell = (uint32_t)y * b->width + (uint32_t)x;
                if (ra_economy_placeable(b, 1, type, cell))
                {
                    ra_economy_command(b, b->tick + 1, 1, RA_ECON_PLACE, cell * RA_BATTLE_TYPES + type, &error);
                    return false;
                }
            }
    return false;
}
static void mining(ra_battle *b)
{
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!u->health || u->team != 1 || !b->economy->types[u->type].harvester || b->economy->state.miners[i].active) continue;
        uint32_t best = UINT32_MAX;
        uint64_t score = UINT64_MAX;
        for (uint32_t cell = 0; cell < b->width * b->height; ++cell)
        {
            if (!(b->economy->ore[cell] & 63) || !battle_cell_available(b, cell, u->id)) continue;
            int64_t dx = (int64_t)(cell % b->width) * RA_BATTLE_CELL - u->x, dy = (int64_t)(cell / b->width) * RA_BATTLE_CELL - u->y;
            uint64_t distance = (uint64_t)(dx * dx + dy * dy);
            if (distance < score)
            {
                score = distance;
                best = cell;
            }
        }
        if (best != UINT32_MAX)
        {
            ra_error error = {0};
            ra_economy_command(b, b->tick + 1, u->id, RA_ECON_HARVEST, best, &error);
        }
    }
}
/* 这是测试玩家，只提交正常命令；不修改生命、对象、变量、触发开关或胜负。 */
static void player(ra_battle *b, uint32_t *phase)
{
    if (b->campaign->state.input_locked || b->campaign->state.outcome || b->tick % 15) return;
    uint32_t tanya = find(b, "TANY", 1);
    if (!tanya) return;
    ra_battle_unit *u = &b->units[tanya - 1];
    if (*phase >= 4) mining(b);
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *enemy = &b->units[i];
        if (!b->types[enemy->type].infantry || !ra_battle_targetable(b, u, enemy, false, false) ||
            battle_distance_squared(u, enemy) > (uint64_t)(*phase >= 4 ? 6u : 8u) * RA_BATTLE_CELL * (*phase >= 4 ? 6u : 8u) * RA_BATTLE_CELL)
            continue;
        if (u->order != RA_ORDER_ATTACK || u->target != enemy->id) order(b, tanya, RA_ORDER_ATTACK, enemy->id);
        return;
    }
    if (*phase >= 4)
    {
        uint32_t refuge = 35 * b->width + 82;
        if (u->destination != refuge || u->order != RA_ORDER_MOVE) order(b, tanya, RA_ORDER_MOVE, refuge);
    }
    if (*phase == 0)
    {
        uint32_t ship = find(b, "DRED", 0);
        if (ship)
        {
            if (!b->units[ship - 1].c4_owner && (u->order != RA_ORDER_ENTER || u->target != ship)) order(b, tanya, RA_ORDER_ENTER, ship);
            return;
        }
        *phase = 1;
    }
    if (*phase == 1)
    {
        if (!fired(b, "07BA8C2C"))
        {
            uint32_t cell = 84 * b->width + 62;
            if (u->destination != cell || u->order != RA_ORDER_MOVE) order(b, tanya, RA_ORDER_MOVE, cell);
            return;
        }
        *phase = 2;
    }
    if (*phase == 2)
    {
        if (!fired(b, "0B3E99EC"))
        {
            uint32_t cell = 77 * b->width + 62;
            if (u->destination != cell || u->order != RA_ORDER_GUARD)
            {
                if (u->cell == cell) order(b, tanya, RA_ORDER_GUARD, 0);
                else if (u->destination != cell) order(b, tanya, RA_ORDER_MOVE, cell);
            }
            return;
        }
        *phase = 3;
    }
    if (*phase == 3)
    {
        if (!fired(b, "0965E07C"))
        {
            uint32_t cell = 38 * b->width + 74;
            if (u->destination != cell || u->order != RA_ORDER_MOVE) order(b, tanya, RA_ORDER_MOVE, cell);
            return;
        }
        *phase = 4;
    }
    if (*phase == 4 && !building(b, "GAPILE")) return;
    if (*phase == 4)
    {
        if (!b->bridge_repaired)
        {
            uint32_t engineer = find(b, "ENGINEER", 1), type = ra_economy_type(b, "ENGINEER");
            if (!engineer && !b->economy->state.houses[0].queues[2].count && ra_economy_available(b, 1, type))
            {
                ra_error error = {0};
                ra_economy_command(b, b->tick + 1, 1, RA_ECON_QUEUE, type, &error);
            }
            if (engineer)
            {
                uint32_t hut = find(b, "CABHUT", 0);
                if (hut && (b->units[engineer - 1].order != RA_ORDER_ENTER || b->units[engineer - 1].target != hut)) order(b, engineer, RA_ORDER_ENTER, hut);
            }
            return;
        }
        *phase = 5;
    }
    if (*phase >= 5)
    {
        uint32_t army = 0, ready = 0, first = 0, type = ra_economy_type(b, "E1");
        for (uint32_t i = b->initial_count; i < b->count; ++i)
            if (b->units[i].health && b->units[i].team == 1 && b->units[i].type == type)
            {
                ++army;
                if (!first) first = i + 1;
                if (*phase == 5)
                {
                    uint32_t cell = (40 + army / 5) * b->width + 75 + army % 5;
                    if (!battle_cell_available(b, cell, i + 1))
                        for (uint32_t offset = 1; offset < 20; ++offset)
                            if (battle_cell_available(b, cell + offset, i + 1))
                            {
                                cell += offset;
                                break;
                            }
                    if (b->units[i].destination != cell) order(b, i + 1, RA_ORDER_MOVE, cell);
                    ra_battle_unit rally = {0};
                    rally.x = 78 * (int32_t)RA_BATTLE_CELL;
                    rally.y = 43 * (int32_t)RA_BATTLE_CELL;
                    if (battle_distance_squared(&rally, &b->units[i]) <= (uint64_t)6 * RA_BATTLE_CELL * 6 * RA_BATTLE_CELL) ++ready;
                }
            }
        if (army + b->economy->state.houses[0].queues[2].count < 24 && ra_economy_available(b, 1, type))
        {
            ra_error error = {0};
            ra_economy_command(b, b->tick + 1, 1, RA_ECON_QUEUE, type, &error);
        }
        if (*phase == 5 && ready < 24) return;
        *phase = 6;
        if (!first) return;
        uint32_t enemy_house = ra_campaign_house(b, "BadGuy1");
        for (uint32_t i = b->initial_count; i < b->count; ++i)
        {
            ra_battle_unit *soldier = &b->units[i];
            if (!soldier->health || soldier->team != 1 || soldier->type != type) continue;
            uint32_t target = 0;
            uint64_t best = UINT64_MAX, range = b->types[type].weapon.range;
            for (uint32_t j = 0; j < b->count; ++j)
            {
                const ra_battle_unit *enemy = &b->units[j];
                if (!b->types[enemy->type].infantry || !ra_battle_targetable(b, soldier, enemy, false, false)) continue;
                uint64_t distance = battle_distance_squared(soldier, enemy);
                if (distance <= range * range && distance < best)
                {
                    best = distance;
                    target = enemy->id;
                }
            }
            for (uint32_t j = 0; j < b->count; ++j)
            {
                const ra_battle_unit *defense = &b->units[j];
                if (defense->health && defense->team == enemy_house && b->types[defense->type].structure && b->types[defense->type].weapon.damage &&
                    battle_distance_squared(soldier, defense) <= range * range)
                {
                    target = defense->id;
                    break;
                }
            }
            if (!target)
                for (uint32_t j = 0; j < b->count; ++j)
                {
                    const ra_battle_unit *enemy = &b->units[j];
                    if (!enemy->health || enemy->team != enemy_house || !b->types[enemy->type].structure || b->types[enemy->type].insignificant ||
                        !ra_battle_targetable(b, soldier, enemy, false, false))
                        continue;
                    uint64_t distance = battle_distance_squared(soldier, enemy);
                    if (b->types[enemy->type].weapon.damage) distance /= 64;
                    if (distance < best)
                    {
                        best = distance;
                        target = enemy->id;
                    }
                }
            if (target && (soldier->order != RA_ORDER_ATTACK || soldier->target != target)) order(b, i + 1, RA_ORDER_ATTACK, target);
        }
    }
}
static int run(int argc, char **argv)
{
    if (argc < 3) return 2;
    bool probe = argc > 3 && !strcmp(argv[3], "--probe");
    ra_error error = {0};
    scene.scenario = scene.campaign_mode = true;
    if (!battle_scene_open(&scene, argv[1], &error)) goto fail;
    size_t map;
    for (map = 0; map < scene.maps.source_count; ++map)
        if (ra_equal(scene.maps.sources[map].name, "all01t.map")) break;
    if (map == scene.maps.source_count || !battle_scene_map(&scene, map, false, &error)) goto fail;
    ra_battle *b = &scene.battle;
    uint32_t limit = argc > 4 ? (uint32_t)strtoul(argv[4], NULL, 10) : 30000, phase = 0, paired = 0, mismatches = 0;
    uint8_t *trace = probe ? NULL : calloc(limit, 20), *bytes = NULL, digest[20], expected[20];
    if (!limit || limit > 30000 || (!probe && !trace)) goto fail;
    fprintf(stderr, "all01t initial=%u missing=%zu\n", b->count, scene.issue_count);
    while (b->tick < limit && !b->campaign->state.outcome)
    {
        player(b, &phase);
        ra_battle_step(b);
        if (trace) ra_battle_hash(b, trace + (size_t)(b->tick - 1) * 20);
        if (b->tick % 600 == 0)
        {
            uint32_t id = find(b, "TANY", 1);
            ra_battle_unit *u = id ? &b->units[id - 1] : NULL;
            fprintf(stderr, "tick=%u phase=%u objects=%u Tanya=%u cell=%u,%u order=%u target=%u fired=%u gaps=%u\n", b->tick, phase, b->count,
                    u ? u->health : 0, u ? u->cell % b->width : 0, u ? u->cell / b->width : 0, u ? u->order : 0, u ? u->target : 0, b->campaign->state.fired,
                    b->campaign->state.script_gaps);
            fflush(stderr);
        }
    }
    uint32_t ticks = b->tick, outcome = b->campaign->state.outcome, repaired = b->bridge_repaired;
    uint32_t milestones[6] = {fired(b, "07B92F3C"), fired(b, "07BA8C2C"), fired(b, "0B3E99EC"),
                              fired(b, "0965E07C"), fired(b, "07506C5C"), fired(b, "075F22EC")};
    char path[32768];
    snprintf(path, sizeof(path), "%s/campaign.json", argv[2]);
    if (!battle_scene_campaign_report(&scene, path, &error)) goto fail_trace;
    ra_battle_hash(b, digest);
    if (!probe)
    {
        size_t size = 0;
        uint32_t end = 0;
        if (!ra_battle_replay_write(b, &bytes, &size, &error)) goto fail_trace;
        snprintf(path, sizeof(path), "%s/first-mission.rpl", argv[2]);
        if (!battle_file_write(path, bytes, size, &error) || !ra_battle_replay_read(b, (ra_view){bytes, size}, &end, expected, &error)) goto fail_trace;
        for (uint32_t i = 0; i < end; ++i)
        {
            ra_battle_step(b);
            ra_battle_hash(b, digest);
            if (memcmp(digest, trace + (size_t)i * 20, 20))
            {
                ++mismatches;
                break;
            }
            ++paired;
        }
        if (memcmp(digest, expected, 20)) ++mismatches;
    }
    char hex[41], report[2048];
    ra_hex(digest, 20, hex);
    int n = snprintf(report, sizeof(report),
                     "{\"simulation\":%u,\"ticks\":%u,\"outcome\":%u,\"phase\":%u,\"paired_steps\":%u,\"mismatches\":%u,\"state_sha1\":\"%s\","
                     "\"milestones\":[%u,%u,%u,%u,%u,%u],\"repaired_bridge_cells\":%u,\"original_runtime_calibration\":false}\n",
                     RA_BATTLE_VERSION, ticks, outcome, phase, paired, mismatches, hex, milestones[0], milestones[1], milestones[2], milestones[3],
                     milestones[4], milestones[5], repaired);
    snprintf(path, sizeof(path), "%s/first-mission.json", argv[2]);
    bool saved = n > 0 && (size_t)n < sizeof(report) && battle_file_write(path, report, (size_t)n, &error);
    printf("%s", report);
    free(trace);
    free(bytes);
    battle_scene_close(&scene);
    return saved && outcome == 1 && !mismatches ? 0 : 1;
fail_trace:
    free(trace);
    free(bytes);
fail:
    fprintf(stderr, "first mission check failed: %s\n", error.message);
    battle_scene_close(&scene);
    return 1;
}
#define app_main run
#include "entry.h"
