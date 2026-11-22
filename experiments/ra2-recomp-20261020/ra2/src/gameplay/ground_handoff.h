#pragma once
#include "unit_movement.h"
/* 桥面存在且高度层差大于2时使用上层。差值和绝对值沿用32位回绕。 */
unsigned ra2_ground_prepare_upper_layer(uint32_t cell_flags,int8_t cell_level,int32_t z,int32_t height_per_level);

/* Upper-layer notification after the caller has established a bridge. */
static inline int ra2_ground_upper_layer_at_height(int32_t cell_level, int32_t z, int32_t height_per_level)
{
    int32_t divided = z / height_per_level;
    uint32_t difference = (uint32_t)divided - (uint32_t)cell_level;
    uint32_t absolute = difference & UINT32_C(0x80000000) ? 0u - difference : difference;
    return absolute > 2u && absolute < UINT32_C(0x80000000);
}
