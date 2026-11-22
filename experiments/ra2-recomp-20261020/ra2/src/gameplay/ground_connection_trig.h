#pragma once
#include <stdint.h>
/* 隧道内部角度换算和查表索引，逐次保留原版舍入。 */
double ra2_ground_connection_angle(int32_t direction, double radians_per_turn, uint16_t control);
float ra2_ground_connection_component(double angle, float index_scale, const float *table,
    int cosine, uint16_t control);

/* Select a wrapped phase slot after the caller's own quantization. */
static inline int32_t ra2_ground_connection_phase_slot(int32_t quantized, int cosine)
{
    int32_t index = quantized / 2 % 8192;
    if (index < 0) index += 8192;
    if (cosine) index += 2048;
    if (((uint32_t)quantized & 1u) && index < (cosine ? 10239 : 8191)) ++index;
    return index;
}
