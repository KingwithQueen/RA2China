#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include "battle_internal.h"
#include <float.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

static const char *land_names[12] = {"Clear", "Road", "Water", "Rock", "Wall", "Tiberium", "Beach", "Rough", "Ice", "Railroad", "Tunnel", "Weeds"};
static const char *unit_names[26] = {"MTNK", "HTNK",   "HARV",   "CMIN", "AMCV", "SMCV", "STANG", "LIMO", "SUVB", "PTRUCK", "CONA",       "SUVW",     "COP",
                                     "HTK",  "TRUCKA", "TRUCKB", "V3",   "DRED", "SAPC", "LCRF",  "ORCA", "ZEP",  "SHAD",   "CARGOPLANE", "V3ROCKET", "DMISL"};

static bool yes(const ra_ini *ini, const char *section, const char *key)
{
    const ra_ini_entry *e = ra_ini_get(ini, section, key);
    return e && (ra_equal(e->value, "yes") || ra_equal(e->value, "true") || !strcmp(e->value, "1"));
}

bool battle_file_write(const char *path, const void *data, size_t size, ra_error *error)
{
    FILE *file;
    bool ok;
#ifdef _WIN32
    wchar_t wide[32768];
    if (!path || !MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, wide, 32768)) return ra_fail(error, RA_ARGUMENT, 0, "invalid UTF-8 output path");
    file = _wfopen(wide, L"wb");
#else
    file = fopen(path, "wb");
#endif
    if (!file) return ra_fail(error, RA_IO, 0, "cannot create output file");
    ok = fwrite(data, 1, size, file) == size;
    if (fclose(file)) ok = false;
    return ok || ra_fail(error, RA_IO, 0, "output file write failed");
}

void battle_scene_close(battle_scene *s)
{
    size_t i, j, k, team;
    if (!s) return;
    battle_scene_structures_clear(s);
    battle_scene_infantry_clear(s);
    free(s->structure_visuals);
    free(s->issues);
    for (i = 0; i < 26; ++i)
    {
        for (team = 0; team < 2; ++team)
            for (j = 0; j < 32; ++j)
                for (k = 0; k < 32; ++k) ra_voxel_image_close(&s->sprites[i][team][j][k]);
        voxel_scene_close(&s->models[i]);
    }
    for (i = 0; i < 2; ++i)
    {
        free(s->ore_pixels[i]);
        ra_shp_close(&s->ore_shapes[i]);
        ra_resource_close(&s->ore_bytes[i]);
    }
    ra_battle_close(&s->battle);
    for (i = 0; i < RA_BATTLE_UNITS; ++i) ra_voxel_image_close(&s->slope_sprites[i]);
    ra_shp_close(&s->impact);
    ra_resource_close(&s->impact_bytes);
    free(s->impact_pixels);
    map_image_close(&s->ground);
    map_image_close(&s->deck);
    free(s->deck_heights);
    ra_map_close(&s->map);
    voxel_context_close(&s->voxels);
    map_context_close(&s->maps);
    memset(s, 0, sizeof(*s));
}

bool battle_scene_open(battle_scene *s, const char *original, ra_error *error)
{
    size_t i;
    s->structure_visuals = calloc(RA_BATTLE_TYPES, sizeof(*s->structure_visuals));
    if (!s->structure_visuals) return ra_fail(error, RA_MEMORY, 0, "structure visual allocation failed");
    if (!map_context_open(&s->maps, original, NULL, error) || !voxel_context_open(&s->voxels, original, NULL, error)) return false;
    for (i = 0; i < 2; ++i)
    {
        voxel_scene *model = &s->models[i];
        if (!voxel_scene_load(model, &s->voxels, unit_names[i], true, error)) return false;
    }
    if (!ra_vfs_read(&s->voxels.vfs, "s_clsn16.shp", &s->impact_bytes, error) || !ra_shp_open(&s->impact, s->impact_bytes.view, error)) return false;
    if (!ra_asset_palette(&s->voxels.vfs, "anim.pal", &s->impact_palette, error)) return false;
    size_t frame_size = (size_t)s->impact.width * s->impact.height;
    if (!frame_size || frame_size > 16777216 / s->impact.count) return ra_fail(error, RA_RANGE, 0, "impact animation exceeds cache limit");
    s->impact_pixels = malloc(frame_size * s->impact.count);
    if (!s->impact_pixels) return ra_fail(error, RA_MEMORY, 0, "impact animation allocation failed");
    for (i = 0; i < s->impact.count; ++i)
        if (!ra_shp_decode(&s->impact, i, s->impact_pixels + i * frame_size, frame_size, error)) return false;
    return true;
}

const ra_voxel_image *battle_scene_sprite(battle_scene *s, const ra_battle_unit *u, ra_error *error)
{
    if (s->battle.types[u->type].infantry) return battle_scene_infantry_sprite(s, u, error);
    uint32_t body = ((ra_battle_turn_value(&u->body, s->battle.tick) + 1024) & 65535) / 2048;
    uint32_t turret = ((ra_battle_turn_value(&u->turret, s->battle.tick) + 1024) & 65535) / 2048;
    uint32_t ramp = ra_battle_unit_ramp(&s->battle, u);
    uint32_t key = (((u->type * 2 + (u->team == 1 ? 0 : 1)) * 21 + ramp) * 32 + body) * 32 + turret;
    uint32_t bits[12];
    float chassis[12];
    if (!ra_battle_chassis(ramp, body * 2048, bits)) return NULL;
    memcpy(chassis, bits, sizeof(chassis));
    ra_voxel_image *image;
    ra_voxel_camera camera = {0};
    voxel_scene *model;
    uint32_t model_index;
    for (model_index = 0; model_index < 26; ++model_index)
        if (ra_equal(s->battle.types[u->type].id, unit_names[model_index])) break;
    if (model_index == 26) return NULL;
    if (!s->models[model_index].count && !voxel_scene_load(&s->models[model_index], &s->voxels, unit_names[model_index], true, error)) return NULL;
    size_t frame = s->models[model_index].frames > 1 ? (s->battle.tick / 2) % s->models[model_index].frames : 0;
    key = key * (uint32_t)(s->models[model_index].frames ? s->models[model_index].frames : 1) + (uint32_t)frame;
    image = &s->sprites[model_index][u->team == 1 ? 0 : 1][body][turret];
    if ((ramp || s->models[model_index].frames > 1) && u->id && u->id <= RA_BATTLE_UNITS)
    {
        image = &s->slope_sprites[u->id - 1];
        if (s->slope_keys[u->id - 1] != key) ra_voxel_image_close(image);
        s->slope_keys[u->id - 1] = key;
    }
    if (image->pixels) return image;
    model = &s->models[model_index];
    for (size_t i = 1; i < model->count; ++i)
    {
        /* 模拟方向顺时针增大，模型旋转相反；偏移跟随车身，不能跟随炮塔转动。 */
        model->parts[i].yaw = ((float)body - (float)turret) * 11.25f;
        model->parts[i].offset[0] = (float)s->battle.types[u->type].turret_offset * (30.0f * 1.4142135623730951f / (256.0f * 12.0f));
    }
    camera.yaw = 45;
    camera.pitch = 30;
    camera.zoom = 1;
    camera.pixels_per_unit = 12;
    camera.origin_x = model_index >= 16 ? 96.0f : 64.0f;
    camera.origin_y = model_index >= 16 ? 120.0f : 80.0f;
    camera.world_axes = true;
    camera.light_yaw = -60;
    camera.use_vpl = camera.remap = true;
    camera.section = -1;
    camera.house_color = u->team == 1 ? (ra_rgb){70, 155, 245} : (ra_rgb){235, 65, 55};
    if (!ra_voxel_image_create(image, model_index >= 16 ? 192 : 128, model_index >= 16 ? 160 : 112, error) ||
        !ra_voxel_render_chassis(model->parts, model->count, frame, &s->voxels.palette, &s->voxels.vpl, &camera, chassis, image, error))
    {
        ra_voxel_image_close(image);
        return NULL;
    }
    for (size_t i = 0; i < image->width * image->height; ++i) image->pixels[i] |= image->depth[i] == -FLT_MAX ? 0 : 0xff000000u;
    return image;
}

const ra_voxel_image *battle_scene_missile_sprite(battle_scene *s, const ra_battle_shot *shot, ra_error *error)
{
    if (!shot || !s->battle.types[shot->type].weapon.missile) return NULL;
    uint32_t type = ra_economy_type(&s->battle, s->battle.types[shot->type].weapon.missile == 1 ? "V3ROCKET" : "DMISL");
    if (type == UINT32_MAX) return NULL;
    ra_battle_unit model = {0};
    model.type = type;
    model.team = shot->team;
    model.x = shot->x;
    model.y = shot->y;
    uint32_t direction = battle_direction((int64_t)shot->end_x - shot->start_x, (int64_t)shot->end_y - shot->start_y);
    model.body = model.turret = (ra_battle_turn){direction, direction, 0, 0};
    return battle_scene_sprite(s, &model, error);
}

static void block(battle_scene *s, ra_battle_tile *tiles, int x, int y)
{
    if (x >= 0 && y >= 0 && x < 512 && y < 512 && !tiles[y * 512 + x].blocked)
    {
        tiles[y * 512 + x].blocked = 1;
        ++s->obstacles;
    }
}

int battle_bridge_draw_offset(uint32_t kind, uint32_t frame)
{
    /* 原版 1.006 的 475457 分支：高桥两个方向分别上移 16、31 像素。 */
    return kind < 2 ? (frame >= 9 && frame <= 17 ? -31 : -16) : 0;
}

static bool bridge_images(battle_scene *s, int theater, ra_error *error)
{
    static const char *extensions[3] = {"tem", "sno", "urb"};
    ra_shp shapes[2] = {0};
    ra_resource resources[2] = {0};
    uint8_t *pixels = NULL;
    bool ok = false;
    size_t count = (size_t)s->ground.width * s->ground.height;
    map_image_close(&s->deck);
    free(s->deck_heights);
    s->deck_heights = calloc(count, sizeof(*s->deck_heights));
    s->deck.width = s->ground.width;
    s->deck.height = s->ground.height;
    s->deck.pixels = calloc(count, sizeof(*s->deck.pixels));
    s->deck.picked = malloc(count * sizeof(*s->deck.picked));
    if (!s->deck.pixels || !s->deck.picked || !s->deck_heights) return ra_fail(error, RA_MEMORY, 0, "bridge image allocation failed");
    for (size_t i = 0; i < count; ++i) s->deck.picked[i] = -1;
    for (unsigned kind = 0; kind < 2; ++kind)
    {
        char name[32];
        snprintf(name, sizeof(name), "%s.%s", kind ? "bridgb" : "bridge", extensions[theater]);
        if (!ra_vfs_read(&s->maps.vfs, name, &resources[kind], error) || !ra_shp_open(&shapes[kind], resources[kind].view, error)) goto done;
    }
    pixels = malloc(512 * 512);
    if (!pixels)
    {
        ra_fail(error, RA_MEMORY, 0, "bridge frame allocation failed");
        goto done;
    }
    for (uint32_t i = 0; i < s->battle.bridge_count; ++i)
    {
        const ra_battle_bridge *part = &s->battle.bridge_parts[i];
        if (part->kind < 2 && part->frame == 255) continue;
        const ra_map_cell *cell = ra_map_at(&s->map, (int)(part->cell % 512), (int)(part->cell / 512));
        if (!cell) continue;
        ra_resource low_resource = {0};
        ra_shp low_shape = {0};
        const ra_shp *shape = &shapes[part->kind == 1 ? 1 : 0];
        map_image *target = &s->deck;
        unsigned frame = part->frame;
        if (part->kind >= 2)
        {
            char name[32];
            snprintf(name, sizeof(name), "%s%02u.%s", part->kind == 2 ? "lobrdg" : "lobrdb", part->frame, extensions[theater]);
            if (!ra_vfs_read(&s->maps.vfs, name, &low_resource, error) || !ra_shp_open(&low_shape, low_resource.view, error))
            {
                ra_resource_close(&low_resource);
                goto done;
            }
            shape = &low_shape;
            frame = 0;
            target = &s->ground;
        }
        bool valid = frame < shape->count && shape->width <= 512 && shape->height <= 512;
        bool decoded = valid && ra_shp_decode(shape, frame, pixels, 512 * 512, error);
        if (decoded)
        {
            int cx = ((int)cell->x - cell->y) * 30 + s->ground.origin_x + 30;
            int cy = ((int)cell->x + cell->y - cell->height) * 15 + s->ground.origin_y + 15;
            cy += battle_bridge_draw_offset(part->kind, part->frame);
            for (int y = 0; y < shape->height; ++y)
                for (int x = 0; x < shape->width; ++x)
                {
                    int px = cx - shape->width / 2 + x, py = cy - shape->height / 2 + y;
                    uint8_t index = pixels[(size_t)y * shape->width + x];
                    if (!index || px < 0 || py < 0 || px >= target->width || py >= target->height) continue;
                    ra_rgb rgb = s->maps.theaters[theater].palette.colors[index];
                    target->pixels[(size_t)py * target->width + px] = 0xff000000u | (uint32_t)rgb.r << 16 | (uint32_t)rgb.g << 8 | rgb.b;
                    if (target == &s->deck) s->deck_heights[(size_t)py * target->width + px] = s->battle.tiles[part->cell + 512 * 512].height;
                    ++target->drawn;
                }
        }
        ra_shp_close(&low_shape);
        ra_resource_close(&low_resource);
        if (!decoded)
        {
            if (!valid) ra_fail(error, RA_FORMAT, 0, "unsupported bridge image frame");
            goto done;
        }
    }
    for (size_t i = 0; i < s->map.cell_count; ++i)
    {
        const ra_map_cell *cell = &s->map.cells[i];
        uint32_t node = cell->y * 512 + cell->x + 512 * 512;
        if (!ra_battle_passable(&s->battle, node)) continue;
        int cx = ((int)cell->x - cell->y) * 30 + s->ground.origin_x + 30;
        int cy = ((int)cell->x + cell->y - s->battle.tiles[node].height) * 15 + s->ground.origin_y + 15;
        for (int y = -14; y <= 14; ++y)
            for (int x = -29; x <= 29; ++x)
            {
                if (abs(x) + abs(y) * 2 > 29) continue;
                int px = cx + x, py = cy + y;
                if (px >= 0 && py >= 0 && px < s->deck.width && py < s->deck.height) s->deck.picked[(size_t)py * s->deck.width + px] = (int32_t)node;
            }
    }
    ok = true;
done:
    free(pixels);
    for (unsigned kind = 0; kind < 2; ++kind)
    {
        ra_shp_close(&shapes[kind]);
        ra_resource_close(&resources[kind]);
    }
    return ok;
}

bool battle_scene_refresh(battle_scene *s, ra_error *error)
{
    if (s->ground.pixels && s->rendered_revision == s->battle.topology_revision) return true;
    int theater = map_theater_id(s->map.theater);
    ra_map visible = s->map;
    uint8_t *overlays = NULL;
    if (s->battle.economy)
    {
        size_t n = (size_t)s->battle.width * s->battle.height;
        overlays = malloc(n);
        if (!overlays) return ra_fail(error, RA_MEMORY, 0, "economy overlay allocation failed");
        memcpy(overlays, s->map.overlay, n);
        for (size_t i = 0; i < n; ++i)
            if (s->battle.economy->initial_ore[i] || s->battle.economy->ore[i]) overlays[i] = 255;
        visible.overlay = overlays;
    }
    bool rendered = map_render(&s->maps, &visible, &s->ground, true, !s->scenario, true, error);
    free(overlays);
    if (!rendered || !bridge_images(s, theater, error)) return false;
    s->rendered_revision = s->battle.topology_revision;
    return true;
}

static bool bridge_gaps(battle_scene *s, ra_error *error)
{
    ra_battle *b = &s->battle;
    uint32_t count = b->bridge_count;
    for (uint32_t i = 0; i < count; ++i)
    {
        const ra_battle_bridge p = b->bridge_parts[i];
        if (p.kind >= 2 || p.frame != (p.axis == 1 ? 8u : 16u)) continue;
        uint32_t stride = p.axis == 1 ? 1u : b->width, distance = 1;
        for (; distance <= 128; ++distance)
        {
            uint32_t cell = p.cell + distance * stride;
            if (cell >= b->width * b->height || (p.axis == 1 && cell / b->width != p.cell / b->width)) break;
            if (!ra_map_at(&s->map, (int)(cell % b->width), (int)(cell / b->width)) || b->tiles[cell].height != b->tiles[p.cell].height) break;
            uint32_t id = b->bridge_at[cell];
            if (!id) continue;
            const ra_battle_bridge *q = &b->bridge_parts[id - 1];
            if (q->kind == p.kind && q->axis == p.axis && q->frame == (p.axis == 1 ? 7u : 17u))
                for (uint32_t j = 1; j < distance; ++j)
                    if (!ra_battle_bridge_segment_add(b, p.cell + j * stride, p.axis, p.kind, 255, error)) return false;
            break;
        }
    }
    return true;
}

bool battle_scene_map(battle_scene *s, size_t source, bool graphics, ra_error *error)
{
    ra_battle_tile *tiles;
    uint16_t multipliers[12];
    uint8_t hashes[60], digest[20];
    ra_map *map = &s->map;
    int theater, spawn_x = 0, spawn_y = 0;
    size_t i;
    if (source >= s->maps.source_count) return ra_fail(error, RA_ARGUMENT, 0, "map index is invalid");
    battle_scene_structures_clear(s);
    battle_scene_infantry_clear(s);
    ra_ini_close(&s->voxels.rules);
    if (!ra_ini_parse(&s->voxels.rules, s->voxels.rule_bytes.view, "rules.ini", error)) return false;
    free(s->issues);
    s->issues = NULL;
    s->issue_count = s->structure_count = s->imported_units = s->pending_weapons = s->house_count = 0;
    memset(s->houses, 0, sizeof(s->houses));
    memset(s->unit_source_lines, 0, sizeof(s->unit_source_lines));
    ra_battle_close(&s->battle);
    ra_map_close(map);
    map_image_close(&s->ground);
    map_image_close(&s->deck);
    free(s->deck_heights);
    s->deck_heights = NULL;
    s->missing = s->obstacles = s->bridges = s->unsupported_foundations = s->low_bridges = s->pending_bridges = 0;
    s->source = source;
    s->rendered_revision = UINT32_MAX;
    if (!ra_map_open(map, s->maps.sources[source].bytes, s->maps.sources[source].source, error)) return false;
    theater = map_theater_id(map->theater);
    if (!map_theater_open(&s->maps, theater, error)) return false;
    static const char *unit_palettes[3] = {"unittem.pal", "unitsno.pal", "uniturb.pal"};
    if (!ra_asset_palette(&s->voxels.vfs, unit_palettes[theater], &s->voxels.palette, error)) return false;
    /* 三个剧场的单位调色板独立；切图时不能复用旧调色板生成的图像。 */
    for (size_t type = 0; type < 26; ++type)
        for (size_t team = 0; team < 2; ++team)
            for (size_t body = 0; body < 32; ++body)
                for (size_t turret = 0; turret < 32; ++turret) ra_voxel_image_close(&s->sprites[type][team][body][turret]);
    for (size_t unit = 0; unit < RA_BATTLE_UNITS; ++unit) ra_voxel_image_close(&s->slope_sprites[unit]);
    tiles = calloc(512 * 512, sizeof(*tiles));
    if (!tiles) return ra_fail(error, RA_MEMORY, 0, "navigation allocation failed");
    for (i = 0; i < 512 * 512; ++i)
    {
        tiles[i].blocked = 1;
        tiles[i].land = 255;
    }
    for (i = 0; i < 12; ++i)
    {
        const ra_ini_entry *e = ra_ini_get(&s->voxels.rules, land_names[i], "Track");
        multipliers[i] = e ? (uint16_t)strtoul(e->value, NULL, 10) : 0;
    }
    for (i = 0; i < map->cell_count; ++i)
    {
        const ra_map_cell *cell = &map->cells[i];
        map_template *entry;
        unsigned sub = cell->tile == 65535 || cell->tile == UINT32_MAX ? 0 : cell->subtile;
        int px = ((int)cell->x - cell->y) * 30 + map->size[2] * 30 - map->local[0] * 60 + 30;
        int py = ((int)cell->x + cell->y - cell->height) * 15 - map->size[2] * 15 - map->local[1] * 30 + 15;
        ra_battle_tile *tile = &tiles[cell->y * 512 + cell->x];
        tile->height = cell->height;
        if (!map_template_get(&s->maps, theater, cell->tile, &entry, error) || sub >= entry->tmp.count || !entry->tmp.tiles[sub].present)
        {
            ++s->missing;
            continue;
        }
        tile->land = ra_battle_land(entry->tmp.tiles[sub].terrain);
        tile->ramp = entry->tmp.tiles[sub].ramp;
        tile->track = tile->land < 12 ? multipliers[tile->land] : 0;
        tile->blocked = !s->scenario && (px < 0 || py < 0 || px >= map->local[2] * 60 || py >= map->local[3] * 30);
        if (map->overlay)
        {
            unsigned index = map->overlay[cell->y * 512 + cell->x];
            const char *name = index < s->maps.overlay_name_count ? s->maps.overlay_names[index] : "";
            if (yes(&s->voxels.rules, name, "Wall")) tile->blocked = 1;
            if (yes(&s->voxels.rules, name, "Wall")) tile->land = 4;
            /* 高桥另建桥面节点，地表保留原有水陆属性。 */
            if (!strncmp(name, "BRIDGE", 6))
            {
                ++s->bridges;
            }
            if (!strncmp(name, "GOLD", 4) || !strncmp(name, "GEM", 3)) tile->track = multipliers[5];
        }
    }
    for (i = 0; i < map->object_count; ++i)
    {
        const ra_map_object *object = &map->objects[i];
        int width = 1, height = 1, x, y;
        if (object->kind == RA_MAP_WAYPOINT && object->number == 0)
        {
            spawn_x = object->x;
            spawn_y = object->y;
        }
        if (object->kind != RA_MAP_STRUCTURE && object->kind != RA_MAP_TERRAIN && object->kind != RA_MAP_UNIT && object->kind != RA_MAP_INFANTRY) continue;
        if (s->scenario && (object->kind == RA_MAP_STRUCTURE || object->kind == RA_MAP_UNIT || object->kind == RA_MAP_INFANTRY)) continue;
        if (object->kind == RA_MAP_STRUCTURE)
        {
            const ra_ini_entry *image = ra_ini_get(&s->voxels.rules, object->type, "Image");
            const ra_ini_entry *foundation = ra_ini_get(&s->voxels.art, image ? image->value : object->type, "Foundation");
            if (!foundation || sscanf(foundation->value, "%dx%d", &width, &height) != 2 || width < 1 || height < 1 || width > 16 || height > 16)
            {
                width = height = 1;
                ++s->unsupported_foundations;
            }
        }
        for (y = 0; y < height; ++y)
            for (x = 0; x < width; ++x) block(s, tiles, object->x + x, object->y + y);
    }
    ra_sha1(s->maps.sources[source].bytes, hashes);
    ra_sha1(s->voxels.rule_bytes.view, hashes + 20);
    ra_sha1(s->voxels.art_bytes.view, hashes + 40);
    ra_sha1((ra_view){hashes, sizeof(hashes)}, digest);
    if (!ra_battle_create(&s->battle, 512, 512, tiles, digest, error))
    {
        free(tiles);
        return false;
    }
    free(tiles);
    if (map->overlay)
        for (i = 0; i < map->cell_count; ++i)
        {
            const ra_map_cell *cell = &map->cells[i];
            uint32_t at = cell->y * 512 + cell->x;
            unsigned index = map->overlay[at], data = map->overlay_data ? map->overlay_data[at] : 0;
            const char *name = index < s->maps.overlay_name_count ? s->maps.overlay_names[index] : "";
            if (!strcmp(name, "BRIDGE1") || !strcmp(name, "BRIDGE2") || !strcmp(name, "BRIDGEB1") || !strcmp(name, "BRIDGEB2"))
            {
                uint32_t axis = name[strlen(name) - 1] == '1' ? 1u : 2u;
                if (!ra_battle_bridge_segment_add(&s->battle, at, axis, !strncmp(name, "BRIDGEB", 7) ? 1u : 0u, data, error)) return false;
            }
            else if (!strncmp(name, "LOBRDG", 6) || !strncmp(name, "LOBRDB", 6) || !strncmp(name, "RAILBRDG", 8))
            {
                unsigned variant = (unsigned)strtoul(name + 6, NULL, 10);
                bool low = !strncmp(name, "LOBRDG", 6) || !strncmp(name, "LOBRDB", 6);
                if (low && variant >= 1 && variant <= 28)
                {
                    uint32_t axis = variant <= 9 || variant == 27 || (variant >= 19 && variant <= 22) ? 1u : 2u;
                    if (!ra_battle_bridge_segment_add(&s->battle, at, axis, !strncmp(name, "LOBRDB", 6) ? 3u : 2u, variant, error)) return false;
                    ++s->low_bridges;
                }
                else
                {
                    s->battle.tiles[at].blocked = 1;
                    ++s->pending_bridges;
                }
            }
        }
    if (!bridge_gaps(s, error)) return false;
    const ra_ini_entry *bridge_strength = ra_ini_get(&s->voxels.rules, "CombatDamage", "BridgeStrength");
    if (bridge_strength)
    {
        uint32_t value = (uint32_t)strtoul(bridge_strength->value, NULL, 10);
        if (!value || value > 10000000) return ra_fail(error, RA_RANGE, 0, "invalid BridgeStrength");
        s->battle.bridge_strength = value;
    }
    if (s->campaign_mode)
    {
        size_t base = s->voxels.rule_bytes.view.size, local = s->maps.sources[source].bytes.size;
        uint8_t *combined = malloc(base + local + 2);
        if (!combined) return ra_fail(error, RA_MEMORY, 0, "campaign rule merge allocation failed");
        memcpy(combined, s->voxels.rule_bytes.view.data, base);
        combined[base] = '\n';
        memcpy(combined + base + 1, s->maps.sources[source].bytes.data, local);
        ra_ini_close(&s->voxels.rules);
        bool parsed = ra_ini_parse(&s->voxels.rules, (ra_view){combined, base + local + 1}, "campaign rules", error);
        free(combined);
        if (!parsed) return false;
    }
    for (i = 0; i < 2; ++i)
    {
        const ra_ini_entry *speed = ra_ini_get(&s->voxels.rules, unit_names[i], "Speed");
        uint32_t value = speed ? (uint32_t)strtoul(speed->value, NULL, 10) : 0;
        if (!value || value > 100 ||
            !ra_battle_type_add(&s->battle, unit_names[i], i ? "ra2.soviet" : "ra2.allied", ra_battle_native_speed(value) * 256, error) ||
            !ra_battle_type_rules(&s->battle, (uint32_t)i, &s->voxels.rules, error) ||
            !ra_battle_type_art(&s->battle, (uint32_t)i, &s->voxels.rules, &s->voxels.art, error))
            return false;
    }
    if (s->economy_mode) return battle_scene_economy_fixture(s, error) && (!graphics || battle_scene_refresh(s, error));
    if (s->scenario)
    {
        if (!battle_scene_import(s, error)) return false;
        return !graphics || battle_scene_refresh(s, error);
    }
    if (!spawn_x && !spawn_y)
    {
        spawn_x = map->size[2];
        spawn_y = map->size[3] / 2;
    }
    /* 小场景在路径点零附近创建四辆测试坦克，不执行地图的任务和触发脚本。 */
    for (int radius = 0; radius < 512 && s->battle.count < 4; ++radius)
        for (int y = spawn_y - radius; y <= spawn_y + radius && s->battle.count < 4; ++y)
            for (int x = spawn_x - radius; x <= spawn_x + radius && s->battle.count < 4; ++x)
            {
                if (abs(x - spawn_x) != radius && abs(y - spawn_y) != radius) continue;
                if (x < 0 || y < 0 || x >= 512 || y >= 512 || !ra_battle_passable(&s->battle, (uint32_t)y * 512 + (uint32_t)x)) continue;
                if (!ra_battle_spawn_team(&s->battle, s->battle.count & 1, s->battle.count < 2 ? 1u : 2u, (uint32_t)x, (uint32_t)y, error)) return false;
            }
    if (s->battle.count != 4) return ra_fail(error, RA_NOT_FOUND, 0, "map has insufficient passable spawn cells");
    if (graphics && !battle_scene_refresh(s, error)) return false;
    return true;
}

void battle_unit_pixel(const battle_scene *s, const ra_battle_unit *u, int *x, int *y)
{
    const ra_battle *b = &s->battle;
    int64_t height = (int64_t)ra_battle_unit_height(b, u) * RA_BATTLE_CELL / 104;
    *x = (int)(((int64_t)u->x - u->y) * 30 / RA_BATTLE_CELL) + s->ground.origin_x + 30;
    *y = (int)(((int64_t)u->x + u->y - height) * 15 / RA_BATTLE_CELL) + s->ground.origin_y + 15;
    if (b->types[u->type].infantry && u->subcell < 5)
    {
        static const int offsets[5][2] = {{0, 0}, {0, -5}, {15, 0}, {-15, 0}, {0, 5}};
        *x += offsets[u->subcell][0];
        *y += offsets[u->subcell][1];
    }
}

float battle_sprite_height(const ra_voxel_image *sprite, size_t pixel, int32_t unit_height)
{
    /* 相机俯角为 30 度，体素比例为 12；逆变换使用像素中心，深度尚未乘比例。 */
    float screen_y = (float)(pixel / sprite->width) + 0.5f - sprite->origin_y;
    float world_z = sprite->depth[pixel] * 6.0f - screen_y * 0.8660254037844386f;
    /* 地图每级高度投影为 15 像素，换算为竖直高度时除以 cos(30)。 */
    return (float)unit_height / 104.0f + world_z / 17.32050807568877f;
}

bool battle_scene_goal(battle_scene *s, uint32_t unit, uint32_t distance, uint32_t *goal)
{
    ra_battle *b = &s->battle;
    uint32_t start;
    int x, y;
    if (!unit || unit > b->count || !goal) return false;
    start = b->units[unit - 1].cell;
    for (int radius = (int)distance; radius > 0; --radius)
        for (y = (int)ra_battle_cell_y(b, start) - radius; y <= (int)ra_battle_cell_y(b, start) + radius; ++y)
            for (x = (int)(start % 512) - radius; x <= (int)(start % 512) + radius; ++x)
            {
                uint32_t cell;
                if (abs(x - (int)(start % 512)) != radius && abs(y - (int)ra_battle_cell_y(b, start)) != radius) continue;
                if (x < 0 || y < 0 || x >= 512 || y >= 512) continue;
                cell = (uint32_t)y * 512 + (uint32_t)x + start / (512 * 512) * (512 * 512);
                if (ra_battle_route(b, unit, cell))
                {
                    *goal = cell;
                    return true;
                }
            }
    return false;
}

bool battle_scene_bridge_fixture(battle_scene *s, uint32_t *goal, ra_error *error)
{
    ra_battle *b = &s->battle;
    uint32_t n = b->width * b->height;
    if (!goal || !b->tiles) return ra_fail(error, RA_ARGUMENT, 0, "bridge fixture requires a map");
    for (uint32_t cell = 0; cell < n; ++cell)
    {
        if (!(b->bridges[cell] & 4)) continue;
        uint32_t stride = (b->bridges[cell] & 3) == 1 ? 1u : b->width;
        if (cell < stride || cell % b->width == 0 || ra_battle_passable(b, n + cell - stride)) continue;
        uint32_t start = cell - stride, end = cell;
        while (end < n && b->bridges[end] == b->bridges[cell] && ra_battle_passable(b, n + end)) end += stride;
        if (end >= n || !ra_battle_passable(b, start) || !ra_battle_passable(b, end)) continue;
        if (b->tiles[start].height != b->tiles[n + cell].height || b->tiles[end].height != b->tiles[n + cell].height) continue;
        /* 不改写地表、桥段或规则；仅替换本程序的初始单位数组。 */
        b->count = b->tick = b->command_count = b->command_cursor = 0;
        memset(b->units, 0, RA_BATTLE_UNITS * sizeof(*b->units));
        memset(b->initial, 0, RA_BATTLE_UNITS * sizeof(*b->initial));
        memset(b->occupied, 0, (size_t)2 * n * sizeof(*b->occupied));
        if (!ra_battle_spawn_team(b, 0, 1, start % b->width, start / b->width, error)) return false;
        if (!ra_battle_route(b, 1, end)) continue;
        bool layered = false;
        for (uint32_t i = 0; i < b->units[0].path_count; ++i)
            if (b->units[0].path[i] >= n) layered = true;
        if (!layered) continue;
        *goal = end;
        ra_battle_reset(b);
        return true;
    }
    return ra_fail(error, RA_NOT_FOUND, 0, "map has no supported intact bridge with both banks");
}

bool battle_scene_bridge_lifecycle_fixture(battle_scene *s, uint32_t *cell, uint32_t *goal, ra_error *error)
{
    if (!cell || !goal || !battle_scene_bridge_fixture(s, goal, error)) return false;
    ra_battle *b = &s->battle;
    if (!ra_battle_route(b, 1, *goal)) return ra_fail(error, RA_NOT_FOUND, 0, "bridge fixture route unavailable");
    uint32_t deck[512], count = 0, n = b->width * b->height;
    for (uint32_t i = 0; i < b->units[0].path_count && count < 512; ++i)
        if (b->units[0].path[i] >= n) deck[count++] = b->units[0].path[i];
    if (!count) return ra_fail(error, RA_NOT_FOUND, 0, "bridge fixture has no deck");
    *cell = deck[count / 2] % n;
    ra_battle_reset(b);
    return ra_battle_spawn_layer(b, 0, 1, *cell % b->width, *cell / b->width, 1, error);
}
