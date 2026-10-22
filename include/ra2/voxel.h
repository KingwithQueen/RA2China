#ifndef RA2_VOXEL_H
#define RA2_VOXEL_H
#include "assets.h"

typedef struct
{
    uint8_t x, y, z, color, normal;
} ra_voxel;
typedef struct
{
    char name[17];
    uint32_t id, header_one, header_zero;
    float scale, transform[12], bounds[6];
    uint8_t size[3], normal_type;
    ra_voxel *voxels;
    size_t voxel_count, unmapped_normals;
} ra_vxl_section;
typedef struct
{
    uint8_t remap_start, remap_end, palette[768];
    ra_vxl_section *sections;
    size_t section_count, voxel_count;
} ra_vxl;

/* VXL 完整解码后拥有全部数据，不再借用输入。 */
bool ra_vxl_parse(ra_vxl *vxl, ra_view bytes, ra_error *error);
void ra_vxl_close(ra_vxl *vxl);

typedef struct
{
    char name[17];
    char (*sections)[17];
    float *matrices;
    size_t frame_count, section_count;
} ra_hva;
/* HVA 保留帧优先的行主序 3×4 矩阵；名称映射独立于文件中的排列。 */
bool ra_hva_parse(ra_hva *hva, ra_view bytes, ra_error *error);
bool ra_hva_bind(const ra_vxl *vxl, const ra_hva *hva, size_t *mapping, size_t capacity, ra_error *error);
void ra_hva_close(ra_hva *hva);

typedef struct
{
    uint32_t remap_start, remap_end, section_count, reserved;
    uint8_t palette[768];
    ra_view tables;
} ra_vpl;
/* VPL 的查色表借用输入；调色板按原始字节保留，预览使用外部 PAL。 */
bool ra_vpl_parse(ra_vpl *vpl, ra_view bytes, ra_error *error);
bool ra_vpl_lookup(const ra_vpl *vpl, size_t shade, uint8_t color, uint8_t *result, ra_error *error);

/* 每个部件可独立旋转；VXL/HVA 和映射须在绘制期间保持有效。 */
typedef struct
{
    const ra_vxl *vxl;
    const ra_hva *hva;
    const size_t *mapping;
    float yaw, offset[3];
} ra_voxel_part;
typedef struct
{
    float yaw, pitch, zoom, light_yaw;
    bool use_vpl, remap;
    ra_rgb house_color;
    int section; /* -1 显示全部，其他值仅用于单个部件的节序号。 */
    /* 零值沿用资源预览；战场使用固定像素比例、模型原点与地图 Y 轴约定。 */
    float pixels_per_unit, origin_x, origin_y;
    bool world_axes;
} ra_voxel_camera;
typedef struct
{
    uint32_t *pixels;
    float *depth;
    size_t width, height, drawn_pixels;
    float origin_x, origin_y;
    int min_x, min_y, max_x, max_y;
} ra_voxel_image;

bool ra_voxel_image_create(ra_voxel_image *image, size_t width, size_t height, ra_error *error);
void ra_voxel_image_close(ra_voxel_image *image);
bool ra_voxel_render(const ra_voxel_part *parts, size_t count, size_t frame, const ra_palette *palette, const ra_vpl *vpl, const ra_voxel_camera *camera,
                     ra_voxel_image *image, ra_error *error);
/* 底盘矩阵在部件旋转之后、相机投影之前应用；普通预览可传 NULL。 */
bool ra_voxel_render_chassis(const ra_voxel_part *parts, size_t count, size_t frame, const ra_palette *palette, const ra_vpl *vpl,
                             const ra_voxel_camera *camera, const float chassis[12], ra_voxel_image *image, ra_error *error);
bool ra_voxel_transform(const ra_vxl_section *section, const float *matrix, const float point[3], float output[3], ra_error *error);
bool ra_voxel_normal(uint8_t type, uint8_t index, float output[3]);
#endif
