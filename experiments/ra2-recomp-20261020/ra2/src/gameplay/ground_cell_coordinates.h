#pragma once
#include "unit_movement.h"

/* Convert a world axis before caller-specific narrowing. */
static inline int32_t ra2_ground_world_cell_quotient(int32_t coordinate)
{
    return coordinate / 256;
}

/* Original X/Y cell projection: truncate toward zero, then narrow; ignore altitude. */
static inline int ra2_ground_same_map_cell(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return (uint16_t)(left.x / 256) == (uint16_t)(right.x / 256)
        && (uint16_t)(left.y / 256) == (uint16_t)(right.y / 256);
}

/* Preserve the original packed cell layout: X in the low half, Y in the high half. */
static inline uint32_t ra2_ground_pack_cell_components(uint16_t x, uint16_t y)
{
    return (uint32_t)x | ((uint32_t)y << 16);
}

/* Project world X/Y before packing the two unsigned cell components. */
static inline uint32_t ra2_ground_pack_world_cell(int32_t x, int32_t y)
{
    return ra2_ground_pack_cell_components((uint16_t)ra2_ground_world_cell_quotient(x),
        (uint16_t)ra2_ground_world_cell_quotient(y));
}
