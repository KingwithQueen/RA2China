#pragma once
#include "unit_movement.h"

/* Integer constant expressions also used by the opt-in cell value contract. */
#define RA2_GROUND_CELL_QUOTIENT_VALUE(coordinate) ((int32_t)(coordinate) / 256)
#define RA2_GROUND_CELL_COMPONENTS_VALUE(x, y) ((uint32_t)(uint16_t)(x) | ((uint32_t)(uint16_t)(y) << 16))
#define RA2_GROUND_PACKED_WORLD_CELL_VALUE(x, y) RA2_GROUND_CELL_COMPONENTS_VALUE(RA2_GROUND_CELL_QUOTIENT_VALUE(x), RA2_GROUND_CELL_QUOTIENT_VALUE(y))

/* Convert a world axis before caller-specific narrowing. */
static inline int32_t ra2_ground_world_cell_quotient(int32_t coordinate)
{
    return RA2_GROUND_CELL_QUOTIENT_VALUE(coordinate);
}

/* Original X/Y cell projection: truncate toward zero, then narrow; ignore altitude. */
static inline int ra2_ground_same_map_cell(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return (uint16_t)ra2_ground_world_cell_quotient(left.x) == (uint16_t)ra2_ground_world_cell_quotient(right.x)
        && (uint16_t)ra2_ground_world_cell_quotient(left.y) == (uint16_t)ra2_ground_world_cell_quotient(right.y);
}

/* Preserve the original packed cell layout: X in the low half, Y in the high half. */
static inline uint32_t ra2_ground_pack_cell_components(uint16_t x, uint16_t y)
{
    return RA2_GROUND_CELL_COMPONENTS_VALUE(x, y);
}

/* Project world X/Y before packing the two unsigned cell components. */
static inline uint32_t ra2_ground_pack_world_cell(int32_t x, int32_t y)
{
    return RA2_GROUND_PACKED_WORLD_CELL_VALUE(x, y);
}
