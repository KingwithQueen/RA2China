#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>
#include <float.h>

typedef struct battle_infantry_visual
{
    bool opened, failed;
    ra_resource bytes;
    ra_shp shape;
    uint32_t ready[3], walk[3], fire[3], tread[3], swim[3], wet_attack[3];
} battle_infantry_visual;
void battle_scene_infantry_clear(battle_scene *s)
{
    if (s->infantry_visuals)
        for (uint32_t i = 0; i < RA_BATTLE_TYPES; ++i)
        {
            ra_shp_close(&s->infantry_visuals[i].shape);
            ra_resource_close(&s->infantry_visuals[i].bytes);
        }
    free(s->infantry_visuals);
    s->infantry_visuals = NULL;
    for (uint32_t i = 0; i < 96; ++i)
    {
        ra_voxel_image_close(&s->infantry_sprites[i].image);
        memset(&s->infantry_sprites[i], 0, sizeof(s->infantry_sprites[i]));
    }
}
static bool sequence(const ra_ini *art, const char *section, const char *name, uint32_t result[3], ra_error *error)
{
    const ra_ini_entry *e = ra_ini_get(art, section, name);
    unsigned first, count, stride;
    if (!e || sscanf(e->value, "%u,%u,%u", &first, &count, &stride) != 3 || !count || count > 128 || stride > 128 || first > 65535)
        return ra_fail(error, RA_FORMAT, 0, "unsupported infantry sequence %s/%s", section, name);
    result[0] = first;
    result[1] = count;
    result[2] = stride;
    return true;
}
const ra_voxel_image *battle_scene_infantry_sprite(battle_scene *s, const ra_battle_unit *u, ra_error *error)
{
    if (!s->infantry_visuals) s->infantry_visuals = calloc(RA_BATTLE_TYPES, sizeof(*s->infantry_visuals));
    if (!s->infantry_visuals)
    {
        ra_fail(error, RA_MEMORY, 0, "infantry visual allocation failed");
        return NULL;
    }
    battle_infantry_visual *v = &s->infantry_visuals[u->type];
    if (v->failed) return NULL;
    if (!v->opened)
    {
        const char *id = s->battle.types[u->type].id;
        const ra_ini_entry *image = ra_ini_get(&s->voxels.rules, id, "Image");
        const char *name = image ? image->value : id;
        const ra_ini_entry *seq = ra_ini_get(&s->voxels.art, name, "Sequence");
        char file[64];
        snprintf(file, sizeof(file), "%s.shp", name);
        if (!seq || !ra_vfs_read(&s->maps.vfs, file, &v->bytes, error) || !ra_shp_open(&v->shape, v->bytes.view, error) ||
            !sequence(&s->voxels.art, seq->value, "Ready", v->ready, error) || !sequence(&s->voxels.art, seq->value, "Walk", v->walk, error) ||
            !sequence(&s->voxels.art, seq->value, "FireUp", v->fire, error))
        {
            v->failed = true;
            return NULL;
        }
        if (s->battle.types[u->type].amphibious &&
            (!sequence(&s->voxels.art, seq->value, "Tread", v->tread, error) || !sequence(&s->voxels.art, seq->value, "Swim", v->swim, error) ||
             !sequence(&s->voxels.art, seq->value, "WetAttack", v->wet_attack, error)))
        {
            v->failed = true;
            return NULL;
        }
        v->opened = true;
    }
    bool moving = u->cell != u->next;
    uint32_t facing = ra_battle_turn_value(u->target && !moving ? &u->turret : &u->body, s->battle.tick);
    uint32_t direction = ((facing + 4096) & 65535) / 8192;
    const uint32_t *seq = moving ? v->walk : u->cooldown && u->target ? v->fire : v->ready;
    if (s->battle.types[u->type].amphibious && s->battle.tiles[u->cell].land == 2) seq = moving ? v->swim : u->cooldown && u->target ? v->wet_attack : v->tread;
    uint32_t frame = seq[0] + direction * seq[2] + s->battle.tick / 2 % seq[1];
    if (frame >= v->shape.count)
    {
        ra_fail(error, RA_RANGE, 0, "infantry sequence frame exceeds SHP");
        return NULL;
    }
    structure_sprite *chosen = &s->infantry_sprites[0];
    for (uint32_t i = 0; i < 96; ++i)
    {
        structure_sprite *e = &s->infantry_sprites[i];
        if (e->occupied && e->type == u->type && e->team == u->team && e->frame == frame)
        {
            e->used = ++s->sprite_clock;
            return &e->image;
        }
        if (!e->occupied || e->used < chosen->used) chosen = e;
    }
    ra_voxel_image_close(&chosen->image);
    chosen->occupied = false;
    size_t size = (size_t)v->shape.width * v->shape.height;
    uint8_t *pixels = malloc(size);
    if (!pixels)
    {
        ra_fail(error, RA_MEMORY, 0, "infantry frame allocation failed");
        return NULL;
    }
    bool ok = ra_shp_decode(&v->shape, frame, pixels, size, error) && ra_voxel_image_create(&chosen->image, v->shape.width, v->shape.height, error);
    if (!ok)
    {
        free(pixels);
        return NULL;
    }
    ra_voxel_image *out = &chosen->image;
    /* SHP 透明区必须确定性清零；图像分配器不承诺返回已初始化的堆内存。 */
    memset(out->pixels, 0, size * sizeof(*out->pixels));
    memset(out->depth, 0, size * sizeof(*out->depth));
    out->origin_x = (float)out->width / 2;
    out->origin_y = (float)out->height / 2;
    out->min_x = (int)out->width;
    out->min_y = (int)out->height;
    out->max_x = out->max_y = 0;
    ra_rgb house = u->team == 1 ? (ra_rgb){70, 155, 245} : ra_battle_allied(&s->battle, 1, u->team) ? (ra_rgb){235, 210, 70} : (ra_rgb){235, 65, 55};
    for (uint32_t y = 0; y < out->height; ++y)
        for (uint32_t x = 0; x < out->width; ++x)
        {
            size_t at = (size_t)y * out->width + x;
            uint8_t index = pixels[at];
            if (!index) continue;
            ra_rgb color = s->voxels.palette.colors[index];
            if (index >= 16 && index <= 31)
            {
                uint32_t shade = (31 - index) * 10 + 105;
                color.r = (uint8_t)(house.r * shade / 255);
                color.g = (uint8_t)(house.g * shade / 255);
                color.b = (uint8_t)(house.b * shade / 255);
            }
            out->pixels[at] = 0xff000000u | (uint32_t)color.r << 16 | (uint32_t)color.g << 8 | color.b;
            out->depth[at] = 0;
            ++out->drawn_pixels;
            if ((int)x < out->min_x) out->min_x = (int)x;
            if ((int)x > out->max_x) out->max_x = (int)x;
            if ((int)y < out->min_y) out->min_y = (int)y;
            if ((int)y > out->max_y) out->max_y = (int)y;
        }
    free(pixels);
    chosen->type = u->type;
    chosen->team = u->team;
    chosen->frame = frame;
    chosen->occupied = true;
    chosen->used = ++s->sprite_clock;
    return out;
}
