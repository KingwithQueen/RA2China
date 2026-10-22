#pragma once
#include <stdint.h>
/* 隧道内部角度换算和查表索引，逐次保留原版舍入。 */
double ra2_ground_connection_angle(int32_t direction, double radians_per_turn, uint16_t control);
float ra2_ground_connection_component(double angle, float index_scale, const float *table,
    int cosine, uint16_t control);
