#pragma once
#include "unit_movement.h"

/* Exact world-point equality includes altitude; not a planar cell test. */
static inline int ra2_ground_same_world_point(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return left.x == right.x && left.y == right.y && left.z == right.z;
}
