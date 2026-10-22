#include <stdint.h>
#include "x87_precision.h"

/* 使用整数保存精确乘积，避免宿主 SSE 舍入方式改变原版 x87 指令的结果。 */
static unsigned highest_bit(uint64_t value)
{
    unsigned bit = 0;
    while (value >>= 1) ++bit;
    return bit;
}

static int round_up(uint64_t quotient, uint64_t remainder, uint64_t half, unsigned rounding, unsigned negative)
{
    if (!remainder) return 0;
    if (rounding == 1) return negative != 0;
    if (rounding == 2) return negative == 0;
    if (rounding == 3) return 0;
    return remainder > half || (remainder == half && (quotient & 1));
}

static uint64_t round_shift(uint64_t value, unsigned shift, unsigned rounding, unsigned negative)
{
    if (!shift) return value;
    if (shift > 64) return round_up(0, value, UINT64_MAX, rounding, negative) ? 1 : 0;
    uint64_t quotient = shift == 64 ? 0 : value >> shift;
    uint64_t remainder = shift == 64 ? value : value & ((UINT64_C(1) << shift) - 1);
    return quotient + (uint64_t)round_up(quotient, remainder, UINT64_C(1) << (shift - 1), rounding, negative);
}

static uint32_t overflow_value(unsigned rounding, unsigned negative)
{
    int infinity = rounding == 0 || (rounding == 1 && negative) || (rounding == 2 && !negative);
    return (negative << 31) | (infinity ? 0x7F800000u : 0x7F7FFFFFu);
}

uint32_t ra2_x87_imul_store_f32(int32_t integer, uint64_t coefficient, uint16_t control)
{
    unsigned negative = (unsigned)(coefficient >> 63) ^ (integer < 0);
    unsigned rounding = (control >> 10) & 3, pc = (control >> 8) & 3;
    unsigned precision = pc == 0 ? 24 : pc == 2 ? 53 : 64;
    unsigned encoded_exponent = (unsigned)((coefficient >> 52) & 2047);
    uint64_t significand = coefficient & UINT64_C(0xFFFFFFFFFFFFF);
    uint32_t magnitude = integer < 0 ? 0u - (uint32_t)integer : (uint32_t)integer;
    uint32_t sign = negative << 31;
    if (encoded_exponent == 2047)
    {
        if (significand) return ((uint32_t)(coefficient >> 32) & 0x80000000u) | 0x7FC00000u | (uint32_t)(significand >> 29);
        return magnitude ? sign | 0x7F800000u : 0xFFC00000u;
    }
    if (!magnitude || (!encoded_exponent && !significand)) return sign;
    int scale = (encoded_exponent ? (int)encoded_exponent - 1023 : -1022) - 52;
    if (encoded_exponent) significand |= UINT64_C(1) << 52;

    /* 53 位尾数乘 32 位整数，最多 84 位；拆成两个 64 位字即可精确容纳。 */
    uint64_t low_product = (significand & UINT32_MAX) * magnitude;
    uint64_t high_product = (significand >> 32) * magnitude;
    uint64_t low = low_product + (high_product << 32);
    uint64_t high = (high_product >> 32) + (low < low_product);
    unsigned top = high ? highest_bit(high) + 64 : highest_bit(low);
    unsigned shift = top + 1 > precision ? top + 1 - precision : 0;
    uint64_t rounded = low;
    if (shift)
    {
        /* 此乘积长度保证 shift < 64；首先按原版 PC 和 RC 舍入乘法结果。 */
        rounded = (low >> shift) | (high << (64 - shift));
        uint64_t remainder = low & ((UINT64_C(1) << shift) - 1);
        int increment = round_up(rounded, remainder, UINT64_C(1) << (shift - 1), rounding, negative);
        scale += (int)shift;
        if (increment && rounded == UINT64_MAX)
        {
            rounded = UINT64_C(1) << 63;
            ++scale;
        }
        else rounded += (uint64_t)increment;
    }

    /* 再按 RC 舍入到单精度；这与先用 C double 最近舍入再转换不同。 */
    top = highest_bit(rounded);
    int exponent = scale + (int)top;
    if (exponent > 127) return overflow_value(rounding, negative);
    if (exponent < -126)
    {
        unsigned subnormal_shift = (unsigned)(-149 - scale);
        return sign | (uint32_t)round_shift(rounded, subnormal_shift, rounding, negative);
    }
    uint64_t fraction = top > 23 ? round_shift(rounded, top - 23, rounding, negative) : rounded << (23 - top);
    if (fraction >= (UINT64_C(1) << 24))
    {
        fraction >>= 1;
        if (++exponent > 127) return overflow_value(rounding, negative);
    }
    return sign | ((uint32_t)(exponent + 127) << 23) | ((uint32_t)fraction & 0x7FFFFFu);
}
