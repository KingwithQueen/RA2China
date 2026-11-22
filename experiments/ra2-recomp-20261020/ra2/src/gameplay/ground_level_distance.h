#pragma once
#include <stdint.h>

/* Preserve the original signed comparison of the folded level difference. */
static inline int ra2_ground_levels_separated(int32_t left, int32_t right)
{
    uint32_t distance = (uint32_t)left - (uint32_t)right;
    if (distance & UINT32_C(0x80000000))
        distance = 0u - distance;
    return distance >= 2u && distance < UINT32_C(0x80000000);
}
