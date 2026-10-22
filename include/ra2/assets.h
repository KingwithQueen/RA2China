#ifndef RA2_ASSETS_H
#define RA2_ASSETS_H

#include "ra2.h"

/* PAL 不拥有输入；RGB 分量采用 (v << 2) | (v >> 4) 扩展至八位。 */
typedef struct { uint8_t r, g, b; } ra_rgb;
typedef struct { ra_rgb colors[256]; } ra_palette;
bool ra_palette_parse(ra_palette *palette, ra_view bytes, ra_error *error);

/* SHP 借用输入，帧表由对象拥有。关闭 SHP 后才能释放资源或卸载 VFS。 */
typedef struct {
    uint16_t x, y, width, height;
    uint32_t flags, color, reserved, offset;
    size_t data_end;
} ra_shp_frame;

typedef struct {
    ra_view bytes;
    uint16_t width, height, count;
    ra_shp_frame *frames;
    size_t clipped_zero_runs, short_rows;
} ra_shp;

/* 打开时验证全部帧；解码输出完整画布的索引，裁剪区域外补零。 */
bool ra_shp_open(ra_shp *shp, ra_view bytes, ra_error *error);
bool ra_shp_decode(const ra_shp *shp, size_t frame, uint8_t *pixels, size_t capacity, ra_error *error);
void ra_shp_close(ra_shp *shp);

/* CSF 拥有标签及 UTF-8 文本；附加字节借用原文件，长度单独保存。 */
typedef struct { char *text; size_t length; ra_view extra; bool has_extra; } ra_csf_value;
typedef struct { char *name; size_t first_value, value_count; } ra_csf_label;
typedef struct {
    uint32_t version, language, reserved;
    ra_csf_label *labels;
    ra_csf_value *values;
    size_t label_count, value_count, duplicate_count;
    size_t *index;
    size_t index_capacity;
} ra_csf;

/* 支持版本 2/3；查询忽略 ASCII 大小写，重复标签保留且末次生效。 */
bool ra_csf_parse(ra_csf *csf, ra_view bytes, ra_error *error);
const ra_csf_label *ra_csf_get(const ra_csf *csf, const char *name);
void ra_csf_close(ra_csf *csf);

#endif
