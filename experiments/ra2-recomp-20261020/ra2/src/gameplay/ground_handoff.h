#pragma once
#include "unit_movement.h"
/* 桥面存在且高度层差大于2时使用上层。差值和绝对值沿用32位回绕。 */
unsigned ra2_ground_prepare_upper_layer(uint32_t cell_flags,int8_t cell_level,int32_t z,int32_t height_per_level);
