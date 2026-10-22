#pragma once
#include <stdint.h>

/* 模拟 fild int32 / fmul float64 / fstp float32，保留原版 PC/RC 语义，返回 IEEE 754 位模式。 */
uint32_t ra2_x87_imul_store_f32(int32_t integer, uint64_t coefficient, uint16_t control);
