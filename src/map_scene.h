#ifndef RA2_MAP_SCENE_H
#define RA2_MAP_SCENE_H
#include "ra2/map.h"
#include "asset_profile.h"

typedef struct
{
    char name[64];
    char *source;
    ra_view bytes;
} map_source;
typedef struct
{
    char name[64];
    ra_resource resource;
    ra_tmp tmp;
    bool loaded;
} map_template;
typedef struct
{
    ra_ini ini;
    ra_palette palette;
    map_template *templates;
    size_t count;
} map_theater;
typedef struct
{
    ra_vfs vfs;
    ra_file archives[3];
    ra_mix maps[3];
    ra_file terrain_file;
    ra_mix terrain_root, terrain_archives[7];
    ra_ini missions;
    ra_ini rules;
    const char *overlay_names[256];
    size_t overlay_name_count;
    ra_csf strings;
    map_source *sources;
    size_t source_count;
    map_theater theaters[3];
} map_context;
typedef struct
{
    uint32_t *pixels;
    int32_t *picked;
    int width, height, origin_x, origin_y;
    size_t drawn, missing;
} map_image;

bool map_context_open(map_context *context, const char *original, const char *mod, ra_error *error);
void map_context_close(map_context *context);
int map_theater_id(const char *name);
bool map_theater_open(map_context *context, int theater, ra_error *error);
bool map_template_get(map_context *context, int theater, uint32_t id, map_template **tile, ra_error *error);
bool map_render(map_context *context, const ra_map *map, map_image *image, bool overlays, bool objects, bool local, ra_error *error);
bool map_tmp_render(const ra_tmp *tmp, const ra_palette *palette, map_image *image, ra_error *error);
bool map_image_bmp(const map_image *image, const char *path, ra_error *error);
void map_image_close(map_image *image);
#endif
