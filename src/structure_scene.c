#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "structure_scene.h"
#include <float.h>
#include <stdlib.h>
#include <string.h>

static const char *value(const ra_ini *ini, const char *id, const char *key, const char *fallback)
{
    const ra_ini_entry *entry = ra_ini_get(ini, id, key);
    return entry ? entry->value : fallback;
}
static int number(const ra_ini *ini, const char *id, const char *key, int fallback)
{
    int64_t result;
    const ra_ini_entry *entry = ra_ini_get(ini, id, key);
    return entry && ra_ini_integer(entry, &result, NULL) && result >= -4096 && result <= 65535 ? (int)result : fallback;
}
static bool yes(const ra_ini *ini, const char *id, const char *key)
{
    const char *text = value(ini, id, key, "no");
    return ra_equal(text, "yes") || ra_equal(text, "true") || !strcmp(text, "1");
}

static bool shape(structure_layer *layer, const voxel_context *context, const char *id, int theater, bool inherited, ra_error *error)
{
    const char *image = value(&context->art, id, "Image", id);
    if (strlen(image) > 80) return ra_fail(error, RA_RANGE, 0, "structure image name exceeds limit");
    char candidates[4][96];
    unsigned count = 0;
    if ((inherited || yes(&context->art, id, "NewTheater")) && strlen(image) >= 2)
    {
        snprintf(candidates[count], sizeof(candidates[count]), "%s.shp", image);
        candidates[count++][1] = theater == 1 ? 'A' : theater == 2 ? 'U' : 'T';
        snprintf(candidates[count], sizeof(candidates[count]), "%s.shp", image);
        candidates[count++][1] = 'G';
    }
    snprintf(candidates[count++], sizeof(candidates[0]), "%s.shp", image);
    for (unsigned i = 0; i < count; ++i)
    {
        ra_error failure = {0};
        if (!ra_vfs_read(&context->vfs, candidates[i], &layer->bytes, &failure))
        {
            if (failure.code == RA_NOT_FOUND) continue;
            if (error) *error = failure;
            return false;
        }
        if (!ra_shp_open(&layer->shape, layer->bytes.view, error)) return false;
        strcpy(layer->filename, candidates[i]);
        return true;
    }
    return ra_fail(error, RA_NOT_FOUND, 0, "structure SHP is missing: %s", image);
}

static bool add_layer(structure_visual *visual, const voxel_context *context, const char *id, int theater, bool inherited, unsigned state, bool animated, int x,
                      int y, bool required, ra_error *error)
{
    if (!id || !*id) return true;
    if (visual->count >= 18) return ra_fail(error, RA_RANGE, 0, "too many structure image layers");
    structure_layer *layer = &visual->layers[visual->count];
    ra_error failure = {0};
    if (!shape(layer, context, id, theater, inherited, &failure))
    {
        ra_shp_close(&layer->shape);
        ra_resource_close(&layer->bytes);
        if (!required && failure.code == RA_NOT_FOUND)
        {
            ++visual->missing_layers;
            return true;
        }
        if (error) *error = failure;
        return false;
    }
    layer->state = state;
    layer->animated = animated;
    layer->x = x;
    layer->y = y;
    int start = number(&context->art, id, "LoopStart", number(&context->art, id, "Start", 0));
    int end = number(&context->art, id, "LoopEnd", start);
    layer->first = start >= 0 && start < layer->shape.count ? (uint32_t)start : 0;
    layer->last = end >= (int)layer->first && end < layer->shape.count ? (uint32_t)end : layer->first;
    if (!animated)
    {
        layer->first = state == 2 && layer->shape.count >= 4 ? 1u : 0u;
        layer->last = layer->first;
    }
    int width = layer->shape.width + 2 * abs(x), height = layer->shape.height + 2 * abs(y);
    if (width > 2048 || height > 2048) return ra_fail(error, RA_RANGE, 0, "structure composite exceeds canvas limit");
    if (width > visual->width) visual->width = width;
    if (height > visual->height) visual->height = height;
    ++visual->count;
    return true;
}

bool structure_visual_open(structure_visual *visual, const voxel_context *context, const char *id, const char *override_image, int theater, ra_error *error)
{
    const char *image = override_image ? override_image : value(&context->rules, id, "Image", id);
    if (strlen(image) >= sizeof(visual->image)) return ra_fail(error, RA_RANGE, 0, "structure art identifier exceeds limit");
    strcpy(visual->image, image);
    visual->remap = yes(&context->art, image, "Remapable");
    visual->terrain_palette = yes(&context->art, image, "TerrainPalette");
    bool inherited = yes(&context->art, image, "NewTheater");
    const char *bib = value(&context->art, image, "BibShape", "");
    if (!add_layer(visual, context, bib, theater, inherited, 1, false, 0, 0, false, error) ||
        !add_layer(visual, context, bib, theater, inherited, 2, false, 0, 0, false, error) ||
        !add_layer(visual, context, image, theater, inherited, 1, false, 0, 0, true, error) ||
        !add_layer(visual, context, image, theater, inherited, 2, false, 0, 0, true, error))
        goto fail;
    static const char *names[] = {"IdleAnim", "ActiveAnim", "ActiveAnimTwo", "ActiveAnimThree", "ActiveAnimFour", "SuperAnim"};
    for (unsigned i = 0; i < 6; ++i)
    {
        char damaged[64], key[64];
        snprintf(damaged, sizeof(damaged), "%sDamaged", names[i]);
        snprintf(key, sizeof(key), "%sX", names[i]);
        int x = number(&context->art, image, key, 0);
        snprintf(key, sizeof(key), "%sY", names[i]);
        int y = number(&context->art, image, key, 0);
        const char *normal = value(&context->art, image, names[i], "");
        const char *hurt = value(&context->art, image, damaged, normal);
        if (!add_layer(visual, context, normal, theater, inherited, 1, true, x, y, false, error) ||
            !add_layer(visual, context, hurt, theater, inherited, 2, true, x, y, false, error))
            goto fail;
    }
    visual->opened = true;
    return true;
fail:
    structure_visual_close(visual);
    visual->failed = true;
    return false;
}

bool structure_visual_render(const structure_visual *visual, const ra_palette *palette, const ra_battle_type *type, uint32_t team, bool damaged, uint32_t tick,
                             ra_voxel_image *image, ra_error *error)
{
    if (!visual->opened || !palette || !type || !image) return ra_fail(error, RA_ARGUMENT, 0, "invalid structure image arguments");
    if (!image->pixels && !ra_voxel_image_create(image, (size_t)visual->width, (size_t)visual->height, error)) return false;
    if (image->width != (size_t)visual->width || image->height != (size_t)visual->height) return ra_fail(error, RA_ARGUMENT, 0, "structure image size differs");
    memset(image->pixels, 0, image->width * image->height * sizeof(*image->pixels));
    for (size_t i = 0; i < image->width * image->height; ++i) image->depth[i] = -FLT_MAX;
    image->origin_x = (float)image->width / 2;
    /* 以占地中心投影，再使用矩形尺寸的通用美术偏移；不能按裁剪框底部重新定位。 */
    image->origin_y = (float)image->height / 2 + (type->foundation_width + type->foundation_height) * 7.5f;
    image->min_x = (int)image->width;
    image->min_y = (int)image->height;
    image->max_x = image->max_y = -1;
    image->drawn_pixels = 0;
    size_t capacity = (size_t)visual->width * visual->height;
    uint8_t *indices = malloc(capacity);
    if (!indices) return ra_fail(error, RA_MEMORY, 0, "structure frame allocation failed");
    static const ra_rgb houses[] = {{73, 140, 246}, {222, 67, 56},  {229, 207, 64}, {87, 204, 111},
                                    {174, 91, 219}, {63, 211, 213}, {234, 139, 48}, {210, 210, 210}};
    for (size_t i = 0; i < visual->count; ++i)
    {
        const structure_layer *layer = &visual->layers[i];
        if (layer->state != (damaged ? 2u : 1u)) continue;
        uint32_t frame = layer->first + (layer->animated ? tick / 3 % (layer->last - layer->first + 1) : 0);
        if (!ra_shp_decode(&layer->shape, frame, indices, capacity, error))
        {
            free(indices);
            return false;
        }
        int left = (visual->width - layer->shape.width) / 2 + layer->x, top = (visual->height - layer->shape.height) / 2 + layer->y;
        for (int y = 0; y < layer->shape.height; ++y)
            for (int x = 0; x < layer->shape.width; ++x)
            {
                uint8_t index = indices[(size_t)y * layer->shape.width + x];
                if (!index) continue;
                ra_rgb color = palette->colors[index];
                if (visual->remap && index >= 16 && index <= 31)
                {
                    ra_rgb house = houses[(team ? team - 1 : 0) % 8];
                    unsigned amount = 80 + (31 - index) * 175 / 15;
                    color = (ra_rgb){(uint8_t)(house.r * amount / 255), (uint8_t)(house.g * amount / 255), (uint8_t)(house.b * amount / 255)};
                }
                int px = left + x, py = top + y;
                size_t at = (size_t)py * image->width + px;
                if (!(image->pixels[at] >> 24)) ++image->drawn_pixels;
                image->pixels[at] = 0xff000000u | ((uint32_t)color.r << 16) | ((uint32_t)color.g << 8) | color.b;
                image->depth[at] = 0;
                if (px < image->min_x) image->min_x = px;
                if (px > image->max_x) image->max_x = px;
                if (py < image->min_y) image->min_y = py;
                if (py > image->max_y) image->max_y = py;
            }
    }
    free(indices);
    return true;
}

void structure_visual_close(structure_visual *visual)
{
    if (!visual) return;
    for (size_t i = 0; i < 18; ++i)
    {
        ra_shp_close(&visual->layers[i].shape);
        ra_resource_close(&visual->layers[i].bytes);
    }
    memset(visual, 0, sizeof(*visual));
}
