#pragma once
#include <stdint.h>

/* 按原版乘法精度与舍入方向计算百分比，再保存为规则表的double。 */
double ra2_combat_warhead_percent(int32_t percent,double percent_unit,uint16_t control);
