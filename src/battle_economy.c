#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

uint32_t ra_economy_type(const ra_battle *b, const char *id)
{
    if (b && id)
        for (uint32_t i = 0; i < b->type_count; ++i)
            if (ra_equal(b->types[i].id, id)) return i;
    return UINT32_MAX;
}
static bool contains(const char *list, const char *word)
{
    while (*list)
    {
        char token[64];
        size_t n = 0;
        while (isspace((unsigned char)*list)) ++list;
        while (*list && *list != ',')
        {
            if (n + 1 < sizeof(token)) token[n++] = *list;
            ++list;
        }
        if (*list) ++list;
        while (n && isspace((unsigned char)token[n - 1])) --n;
        token[n] = 0;
        if (ra_equal(token, word)) return true;
    }
    return false;
}
static bool integer(const ra_ini *rules, const char *section, const char *key, int32_t fallback, int32_t *value, ra_error *error)
{
    const ra_ini_entry *entry = ra_ini_get(rules, section, key);
    int64_t result = fallback;
    if (entry && (!ra_ini_integer(entry, &result, error) || result < -1 || result > 1000000))
        return ra_fail(error, RA_RANGE, entry->line, "invalid economy integer %s.%s", section, key);
    *value = (int32_t)result;
    return true;
}
static bool decimal(const ra_ini *rules, const char *section, const char *key, uint32_t fallback, uint32_t *out, ra_error *error)
{
    const ra_ini_entry *entry = ra_ini_get(rules, section, key);
    if (!entry)
    {
        *out = fallback;
        return true;
    }
    const char *p = entry->value;
    uint64_t whole = 0, fraction = 0, divisor = 1;
    bool digit = false;
    while (isdigit((unsigned char)*p))
    {
        digit = true;
        whole = whole * 10 + (unsigned)(*p++ - '0');
        if (whole > 10000) break;
    }
    if (*p == '.')
    {
        ++p;
        while (isdigit((unsigned char)*p) && divisor < 1000000)
        {
            digit = true;
            fraction = fraction * 10 + (unsigned)(*p++ - '0');
            divisor *= 10;
        }
    }
    if (!digit || *p || whole > 10000) return ra_fail(error, RA_SYNTAX, entry->line, "invalid economy decimal %s.%s", section, key);
    *out = (uint32_t)(whole * 1000 + fraction * 1000 / divisor);
    return true;
}
static bool text(const ra_ini *rules, const char *section, const char *key, char *out, size_t capacity, ra_error *error)
{
    const ra_ini_entry *entry = ra_ini_get(rules, section, key);
    const char *value = entry ? entry->value : "";
    if (strlen(value) >= capacity) return ra_fail(error, RA_RANGE, entry->line, "economy list exceeds capacity");
    strcpy(out, value);
    return true;
}
static bool yes(const ra_ini *rules, const char *section, const char *key)
{
    const ra_ini_entry *entry = ra_ini_get(rules, section, key);
    return entry && (ra_equal(entry->value, "yes") || ra_equal(entry->value, "true") || !strcmp(entry->value, "1"));
}
bool ra_economy_open(ra_battle *b, const ra_ini *rules, ra_error *error)
{
    if (!b || !b->tiles || !rules || b->tick || b->command_count || b->terrain_sealed || b->economy)
        return ra_fail(error, RA_ARGUMENT, 0, "economy requires an unsealed initial scene");
    ra_battle_economy *e = calloc(1, sizeof(*e));
    if (!e) return ra_fail(error, RA_MEMORY, 0, "economy allocation failed");
    e->ore = calloc((size_t)b->width * b->height, 1);
    e->initial_ore = calloc((size_t)b->width * b->height, 1);
    if (!e->ore || !e->initial_ore) goto fail;
    if (!decimal(rules, "General", "BuildSpeed", 700, &e->build_rate, error) || !e->build_rate || e->build_rate > 10000 ||
        !decimal(rules, "General", "MinLowPowerProductionSpeed", 500, &e->low_min, error) ||
        !decimal(rules, "General", "MaxLowPowerProductionSpeed", 800, &e->low_max, error) ||
        !decimal(rules, "General", "LowPowerPenaltyModifier", 1000, &e->low_penalty, error) || e->low_min > e->low_max || e->low_max > 1000)
        goto fail;
    e->harvest_ticks = e->unload_ticks = 5; /* 缺省采卸节拍暂用五步；具体动画与硬编码默认值仍需实机校准。 */
    int32_t value;
    if (!integer(rules, "General", "HarvesterLoadRate", 5, &value, error) || value < 1 || value > 900) goto fail;
    e->harvest_ticks = (uint32_t)value;
    if (!integer(rules, "Riparius", "Value", 25, &value, error) || value < 1) goto fail;
    e->ore_value = (uint32_t)value;
    if (!integer(rules, "Cruentus", "Value", 50, &value, error) || value < 1) goto fail;
    e->gem_value = (uint32_t)value;
    static const char *keys[] = {"PrerequisitePower", "PrerequisiteFactory", "PrerequisiteBarracks",
                                 "PrerequisiteRadar", "PrerequisiteTech",    "PrerequisiteProc"};
    for (uint32_t i = 0; i < 6; ++i)
        if (!text(rules, "General", keys[i], e->generic[i], sizeof(e->generic[i]), error)) goto fail;
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        const char *id = b->types[i].id;
        ra_econ_type *t = &e->types[i];
        if (!integer(rules, id, "Cost", 0, &value, error) || value < 0) goto fail;
        t->cost = (uint32_t)value;
        if (!integer(rules, id, "TechLevel", -1, &t->tech, error) || !integer(rules, id, "Adjacent", 2, &value, error) || value < 0 || value > 16) goto fail;
        t->adjacent = (uint32_t)value;
        if (!integer(rules, id, "Storage", 0, &value, error) || value < 0 || value > 10000) goto fail;
        t->storage = (uint32_t)value;
        if (!text(rules, id, "Prerequisite", t->prerequisite, sizeof(t->prerequisite), error) ||
            !text(rules, id, "Owner", t->owners, sizeof(t->owners), error) || !text(rules, id, "ForbiddenHouses", t->forbidden, sizeof(t->forbidden), error) ||
            !text(rules, id, "Dock", t->docks, sizeof(t->docks), error))
            goto fail;
        const ra_ini_entry *factory = ra_ini_get(rules, id, "Factory"), *free_unit = ra_ini_get(rules, id, "FreeUnit");
        t->factory = factory && ra_equal(factory->value, "BuildingType")   ? 1
                     : factory && ra_equal(factory->value, "UnitType")     ? 2
                     : factory && ra_equal(factory->value, "InfantryType") ? 3
                                                                           : 0;
        const ra_ini_entry *airport = ra_ini_get(rules, id, "AirportBound"), *naval = ra_ini_get(rules, id, "Naval");
        t->airport_bound = airport && ra_equal(airport->value, "yes");
        if (factory && ra_equal(factory->value, "AircraftType")) t->factory = 4;
        if (t->factory == 2 && naval && ra_equal(naval->value, "yes")) t->factory = 5;
        t->free_type = free_unit ? ra_economy_type(b, free_unit->value) : UINT32_MAX;
        if (free_unit && t->free_type == UINT32_MAX)
        {
            ra_fail(error, RA_NOT_FOUND, free_unit->line, "unregistered refinery free unit");
            goto fail;
        }
        t->harvester = yes(rules, id, "Harvester");
        t->refinery = yes(rules, id, "Refinery");
        t->chrono = t->harvester && yes(rules, id, "Teleporter");
        if (t->harvester && !t->storage)
        {
            ra_fail(error, RA_RANGE, 0, "harvester storage must be positive");
            goto fail;
        }
        uint32_t multiplier;
        if (!decimal(rules, id, "BuildTimeMultiplier", 1000, &multiplier, error) || !multiplier || multiplier > 10000) goto fail;
        uint64_t ticks = ((uint64_t)t->cost * e->build_rate * 60 * RA_BATTLE_HZ * multiplier + 999999999) / 1000000000;
        if (ticks > 1000000)
        {
            ra_fail(error, RA_RANGE, 0, "build duration exceeds simulation limits");
            goto fail;
        }
        t->ticks = ticks ? (uint32_t)ticks : 1;
        t->enabled = t->tech >= 0 && t->cost > 0;
    }
    b->economy = e;
    return true;
fail:
    free(e->ore);
    free(e->initial_ore);
    free(e);
    if (!error || !error->code) ra_fail(error, RA_RANGE, 0, "invalid economy configuration or allocation");
    return false;
}
void battle_economy_close(ra_battle *b)
{
    if (!b->economy) return;
    free(b->economy->ore);
    free(b->economy->initial_ore);
    free(b->economy);
    b->economy = NULL;
}
void battle_economy_seal(ra_battle *b)
{
    if (!b->economy) return;
    b->economy->initial = b->economy->state;
    memcpy(b->economy->initial_ore, b->economy->ore, (size_t)b->width * b->height);
}
bool ra_economy_house(ra_battle *b, uint32_t team, const char *country, uint32_t credits, uint32_t tech, ra_error *error)
{
    if (!b || !b->economy || b->tick || b->command_count || b->terrain_sealed || !team || team > RA_BATTLE_TEAMS || !country || !*country ||
        strlen(country) >= 32 || credits > 1000000000 || tech > 10)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial economy house");
    ra_econ_house *h = &b->economy->state.houses[team - 1];
    strcpy(h->country, country);
    h->credits = credits;
    h->tech = tech;
    return true;
}
bool ra_economy_ore(ra_battle *b, uint32_t cell, uint32_t kind, uint32_t amount, ra_error *error)
{
    if (!b || !b->economy || b->tick || b->command_count || b->terrain_sealed || cell >= b->width * b->height || kind > 2 || amount > 63 || (!kind != !amount))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial ore cell");
    b->economy->ore[cell] = (uint8_t)(amount | kind << 6);
    return true;
}
uint32_t ra_economy_category(const ra_battle *b, uint32_t type)
{
    return b->types[type].structure ? 0 : b->types[type].infantry ? 2 : b->economy->types[type].airport_bound ? 3 : b->types[type].naval ? 4 : 1;
}
static uint32_t producer(const ra_battle *b, uint32_t team, uint32_t category)
{
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].team == team && b->economy->types[b->units[i].type].factory == category + 1) return i + 1;
    return 0;
}
static bool prerequisite(const ra_battle *b, uint32_t team, const char *token)
{
    static const char *names[] = {"POWER", "FACTORY", "BARRACKS", "RADAR", "TECH", "PROC"};
    const char *list = token;
    for (uint32_t i = 0; i < 6; ++i)
        if (ra_equal(token, names[i])) list = b->economy->generic[i];
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].team == team && b->types[b->units[i].type].structure && contains(list, b->types[b->units[i].type].id))
            return true;
    return false;
}
bool ra_economy_owner_allowed(const ra_battle *b, uint32_t team, uint32_t type)
{
    if (!b || !b->economy || !team || team > RA_BATTLE_TEAMS || type >= b->type_count) return false;
    const ra_econ_type *t = &b->economy->types[type];
    const char *country = b->economy->state.houses[team - 1].country;
    return *country && contains(t->owners, country) && !contains(t->forbidden, country);
}
bool ra_economy_available(const ra_battle *b, uint32_t team, uint32_t type)
{
    if (!b || !b->economy || !team || team > RA_BATTLE_TEAMS || type >= b->type_count) return false;
    const ra_econ_type *t = &b->economy->types[type];
    const ra_econ_house *h = &b->economy->state.houses[team - 1];
    if (!t->enabled || (uint32_t)t->tech > h->tech || !ra_economy_owner_allowed(b, team, type) || !producer(b, team, ra_economy_category(b, type)))
        return false;
    const char *p = t->prerequisite;
    while (*p)
    {
        char token[64];
        size_t n = 0;
        while (isspace((unsigned char)*p)) ++p;
        while (*p && *p != ',')
        {
            if (n + 1 >= sizeof(token)) return false;
            token[n++] = *p++;
        }
        if (*p) ++p;
        while (n && isspace((unsigned char)token[n - 1])) --n;
        token[n] = 0;
        if (!n || !prerequisite(b, team, token)) return false;
    }
    return true;
}
static uint32_t distance(uint32_t x, uint32_t y, uint32_t left, uint32_t top, uint32_t right, uint32_t bottom)
{
    uint32_t dx = x < left ? left - x : x > right ? x - right : 0;
    uint32_t dy = y < top ? top - y : y > bottom ? y - bottom : 0;
    return dx > dy ? dx : dy;
}
bool ra_economy_placeable(const ra_battle *b, uint32_t team, uint32_t type, uint32_t cell)
{
    if (!b || !b->economy || !team || team > RA_BATTLE_TEAMS || type >= b->type_count || cell >= b->width * b->height) return false;
    const ra_battle_type *t = &b->types[type];
    uint32_t x = cell % b->width, y = cell / b->width, w = t->foundation_width, h = t->foundation_height;
    if (!t->structure || !w || !h || w > b->width - x || h > b->height - y || b->count == RA_BATTLE_UNITS) return false;
    for (uint32_t row = 0; row < h; ++row)
        for (uint32_t col = 0; col < w; ++col)
        {
            uint32_t at = cell + row * b->width + col;
            if (!battle_cell_available(b, at, 0) || b->bridges[at] || b->tiles[at].ramp || b->tiles[at].height != b->tiles[cell].height ||
                (b->economy->ore[at] & 63))
                return false;
        }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!u->health || u->team != team || !b->types[u->type].structure) continue;
        uint32_t ux = u->cell % b->width, uy = u->cell / b->width;
        uint32_t dx = ux + b->types[u->type].foundation_width - 1, dy = uy + b->types[u->type].foundation_height - 1;
        uint32_t nearest_x = ux > x + w - 1 ? x + w - 1 : ux < x ? x : ux;
        uint32_t nearest_y = uy > y + h - 1 ? y + h - 1 : uy < y ? y : uy;
        if (distance(nearest_x, nearest_y, ux, uy, dx, dy) <= b->economy->types[type].adjacent + 1) return true;
    }
    return false;
}
bool battle_economy_target(const ra_battle *b, uint32_t actor, uint32_t kind, uint32_t target)
{
    if (!b || !b->economy) return false;
    if (kind == RA_ECON_HARVEST) return actor && actor <= RA_BATTLE_UNITS && target < b->width * b->height;
    if (kind == RA_ECON_RETURN) return actor && actor <= RA_BATTLE_UNITS && target && target <= RA_BATTLE_UNITS;
    if (!actor || actor > RA_BATTLE_TEAMS) return false;
    if (kind == RA_ECON_QUEUE) return target < b->type_count;
    if (kind == RA_ECON_PAUSE || kind == RA_ECON_CANCEL) return target < RA_ECON_CATEGORIES;
    return kind == RA_ECON_PLACE && target / RA_BATTLE_TYPES < b->width * b->height && target % RA_BATTLE_TYPES < b->type_count &&
           b->types[target % RA_BATTLE_TYPES].structure;
}
bool ra_economy_command(ra_battle *b, uint32_t tick, uint32_t actor, ra_battle_order kind, uint32_t target, ra_error *error)
{
    if (!battle_economy_target(b, actor, kind, target) || tick <= b->tick || tick > 10000000 || b->command_count == RA_BATTLE_COMMANDS ||
        (b->command_count && tick < b->commands[b->command_count - 1].tick))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid economy command");
    b->commands[b->command_count] = (ra_battle_command){tick, b->command_count + 1, actor, target, kind};
    ++b->command_count;
    return true;
}
bool battle_spawn_runtime(ra_battle *b, uint32_t type, uint32_t team, uint32_t cell, ra_error *error)
{
    return b->types[type].structure ? battle_spawn_building(b, type, team, cell % b->width, cell / b->width, true, error)
                                    : battle_spawn_mobile(b, type, team, cell % b->width, cell / b->width, 0, true, error);
}
static void pop(ra_econ_queue *q)
{
    memmove(q->types, q->types + 1, (RA_ECON_QUEUE_LIMIT - 1) * sizeof(*q->types));
    q->types[RA_ECON_QUEUE_LIMIT - 1] = 0;
    --q->count;
    q->progress = q->paid = q->paused = q->producer = 0;
}
static void goal(ra_battle_unit *u, uint32_t cell)
{
    u->destination = cell;
    if (u->goal == cell) return;
    u->goal = cell;
    u->path_count = u->path_cursor = u->retry = 0;
}
void battle_economy_apply(ra_battle *b, const ra_battle_command *c)
{
    ra_battle_economy *e = b->economy;
    if (!battle_economy_target(b, c->unit, c->kind, c->target))
    {
        ++b->rejected;
        return;
    }
    if (c->kind == RA_ECON_HARVEST || c->kind == RA_ECON_RETURN)
    {
        if (c->unit > b->count || !b->units[c->unit - 1].health || !e->types[b->units[c->unit - 1].type].harvester)
        {
            ++b->rejected;
            return;
        }
        ra_battle_unit *u = &b->units[c->unit - 1];
        ra_econ_miner *m = &e->state.miners[c->unit - 1];
        if (c->kind == RA_ECON_RETURN && (c->target > b->count || !b->units[c->target - 1].health || b->units[c->target - 1].team != u->team ||
                                          !e->types[b->units[c->target - 1].type].refinery))
        {
            ++b->rejected;
            return;
        }
        m->active = c->kind == RA_ECON_RETURN ? 2 : 1;
        m->destination = c->kind == RA_ECON_HARVEST ? c->target : UINT32_MAX;
        m->refinery = c->kind == RA_ECON_RETURN ? c->target : 0;
        m->delay = 0;
        u->target = u->waypoint_count = u->waypoint_cursor = u->waypoint_loop = 0;
        u->order = RA_ECON_HARVEST;
        goal(u, u->next);
        return;
    }
    ra_econ_house *h = &e->state.houses[c->unit - 1];
    if (c->kind == RA_ECON_QUEUE)
    {
        uint32_t category = ra_economy_category(b, c->target);
        ra_econ_queue *q = &h->queues[category];
        if (!ra_economy_available(b, c->unit, c->target) || q->count >= (category ? RA_ECON_QUEUE_LIMIT : 1))
        {
            ++b->rejected;
            return;
        }
        q->types[q->count++] = c->target;
    }
    else if (c->kind == RA_ECON_PAUSE || c->kind == RA_ECON_CANCEL)
    {
        ra_econ_queue *q = &h->queues[c->target];
        if (!q->count)
        {
            ++b->rejected;
            return;
        }
        if (c->kind == RA_ECON_PAUSE) q->paused ^= 1;
        else
        {
            h->credits += q->paid;
            h->spent -= q->paid;
            pop(q);
        }
    }
    else if (c->kind == RA_ECON_PLACE)
    {
        uint32_t type = c->target % RA_BATTLE_TYPES, cell = c->target / RA_BATTLE_TYPES;
        ra_econ_queue *q = &h->queues[0];
        ra_error error = {0};
        if (!q->count || q->types[0] != type || q->progress < e->types[type].ticks * 1000 || !ra_economy_available(b, c->unit, type) ||
            !ra_economy_placeable(b, c->unit, type, cell) || !battle_spawn_runtime(b, type, c->unit, cell, &error))
        {
            ++b->rejected;
            return;
        }
        e->state.free_pending[b->count - 1] = e->types[type].free_type == UINT32_MAX ? 0 : e->types[type].free_type + 1;
        ++h->built;
        pop(q);
    }
}
static uint32_t perimeter(const ra_battle *b, const ra_battle_unit *building, uint32_t n)
{
    uint32_t w = b->types[building->type].foundation_width, h = b->types[building->type].foundation_height;
    int x = (int)(building->cell % b->width), y = (int)(building->cell / b->width);
    /* 从南侧左端开始，沿外圈顺序寻找；堵出口时保留成品，不能凭空穿过占地。 */
    if (n < w + 2)
    {
        x += (int)n - 1;
        y += (int)h;
    }
    else if ((n -= w + 2) < h)
    {
        x += (int)w;
        y += (int)h - 1 - (int)n;
    }
    else if ((n -= h) < w + 2)
    {
        x += (int)w - (int)n;
        --y;
    }
    else
    {
        n -= w + 2;
        --x;
        y += (int)n;
    }
    return x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height ? UINT32_MAX : (uint32_t)y * b->width + (uint32_t)x;
}
static uint32_t exit_cell(const ra_battle *b, const ra_battle_unit *building, uint32_t type)
{
    if (b->types[type].flying) return building->cell;
    uint32_t total = 2 * (b->types[building->type].foundation_width + b->types[building->type].foundation_height) + 4;
    for (uint32_t n = 0; n < total; ++n)
    {
        uint32_t cell = perimeter(b, building, n);
        if (cell != UINT32_MAX)
        {
            uint32_t feet = 0;
            for (uint32_t i = 0; i < b->count; ++i)
                if (b->units[i].health && !(b->units[i].traits & RA_UNIT_LIMBO) && b->types[b->units[i].type].infantry &&
                    (b->units[i].cell == cell || b->units[i].next == cell))
                    ++feet;
            if (feet >= (b->types[type].infantry ? 5u : 1u)) continue;
        }
        if (cell != UINT32_MAX && battle_type_passable(b, cell, &b->types[type]) && !b->occupied[cell] && !b->bridges[cell] &&
            b->tiles[cell].height == b->tiles[building->cell].height)
            return cell;
    }
    return UINT32_MAX;
}
static bool produce(ra_battle *b, uint32_t type, ra_battle_unit *factory)
{
    uint32_t cell = exit_cell(b, factory, type);
    ra_error error = {0};
    if (cell == UINT32_MAX || !battle_spawn_runtime(b, type, factory->team, cell, &error)) return false;
    if (b->economy->types[type].harvester)
    {
        b->economy->state.miners[b->count - 1].active = 1;
        b->economy->state.miners[b->count - 1].destination = UINT32_MAX;
        b->units[b->count - 1].order = RA_ECON_HARVEST;
    }
    ++b->economy->state.houses[factory->team - 1].produced;
    return true;
}
static void queues(ra_battle *b)
{
    ra_battle_economy *e = b->economy;
    for (uint32_t team = 1; team <= RA_BATTLE_TEAMS; ++team)
    {
        ra_econ_house *h = &e->state.houses[team - 1];
        uint32_t out, drain, rate = 1000;
        ra_battle_power(b, team, &out, &drain);
        if (out < drain)
        {
            uint32_t penalty = (uint32_t)((uint64_t)(drain - out) * e->low_penalty / drain);
            rate = penalty >= 1000 ? 0 : 1000 - penalty;
            if (rate < e->low_min) rate = e->low_min;
            if (rate > e->low_max) rate = e->low_max;
        }
        for (uint32_t category = 0; category < RA_ECON_CATEGORIES; ++category)
        {
            ra_econ_queue *q = &h->queues[category];
            if (!q->count || q->paused || !ra_economy_available(b, team, q->types[0])) continue;
            const ra_econ_type *t = &e->types[q->types[0]];
            q->producer = producer(b, team, category);
            uint32_t total = t->ticks * 1000, progress = q->progress + rate;
            if (progress > total) progress = total;
            uint32_t paid = (uint32_t)((uint64_t)t->cost * progress / total);
            if (paid - q->paid > h->credits) continue;
            h->credits -= paid - q->paid;
            h->spent += paid - q->paid;
            q->progress = progress;
            q->paid = paid;
            if (category && progress == total && produce(b, q->types[0], &b->units[q->producer - 1])) pop(q);
        }
    }
    uint32_t count = b->count;
    for (uint32_t i = 0; i < count; ++i)
        if (e->state.free_pending[i] && b->units[i].health && produce(b, e->state.free_pending[i] - 1, &b->units[i])) e->state.free_pending[i] = 0;
}
static bool dock(ra_battle *b, ra_battle_unit *u, ra_econ_miner *m)
{
    ra_battle_economy *e = b->economy;
    uint64_t best = UINT64_MAX;
    uint32_t chosen = 0, target = UINT32_MAX;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *ref = &b->units[i];
        if (!ref->health || ref->team != u->team || !e->types[ref->type].refinery || !contains(e->types[u->type].docks, b->types[ref->type].id)) continue;
        if (m->refinery && m->refinery != ref->id) continue;
        if (e->state.dock_owner[i] && e->state.dock_owner[i] != u->id) continue;
        uint32_t total = 2 * (b->types[ref->type].foundation_width + b->types[ref->type].foundation_height) + 4;
        for (uint32_t n = 0; n < total; ++n)
        {
            uint32_t cell = perimeter(b, ref, n);
            if (cell == UINT32_MAX || !ra_battle_passable(b, cell) || (b->occupied[cell] && b->occupied[cell] != u->id) || b->bridges[cell] ||
                b->tiles[cell].height != b->tiles[ref->cell].height)
                continue;
            int64_t dx = (int64_t)(cell % b->width) - u->cell % b->width, dy = (int64_t)(cell / b->width) - u->cell / b->width;
            uint64_t score = (uint64_t)(dx * dx + dy * dy);
            if (score >= best) continue;
            if (!e->types[u->type].chrono && !ra_battle_route(b, u->id, cell)) continue;
            best = score;
            chosen = ref->id;
            target = cell;
        }
    }
    if (!chosen)
    {
        m->refinery = 0;
        return false;
    }
    m->refinery = chosen;
    e->state.dock_owner[chosen - 1] = u->id;
    goal(u, target);
    if (e->types[u->type].chrono && u->cell == u->next && !u->track_active)
    {
        battle_reservations_clear(b, u);
        if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
        u->cell = u->next = target;
        u->x = (int32_t)(target % b->width * RA_BATTLE_CELL);
        u->y = (int32_t)(target / b->width * RA_BATTLE_CELL);
        u->path_count = u->path_cursor = u->progress = 0;
        b->occupied[target] = u->id;
    }
    return true;
}
static void miners(ra_battle *b)
{
    ra_battle_economy *e = b->economy;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        uint32_t owner = e->state.dock_owner[i];
        if (owner && (!b->units[i].health || !b->units[owner - 1].health || !e->state.miners[owner - 1].active || e->state.miners[owner - 1].refinery != i + 1))
            e->state.dock_owner[i] = 0;
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_battle_unit *u = &b->units[i];
        ra_econ_miner *m = &e->state.miners[i];
        if (!u->health || !m->active || u->order != RA_ECON_HARVEST) continue;
        if (m->delay)
        {
            --m->delay;
            continue;
        }
        const ra_econ_type *t = &e->types[u->type];
        if (m->ore + m->gems >= t->storage) m->active = 2;
        if (m->active == 2)
        {
            if (!m->refinery || m->refinery > b->count || !b->units[m->refinery - 1].health || !e->state.dock_owner[m->refinery - 1])
            {
                if (m->refinery > b->count || (m->refinery && !b->units[m->refinery - 1].health)) m->refinery = 0;
                if (!dock(b, u, m))
                {
                    m->delay = 30;
                    continue;
                }
            }
            if (t->chrono && u->cell == u->next && !u->track_active && u->cell != u->goal && !dock(b, u, m)) continue;
            if (u->cell != u->next || u->cell != u->goal || u->track_active) continue;
            if (m->ore || m->gems)
            {
                /* 原版卸矿一次交付整车；按包分次卸货是扩展行为，不能套用到 1.006。 */
                uint64_t value = (uint64_t)m->gems * e->gem_value + (uint64_t)m->ore * e->ore_value;
                m->gems = m->ore = 0;
                ra_econ_house *h = &e->state.houses[u->team - 1];
                h->credits += value;
                h->earned += value;
                m->delay = e->unload_ticks - 1;
            }
            else
            {
                e->state.dock_owner[m->refinery - 1] = 0;
                m->refinery = 0;
                m->active = 1;
                m->destination = UINT32_MAX;
            }
            continue;
        }
        if (m->destination >= b->width * b->height || !(e->ore[m->destination] & 63))
        {
            uint64_t best = UINT64_MAX;
            m->destination = UINT32_MAX;
            for (uint32_t cell = 0; cell < b->width * b->height; ++cell)
            {
                if (!(e->ore[cell] & 63) || !ra_battle_passable(b, cell) || (b->occupied[cell] && b->occupied[cell] != u->id)) continue;
                int64_t dx = (int64_t)(cell % b->width) - u->cell % b->width, dy = (int64_t)(cell / b->width) - u->cell / b->width;
                uint64_t score = (uint64_t)(dx * dx + dy * dy);
                if (score < best && ra_battle_route(b, u->id, cell))
                {
                    best = score;
                    m->destination = cell;
                }
            }
            if (m->destination == UINT32_MAX)
            {
                if (m->ore + m->gems) m->active = 2;
                m->delay = 30;
                continue;
            }
        }
        goal(u, m->destination);
        if (u->cell != u->next || u->cell != u->goal || u->track_active) continue;
        uint8_t resource = e->ore[u->cell];
        if (!(resource & 63))
        {
            m->destination = UINT32_MAX;
            continue;
        }
        if (resource >> 6 == 2) ++m->gems;
        else ++m->ore;
        e->ore[u->cell] = (resource & 63) == 1 ? 0 : (uint8_t)(resource - 1);
        m->delay = e->harvest_ticks - 1;
    }
}
void battle_economy_step(ra_battle *b)
{
    if (!b->economy) return;
    queues(b);
    miners(b);
}
