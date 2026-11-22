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

/* Opposite slot in the eight-way direction ring. */
static inline unsigned ra2_ground_opposite_heading(int32_t heading)
{
    return ((uint32_t)heading - 4u) & 7u;
}

/* Round a heading byte to the nearest slot, wrapping slot eight to zero. */
static inline unsigned ra2_ground_heading_octant(uint8_t heading)
{
    return ((((unsigned)heading >> 4) + 1u) >> 1) & 7u;
}

/* Row-major selector for the eight direction columns. */
static inline uint32_t ra2_ground_template_selector_bits(uint32_t row, uint32_t column)
{
    return column + row * 8u;
}

/* Quarter-turn classification on the eight-way ring; callers handle sentinels. */
static inline int ra2_ground_is_quarter_turn(int32_t direction, int32_t previous)
{
    unsigned turn = ((uint32_t)direction - (uint32_t)previous) & 7u;
    return turn == 2u || turn == 6u;
}

/* Path shortening uses a linear middle heading and keeps the zero fallback. */
static inline int32_t ra2_ground_legacy_corner_middle(int32_t first, int32_t second)
{
    int32_t middle = (first + second) / 2;
    return (middle + 1 == first || middle + 1 == second) ? middle : 0;
}
