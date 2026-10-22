#ifndef RA2_VOXEL_SCENE_H
#define RA2_VOXEL_SCENE_H
#include "asset_profile.h"
#include "ra2/voxel.h"

typedef struct {
    ra_vfs vfs;
    ra_resource rule_bytes, art_bytes, text_bytes, vpl_bytes;
    ra_ini rules, art;
    ra_csf text;
    ra_palette palette;
    ra_vpl vpl;
} voxel_context;
typedef struct {
    ra_vxl vxl;
    ra_hva hva;
    size_t *mapping;
    char *source, *animation_source;
    bool index_binding;
} voxel_model;
typedef struct {
    voxel_model models[3];
    ra_voxel_part parts[3];
    size_t count, frames;
    char id[128], image[128];
    const char *title;
} voxel_scene;

bool voxel_context_open(voxel_context *context, const char *original, const char *mod, ra_error *error);
void voxel_context_close(voxel_context *context);
bool voxel_model_load(voxel_model *model, const ra_vfs *vfs, const char *base, ra_error *error);
void voxel_model_close(voxel_model *model);
bool voxel_scene_load(voxel_scene *scene, const voxel_context *context, const char *id, bool assemble, ra_error *error);
void voxel_scene_close(voxel_scene *scene);
#endif
