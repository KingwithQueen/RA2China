#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "ra2/map.h"
#include <stdlib.h>
#include <string.h>
#include <errno.h>

static bool integers(const char *text, int *values, size_t count)
{
    size_t i;
    const char *p = text;
    for (i = 0; i < count; ++i)
    {
        long value;
        char *end;
        errno = 0;
        value = strtol(p, &end, 10);
        if (end == p || errno || value < -1000000 || value > 1000000) return false;
        while (*end == ' ' || *end == '\t') ++end;
        if (*end != (i + 1 == count ? 0 : ',')) return false;
        values[i] = (int)value;
        p = end + 1;
    }
    return true;
}

static bool rectangle(const ra_ini *ini, const char *section, const char *key, int out[4], ra_error *error)
{
    const ra_ini_entry *entry = ra_ini_get(ini, section, key);
    if (!entry || !integers(entry->value, out, 4) || out[0] < 0 || out[1] < 0 || out[2] < 1 || out[3] < 1 || out[2] > 512 || out[3] > 512)
        return ra_fail(error, RA_FORMAT, entry ? entry->line : 0, "invalid [%s] %s rectangle", section, key);
    return true;
}

const ra_map_cell *ra_map_at(const ra_map *map, int x, int y)
{
    int32_t index;
    if (!map || !map->cell_index || x < 0 || y < 0 || x >= 512 || y >= 512) return NULL;
    index = map->cell_index[(size_t)y * 512 + x];
    return index < 0 ? NULL : &map->cells[index];
}

static bool objects(ra_map *map, ra_error *error)
{
    static const char *sections[] = {"Waypoints", "Structures", "Units", "Infantry", "Aircraft", "Terrain", "Smudge"};
    size_t i, kind;
    map->objects = calloc(map->ini.entry_count ? map->ini.entry_count : 1, sizeof(*map->objects));
    if (!map->objects) return ra_fail(error, RA_MEMORY, 0, "map object allocation failed");
    for (i = 0; i < map->ini.entry_count; ++i)
    {
        const ra_ini_entry *e = &map->ini.entries[i];
        char *copy, *parts[24], *p;
        size_t fields = 0;
        int xy[2];
        ra_map_object object = {0};
        for (kind = 0; kind < 7; ++kind)
            if (ra_equal(e->section, sections[kind])) break;
        if (kind == 7 || ra_ini_get(&map->ini, e->section, e->key) != e) continue;
        object.kind = (ra_map_object_kind)kind;
        object.health = 256;
        object.source_line = e->line;
        object.number = -1;
        copy = ra_copy(e->value, strlen(e->value));
        if (!copy) return ra_fail(error, RA_MEMORY, e->line, "map object allocation failed");
        p = copy;
        while (fields < 24)
        {
            char *comma = strchr(p, ',');
            parts[fields++] = p;
            if (!comma) break;
            *comma = 0;
            p = comma + 1;
        }
        if (kind == RA_MAP_WAYPOINT || kind == RA_MAP_TERRAIN)
        {
            int code;
            if (!integers(kind == RA_MAP_WAYPOINT ? e->value : e->key, &code, 1)) goto invalid;
            object.x = code % 1000;
            object.y = code / 1000;
            if (object.x < 0)
            {
                object.x += 1000;
                --object.y;
            }
            if (kind == RA_MAP_WAYPOINT && !integers(e->key, &object.number, 1)) goto invalid;
            object.type = ra_copy(kind == RA_MAP_WAYPOINT ? e->key : parts[0], strlen(kind == RA_MAP_WAYPOINT ? e->key : parts[0]));
            object.owner = ra_copy("", 0);
        }
        else
        {
            size_t xfield = kind == RA_MAP_SMUDGE ? 1 : 3;
            if (fields < xfield + 2 || !integers(parts[xfield], &xy[0], 1) || !integers(parts[xfield + 1], &xy[1], 1)) goto invalid;
            object.x = xy[0];
            object.y = xy[1];
            object.type = ra_copy(parts[kind == RA_MAP_SMUDGE ? 0 : 1], strlen(parts[kind == RA_MAP_SMUDGE ? 0 : 1]));
            object.owner = ra_copy(kind == RA_MAP_SMUDGE ? "" : parts[0], strlen(kind == RA_MAP_SMUDGE ? "" : parts[0]));
            if (kind != RA_MAP_SMUDGE)
            {
                int health, facing = 0;
                size_t facing_field = kind == RA_MAP_INFANTRY ? 7 : 5;
                if (!integers(parts[2], &health, 1) || health < 0 || health > 256) goto invalid;
                if (fields > facing_field && (!integers(parts[facing_field], &facing, 1) || facing < 0 || facing > 255)) goto invalid;
                object.health = (uint32_t)health;
                object.facing = (uint32_t)facing;
            }
        }
        free(copy);
        if (!object.type || !object.owner)
        {
            free(object.type);
            free(object.owner);
            return ra_fail(error, RA_MEMORY, e->line, "map object string allocation failed");
        }
        if (!ra_map_at(map, object.x, object.y)) ++map->outside_objects;
        map->objects[map->object_count++] = object;
        continue;
    invalid:
        free(copy);
        free(object.type);
        free(object.owner);
        return ra_fail(error, RA_FORMAT, e->line, "invalid [%s] object coordinates", sections[kind]);
    }
    return true;
}

bool ra_map_open(ra_map *map, ra_view input, const char *source, ra_error *error)
{
    ra_error local_error = {0};
    ra_map result = {0};
    const ra_ini_entry *theater;
    uint8_t *packed = NULL;
    size_t size = 0, i, overlay_size = 0, data_size = 0, capacity;
    int preview[4];
    if (!error) error = &local_error;
    if (!map) return ra_fail(error, RA_ARGUMENT, 0, "map output is required");
    if (!ra_ini_parse(&result.ini, input, source, error))
    {
        static const char prefix[] = "[__RA2_Map_Preamble]\n";
        uint8_t *adapted;
        size_t skip = input.size >= 3 && !memcmp(input.data, "\xef\xbb\xbf", 3) ? 3 : 0;
        /* TN01T2 带有节外的战役参数；仅地图适配层将它们显式归入前导节。 */
        if (!error || error->code != RA_SYNTAX || strcmp(error->message, "expected key=value inside a section") || input.size > 32 * 1024 * 1024) return false;
        adapted = malloc(sizeof(prefix) - 1 + input.size - skip);
        if (!adapted) return ra_fail(error, RA_MEMORY, 0, "map preamble allocation failed");
        memcpy(adapted, prefix, sizeof(prefix) - 1);
        memcpy(adapted + sizeof(prefix) - 1, input.data + skip, input.size - skip);
        if (!ra_ini_parse(&result.ini, (ra_view){adapted, sizeof(prefix) - 1 + input.size - skip}, source, error))
        {
            free(adapted);
            return false;
        }
        free(adapted);
        for (i = 0; i < result.ini.entry_count; ++i)
        {
            if (result.ini.entries[i].line) --result.ini.entries[i].line;
            if (ra_equal(result.ini.entries[i].section, "__RA2_Map_Preamble")) ++result.preamble_entries;
        }
        for (i = 0; i < result.ini.section_count; ++i)
            if (result.ini.sections[i].line) --result.ini.sections[i].line;
        for (i = 0; i < result.ini.ignored_count; ++i)
            if (result.ini.ignored_lines[i].line) --result.ini.ignored_lines[i].line;
    }
    if (!rectangle(&result.ini, "Map", "Size", result.size, error) || !rectangle(&result.ini, "Map", "LocalSize", result.local, error)) goto fail;
    if (result.size[0] || result.size[1] || result.size[2] + result.size[3] > 510 || result.local[0] + result.local[2] > result.size[2] ||
        result.local[1] + result.local[3] > result.size[3])
    {
        ra_fail(error, RA_RANGE, 0, "map rectangle exceeds supported RA2 grid");
        goto fail;
    }
    theater = ra_ini_get(&result.ini, "Map", "Theater");
    if (!theater || (!ra_equal(theater->value, "TEMPERATE") && !ra_equal(theater->value, "SNOW") && !ra_equal(theater->value, "URBAN")))
    {
        ra_fail(error, RA_FORMAT, 0, "unsupported or missing RA2 1.006 theater");
        goto fail;
    }
    snprintf(result.theater, sizeof(result.theater), "%s", theater->value);
    if (!ra_map_pack(&result.ini, "IsoMapPack5", true, &packed, &size, error)) goto fail;
    /* 地图列表以四字节的零坐标结束；部分工具只写完整记录。 */
    if (size >= 4 && size % 11 == 4 && !ra_le32(packed + size - 4))
    {
        size -= 4;
        result.trailing_bytes = 4;
    }
    if (size % 11)
    {
        ra_fail(error, RA_FORMAT, 0, "IsoMapPack5 must contain whole 11-byte cells and optional zero terminator");
        goto fail;
    }
    result.cell_count = size / 11;
    result.stored_cells = result.cell_count;
    if (result.cell_count > 262144)
    {
        ra_fail(error, RA_RANGE, 0, "too many map cells");
        goto fail;
    }
    capacity = result.cell_count + (size_t)(result.size[2] * 2 - 1) * result.size[3];
    result.cells = calloc(capacity ? capacity : 1, sizeof(*result.cells));
    result.cell_index = malloc(262144 * sizeof(*result.cell_index));
    if (!result.cells || !result.cell_index)
    {
        ra_fail(error, RA_MEMORY, 0, "map cell allocation failed");
        goto fail;
    }
    for (i = 0; i < 262144; ++i) result.cell_index[i] = -1;
    for (i = 0; i < result.cell_count; ++i)
    {
        const uint8_t *p = packed + i * 11;
        ra_map_cell *cell = &result.cells[i];
        size_t index;
        cell->x = ra_le16(p);
        cell->y = ra_le16(p + 2);
        cell->tile = ra_le32(p + 4);
        cell->subtile = p[8];
        cell->height = p[9];
        cell->ice = p[10];
        if (cell->x >= 512 || cell->y >= 512 || cell->height > 64)
        {
            ra_fail(error, RA_RANGE, 0, "invalid map cell %zu coordinate/height", i);
            goto fail;
        }
        index = (size_t)cell->y * 512 + cell->x;
        if (result.cell_index[index] >= 0)
        {
            ra_fail(error, RA_FORMAT, 0, "duplicate map cell coordinate");
            goto fail;
        }
        result.cell_index[index] = (int32_t)i;
    }
    /* 未存储的平地由游戏补零；按 RA2 的交错行生成完整地图范围。 */
    {
        int left = result.size[2], right = left + 1, y = 1;
        while (left < right)
        {
            int x;
            for (x = left; x < right; ++x)
                if (!ra_map_at(&result, x, y))
                {
                    ra_map_cell *cell;
                    if (result.cell_count == 262144 || x < 0 || x >= 512 || y >= 512)
                    {
                        ra_fail(error, RA_RANGE, 0, "map default cells exceed grid");
                        goto fail;
                    }
                    cell = &result.cells[result.cell_count];
                    cell->x = (uint16_t)x;
                    cell->y = (uint16_t)y;
                    result.cell_index[(size_t)y * 512 + x] = (int32_t)result.cell_count++;
                    ++result.defaulted_cells;
                }
            left += y < result.size[2] ? -1 : 1;
            right += y < result.size[3] ? 1 : y > result.size[3] ? -1 : 0;
            ++y;
        }
    }
    free(packed);
    packed = NULL;
    if (!ra_map_pack(&result.ini, "OverlayPack", false, &result.overlay, &overlay_size, error) ||
        !ra_map_pack(&result.ini, "OverlayDataPack", false, &result.overlay_data, &data_size, error))
        goto fail;
    if ((overlay_size && overlay_size != 262144) || (data_size && data_size != 262144) || (!!overlay_size != !!data_size))
    {
        ra_fail(error, RA_FORMAT, 0, "overlay packs must both cover the 512x512 grid");
        goto fail;
    }
    if (result.overlay)
        for (i = 0; i < result.cell_count; ++i)
            if (result.overlay[(size_t)result.cells[i].y * 512 + result.cells[i].x] != 255) ++result.overlay_count;
    if (!ra_map_pack(&result.ini, "PreviewPack", true, &result.preview, &result.preview_size, error)) goto fail;
    if (result.preview_size)
    {
        if (!rectangle(&result.ini, "Preview", "Size", preview, error) || (size_t)preview[2] * preview[3] * 3 != result.preview_size)
        {
            ra_fail(error, RA_FORMAT, 0, "preview RGB dimensions disagree with pack");
            goto fail;
        }
        result.preview_width = preview[2];
        result.preview_height = preview[3];
    }
    if (!objects(&result, error)) goto fail;
    *map = result;
    return true;
fail:
    free(packed);
    ra_map_close(&result);
    return false;
}

void ra_map_close(ra_map *map)
{
    size_t i;
    if (!map) return;
    for (i = 0; i < map->object_count; ++i)
    {
        free(map->objects[i].type);
        free(map->objects[i].owner);
    }
    free(map->objects);
    free(map->preview);
    free(map->overlay);
    free(map->overlay_data);
    free(map->cell_index);
    free(map->cells);
    ra_ini_close(&map->ini);
    memset(map, 0, sizeof(*map));
}
