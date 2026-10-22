#pragma once
#include <stdint.h>

/* 原版数值兼容层：数值表示为带符号整数尾数乘二的幂，不依赖宿主浮点舍入。 */
typedef struct Ra2LegacyReal
{
    uint64_t significand;
    int32_t exponent;
    unsigned negative;
} Ra2LegacyReal;

Ra2LegacyReal ra2_real_from_i32(int32_t value);
Ra2LegacyReal ra2_real_from_f32(float value);
Ra2LegacyReal ra2_real_from_f64(double value);
Ra2LegacyReal ra2_real_add(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control);
Ra2LegacyReal ra2_real_subtract(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control);
Ra2LegacyReal ra2_real_multiply(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control);
int32_t ra2_real_truncate_i32(Ra2LegacyReal value);
/* 有限、范围受约束的坐标/方向值：按 RC 舍入为整数，保留 EAX 的低 32 位。 */
int32_t ra2_real_round_i32(Ra2LegacyReal value, uint16_t control);
float ra2_real_store_f32(Ra2LegacyReal value, uint16_t control);
double ra2_real_store_f64(Ra2LegacyReal value, uint16_t control);
