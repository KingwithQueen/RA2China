#pragma once
#include <stdint.h>

typedef struct Ra2TerrainConstraint
{
    int32_t required_land;
    int32_t cell_land;
    int32_t overlay_index;
    int32_t reference_level;
    int32_t cell_level;
    int32_t tile_property_2b4;
    int32_t tile_property_2b8;
    unsigned cell_subposition;
} Ra2TerrainConstraint;

/* 0x7030B6..0x703182：指定地形类别的限制及两组斜坡子格。
   tile 的两个字段尚未确认正式名称，保留偏移名以免误导 MOD 修改者。
   不受地形限制的 -1、特殊地形 10 和桥覆盖物 237/238 都有独立规则。 */
int ra2_ground_terrain_is_blocked(const Ra2TerrainConstraint *terrain);

/* 对象扫描结束后，只在地面层检查地形速度；上层占用沿用既有占格收尾。
   保留 x87 fcomp 的无序比较行为，便于片段对照；合法规则使用有限非负速度。 */
int ra2_ground_terrain_speed_is_blocked(unsigned upper_layer, uint32_t speed_factor_bits);
