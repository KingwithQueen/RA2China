#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

static void issue(battle_scene *s, const ra_map_object *object, const char *reason)
{
    scene_issue *entry = &s->issues[s->issue_count++];
    entry->line = object->source_line;
    snprintf(entry->type, sizeof(entry->type), "%s", object->type);
    snprintf(entry->reason, sizeof(entry->reason), "%s", reason);
}
static uint32_t house(battle_scene *s, const char *name, ra_error *error)
{
    for (uint32_t i = 0; i < s->house_count; ++i)
        if (ra_equal(s->houses[i].id, name)) return i + 1;
    if (!name || !*name || strlen(name) >= sizeof(s->houses[0].id) || s->house_count == RA_BATTLE_TEAMS)
    {
        ra_fail(error, RA_RANGE, 0, "scenario house capacity or identifier exceeded");
        return 0;
    }
    scene_house *result = &s->houses[s->house_count++];
    strcpy(result->id, name);
    const ra_ini_entry *country = ra_ini_get(&s->map.ini, name, "Country"), *credits = ra_ini_get(&s->map.ini, name, "Credits");
    snprintf(result->country, sizeof(result->country), "%s", country ? country->value : name);
    int64_t amount = 0;
    if (credits && ra_ini_integer(credits, &amount, NULL) && amount >= 0 && amount <= 10000000) result->credits = (uint32_t)amount * 100;
    return s->house_count;
}
static bool houses(battle_scene *s, ra_error *error)
{
    const ra_ini_entry *player = ra_ini_get(&s->map.ini, "Basic", "Player");
    if (!house(s, player && *player->value ? player->value : "Americans", error)) return false;
    for (size_t i = 0; i < s->map.ini.entry_count; ++i)
    {
        const ra_ini_entry *e = &s->map.ini.entries[i];
        if (ra_equal(e->section, "Houses") && ra_ini_get(&s->map.ini, e->section, e->key) == e && !house(s, e->value, error)) return false;
    }
    for (size_t i = 0; i < s->map.object_count; ++i)
        if (*s->map.objects[i].owner && !house(s, s->map.objects[i].owner, error)) return false;
    for (uint32_t i = 0; i < s->house_count; ++i)
    {
        s->battle.allies[i] = 1u << i;
        const ra_ini_entry *allies = ra_ini_get(&s->map.ini, s->houses[i].id, "Allies");
        if (!allies || strlen(allies->value) >= 512) continue;
        char text[512], *cursor;
        strcpy(text, allies->value);
        cursor = text;
        while (cursor && *cursor)
        {
            char *next = strchr(cursor, ',');
            if (next) *next++ = 0;
            const ra_ini_entry *name = ra_ini_get(&s->map.ini, "Houses", cursor);
            const char *id = name ? name->value : cursor;
            for (uint32_t j = 0; j < s->house_count; ++j)
                if (ra_equal(s->houses[j].id, id)) s->battle.allies[i] |= 1u << j;
            cursor = next;
        }
    }
    return true;
}

static bool flag(const ra_ini *ini, const char *id, const char *key)
{
    const ra_ini_entry *e = ra_ini_get(ini, id, key);
    return e && (ra_equal(e->value, "yes") || ra_equal(e->value, "true") || !strcmp(e->value, "1"));
}
bool battle_scene_people_types(battle_scene *s, ra_error *error)
{
    static const char *ids[] = {"HARV",   "CMIN",   "AMCV",   "SMCV",   "ENGINEER", "SENGINEER", "E1",     "E2",     "TANY",   "GACNST", "NACNST",
                                "GAPILE", "NAHAND", "GAWEAP", "GAAIRC", "GATECH",   "GAPOWR",    "GAREFN", "NARADR", "NATECH", "NAYARD", "GAYARD"};
    ra_battle *b = &s->battle;
    for (uint32_t i = 0; i < sizeof(ids) / sizeof(ids[0]); ++i)
    {
        if (ra_economy_type(b, ids[i]) != UINT32_MAX) continue;
        if (!ra_battle_type_add(b, ids[i], "ra2.neutral", 1, error)) return false;
        uint32_t type = b->type_count - 1;
        if (i >= 9)
        {
            if (!ra_battle_structure_rules(b, type, &s->voxels.rules, &s->map.ini, &s->voxels.art, error)) return false;
        }
        else
        {
            b->types[type].infantry = i >= 4;
            if (!ra_battle_type_rules(b, type, &s->voxels.rules, error)) return false;
            if (!b->types[type].infantry && !ra_battle_type_art(b, type, &s->voxels.rules, &s->voxels.art, error)) return false;
        }
    }
    if (s->campaign_mode)
    {
        static const char *mission_types[] = {"DRED", "V3",    "SAPC",   "LCRF",  "ORCA",   "ZEP",      "SHAD", "CARGOPLANE",
                                              "ADOG", "GHOST", "CIVBFM", "CIVBF", "CIVBTM", "V3ROCKET", "DMISL"};
        for (uint32_t i = 0; i < sizeof(mission_types) / sizeof(mission_types[0]); ++i)
        {
            if (ra_economy_type(b, mission_types[i]) != UINT32_MAX) continue;
            if (!ra_battle_type_add(b, mission_types[i], "ra2.neutral", 1, error)) return false;
            uint32_t type = b->type_count - 1;
            b->types[type].infantry = i >= 8 && i <= 12;
            if (!ra_battle_type_rules(b, type, &s->voxels.rules, error)) return false;
            if (!b->types[type].infantry && !ra_battle_type_art(b, type, &s->voxels.rules, &s->voxels.art, error))
            {
                /* 原版飞机及运输工具允许省略炮口，以模型原点作为未指定的偏移。 */
                if (error && error->code != RA_NOT_FOUND) return false;
                if (error) memset(error, 0, sizeof(*error));
            }
        }
    }
    if (s->campaign_mode)
    {
        static const char *civilian[] = {"STANG", "LIMO", "SUVB", "PTRUCK", "CONA", "SUVW", "COP", "TRUCKA", "TRUCKB"};
        for (uint32_t i = 0; i < sizeof(civilian) / sizeof(civilian[0]); ++i)
        {
            if (ra_economy_type(b, civilian[i]) != UINT32_MAX) continue;
            if (!ra_battle_type_add(b, civilian[i], "ra2.neutral", 1, error)) return false;
            uint32_t type = b->type_count - 1;
            if (!ra_battle_type_rules(b, type, &s->voxels.rules, error) || !ra_battle_type_art(b, type, &s->voxels.rules, &s->voxels.art, error)) return false;
        }
    }
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        const ra_ini_entry *deploy = ra_ini_get(&s->voxels.rules, b->types[i].id, "DeploysInto");
        if (deploy)
        {
            uint32_t target = ra_economy_type(b, deploy->value);
            if (target == UINT32_MAX) return ra_fail(error, RA_NOT_FOUND, deploy->line, "MCV deployment type is not registered");
            b->types[i].deploy_type = target + 1;
        }
        b->types[i].capturable = flag(&s->voxels.rules, b->types[i].id, "Capturable");
        b->types[i].bridge_hut = flag(&s->voxels.rules, b->types[i].id, "BridgeRepairHut");
        b->types[i].insignificant = flag(&s->voxels.rules, b->types[i].id, "Insignificant");
        if (s->campaign_mode && (ra_equal(b->types[i].id, "GAPILL") || ra_equal(b->types[i].id, "NALASR") || ra_equal(b->types[i].id, "NASAM")))
        {
            if (!ra_battle_type_rules(b, i, &s->voxels.rules, error)) return false;
            if (!ra_battle_type_art(b, i, &s->voxels.rules, &s->voxels.art, error) && error && error->code != RA_NOT_FOUND) return false;
        }
    }
    return true;
}
static void object_tag(battle_scene *s, const ra_map_object *object, ra_battle_unit *u)
{
    for (size_t i = 0; i < s->map.ini.entry_count; ++i)
    {
        const ra_ini_entry *entry = &s->map.ini.entries[i];
        if (entry->line != object->source_line || strlen(entry->value) >= 2048) continue;
        char text[2048], *fields[24], *cursor;
        uint32_t count = 0;
        strcpy(text, entry->value);
        cursor = text;
        while (cursor && count < 24)
        {
            fields[count++] = cursor;
            char *next = strchr(cursor, ',');
            if (next) *next++ = 0;
            cursor = next;
        }
        uint32_t at = object->kind == RA_MAP_STRUCTURE ? 6 : object->kind == RA_MAP_INFANTRY ? 8 : 7;
        if (count > at) u->tag = ra_campaign_tag(&s->battle, &s->map.ini, fields[at]);
        if (object->kind == RA_MAP_INFANTRY && count > 5)
        {
            uint32_t requested = (uint32_t)strtoul(fields[5], NULL, 10);
            bool used = false;
            for (uint32_t j = 0; j + 1 < s->battle.count; ++j)
                if (s->battle.units[j].health && s->battle.types[s->battle.units[j].type].infantry && s->battle.units[j].cell == u->cell &&
                    s->battle.units[j].subcell == requested)
                    used = true;
            if (requested < 5 && !used) u->subcell = requested;
        }
        uint32_t mission = object->kind == RA_MAP_INFANTRY ? 6 : 6;
        if (object->kind != RA_MAP_STRUCTURE && count > mission)
            u->order = ra_equal(fields[mission], "Guard") || ra_equal(fields[mission], "Area Guard") ? RA_ORDER_GUARD : RA_ORDER_STOP;
        return;
    }
}
bool battle_scene_import(battle_scene *s, ra_error *error)
{
    ra_battle *b = &s->battle;
    size_t count = s->map.object_count;
    s->issues = calloc(count ? count : 1, sizeof(*s->issues));
    uint32_t *types = malloc((count ? count : 1) * sizeof(*types));
    if (!s->issues || !types)
    {
        free(types);
        return ra_fail(error, RA_MEMORY, 0, "scenario object allocation failed");
    }
    if (!houses(s, error)) goto fail;
    for (size_t i = 0; i < count; ++i)
    {
        const ra_map_object *object = &s->map.objects[i];
        types[i] = UINT32_MAX;
        if (object->kind == RA_MAP_STRUCTURE)
        {
            uint32_t type;
            for (type = 2; type < b->type_count; ++type)
                if (!strcmp(b->types[type].id, object->type)) break;
            if (type == b->type_count)
            {
                ra_error failure = {0};
                if (!ra_battle_type_add(b, object->type, "ra2.neutral", 1, &failure))
                {
                    issue(s, object, failure.message);
                    continue;
                }
                if (!ra_battle_structure_rules(b, type, &s->voxels.rules, &s->map.ini, &s->voxels.art, &failure))
                {
                    --b->type_count;
                    memset(&b->types[type], 0, sizeof(b->types[type]));
                    issue(s, object, failure.message);
                    continue;
                }
            }
            types[i] = type;
        }
        else if (object->kind == RA_MAP_UNIT && (!strcmp(object->type, "MTNK") || !strcmp(object->type, "HTNK")))
            types[i] = strcmp(object->type, "MTNK") ? 1u : 0u;
        else if (object->kind == RA_MAP_UNIT || object->kind == RA_MAP_INFANTRY || object->kind == RA_MAP_AIRCRAFT)
            issue(s, object, "object behavior is not implemented; original INI retained");
    }
    if (s->campaign_mode)
    {
        if (!battle_scene_people_types(s, error)) goto fail;
        for (size_t i = 0; i < count; ++i)
        {
            const ra_map_object *o = &s->map.objects[i];
            if (o->kind == RA_MAP_INFANTRY || o->kind == RA_MAP_UNIT) types[i] = ra_economy_type(b, o->type);
        }
        const char *names[RA_BATTLE_TEAMS], *countries[RA_BATTLE_TEAMS];
        for (uint32_t i = 0; i < s->house_count; ++i)
        {
            names[i] = s->houses[i].id;
            countries[i] = s->houses[i].country;
        }
        if (!ra_campaign_open(b, &s->voxels.rules, names, countries, s->house_count, error) || !ra_economy_open(b, &s->voxels.rules, error)) goto fail;
        for (uint32_t i = 0; i < s->house_count; ++i)
        {
            const char *country = s->houses[i].country;
            const ra_ini_entry *parent = ra_ini_get(&s->map.ini, country, "ParentCountry"), *tech = ra_ini_get(&s->map.ini, s->houses[i].id, "TechLevel");
            uint32_t level = tech ? (uint32_t)strtoul(tech->value, NULL, 10) : 10;
            if (!ra_economy_house(b, i + 1, parent ? parent->value : country, s->houses[i].credits, level > 10 ? 10 : level, error)) goto fail;
        }
        /* 先前预览模式的待实现记录重新按本轮覆盖生成。 */
        s->issue_count = 0;
        for (size_t i = 0; i < count; ++i)
        {
            const ra_map_object *o = &s->map.objects[i];
            if (types[i] == UINT32_MAX && (o->kind == RA_MAP_UNIT || o->kind == RA_MAP_INFANTRY || o->kind == RA_MAP_AIRCRAFT || o->kind == RA_MAP_STRUCTURE))
            {
                issue(s, o, "object behavior is not implemented; original INI retained");
                uint32_t team = house(s, o->owner, error);
                if (team)
                {
                    if (o->kind == RA_MAP_STRUCTURE) ++b->campaign->incomplete_buildings[team - 1];
                    else ++b->campaign->incomplete_units[team - 1];
                }
            }
        }
    }
    /* 先登记全部类型，再建立对象；稳定编号沿用地图对象顺序，不能由资源完成时间决定。 */
    for (size_t i = 0; i < count; ++i)
    {
        const ra_map_object *object = &s->map.objects[i];
        if (types[i] == UINT32_MAX) continue;
        uint32_t team = house(s, object->owner, error);
        if (!team) goto fail;
        ra_error failure = {0};
        bool added = object->kind == RA_MAP_STRUCTURE ? ra_battle_spawn_structure(b, types[i], team, (uint32_t)object->x, (uint32_t)object->y, &failure)
                                                      : ra_battle_spawn_team(b, types[i], team, (uint32_t)object->x, (uint32_t)object->y, &failure);
        if (!added)
        {
            issue(s, object, failure.message);
            if (b->campaign)
            {
                if (object->kind == RA_MAP_STRUCTURE) ++b->campaign->incomplete_buildings[team - 1];
                else ++b->campaign->incomplete_units[team - 1];
            }
            continue;
        }
        ra_battle_unit *unit = &b->units[b->count - 1];
        s->unit_source_lines[b->count - 1] = object->source_line;
        unit->health = (uint32_t)((uint64_t)b->types[types[i]].strength * object->health / 256);
        if (object->health && !unit->health) unit->health = 1;
        unit->body = unit->turret = (ra_battle_turn){object->facing * 256, object->facing * 256, 0, 0};
        if (!unit->health)
        {
            battle_structure_release(b, unit);
            if (b->occupied[unit->cell] == unit->id) b->occupied[unit->cell] = 0;
        }
        const ra_ini_entry *immune = ra_ini_get(&s->voxels.rules, object->type, "Immune");
        if (immune && ra_equal(immune->value, "yes")) unit->traits |= RA_UNIT_IMMUNE;
        if (s->campaign_mode) object_tag(s, object, unit);
        b->initial[b->count - 1] = *unit;
        if (object->kind == RA_MAP_STRUCTURE)
        {
            ++s->structure_count;
            if (ra_ini_get(&s->voxels.rules, object->type, "Primary")) ++s->pending_weapons;
        }
        else ++s->imported_units;
    }
    if (s->campaign_mode)
    {
        for (uint32_t cell = 0; cell < b->width * b->height; ++cell)
        {
            const char *name = s->map.overlay && s->map.overlay[cell] < s->maps.overlay_name_count ? s->maps.overlay_names[s->map.overlay[cell]] : "";
            uint32_t kind = !strncmp(name, "GEM", 3) ? 2 : !strncmp(name, "TIB", 3) || !strncmp(name, "GOLD", 4) ? 1 : 0;
            if (kind && !ra_economy_ore(b, cell, kind, (uint32_t)s->map.overlay_data[cell] + 1, error)) goto fail;
        }
        if (!battle_scene_economy_images(s, error)) goto fail;
    }
    free(types);
    return true;
fail:
    free(types);
    return false;
}

void battle_scene_structures_clear(battle_scene *s)
{
    if (s->structure_visuals)
        for (size_t i = 0; i < RA_BATTLE_TYPES; ++i) structure_visual_close(&s->structure_visuals[i]);
    for (size_t i = 0; i < 96; ++i)
    {
        ra_voxel_image_close(&s->structure_sprites[i].image);
        memset(&s->structure_sprites[i], 0, sizeof(s->structure_sprites[i]));
    }
    s->sprite_clock = 0;
}

const ra_voxel_image *battle_scene_structure_sprite(battle_scene *s, const ra_battle_unit *u, ra_error *error)
{
    if (!s->structure_visuals || u->type >= s->battle.type_count || !s->battle.types[u->type].structure) return NULL;
    structure_visual *visual = &s->structure_visuals[u->type];
    if (visual->failed) return NULL;
    const ra_ini_entry *override_image = ra_ini_get(&s->map.ini, s->battle.types[u->type].id, "Image");
    /* 平民建筑位于 isotemp/isosnow/isourb；借用地图的完整挂载，浅拷贝不取得所有权。 */
    voxel_context resources = s->voxels;
    resources.vfs = s->maps.vfs;
    if (!visual->opened && !structure_visual_open(visual, &resources, s->battle.types[u->type].id, override_image ? override_image->value : NULL,
                                                  map_theater_id(s->map.theater), error))
        return NULL;
    uint32_t state = (uint64_t)u->health * 2 <= s->battle.types[u->type].strength, frame = s->battle.tick / 3;
    if (u->gate_open_until) frame |= 0x80000000u;
    structure_sprite *chosen = &s->structure_sprites[0];
    for (size_t i = 0; i < 96; ++i)
    {
        structure_sprite *entry = &s->structure_sprites[i];
        if (entry->occupied && entry->type == u->type && entry->team == u->team && entry->state == state && entry->frame == frame)
        {
            entry->used = ++s->sprite_clock;
            return &entry->image;
        }
        if (!entry->occupied || entry->used < chosen->used) chosen = entry;
    }
    ra_voxel_image_close(&chosen->image);
    chosen->occupied = false;
    const ra_palette *palette = visual->terrain_palette ? &s->maps.theaters[map_theater_id(s->map.theater)].palette : &s->voxels.palette;
    structure_visual pose = *visual;
    if (u->gate_open_until && pose.count && pose.layers[0].shape.count >= 9) pose.layers[0].first = pose.layers[0].last = 8;
    if (!structure_visual_render(&pose, palette, &s->battle.types[u->type], u->team, state != 0, s->battle.tick, &chosen->image, error)) return NULL;
    chosen->type = u->type;
    chosen->team = u->team;
    chosen->state = state;
    chosen->frame = frame;
    chosen->used = ++s->sprite_clock;
    chosen->occupied = true;
    return &chosen->image;
}

bool battle_scene_base_fixture(battle_scene *s, uint32_t *target, ra_error *error)
{
    ra_battle *b = &s->battle;
    if (b->tick || !target || s->scenario) return ra_fail(error, RA_ARGUMENT, 0, "base fixture requires a fresh prototype map");
    b->count = 0;
    memset(b->occupied, 0, (size_t)2 * b->width * b->height * sizeof(*b->occupied));
    static const char *ids[] = {"GAPOWR", "GAPILE", "GACNST", "NAPOWR", "NAHAND", "NACNST"};
    for (uint32_t i = 0; i < 6; ++i)
        if (!ra_battle_type_add(b, ids[i], i < 3 ? "ra2.allied" : "ra2.soviet", 1, error) ||
            !ra_battle_structure_rules(b, i + 2, &s->voxels.rules, NULL, &s->voxels.art, error))
            return false;
    for (uint32_t y = 12; y + 18 < b->height; ++y)
        for (uint32_t x = 12; x + 22 < b->width; ++x)
        {
            bool clear = true;
            uint32_t height = b->tiles[y * b->width + x].height;
            for (uint32_t row = 0; row < 16 && clear; ++row)
                for (uint32_t column = 0; column < 20; ++column)
                {
                    uint32_t cell = (y + row) * b->width + x + column;
                    if (!ra_battle_passable(b, cell) || b->tiles[cell].ramp || b->tiles[cell].height != height || b->bridges[cell]) clear = false;
                }
            if (!clear) continue;
            /* 双基地是显式开发夹具，不作为原版遭遇战的开局规则。 */
            for (uint32_t i = 0; i < 6; ++i)
                if (!ra_battle_spawn_structure(b, i + 2, i < 3 ? 1u : 2u, x + (i % 3) * 6, y + (i < 3 ? 0u : 10u), error)) return false;
            if (!ra_battle_spawn_team(b, 0, 1, x + 1, y + 6, error) || !ra_battle_spawn_team(b, 1, 1, x + 5, y + 6, error)) return false;
            s->structure_count = 6;
            *target = 4;
            return true;
        }
    return ra_fail(error, RA_NOT_FOUND, 0, "map has no clear base fixture area");
}
