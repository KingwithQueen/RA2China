#ifndef RA2_BATTLE_SCENE_H
#define RA2_BATTLE_SCENE_H
#include "map_scene.h"
#include "voxel_scene.h"
#include "ra2/battle.h"
#include "ra2/economy.h"
#include "ra2/campaign.h"
#include "structure_scene.h"
typedef struct
{
    char id[64], country[64];
    uint32_t credits;
} scene_house;
typedef struct
{
    size_t line;
    char type[64], reason[160];
} scene_issue;
typedef struct
{
    map_context maps;
    voxel_context voxels;
    ra_map map;
    map_image ground, deck;
    uint8_t *deck_heights;
    ra_battle battle;
    voxel_scene models[26];
    ra_voxel_image sprites[26][2][32][32], slope_sprites[RA_BATTLE_UNITS];
    uint32_t slope_keys[RA_BATTLE_UNITS];
    structure_visual *structure_visuals;
    structure_sprite structure_sprites[96];
    uint32_t sprite_clock;
    scene_house houses[RA_BATTLE_TEAMS];
    uint32_t house_count;
    scene_issue *issues;
    size_t unit_source_lines[RA_BATTLE_UNITS];
    size_t issue_count, structure_count, imported_units, pending_weapons;
    bool scenario, campaign_mode;
    struct battle_infantry_visual *infantry_visuals;
    structure_sprite infantry_sprites[96];
    bool economy_mode, economy_allied, mcv_mode;
    ra_resource ore_bytes[2];
    ra_shp ore_shapes[2];
    ra_palette ore_palette;
    uint8_t *ore_pixels[2];
    ra_resource impact_bytes;
    ra_shp impact;
    ra_palette impact_palette;
    uint8_t *impact_pixels;
    uint32_t rendered_revision;
    size_t source, missing, obstacles, bridges, unsupported_foundations, low_bridges, pending_bridges;
} battle_scene;
bool battle_scene_open(battle_scene *scene, const char *original, ra_error *error);
bool battle_scene_refresh(battle_scene *scene, ra_error *error);
bool battle_scene_map(battle_scene *scene, size_t source, bool graphics, ra_error *error);
void battle_scene_close(battle_scene *scene);
void battle_unit_pixel(const battle_scene *scene, const ra_battle_unit *unit, int *x, int *y);
/* 固定战场相机下，将体素像素的深度还原为地图高度。 */
float battle_sprite_height(const ra_voxel_image *sprite, size_t pixel, int32_t unit_height);
bool battle_scene_goal(battle_scene *scene, uint32_t unit, uint32_t distance, uint32_t *goal);
/* 原版地图桥口验证夹具：重新布置测试坦克，地图和资源保持只读。 */
bool battle_scene_bridge_fixture(battle_scene *scene, uint32_t *goal, ra_error *error);
bool battle_scene_bridge_lifecycle_fixture(battle_scene *scene, uint32_t *cell, uint32_t *goal, ra_error *error);
bool battle_file_write(const char *path, const void *data, size_t size, ra_error *error);
const ra_voxel_image *battle_scene_missile_sprite(battle_scene *scene, const ra_battle_shot *shot, ra_error *error);
const ra_voxel_image *battle_scene_sprite(battle_scene *scene, const ra_battle_unit *unit, ra_error *error);
int battle_bridge_draw_offset(uint32_t kind, uint32_t frame);
const ra_voxel_image *battle_scene_infantry_sprite(battle_scene *scene, const ra_battle_unit *unit, ra_error *error);
void battle_scene_infantry_clear(battle_scene *scene);
bool battle_scene_campaign_report(const battle_scene *scene, const char *path, ra_error *error);
bool battle_scene_people_types(battle_scene *scene, ra_error *error);
bool battle_scene_import(battle_scene *scene, ra_error *error);
const ra_voxel_image *battle_scene_structure_sprite(battle_scene *scene, const ra_battle_unit *unit, ra_error *error);
void battle_scene_structures_clear(battle_scene *scene);
bool battle_scene_base_fixture(battle_scene *scene, uint32_t *target, ra_error *error);
bool battle_scene_economy_fixture(battle_scene *scene, ra_error *error);
bool battle_scene_economy_images(battle_scene *scene, ra_error *error);
bool battle_scene_economy_report(const battle_scene *scene, const char *path, ra_error *error);
#endif
