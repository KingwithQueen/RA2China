#ifndef RA2_VOXEL_INTERNAL_H
#define RA2_VOXEL_INTERNAL_H
#include "internal.h"
#include "ra2/voxel.h"
#include <math.h>
#include <string.h>

static inline float voxel_float(const uint8_t *p)
{
    uint32_t bits = ra_le32(p);
    float value;
    memcpy(&value, &bits, sizeof(value));
    return value;
}

static inline bool voxel_number(float number)
{
    return isfinite(number) && fabsf(number) <= 1000000.0f;
}

static inline bool voxel_name(char result[17], const uint8_t *data)
{
    size_t i;
    memcpy(result, data, 16);
    result[16] = 0;
    for (i = 0; i < 16 && result[i]; ++i) if ((uint8_t)result[i] < 32 || (uint8_t)result[i] > 126) return false;
    return result[0] != 0;
}
#endif
