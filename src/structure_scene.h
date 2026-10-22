#ifndef RA2_STRUCTURE_SCENE_H
#define RA2_STRUCTURE_SCENE_H
#include "voxel_scene.h"
#include "ra2/battle.h"

typedef struct
{
    ra_resource bytes;
    ra_shp shape;
    uint32_t first, last;
    int x, y;
    unsigned state;
    bool animated;
    char filename[96];
} structure_layer;
typedef struct
{
    structure_layer layers[18];
    size_t count, missing_layers;
    int width, height;
    bool opened, failed, remap, terrain_palette;
    char image[64];
} structure_visual;
typedef struct
{
    ra_voxel_image image;
    uint32_t type, team, frame, state, used;
    bool occupied;
} structure_sprite;
bool structure_visual_open(structure_visual *visual, const voxel_context *context, const char *id, const char *override_image, int theater, ra_error *error);
bool structure_visual_render(const structure_visual *visual, const ra_palette *palette, const ra_battle_type *type, uint32_t team, bool damaged, uint32_t tick,
                             ra_voxel_image *image, ra_error *error);
void structure_visual_close(structure_visual *visual);
#endif
