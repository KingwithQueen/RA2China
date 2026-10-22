#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

static uint32_t ore_kind(const battle_scene *s, uint32_t cell)
{
    unsigned overlay = s->map.overlay[cell];
    const char *name = overlay < s->maps.overlay_name_count ? s->maps.overlay_names[overlay] : "";
    if (!strncmp(name, "GEM", 3)) return 2;
    return !strncmp(name, "TIB", 3) || !strncmp(name, "GOLD", 4) ? 1 : 0;
}
bool battle_scene_economy_images(battle_scene *s, ra_error *error)
{
    /* 矿藏使用专用调色板，不能套用地形或阵营调色板。 */
    if (!ra_asset_palette(&s->maps.vfs, "temperat.pal", &s->ore_palette, error)) return false;
    static const char *names[] = {"tib01", "gem01"}, *extensions[] = {"tem", "sno", "urb"};
    for (uint32_t i = 0; i < 2; ++i)
    {
        free(s->ore_pixels[i]);
        s->ore_pixels[i] = NULL;
        ra_shp_close(&s->ore_shapes[i]);
        ra_resource_close(&s->ore_bytes[i]);
        char name[64];
        snprintf(name, sizeof(name), "%s.%s", names[i], extensions[map_theater_id(s->map.theater)]);
        if (!ra_vfs_read(&s->maps.vfs, name, &s->ore_bytes[i], error))
        {
            snprintf(name, sizeof(name), "%s.shp", names[i]);
            if (!ra_vfs_read(&s->maps.vfs, name, &s->ore_bytes[i], error)) return false;
        }
        if (!ra_shp_open(&s->ore_shapes[i], s->ore_bytes[i].view, error)) return false;
        const ra_shp *shape = &s->ore_shapes[i];
        size_t area = (size_t)shape->width * shape->height;
        if (!area || shape->count > 16777216 / area) return ra_fail(error, RA_RANGE, 0, "ore sprite exceeds cache limit");
        s->ore_pixels[i] = malloc(area * shape->count);
        if (!s->ore_pixels[i]) return ra_fail(error, RA_MEMORY, 0, "ore sprite allocation failed");
        for (uint32_t frame = 0; frame < shape->count; ++frame)
            if (!ra_shp_decode(shape, frame, s->ore_pixels[i] + frame * area, area, error)) return false;
    }
    return true;
}
bool battle_scene_economy_fixture(battle_scene *s, ra_error *error)
{
    ra_battle *b = &s->battle;
    static const char *ids[] = {"HARV",   "CMIN",   "GACNST", "GAPOWR", "GAPILE", "GAREFN", "GAWEAP", "GAAIRC",
                                "GATECH", "NACNST", "NAPOWR", "NAHAND", "NAREFN", "NAWEAP", "NARADR", "NATECH"};
    if (b->count || b->type_count != 2 || s->scenario) return ra_fail(error, RA_ARGUMENT, 0, "economy fixture requires a fresh prototype map");
    for (uint32_t i = 0; i < sizeof(ids) / sizeof(ids[0]); ++i)
    {
        const char *faction = i == 0 || i >= 9 ? "ra2.soviet" : "ra2.allied";
        if (!ra_battle_type_add(b, ids[i], faction, 1, error)) return false;
        uint32_t type = b->type_count - 1;
        if (i < 2)
        {
            if (!ra_battle_type_rules(b, type, &s->voxels.rules, error) || !ra_battle_type_art(b, type, &s->voxels.rules, &s->voxels.art, error)) return false;
        }
        else if (!ra_battle_structure_rules(b, type, &s->voxels.rules, NULL, &s->voxels.art, error)) return false;
    }
    if (s->mcv_mode && !battle_scene_people_types(s, error)) return false;
    if (!ra_economy_open(b, &s->voxels.rules, error) || !ra_economy_house(b, 1, s->economy_allied ? "Americans" : "Russians", 10000, 10, error)) return false;
    for (uint32_t cell = 0; cell < b->width * b->height; ++cell)
    {
        uint32_t kind = ore_kind(s, cell);
        if (kind && (s->map.overlay_data[cell] >= 63 || !ra_economy_ore(b, cell, kind, (uint32_t)s->map.overlay_data[cell] + 1, error)))
            return ra_fail(error, RA_RANGE, 0, "unsupported ore density index");
    }
    uint32_t chosen = UINT32_MAX, best = UINT32_MAX;
    for (size_t i = 0; i < s->map.cell_count; ++i)
    {
        uint32_t x = s->map.cells[i].x, y = s->map.cells[i].y, cell = y * b->width + x;
        if (x + 10 >= b->width || y + 10 >= b->height || x < 3 || y < 3) continue;
        bool clear = true;
        for (uint32_t row = 0; row < 8 && clear; ++row)
            for (uint32_t col = 0; col < 8; ++col)
            {
                uint32_t at = cell + row * b->width + col;
                if (!ra_battle_passable(b, at) || b->bridges[at] || b->tiles[at].ramp || b->tiles[at].height != b->tiles[cell].height || b->economy->ore[at])
                {
                    clear = false;
                    break;
                }
            }
        if (!clear) continue;
        uint32_t nearest = 10000;
        for (int dy = -16; dy <= 16; ++dy)
            for (int dx = -16; dx <= 16; ++dx)
            {
                int ox = (int)x + dx, oy = (int)y + dy;
                if (ox < 0 || oy < 0 || ox >= (int)b->width || oy >= (int)b->height) continue;
                if (b->economy->ore[(uint32_t)oy * b->width + (uint32_t)ox] && (uint32_t)(abs(dx) + abs(dy)) < nearest) nearest = (uint32_t)(abs(dx) + abs(dy));
            }
        if (nearest < best)
        {
            best = nearest;
            chosen = cell;
        }
        if (best <= 4) break;
    }
    if (chosen == UINT32_MAX) return ra_fail(error, RA_NOT_FOUND, 0, "no economy fixture foundation found");
    uint32_t yard = ra_economy_type(b, s->economy_allied ? "GACNST" : "NACNST");
    bool yard_added =
        s->mcv_mode ? ra_battle_spawn_team(b, ra_economy_type(b, s->economy_allied ? "AMCV" : "SMCV"), 1, chosen % b->width + 1, chosen / b->width + 1, error)
                    : ra_battle_spawn_structure(b, yard, 1, chosen % b->width, chosen / b->width, error);
    if (!yard_added || !ra_battle_spawn_team(b, s->economy_allied ? 0 : 1, 1, chosen % b->width + 5, chosen / b->width + 5, error)) return false;
    s->structure_count = 1;
    s->house_count = 1;
    strcpy(s->houses[0].id, s->economy_allied ? "Americans" : "Russians");
    strcpy(s->houses[0].country, s->houses[0].id);
    s->houses[0].credits = 10000;
    return battle_scene_economy_images(s, error);
}
bool battle_scene_economy_report(const battle_scene *s, const char *path, ra_error *error)
{
    char bytes[16384], rules[41], map[41];
    uint8_t digest[20];
    const ra_battle *b = &s->battle;
    if (!b->economy) return ra_fail(error, RA_ARGUMENT, 0, "economy report requires an economy scene");
    ra_sha1(s->voxels.rule_bytes.view, digest);
    ra_hex(digest, 20, rules);
    ra_sha1(s->maps.sources[s->source].bytes, digest);
    ra_hex(digest, 20, map);
    size_t used = (size_t)snprintf(bytes, sizeof(bytes), "{\"rules_sha1\":\"%s\",\"map_sha1\":\"%s\",\"types\":[", rules, map);
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        const ra_econ_type *t = &b->economy->types[i];
        const ra_battle_type *type = &b->types[i];
        int added = snprintf(bytes + used, sizeof(bytes) - used,
                             "%s{\"id\":\"%s\",\"cost\":%u,\"ticks\":%u,\"tech\":%d,\"storage\":%u,\"factory\":%u,\"adjacent\":%u,\"power\":%d,\"foundation\":["
                             "%u,%u],\"harvester\":%s,\"chrono\":%s}",
                             i ? "," : "", type->id, t->cost, t->ticks, t->tech, t->storage, t->factory, t->adjacent, type->power, type->foundation_width,
                             type->foundation_height, t->harvester ? "true" : "false", t->chrono ? "true" : "false");
        if (added < 0 || (size_t)added >= sizeof(bytes) - used) return ra_fail(error, RA_RANGE, 0, "economy report exceeds capacity");
        used += (size_t)added;
    }
    uint32_t cells[2] = {0}, amounts[2] = {0}, max_density = 0;
    for (uint32_t cell = 0; cell < b->width * b->height; ++cell)
    {
        uint8_t resource = b->economy->initial_ore[cell];
        if (!(resource & 63)) continue;
        uint32_t kind = (resource >> 6) - 1;
        ++cells[kind];
        amounts[kind] += resource & 63;
        if (s->map.overlay_data[cell] > max_density) max_density = s->map.overlay_data[cell];
    }
    int added = snprintf(bytes + used, sizeof(bytes) - used,
                         "],\"ore_cells\":%u,\"gem_cells\":%u,\"ore_amount\":%u,\"gem_amount\":%u,\"max_density_index\":%u,\"ore_frames\":%u,\"gem_frames\":%u,"
                         "\"calibrated_runtime\":false,\"complete_campaign\":false,\"complete_skirmish\":false}\n",
                         cells[0], cells[1], amounts[0], amounts[1], max_density, s->ore_shapes[0].count, s->ore_shapes[1].count);
    if (added < 0 || (size_t)added >= sizeof(bytes) - used) return ra_fail(error, RA_RANGE, 0, "economy report exceeds capacity");
    return battle_file_write(path, bytes, used + (size_t)added, error);
}
