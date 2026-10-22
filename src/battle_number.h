#ifndef RA2_BATTLE_NUMBER_H
#define RA2_BATTLE_NUMBER_H
#include <stdint.h>

/* 有限正规二进制数的位表示；运算用整数复现原版 53 位、向零截断，不依赖宿主浮点环境。 */
typedef uint64_t battle_real;
#define BATTLE_ONE UINT64_C(0x3ff0000000000000)
battle_real battle_real_ratio(uint32_t numerator, uint32_t denominator);
battle_real battle_real_int(int32_t value);
battle_real battle_real_float(uint32_t value);
uint32_t battle_real_float_bits(battle_real value);
battle_real battle_real_add(battle_real a, battle_real b);
battle_real battle_real_sub(battle_real a, battle_real b);
battle_real battle_real_mul(battle_real a, battle_real b);
battle_real battle_real_div(battle_real a, battle_real b);
battle_real battle_real_sqrt(battle_real value);
int32_t battle_real_integer(battle_real value);
int battle_real_compare(battle_real a, battle_real b);
#endif
