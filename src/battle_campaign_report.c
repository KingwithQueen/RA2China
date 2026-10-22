#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

typedef struct
{
    char *bytes;
    size_t used, capacity;
    bool failed;
} report_buffer;
static void add(report_buffer *r, const char *format, ...)
{
    if (r->failed) return;
    va_list args;
    va_start(args, format);
    int n = vsnprintf(r->bytes + r->used, r->capacity - r->used, format, args);
    va_end(args);
    if (n < 0 || (size_t)n >= r->capacity - r->used) r->failed = true;
    else r->used += (size_t)n;
}
static void string(report_buffer *r, const char *text)
{
    add(r, "\"");
    for (; *text; ++text)
    {
        unsigned ch = (uint8_t)*text;
        if (ch == '"' || ch == '\\') add(r, "\\%c", ch);
        else if (ch < 32) add(r, "\\u%04x", ch);
        else add(r, "%c", ch);
    }
    add(r, "\"");
}
bool battle_scene_campaign_report(const battle_scene *scene, const char *path, ra_error *error)
{
    const ra_battle *b = &scene->battle;
    const ra_battle_campaign *c = b->campaign;
    if (!c) return ra_fail(error, RA_ARGUMENT, 0, "campaign report needs campaign scene");
    report_buffer r = {0};
    r.capacity = 1048576;
    r.bytes = malloc(r.capacity);
    if (!r.bytes) return ra_fail(error, RA_MEMORY, 0, "campaign report allocation failed");
    uint8_t source_digest[20];
    char map_hex[41];
    ra_sha1(scene->maps.sources[scene->source].bytes, source_digest);
    ra_hex(source_digest, 20, map_hex);
    add(&r, "{\"map_sha1\":\"%s\",\"map\":", map_hex);
    string(&r, scene->maps.sources[scene->source].name);
    add(&r, ",\"simulation\":%u,\"ticks\":%u,\"objects\":%u,\"infantry\":", RA_BATTLE_VERSION, b->tick, b->count);
    uint32_t infantry = 0;
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->types[b->units[i].type].infantry) ++infantry;
    add(&r,
        "%u,\"triggers\":%u,\"teams\":%u,\"cell_tags\":%u,\"fired\":%u,\"outcome\":%u,\"rejected_actions\":%u,\"rejected_teams\":%u,\"script_gaps\":%u,"
        "\"missing_objects\":[",
        infantry, c->trigger_count, c->team_count, c->cell_count, c->state.fired, c->state.outcome, c->state.rejected_actions, c->state.rejected_teams,
        c->state.script_gaps);
    for (size_t i = 0; i < scene->issue_count; ++i)
    {
        if (i) add(&r, ",");
        add(&r, "{\"line\":%zu,\"type\":", scene->issues[i].line);
        string(&r, scene->issues[i].type);
        add(&r, ",\"reason\":");
        string(&r, scene->issues[i].reason);
        add(&r, "}");
    }
    add(&r, "],\"unsupported_event_kinds\":[");
    bool comma = false;
    for (uint32_t i = 0; i < 128; ++i)
        if (c->unsupported_events[i])
        {
            add(&r, "%s{\"kind\":%u,\"count\":%u}", comma ? "," : "", i, c->unsupported_events[i]);
            comma = true;
        }
    add(&r, "],\"unsupported_action_kinds\":[");
    comma = false;
    for (uint32_t i = 0; i < 160; ++i)
        if (c->unsupported_actions[i])
        {
            add(&r, "%s{\"kind\":%u,\"count\":%u}", comma ? "," : "", i, c->unsupported_actions[i]);
            comma = true;
        }
    add(&r, "],\"unsupported_script_kinds\":[");
    comma = false;
    for (uint32_t i = 0; i < 128; ++i)
        if (c->unsupported_scripts[i])
        {
            add(&r, "%s{\"kind\":%u,\"count\":%u}", comma ? "," : "", i, c->unsupported_scripts[i]);
            comma = true;
        }
    add(&r, "],\"teams_with_unimplemented_types\":[");
    comma = false;
    for (uint32_t i = 0; i < c->team_count; ++i)
    {
        const ra_campaign_team *t = &c->teams[i];
        bool missing = false;
        for (uint32_t j = 0; j < t->member_count; ++j)
            if (t->types[j] == UINT32_MAX) missing = true;
        if (!missing) continue;
        add(&r, "%s{\"id\":", comma ? "," : "");
        string(&r, t->id);
        comma = true;
        const ra_ini_entry *task = ra_ini_get(&scene->map.ini, t->id, "TaskForce");
        add(&r, ",\"taskforce\":");
        string(&r, task ? task->value : "");
        add(&r, ",\"missing_members\":[");
        bool member_comma = false;
        for (uint32_t j = 0; j < t->member_count; ++j)
            if (t->types[j] == UINT32_MAX)
            {
                char key[16];
                snprintf(key, sizeof(key), "%u", j);
                const ra_ini_entry *member = task ? ra_ini_get(&scene->map.ini, task->value, key) : NULL;
                add(&r, "%s", member_comma ? "," : "");
                string(&r, member ? member->value : "missing");
                member_comma = true;
            }
        add(&r, "]}");
    }
    add(&r, "],\"type_ids\":[");
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        if (i) add(&r, ",");
        string(&r, b->types[i].id);
    }
    add(&r, "],\"initial_objects\":%u,\"partial_action_kinds\":[3,74],\"partial_script_kinds\":[5,19],\"trigger_status\":[", b->initial_count);
    for (uint32_t i = 0; i < c->trigger_count; ++i)
    {
        const ra_campaign_trigger *t = &c->triggers[i];
        if (i) add(&r, ",");
        add(&r, "{\"id\":");
        string(&r, t->id);
        add(&r, ",\"name\":");
        string(&r, t->name);
        add(&r, ",\"fired\":%u,\"enabled\":%s,\"events\":[", c->state.triggers[i].fired, c->state.triggers[i].enabled ? "true" : "false");
        for (uint32_t j = 0; j < t->event_count; ++j) add(&r, "%s{\"kind\":%u,\"argument\":%d}", j ? "," : "", t->events[j].kind, t->events[j].argument);
        add(&r, "],\"unsupported_events\":[");
        comma = false;
        for (uint32_t j = 0; j < t->event_count; ++j)
            if (!ra_campaign_event_supported(t->events[j].kind))
            {
                add(&r, "%s%u", comma ? "," : "", t->events[j].kind);
                comma = true;
            }
        add(&r, "],\"unsupported_actions\":[");
        comma = false;
        for (uint32_t j = 0; j < t->action_count; ++j)
            if (!ra_campaign_action_supported(t->actions[j].kind))
            {
                add(&r, "%s%u", comma ? "," : "", t->actions[j].kind);
                comma = true;
            }
        add(&r, "]}");
    }
    add(&r, "],\"economy\":{\"credits\":%llu,\"earned\":%llu,\"spent\":%llu,\"produced\":%u,\"built\":%u},\"object_states\":[",
        (unsigned long long)b->economy->state.houses[0].credits, (unsigned long long)b->economy->state.houses[0].earned,
        (unsigned long long)b->economy->state.houses[0].spent, b->economy->state.houses[0].produced, b->economy->state.houses[0].built);

    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        add(&r, "%s{\"id\":%u,\"type\":", i ? "," : "", u->id);
        string(&r, b->types[u->type].id);
        add(&r,
            ",\"team\":%u,\"health\":%u,\"cell\":[%u,%u],\"goal\":[%u,%u],\"order\":%u,\"target\":%u,\"shots\":%u,\"carrier\":%u,\"script_team\":%u,\"traits\":"
            "%u,\"killer\":%u}",
            u->team, u->health, u->cell % b->width, ra_battle_cell_y(b, u->cell), u->goal % b->width, ra_battle_cell_y(b, u->goal), u->order, u->target,
            u->shots, u->carrier, u->script_team, u->traits, u->killer);
    }
    add(&r, "],\"complete_original_mission\":false,\"original_runtime_calibration\":false,\"china_enabled\":false}\n");
    bool ok = !r.failed && battle_file_write(path, r.bytes, r.used, error);
    free(r.bytes);
    return ok || ra_fail(error, RA_RANGE, 0, "campaign report failed or exceeded capacity");
}
