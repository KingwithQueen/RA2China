#include "internal.h"
#include "map_scene.h"
#include <stdlib.h>
#include <string.h>

static uint32_t color(ra_rgb c)
{
    return ((uint32_t)c.r << 16) | ((uint32_t)c.g << 8) | c.b;
}

static bool image_create(map_image *image, int width, int height, ra_error *error)
{
    map_image result = {0};
    size_t i, count;
    if (width < 1 || height < 1 || width > 32768 || height > 32768 || (size_t)width * height > 64 * 1024 * 1024)
        return ra_fail(error, RA_RANGE, 0, "map preview exceeds 64 million pixels");
    count = (size_t)width * height;
    result.pixels = malloc(count * sizeof(*result.pixels));
    result.picked = malloc(count * sizeof(*result.picked));
    if (!result.pixels || !result.picked)
    {
        map_image_close(&result);
        return ra_fail(error, RA_MEMORY, 0, "map image allocation failed");
    }
    result.width = width;
    result.height = height;
    for (i = 0; i < count; ++i)
    {
        result.pixels[i] = 0x161d26;
        result.picked[i] = -1;
    }
    map_image_close(image);
    *image = result;
    return true;
}

static void pixel(map_image *image, int x, int y, uint32_t rgb, int32_t cell)
{
    size_t p;
    if (x < 0 || y < 0 || x >= image->width || y >= image->height) return;
    p = (size_t)y * image->width + x;
    image->pixels[p] = rgb;
    image->picked[p] = cell;
    ++image->drawn;
}

static void tile_draw(map_image *image, const ra_tmp *tmp, const ra_tmp_tile *tile, const ra_palette *palette, int x, int y, int32_t cell)
{
    int row, width = 4, column;
    size_t cursor = 0;
    for (row = 0; row < (int)tmp->height; ++row)
    {
        int start = ((int)tmp->width - width) / 2;
        for (column = 0; column < width; ++column) pixel(image, x + start + column, y + row, color(palette->colors[tile->pixels.data[cursor++]]), cell);
        width += row < (int)tmp->height / 2 - 1 ? 4 : -4;
    }
    if (tile->extra.size)
    {
        int left = x + tile->extra_x - tile->x, top = y + tile->extra_y - tile->y;
        for (row = 0; row < tile->extra_height; ++row)
            for (column = 0; column < tile->extra_width; ++column)
            {
                uint8_t index = tile->extra.data[(size_t)row * tile->extra_width + column];
                if (index) pixel(image, left + column, top + row, color(palette->colors[index]), cell);
            }
    }
}

static int cell_compare(const void *a, const void *b)
{
    const ra_map_cell *left = *(const ra_map_cell *const *)a, *right = *(const ra_map_cell *const *)b;
    int order = (int)left->x + left->y - right->x - right->y;
    return order ? order : (int)left->x - right->x;
}

static void marker(map_image *image, int x, int y, int radius, uint32_t rgb, int32_t cell, bool hollow)
{
    int dx, dy;
    for (dy = -radius; dy <= radius; ++dy)
        for (dx = -radius; dx <= radius; ++dx)
        {
            int distance = abs(dx) + abs(dy) * 2;
            if (distance <= radius && (!hollow || distance > radius - 3)) pixel(image, x + dx, y + dy, rgb, cell);
        }
}

bool map_render(map_context *context, const ra_map *map, map_image *image, bool overlays, bool objects, bool local, ra_error *error)
{
    const ra_map_cell **order;
    int theater = map_theater_id(map->theater), ox = map->size[2] * 30, oy = -map->size[2] * 15 + 512;
    int width = map->size[2] * 60, height = map->size[3] * 30 + 542;
    size_t i;
    if (!map_theater_open(context, theater, error)) return false;
    if (local)
    {
        ox -= map->local[0] * 60;
        oy -= map->local[1] * 30 + 512;
        width = map->local[2] * 60;
        height = map->local[3] * 30;
    }
    if (!image_create(image, width, height, error)) return false;
    image->origin_x = ox;
    image->origin_y = oy;
    order = malloc(map->cell_count * sizeof(*order));
    if (!order) return ra_fail(error, RA_MEMORY, 0, "map drawing order allocation failed");
    for (i = 0; i < map->cell_count; ++i) order[i] = &map->cells[i];
    qsort(order, map->cell_count, sizeof(*order), cell_compare);
    for (i = 0; i < map->cell_count; ++i)
    {
        const ra_map_cell *cell = order[i];
        map_template *entry;
        uint8_t subtile = cell->tile == 65535 || cell->tile == UINT32_MAX ? 0 : cell->subtile;
        int x = ((int)cell->x - cell->y) * 30 + ox, y = ((int)cell->x + cell->y - cell->height) * 15 + oy;
        int32_t index = (int32_t)(cell - map->cells);
        if (map_template_get(context, theater, cell->tile, &entry, error) && subtile < entry->tmp.count && entry->tmp.tiles[subtile].present)
            tile_draw(image, &entry->tmp, &entry->tmp.tiles[subtile], &context->theaters[theater].palette, x, y, index);
        else
        {
            ++image->missing;
            marker(image, x + 30, y + 15, 25, 0xff00ff, index, false);
        }
    }
    free(order);
    if (overlays && map->overlay)
        for (i = 0; i < map->cell_count; ++i)
        {
            const ra_map_cell *cell = &map->cells[i];
            unsigned overlay = map->overlay[(size_t)cell->y * 512 + cell->x];
            int x = ((int)cell->x - cell->y) * 30 + ox + 30, y = ((int)cell->x + cell->y - cell->height) * 15 + oy + 15;
            const char *name = overlay < context->overlay_name_count ? context->overlay_names[overlay] : "";
            bool ore = !strncmp(name, "GOLD", 4) || !strncmp(name, "TIB", 3);
            if (overlay != 255) marker(image, x, y, 6, ore ? 0xecc351 : 0xb4a2d9, (int32_t)i, false);
        }
    if (objects)
        for (i = 0; i < map->object_count; ++i)
        {
            const ra_map_object *object = &map->objects[i];
            const ra_map_cell *cell = ra_map_at(map, object->x, object->y);
            int x = (object->x - object->y) * 30 + ox + 30, y = (object->x + object->y - (cell ? cell->height : 0)) * 15 + oy + 15;
            int32_t index = cell ? (int32_t)(cell - map->cells) : -1;
            static const uint32_t colors[] = {0xff655b, 0x64c5ed, 0xe2e7ed, 0xffffff, 0xd2abff, 0x438e48, 0xa7927c};
            int radius = object->kind == RA_MAP_WAYPOINT ? (object->number < 8 ? 24 : 9) : object->kind == RA_MAP_STRUCTURE ? 16 : 6;
            marker(image, x, y, radius, colors[object->kind], index, object->kind == RA_MAP_WAYPOINT);
        }
    return true;
}

bool map_tmp_render(const ra_tmp *tmp, const ra_palette *palette, map_image *image, ra_error *error)
{
    int minx = 0, miny = 0, maxx = 0, maxy = 0;
    size_t i;
    for (i = 0; i < tmp->count; ++i)
        if (tmp->tiles[i].present)
        {
            const ra_tmp_tile *t = &tmp->tiles[i];
            int top = t->y - t->height * (int)tmp->height / 2;
            if (t->x < minx) minx = t->x;
            if (top < miny) miny = top;
            if (t->x + (int)tmp->width > maxx) maxx = t->x + (int)tmp->width;
            if (top + (int)tmp->height > maxy) maxy = top + (int)tmp->height;
            if (t->extra.size)
            {
                top = t->extra_y - t->height * (int)tmp->height / 2;
                if (t->extra_x < minx) minx = t->extra_x;
                if (top < miny) miny = top;
                if (t->extra_x + t->extra_width > maxx) maxx = t->extra_x + t->extra_width;
                if (top + t->extra_height > maxy) maxy = top + t->extra_height;
            }
        }
    if (!image_create(image, maxx - minx + 32, maxy - miny + 32, error)) return false;
    for (i = 0; i < tmp->count; ++i)
        if (tmp->tiles[i].present)
        {
            const ra_tmp_tile *t = &tmp->tiles[i];
            tile_draw(image, tmp, t, palette, t->x - minx + 16, t->y - t->height * (int)tmp->height / 2 - miny + 16, (int32_t)i);
        }
    return true;
}
