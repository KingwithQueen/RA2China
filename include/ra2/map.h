#ifndef RA2_MAP_H
#define RA2_MAP_H
#include "assets.h"

/* 解码器要求完整消费压缩流，并精确产生指定长度；绝不返回半幅数据。 */
bool ra_lzo_decode(ra_view input, uint8_t *output, size_t size, ra_error *error);
bool ra_lcw_decode(ra_view input, uint8_t *output, size_t size, ra_error *error);
bool ra_map_pack(const ra_ini *ini, const char *section, bool lzo, uint8_t **output, size_t *size, ra_error *error);

/* TMP 帧表拥有内存，像素和深度数据借用输入；零偏移表示不存在的子块。 */
typedef struct
{
    bool present;
    int32_t x, y, extra_x, extra_y, extra_width, extra_height;
    uint32_t flags;
    uint8_t height, terrain, ramp;
    ra_rgb radar_left, radar_right;
    ra_view pixels, depth, extra, extra_depth;
} ra_tmp_tile;
typedef struct
{
    uint32_t columns, rows, width, height;
    ra_tmp_tile *tiles;
    size_t count;
} ra_tmp;
bool ra_tmp_open(ra_tmp *tmp, ra_view input, ra_error *error);
void ra_tmp_close(ra_tmp *tmp);

typedef struct
{
    uint16_t x, y;
    uint32_t tile;
    uint8_t subtile, height, ice;
} ra_map_cell;
typedef enum
{
    RA_MAP_WAYPOINT,
    RA_MAP_STRUCTURE,
    RA_MAP_UNIT,
    RA_MAP_INFANTRY,
    RA_MAP_AIRCRAFT,
    RA_MAP_TERRAIN,
    RA_MAP_SMUDGE
} ra_map_object_kind;
typedef struct
{
    ra_map_object_kind kind;
    int x, y, number;
    char *type, *owner;
    uint32_t health, facing;
    size_t source_line;
} ra_map_object;
typedef struct
{
    ra_ini ini;
    char theater[16];
    int size[4], local[4];
    ra_map_cell *cells;
    size_t cell_count;
    size_t stored_cells, defaulted_cells;
    int32_t *cell_index;
    uint8_t *overlay, *overlay_data, *preview;
    size_t preview_size;
    int preview_width, preview_height;
    ra_map_object *objects;
    size_t object_count, outside_objects, overlay_count, trailing_bytes, preamble_entries;
} ra_map;
/* 原始 INI 全部保留，未模拟的触发、脚本、局部规则等仍可查询。 */
bool ra_map_open(ra_map *map, ra_view input, const char *source, ra_error *error);
const ra_map_cell *ra_map_at(const ra_map *map, int x, int y);
void ra_map_close(ra_map *map);
#endif
