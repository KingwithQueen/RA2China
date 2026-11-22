#pragma once
#include <stdint.h>

/* A link blocks headings three to five slots away in the eight-way set. */
static inline int ra2_ground_direction_conflicts(int32_t heading, int32_t link_heading)
{
    uint32_t distance = (uint32_t)heading - (uint32_t)link_heading;
    if (distance & UINT32_C(0x80000000))
        distance = 0u - distance;
    return distance > 2u && distance < 6u;
}
