#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* 有界 CSV，不以 atoi 的静默回退处理损坏任务。动作记录固定为八个字段。 */
static uint32_t csv(char *text, char **out, uint32_t limit)
{
    uint32_t count = 0;
    char *p = text;
    for (;;)
    {
        if (count == limit) return UINT32_MAX;
        while (*p == ' ' || *p == '\t') ++p;
        out[count++] = p;
        char *next = strchr(p, ',');
        if (next) *next++ = 0;
        char *end = p + strlen(p);
        while (end > p && isspace((unsigned char)end[-1])) *--end = 0;
        if (!next) return count;
        p = next;
    }
}
static bool integer(const char *text, int32_t *result)
{
    char *end;
    long long value = strtoll(text, &end, 10);
    if (end == text || *end || value < INT32_MIN || value > INT32_MAX) return false;
    *result = (int32_t)value;
    return true;
}
static uint32_t trigger_id(const ra_battle_campaign *c, const char *id)
{
    for (uint32_t i = 0; i < c->trigger_count; ++i)
        if (ra_equal(c->triggers[i].id, id)) return i + 1;
    return 0;
}
uint32_t ra_campaign_house(const ra_battle *b, const char *name)
{
    if (!b || !b->campaign || !name) return 0;
    const ra_battle_campaign *c = b->campaign;
    for (uint32_t i = 0; i < c->house_count; ++i)
        if (ra_equal(c->houses[i], name) || ra_equal(c->countries[i], name)) return i + 1;
    return 0;
}
static uint32_t house_argument(const ra_battle *b, int32_t argument)
{
    /* 十三个内建国家之后，参数按地图 [Countries] 编号查找，不能假设玩家总是地图第一家。 */
    if (argument < 13 || argument >= 13 + RA_BATTLE_TEAMS) return 0;
    return b->campaign->house_arguments[argument - 13];
}
static uint32_t waypoint(const char *text)
{
    uint32_t value = 0;
    if (!text || !*text) return UINT32_MAX;
    for (; *text; ++text)
    {
        int letter = toupper((unsigned char)*text) - 'A' + 1;
        if (letter < 1 || letter > 26 || value > 1024) return UINT32_MAX;
        value = value * 26 + (uint32_t)letter;
    }
    return value - 1;
}
uint32_t ra_campaign_tag(const ra_battle *b, const ra_ini *ini, const char *tag)
{
    const ra_ini_entry *e = ra_ini_get(ini, "Tags", tag);
    if (!b || !b->campaign || !e || strlen(e->value) >= 256) return 0;
    char text[256], *parts[4];
    strcpy(text, e->value);
    if (csv(text, parts, 4) != 3) return 0;
    return trigger_id(b->campaign, parts[2]);
}
bool ra_campaign_event_supported(uint32_t kind)
{
    switch (kind)
    {
    case 0:
    case 1:
    case 4:
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
    case 11:
    case 12:
    case 13:
    case 14:
    case 19:
    case 20:
    case 21:
    case 22:
    case 27:
    case 28:
    case 30:
    case 32:
    case 33:
    case 36:
    case 37:
    case 47:
    case 48:
    case 52:
    case 57:
        return true;
    default:
        return false;
    }
}
bool ra_campaign_action_supported(uint32_t kind)
{
    switch (kind)
    {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 11:
    case 12:
    case 14:
    case 22:
    case 23:
    case 24:
    case 25:
    case 26:
    case 27:
    case 28:
    case 29:
    case 32:
    case 36:
    case 37:
    case 38:
    case 46:
    case 47:
    case 48:
    case 53:
    case 54:
    case 56:
    case 57:
    case 63:
    case 74:
    case 80:
    case 104:
    case 112:
        return true;
    default:
        return false;
    }
}
static const char *value(const ra_ini *ini, const char *section, const char *key)
{
    const ra_ini_entry *e = ra_ini_get(ini, section, key);
    return e ? e->value : "";
}
static const char *type_at(const ra_ini *ini, const char *section, uint32_t index)
{
    /* Westwood 类型编号按登记顺序从零开始；数字键有缺号，不能按键名查找。 */
    uint32_t at = 0;
    for (size_t i = 0; i < ini->entry_count; ++i)
    {
        const ra_ini_entry *e = &ini->entries[i];
        if (!ra_equal(e->section, section)) continue;
        bool duplicate = false;
        for (size_t j = 0; j < i; ++j)
            if (ra_equal(ini->entries[j].section, section) && ra_equal(ini->entries[j].value, e->value))
            {
                duplicate = true;
                break;
            }
        if (duplicate) continue;
        if (at++ == index) return e->value;
    }
    return "";
}
static bool parse_records(ra_battle_campaign *c, const ra_ini *ini, ra_campaign_trigger *t, ra_error *error)
{
    char text[8192], *parts[256];
    int32_t n;
    const ra_ini_entry *entry = ra_ini_get(ini, "Events", t->id);
    if (!entry || strlen(entry->value) >= sizeof(text)) return ra_fail(error, RA_SYNTAX, 0, "missing or oversized trigger events");
    strcpy(text, entry->value);
    uint32_t count = csv(text, parts, 256);
    if (count == UINT32_MAX || !integer(parts[0], &n) || n < 1 || n > RA_CAMPAIGN_EVENTS || count != 1 + (uint32_t)n * 3)
        return ra_fail(error, RA_SYNTAX, entry->line, "invalid trigger event record");
    t->event_count = (uint32_t)n;
    for (uint32_t i = 0; i < t->event_count; ++i)
    {
        if (!integer(parts[1 + i * 3], &n) || n < 0 || n >= 128 || !integer(parts[3 + i * 3], &t->events[i].argument))
            return ra_fail(error, RA_SYNTAX, entry->line, "invalid trigger event fields");
        t->events[i].kind = (uint32_t)n;
        if (!ra_campaign_event_supported((uint32_t)n)) ++c->unsupported_events[n];
    }
    entry = ra_ini_get(ini, "Actions", t->id);
    if (!entry || strlen(entry->value) >= sizeof(text)) return ra_fail(error, RA_SYNTAX, 0, "missing or oversized trigger actions");
    strcpy(text, entry->value);
    count = csv(text, parts, 256);
    if (count == UINT32_MAX || !integer(parts[0], &n) || n < 1 || n > RA_CAMPAIGN_ACTIONS || count != 1 + (uint32_t)n * 8)
        return ra_fail(error, RA_SYNTAX, entry->line, "invalid trigger action record");
    t->action_count = (uint32_t)n;
    for (uint32_t i = 0; i < t->action_count; ++i)
    {
        ra_campaign_action *a = &t->actions[i];
        if (!integer(parts[1 + i * 8], &n) || n < 0 || n >= 160 || strlen(parts[3 + i * 8]) >= sizeof(a->reference))
            return ra_fail(error, RA_SYNTAX, entry->line, "invalid trigger action fields");
        a->kind = (uint32_t)n;
        strcpy(a->reference, parts[3 + i * 8]);
        a->argument = 0;
        integer(a->reference, &a->argument);
        a->waypoint = waypoint(parts[8 + i * 8]);
        if (a->kind == 104 && integer(parts[8 + i * 8], &n) && n >= 0 && n <= 10000) a->waypoint = (uint32_t)n;
        if (!ra_campaign_action_supported(a->kind)) ++c->unsupported_actions[a->kind];
    }
    return true;
}
bool ra_campaign_open(ra_battle *b, const ra_ini *ini, const char *const *houses, const char *const *countries, uint32_t count, ra_error *error)
{
    if (!b || !ini || b->campaign || b->tick || b->terrain_sealed || !count || count > RA_BATTLE_TEAMS)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial campaign");
    ra_battle_campaign *c = calloc(1, sizeof(*c));
    if (!c) return ra_fail(error, RA_MEMORY, 0, "campaign allocation failed");
    b->campaign = c;
    const ra_ini_entry *invalid_entry = NULL;
    c->house_count = count;
    for (uint32_t i = 0; i < count; ++i)
    {
        if (strlen(houses[i]) >= 64 || strlen(countries[i]) >= 64) goto invalid;
        strcpy(c->houses[i], houses[i]);
        strcpy(c->countries[i], countries[i]);
    }
    for (uint32_t i = 0; i < RA_BATTLE_TEAMS; ++i)
    {
        char key[16];
        snprintf(key, sizeof(key), "%u", i);
        c->house_arguments[i] = ra_campaign_house(b, value(ini, "Countries", key));
    }
    for (uint32_t i = 0; i < 1024; ++i) c->waypoints[i] = UINT32_MAX;
    for (size_t i = 0; i < ini->entry_count; ++i)
    {
        const ra_ini_entry *e = &ini->entries[i];
        invalid_entry = e;
        if (ra_ini_get(ini, e->section, e->key) != e) continue;
        if (ra_equal(e->section, "Waypoints"))
        {
            int32_t index, cell;
            if (!integer(e->key, &index) || index < 0 || index >= 1024 || !integer(e->value, &cell) || cell < 0) goto invalid;
            uint32_t x = (uint32_t)cell % 1000, y = (uint32_t)cell / 1000;
            if (x >= b->width || y >= b->height) goto invalid;
            c->waypoints[index] = y * b->width + x;
        }
        if (ra_equal(e->section, "Triggers"))
        {
            if (c->trigger_count == RA_CAMPAIGN_TRIGGERS || strlen(e->key) >= 32 || strlen(e->value) >= 512) goto invalid;
            ra_campaign_trigger *t = &c->triggers[c->trigger_count++];
            char text[512], *parts[10];
            strcpy(text, e->value);
            if (csv(text, parts, 10) != 8 || strlen(parts[2]) >= sizeof(t->name)) goto invalid;
            strcpy(t->id, e->key);
            strcpy(t->name, parts[2]);
            t->house = ra_campaign_house(b, parts[0]);
            t->disabled = !strcmp(parts[3], "1") || !strcmp(parts[5], "0");
        }
    }
    for (uint32_t i = 0; i < c->trigger_count; ++i)
    {
        ra_campaign_trigger *t = &c->triggers[i];
        char text[512], *parts[10];
        strcpy(text, value(ini, "Triggers", t->id));
        csv(text, parts, 10);
        t->linked = trigger_id(c, parts[1]);
        if (!parse_records(c, ini, t, error)) goto fail;
        for (uint32_t j = 0; j < t->event_count; ++j)
            if (t->events[j].kind == 32 || t->events[j].kind == 57 || (t->events[j].kind >= 19 && t->events[j].kind <= 22))
            {
                t->events[j].argument = (int32_t)ra_economy_type(b, type_at(ini,
                                                                            t->events[j].kind == 20   ? "VehicleTypes"
                                                                            : t->events[j].kind == 21 ? "InfantryTypes"
                                                                            : t->events[j].kind == 22 ? "AircraftTypes"
                                                                                                      : "BuildingTypes",
                                                                            (uint32_t)t->events[j].argument));
            }

        for (size_t j = 0; j < ini->entry_count; ++j)
        {
            const ra_ini_entry *e = &ini->entries[j];
            if (!ra_equal(e->section, "Tags") || strlen(e->value) >= 256) continue;
            char tag[256], *p[4];
            strcpy(tag, e->value);
            if (csv(tag, p, 4) == 3 && ra_equal(p[2], t->id)) t->persistence = (uint32_t)strtoul(p[0], NULL, 10);
        }
        c->state.triggers[i].enabled = !t->disabled;
    }
    for (size_t i = 0; i < ini->entry_count; ++i)
    {
        const ra_ini_entry *e = &ini->entries[i];
        invalid_entry = e;
        if (ra_ini_get(ini, e->section, e->key) != e) continue;
        if (ra_equal(e->section, "CellTags"))
        {
            if (c->cell_count == RA_CAMPAIGN_CELLS) goto invalid;
            int32_t packed;
            if (!integer(e->key, &packed) || packed < 0 || (uint32_t)packed % 1000 >= b->width || (uint32_t)packed / 1000 >= b->height) goto invalid;
            uint32_t trigger = ra_campaign_tag(b, ini, e->value);
            if (!trigger) goto invalid;
            c->cells[c->cell_count] = (uint32_t)packed / 1000 * b->width + (uint32_t)packed % 1000;
            c->cell_triggers[c->cell_count++] = trigger;
        }
        else if (ra_equal(e->section, "VariableNames"))
        {
            int32_t index;
            const char *last = strrchr(e->value, ',');
            if (!integer(e->key, &index) || index < 0 || index >= 256) goto invalid;
            c->state.local[index] = last && strtoul(last + 1, NULL, 10) != 0;
        }
        else if (ra_equal(e->section, "TeamTypes"))
        {
            if (c->team_count == RA_CAMPAIGN_TEAMS || strlen(e->value) >= 32) goto invalid;
            ra_campaign_team *t = &c->teams[c->team_count++];
            strcpy(t->id, e->value);
            t->house = ra_campaign_house(b, value(ini, t->id, "House"));
            t->tag = ra_campaign_tag(b, ini, value(ini, t->id, "Tag"));
            t->waypoint = waypoint(value(ini, t->id, "Waypoint"));
            const char *task = value(ini, t->id, "TaskForce"), *script = value(ini, t->id, "Script");
            for (uint32_t j = 0; j < RA_CAMPAIGN_MEMBERS; ++j)
            {
                char key[16], text[128], *parts[3];
                snprintf(key, sizeof(key), "%u", j);
                const char *v = value(ini, task, key);
                if (!*v) break;
                if (strlen(v) >= sizeof(text)) goto invalid;
                strcpy(text, v);
                int32_t number;
                if (csv(text, parts, 3) != 2 || !integer(parts[0], &number) || number < 1 || number > RA_CAMPAIGN_MEMBERS) goto invalid;
                t->numbers[t->member_count] = (uint32_t)number;
                t->types[t->member_count++] = ra_economy_type(b, parts[1]);
            }
            for (uint32_t j = 0; j < RA_CAMPAIGN_SCRIPT; ++j)
            {
                char key[16], text[128], *parts[3];
                snprintf(key, sizeof(key), "%u", j);
                const char *v = value(ini, script, key);
                if (!*v) break;
                if (strlen(v) >= sizeof(text)) goto invalid;
                strcpy(text, v);
                int32_t kind, argument;
                if (csv(text, parts, 3) != 2 || !integer(parts[0], &kind) || kind < 0 || kind >= 128 || !integer(parts[1], &argument)) goto invalid;
                if (kind == 46)
                {
                    uint32_t type = ra_economy_type(b, type_at(ini, "BuildingTypes", (uint32_t)argument & 65535));
                    argument = type == UINT32_MAX ? -1 : (int32_t)(type | ((uint32_t)argument & 0xffff0000u));
                }
                t->script[t->script_count++] = (ra_campaign_event){(uint32_t)kind, argument};
                if (kind != 0 && kind != 1 && kind != 3 && kind != 5 && kind != 6 && kind != 11 && kind != 19 && kind != 20 && kind != 37 && kind != 39 &&
                    kind != 8 && kind != 46 && kind != 49 && kind != 50)
                    ++c->unsupported_scripts[kind];
            }
        }
    }
    return true;
invalid:
    ra_fail(error, RA_SYNTAX, invalid_entry ? invalid_entry->line : 0, "invalid campaign record [%s] %s", invalid_entry ? invalid_entry->section : "houses",
            invalid_entry ? invalid_entry->key : "identifier");
fail:
    battle_campaign_close(b);
    return false;
}
void battle_campaign_close(ra_battle *b)
{
    free(b->campaign);
    b->campaign = NULL;
}
void battle_campaign_seal(ra_battle *b)
{
    if (!b->campaign) return;
    memcpy(b->campaign->state.allies, b->allies, sizeof(b->allies));
    for (uint32_t i = 0; i < b->count; ++i) b->campaign->state.previous_health[i] = b->units[i].health;
    b->campaign->initial = b->campaign->state;
}
void battle_campaign_reset(ra_battle *b)
{
    if (!b->campaign || !b->terrain_sealed) return;
    b->campaign->state = b->campaign->initial;
    memcpy(b->allies, b->campaign->state.allies, sizeof(b->allies));
}

static bool attached(const ra_battle_campaign *c, uint32_t tag, uint32_t trigger)
{
    for (uint32_t depth = 0; tag && depth < RA_CAMPAIGN_TRIGGERS; ++depth)
    {
        if (tag == trigger) return true;
        tag = c->triggers[tag - 1].linked;
    }
    return false;
}
static uint32_t alive_house(const ra_battle *b, uint32_t house, int category)
{
    uint32_t count = 0;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        const ra_battle_type *t = &b->types[u->type];
        if (u->health && u->team == house && !t->insignificant && (category < 0 || (int)t->structure == category)) ++count;
    }
    return count;
}
static bool event_test(ra_battle *b, uint32_t index, const ra_campaign_event *e, uint32_t *actor)
{
    ra_battle_campaign *c = b->campaign;
    const ra_campaign_trigger_state *s = &c->state.triggers[index];
    uint32_t house = house_argument(b, e->argument), argument = (uint32_t)e->argument;
    switch (e->kind)
    {
    case 0:
    case 8:
        return true;
    case 13:
        return e->argument >= 0 && b->tick - s->started >= (uint64_t)argument * RA_BATTLE_HZ;
    case 47:
        return e->argument >= 0 && b->tick >= (uint64_t)argument * RA_BATTLE_HZ;
    case 14:
        return c->state.timer_running && b->tick >= c->state.timer_end;
    case 27:
        return argument < 256 && c->state.global[argument];
    case 28:
        return argument < 256 && !c->state.global[argument];
    case 36:
        return argument < 256 && c->state.local[argument];
    case 37:
        return argument < 256 && !c->state.local[argument];
    case 9:
    case 10:
    case 11:
        if (!house) return false;
        if ((e->kind != 10 && c->incomplete_units[house - 1]) || (e->kind != 9 && c->incomplete_buildings[house - 1])) return false;
        return alive_house(b, house, e->kind == 9 ? 0 : e->kind == 10 ? 1 : -1) == 0;
    case 12:
    case 52:
        house = c->triggers[index].house;
        if (!b->economy || !house || e->argument < 0) return false;
        return e->kind == 12 ? b->economy->state.houses[house - 1].credits > argument : b->economy->state.houses[house - 1].credits < argument;
    case 30:
    {
        uint32_t out, drain;
        ra_battle_power(b, c->triggers[index].house, &out, &drain);
        return out < drain;
    }
    case 19:
    case 20:
    case 21:
    case 22:
        if (e->argument < 0 || argument >= b->type_count) return false;
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && b->units[i].team == c->triggers[index].house && b->units[i].type == argument &&
                (i >= b->initial_count || b->initial[i].type != argument))
                return true;
        return false;
    case 32:
    case 57:
        /* 类型表的原始编号在导入时转换为引擎类型编号；缺失类型禁止误判“不存在”。 */
        if (e->argument < 0 || argument >= b->type_count) return false;
        house = c->triggers[index].house;
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && b->units[i].team == house && b->units[i].type == argument) return e->kind == 32;
        return e->kind == 57;
    case 1:
        if (!house) return false;
        for (uint32_t i = 0; i < b->count; ++i)
        {
            const ra_battle_unit *u = &b->units[i];
            if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->team != house || b->types[u->type].structure) continue;
            for (uint32_t j = 0; j < c->cell_count; ++j)
                if (u->cell % (b->width * b->height) == c->cells[j] && attached(c, c->cell_triggers[j], index + 1))
                {
                    *actor = u->id;
                    return true;
                }
        }
        return false;
    default:
        break;
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!attached(c, u->tag, index + 1)) continue;
        bool hit = false;
        if (e->kind == 7 || e->kind == 48) hit = !u->health && u->destroyed_tick;
        else if (e->kind == 6) hit = u->health < c->state.previous_health[i] && !(u->traits & RA_UNIT_LIMBO);
        else if (e->kind == 33) hit = u->selected_tick == b->tick && u->team == 1;
        else if (e->kind == 4 && u->health)
        {
            for (uint32_t j = 0; j < b->count; ++j)
            {
                const ra_battle_unit *v = &b->units[j];
                uint32_t sight = b->types[v->type].sight;
                if (v->health && v->team == 1 && battle_distance_squared(u, v) <= (uint64_t)sight * sight)
                {
                    hit = true;
                    break;
                }
            }
        }
        if (hit)
        {
            *actor = u->id;
            return true;
        }
    }
    return false;
}
static uint32_t team_id(const ra_battle_campaign *c, const char *id)
{
    for (uint32_t i = 0; i < c->team_count; ++i)
        if (ra_equal(c->teams[i].id, id)) return i + 1;
    return 0;
}
static bool start_team(ra_battle *b, const ra_campaign_action *a)
{
    ra_battle_campaign *c = b->campaign;
    uint32_t definition = team_id(c, a->reference), slot;
    if (!definition) return false;
    const ra_campaign_team *t = &c->teams[definition - 1];
    for (slot = 0; slot < RA_CAMPAIGN_TEAMS && c->state.teams[slot].active; ++slot)
    {
    }
    if (slot == RA_CAMPAIGN_TEAMS || !t->house) return false;
    ra_campaign_team_state result = {0};
    result.active = 1;
    result.definition = definition;
    result.started = b->tick;
    uint32_t recruited = 0;
    for (uint32_t i = 0; i < t->member_count; ++i)
    {
        if (t->types[i] == UINT32_MAX || t->numbers[i] > RA_CAMPAIGN_MEMBERS - result.count) return false;
        for (uint32_t n = 0; n < t->numbers[i]; ++n)
        {
            uint32_t found = 0;
            if (a->kind == 4)
            {
                for (uint32_t j = 0; j < b->count; ++j)
                {
                    const ra_battle_unit *u = &b->units[j];
                    bool used = false;
                    for (uint32_t k = 0; k < result.count; ++k)
                        if (result.members[k] == u->id) used = true;
                    if (!used && u->health && u->team == t->house && u->type == t->types[i] && !u->script_team)
                    {
                        found = u->id;
                        break;
                    }
                }
                if (!found) return false;
            }
            result.members[result.count++] = found;
            if (found) ++recruited;
        }
    }
    if (!result.count) return false;
    if (!recruited)
    {
        uint32_t wp = a->kind == 80 ? a->waypoint : t->waypoint;
        if (wp >= 1024 || c->waypoints[wp] == UINT32_MAX || result.count > RA_BATTLE_UNITS - b->count) return false;
        uint32_t before = b->count, origin = c->waypoints[wp], member = 0;
        ra_error error = {0};
        uint32_t carrier = 0;
        for (uint32_t pass = 0; pass < 2; ++pass)
            for (uint32_t i = 0; i < t->member_count; ++i)
            {
                bool transport = b->types[t->types[i]].passengers != 0;
                if (transport != (pass == 0)) continue;
                for (uint32_t n = 0; n < t->numbers[i]; ++n)
                {
                    bool spawned = false;
                    if (carrier && !transport && !b->types[t->types[i]].flying) spawned = battle_transport_spawn(b, t->types[i], t->house, carrier, &error);
                    else
                        for (int radius = 0; radius <= 8 && !spawned; ++radius)
                            for (int y = (int)(origin / b->width) - radius; y <= (int)(origin / b->width) + radius && !spawned; ++y)
                                for (int x = (int)(origin % b->width) - radius; x <= (int)(origin % b->width) + radius && !spawned; ++x)
                                {
                                    if (abs(x - (int)(origin % b->width)) != radius && abs(y - (int)(origin / b->width)) != radius) continue;
                                    if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
                                    spawned = battle_spawn_runtime(b, t->types[i], t->house, (uint32_t)y * b->width + (uint32_t)x, &error);
                                }
                    if (!spawned)
                    {
                        for (uint32_t j = before; j < b->count; ++j)
                        {
                            battle_structure_release(b, &b->units[j]);
                            if (b->occupied[b->units[j].cell] == j + 1) b->occupied[b->units[j].cell] = 0;
                            memset(&b->units[j], 0, sizeof(b->units[j]));
                        }
                        b->count = before;
                        return false;
                    }
                    result.members[member++] = b->count;
                    if (transport) carrier = b->count;
                }
            }
    }
    c->state.teams[slot] = result;
    for (uint32_t i = 0; i < result.count; ++i)
    {
        ra_battle_unit *u = &b->units[result.members[i] - 1];
        u->script_team = slot + 1;
        if (t->tag) u->tag = t->tag;
    }
    return true;
}
static void fire(ra_battle *b, uint32_t index, uint32_t depth);
static void action(ra_battle *b, uint32_t index, const ra_campaign_action *a, uint32_t depth)
{
    ra_battle_campaign *c = b->campaign;
    ra_campaign_state *s = &c->state;
    uint32_t house = house_argument(b, a->argument), trigger = trigger_id(c, a->reference), argument = (uint32_t)a->argument;
    switch (a->kind)
    {
    case 0:
        break;
    case 1:
    case 2:
        if (house == 1) s->outcome = a->kind;
        break;
    case 3:
    case 74:
        if (house)
        {
            if (a->kind == 3) s->production[house - 1] = 1;
            else s->ai_enabled[house - 1] = 1;
        }
        else ++s->rejected_actions;
        break;
    case 4:
    case 7:
    case 80:
        if (!start_team(b, a))
        {
            uint32_t definition = team_id(c, a->reference);
            if (a->kind == 4 && definition && s->pending_recruit[definition - 1] < RA_CAMPAIGN_TEAMS) ++s->pending_recruit[definition - 1];
            else ++s->rejected_teams;
        }
        break;
    case 5:
        for (uint32_t i = 0; i < RA_CAMPAIGN_TEAMS; ++i)
            if (s->teams[i].active && s->teams[i].definition == team_id(c, a->reference))
            {
                for (uint32_t j = 0; j < s->teams[i].count; ++j) b->units[s->teams[i].members[j] - 1].script_team = 0;
                s->teams[i].active = 0;
            }
        break;
    case 6:
        for (uint32_t i = 0; i < b->count; ++i)
            if (b->units[i].health && b->units[i].team == c->triggers[index].house && !b->types[b->units[i].type].structure)
            {
                b->units[i].order = RA_ORDER_ATTACK;
                b->units[i].target = ra_battle_nearest(b, i + 1);
            }
        break;
    case 11:
        snprintf(s->message, sizeof(s->message), "%s", a->reference);
        s->message_tick = b->tick;
        ++s->message_serial;
        break;
    case 104:
        for (uint32_t i = 0; i < RA_CAMPAIGN_TEAMS; ++i)
            if (s->teams[i].definition == team_id(c, a->reference))
                for (uint32_t j = 0; j < s->teams[i].count; ++j)
                    b->units[s->teams[i].members[j] - 1].flash_until = b->tick + (a->waypoint <= 10000 ? a->waypoint : 0);
        break;
    case 12:
    case 54:
        if (trigger) s->triggers[trigger - 1].enabled = 0;
        else ++s->rejected_actions;
        break;
    case 53:
        if (!trigger)
        {
            ++s->rejected_actions;
            break;
        }
        if (!s->triggers[trigger - 1].enabled)
        {
            s->triggers[trigger - 1].enabled = 1;
            s->triggers[trigger - 1].started = b->tick;
        }
        break;
    case 22:
        if (trigger && depth < 8) fire(b, trigger - 1, depth + 1);
        else ++s->rejected_actions;
        break;
    case 14:
    case 36:
        if (!house)
        {
            ++s->rejected_actions;
            break;
        }
        for (uint32_t i = 0; i < b->count; ++i)
            if ((a->kind == 36 ? b->units[i].team == c->triggers[index].house : attached(c, b->units[i].tag, index + 1)) && b->units[i].health)
                b->units[i].team = house;
        break;
    case 37:
    case 38:
        if (house && c->triggers[index].house)
        {
            uint32_t *mask = &b->allies[c->triggers[index].house - 1];
            if (a->kind == 37) *mask |= 1u << (house - 1);
            else *mask &= ~(1u << (house - 1));
        }
        break;
    case 28:
    case 29:
        if (argument < 256) s->global[argument] = a->kind == 28;
        else ++s->rejected_actions;
        break;
    case 56:
    case 57:
        if (argument < 256) s->local[argument] = a->kind == 56;
        else ++s->rejected_actions;
        break;
    case 46:
        s->input_locked = 1;
        break;
    case 47:
        s->input_locked = 0;
        break;
    case 48:
    case 112:
        s->camera_waypoint = a->waypoint;
        ++s->camera_serial;
        break;
    case 27:
        s->timer_remaining = argument * RA_BATTLE_HZ;
        s->timer_end = b->tick + s->timer_remaining;
        break;
    case 23:
        s->timer_running = 1;
        s->timer_end = b->tick + s->timer_remaining;
        break;
    case 24:
        s->timer_remaining = s->timer_end > b->tick ? s->timer_end - b->tick : 0;
        s->timer_running = 0;
        break;
    case 25:
        s->timer_end += argument * RA_BATTLE_HZ;
        s->timer_remaining += argument * RA_BATTLE_HZ;
        break;
    case 26:
    {
        uint32_t n = argument * RA_BATTLE_HZ;
        s->timer_end = s->timer_end > n ? s->timer_end - n : b->tick;
        break;
    }
    case 32:
        for (uint32_t i = 0; i < b->count; ++i)
            if (attached(c, b->units[i].tag, index + 1)) battle_kill(b, &b->units[i], 0);
        break;
    case 63:
        if (argument < 1024 && c->waypoints[argument] != UINT32_MAX)
        {
            uint32_t cell = c->waypoints[argument];
            ra_battle_command event = {b->tick, 0, 0, cell, RA_EVENT_BRIDGE_HIT};
            if (b->bridge_at[cell]) battle_bridge_event(b, &event);
            else
                for (uint32_t i = 0; i < b->count; ++i)
                    if (b->units[i].health && b->units[i].cell == cell)
                    {
                        if (b->units[i].health <= 100) battle_kill(b, &b->units[i], 0);
                        else b->units[i].health -= 100;
                    }
        }
        break;
    default:
        ++s->rejected_actions;
        break;
    }
}
static void fire(ra_battle *b, uint32_t index, uint32_t depth)
{
    ra_battle_campaign *c = b->campaign;
    ra_campaign_trigger_state *s = &c->state.triggers[index];
    ++s->fired;
    ++c->state.fired;
    s->enabled = c->triggers[index].persistence == 2;
    s->started = b->tick;
    for (uint32_t i = 0; i < c->triggers[index].action_count; ++i) action(b, index, &c->triggers[index].actions[i], depth);
}
static void team_release(ra_battle *b, uint32_t slot)
{
    ra_campaign_team_state *s = &b->campaign->state.teams[slot];
    for (uint32_t j = 0; j < s->count; ++j)
        if (b->units[s->members[j] - 1].script_team == slot + 1) b->units[s->members[j] - 1].script_team = 0;
    s->active = 0;
}
static uint32_t script_target(const ra_battle *b, const ra_battle_unit *u, const ra_campaign_event *step)
{
    uint32_t target = 0, mode = step->kind == 46 ? (uint32_t)step->argument >> 16 : 2;
    uint64_t best = 0;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *v = &b->units[i];
        const ra_battle_type *t = &b->types[v->type];
        if (!ra_battle_targetable(b, u, v, false, false)) continue;
        if (step->kind == 46 && (step->argument < 0 || v->type != ((uint32_t)step->argument & 65535))) continue;
        if (step->kind == 0 && ((step->argument == 2 && !t->structure) || (step->argument == 4 && !t->infantry) ||
                                (step->argument == 5 && (t->structure || t->infantry || t->flying))))
            continue;
        uint64_t score = battle_distance_squared(u, v);
        if (mode < 2) score = (uint32_t)battle_threat_score(b, u, v);
        if (!target || ((mode == 1 || mode == 3) ? score > best : score < best))
        {
            target = v->id;
            best = score;
        }
    }
    return target;
}
static void campaign_production(ra_battle *b)
{
    if (!b->economy || b->tick % RA_BATTLE_HZ) return;
    ra_battle_campaign *c = b->campaign;
    /* 只补齐地图明确请求的队伍，不凭固定周期凭空扩张敌军。完整 AI.ini 调度另列待实现。 */
    for (uint32_t definition = 0; definition < c->team_count; ++definition)
    {
        const ra_campaign_team *t = &c->teams[definition];
        if (!c->state.pending_recruit[definition] || !t->house || !c->state.production[t->house - 1]) continue;
        for (uint32_t member = 0; member < t->member_count; ++member)
        {
            uint32_t type = t->types[member], available = 0;
            if (type == UINT32_MAX || !ra_economy_available(b, t->house, type)) continue;
            for (uint32_t i = 0; i < b->count; ++i)
                if (b->units[i].health && b->units[i].team == t->house && b->units[i].type == type && !b->units[i].script_team) ++available;
            if (available >= t->numbers[member]) continue;
            ra_econ_house *h = &b->economy->state.houses[t->house - 1];
            uint32_t category = ra_economy_category(b, type);
            if (!h->queues[category].count && h->credits >= b->economy->types[type].cost)
                battle_economy_apply(b, &(ra_battle_command){b->tick, 0, t->house, type, RA_ECON_QUEUE});
        }
    }
}
static void scripts(ra_battle *b)
{
    ra_battle_campaign *c = b->campaign;
    if (b->tick % RA_BATTLE_HZ == 0)
        for (uint32_t i = 0; i < c->team_count; ++i)
            if (c->state.pending_recruit[i])
            {
                ra_campaign_action a = {0};
                a.kind = 4;
                strcpy(a.reference, c->teams[i].id);
                if (start_team(b, &a)) --c->state.pending_recruit[i];
            }
    for (uint32_t i = 0; i < RA_CAMPAIGN_TEAMS; ++i)
    {
        ra_campaign_team_state *s = &c->state.teams[i];
        if (!s->active) continue;
        const ra_campaign_team *t = &c->teams[s->definition - 1];
        if (s->cursor >= t->script_count)
        {
            team_release(b, i);
            continue;
        }
        const ra_campaign_event *step = &t->script[s->cursor];
        uint32_t alive = 0, shots = 0;
        bool finished = true;
        if (!s->waiting)
        {
            s->shots_start = 0;
            for (uint32_t j = 0; j < s->count; ++j) s->shots_start += b->units[s->members[j] - 1].shots;
        }
        for (uint32_t j = 0; j < s->count; ++j)
        {
            ra_battle_unit *u = &b->units[s->members[j] - 1];
            if (!u->health || u->script_team != i + 1) continue;
            ++alive;
            shots += u->shots;
            if ((u->traits & RA_UNIT_LIMBO) && step->kind != 20) continue;
            if (step->kind == 20)
            {
                uint32_t h = house_argument(b, step->argument);
                if (h) u->team = h;
            }
            else if (step->kind == 3 || step->kind == 1)
            {
                uint32_t wp = (uint32_t)step->argument;
                if (wp >= 1024 || c->waypoints[wp] == UINT32_MAX)
                {
                    ++c->state.script_gaps;
                    team_release(b, i);
                    break;
                }
                if (!s->waiting)
                {
                    u->order = step->kind == 1 ? RA_ORDER_FORCE_GROUND : RA_ORDER_MOVE;
                    u->goal = u->destination = u->fire_cell = c->waypoints[wp];
                    u->path_count = u->path_cursor = 0;
                }
                int64_t dx = (int64_t)(u->destination % b->width) * RA_BATTLE_CELL - u->x;
                int64_t dy = (int64_t)(u->destination / b->width) * RA_BATTLE_CELL - u->y;
                if (step->kind == 3 && (uint64_t)(dx * dx + dy * dy) > (uint64_t)(RA_BATTLE_CELL * 3 / 2) * (RA_BATTLE_CELL * 3 / 2)) finished = false;
            }
            else if (step->kind == 0 || step->kind == 46)
            {
                if (!s->waiting || !u->target || !b->units[u->target - 1].health)
                {
                    u->target = script_target(b, u, step);
                    u->order = u->target ? RA_ORDER_ATTACK : RA_ORDER_GUARD;
                }
                if ((u->target && b->units[u->target - 1].health) || (!u->target && s->repeat_until_success)) finished = false;
            }
            else if (step->kind == 8)
            {
                if (b->types[u->type].passengers)
                {
                    u->unloading = 1;
                    u->goal = u->destination = u->next;
                    u->path_count = u->path_cursor = 0;
                    if (battle_transport_count(b, u->id)) finished = false;
                    else
                    {
                        u->unloading = 0;
                        if (step->argument == 2) u->script_team = 0;
                    }
                }
            }
            else if (step->kind == 5)
            {
                u->order = RA_ORDER_GUARD;
                u->anchor = u->cell;
                if (step->argument > 0 && b->tick - s->started < (uint32_t)step->argument * RA_BATTLE_HZ) finished = false;
            }
            else if (step->kind == 11)
            {
                u->order = step->argument == 1 || step->argument == 15  ? RA_ORDER_ATTACK
                           : step->argument == 0 || step->argument == 6 ? RA_ORDER_STOP
                                                                        : RA_ORDER_GUARD;
                u->anchor = u->cell;
                if (u->order == RA_ORDER_ATTACK) u->target = script_target(b, u, &(ra_campaign_event){0, 1});
            }
            else if (step->kind == 37)
            {
                u->health = 0;
                u->traits |= RA_UNIT_LIMBO;
                if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
            }
            else if (step->kind == 19)
            {
                /* 随机逃跑使用模拟随机数，绝不依赖显示帧或墙钟。 */
                if (!s->waiting)
                {
                    uint32_t wp = battle_random_range(b, 0, 100);
                    if (c->waypoints[wp] != UINT32_MAX && battle_cell_passable(b, c->waypoints[wp], u->id))
                    {
                        u->order = RA_ORDER_MOVE;
                        u->goal = u->destination = c->waypoints[wp];
                    }
                }
                if (u->cell != u->goal) finished = false;
            }
            else if (step->kind == 50)
            {
                /* 原版动作 50 是计时闪烁，不是移动；显示仅消费这个截止步。 */
                u->flash_until = b->tick + (step->argument > 0 ? (uint32_t)step->argument : 0);
            }
            else if (step->kind != 6 && step->kind != 39 && step->kind != 49)
            {
                ++c->state.script_gaps;
                team_release(b, i);
                break;
            }
        }
        if (!alive)
        {
            team_release(b, i);
            continue;
        }
        if (step->kind == 1) finished = shots > s->shots_start;
        if (step->kind == 49) s->repeat_until_success = step->argument != 0;
        if (step->kind == 6)
        {
            s->cursor = step->argument > 0 ? (uint32_t)step->argument - 1 : 0;
            s->waiting = 0;
            continue;
        }
        if (step->kind == 39 && step->argument >= 0 && step->argument < 256) c->state.local[step->argument] = 1;
        if (finished)
        {
            ++s->cursor;
            s->waiting = 0;
            s->started = b->tick;
        }
        else s->waiting = 1;
    }
}
void battle_campaign_step(ra_battle *b)
{
    if (!b->campaign) return;
    ra_battle_campaign *c = b->campaign;
    if (c->state.outcome) return;
    campaign_production(b);
    scripts(b);
    for (uint32_t i = 0; i < c->trigger_count; ++i)
    {
        ra_campaign_trigger_state *s = &c->state.triggers[i];
        if (!s->enabled) continue;
        bool ready = true;
        for (uint32_t j = 0; j < c->triggers[i].event_count; ++j)
            if (!event_test(b, i, &c->triggers[i].events[j], &s->actor))
            {
                ready = false;
                break;
            }
        if (ready) fire(b, i, 0);
    }
    for (uint32_t i = 0; i < b->count; ++i) c->state.previous_health[i] = b->units[i].health;
}
