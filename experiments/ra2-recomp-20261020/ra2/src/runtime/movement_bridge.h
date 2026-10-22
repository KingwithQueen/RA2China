#pragma once
#include <stdint.h>

uint32_t ra2_movement_progress_bits(int32_t progress, uint16_t control);
void ra2_movement_interpolate_bridge(void);
void ra2_movement_transform_bridge(void);
