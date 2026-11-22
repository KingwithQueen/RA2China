#pragma once
#include "unit_movement.h"

/* Original X/Y cell projection: truncate toward zero, then narrow; ignore altitude. */
static inline int ra2_ground_same_map_cell(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return (uint16_t)(left.x / 256) == (uint16_t)(right.x / 256)
        && (uint16_t)(left.y / 256) == (uint16_t)(right.y / 256);
}
