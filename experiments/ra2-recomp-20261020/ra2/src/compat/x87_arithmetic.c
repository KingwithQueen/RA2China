#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "x87_arithmetic.h"

typedef struct WideUnsigned
{
    uint64_t high;
    uint64_t low;
} WideUnsigned;

_Noreturn static void unsupported_value(void)
{
    fputs("[movement-numeric-error] unsupported non-finite operand or reserved precision\n", stderr);
    abort();
}

static unsigned highest_bit(uint64_t value)
{
    unsigned bit = 0;
    while (value >>= 1)
    {
        ++bit;
    }
    return bit;
}

static unsigned precision_bits(uint16_t control)
{
    switch ((control >> 8) & 3)
    {
        case 0: return 24;
        case 2: return 53;
        case 3: return 64;
        default: unsupported_value();
    }
}

/* remainder_relation：-1 表示小于半单位，0 表示恰好一半，1 表示大于一半。 */
static int increment_required(uint64_t retained, int discarded, int remainder_relation, unsigned negative, uint16_t control)
{
    if (!discarded)
    {
        return 0;
    }
    switch ((control >> 10) & 3)
    {
        case 0: return remainder_relation > 0 || (remainder_relation == 0 && (retained & 1));
        case 1: return negative != 0;
        case 2: return negative == 0;
        default: return 0;
    }
}

static uint64_t shift_and_round(WideUnsigned value, unsigned shift, unsigned negative, uint16_t control, int *carry)
{
    uint64_t retained, remainder, half;
    int discarded, relation;
    *carry = 0;
    if (!shift)
    {
        return value.low;
    }
    if (shift < 64)
    {
        retained = (value.low >> shift) | (value.high << (64 - shift));
        remainder = value.low & ((UINT64_C(1) << shift) - 1);
        half = UINT64_C(1) << (shift - 1);
        discarded = remainder != 0;
        relation = (remainder > half) - (remainder < half);
    }
    else if (shift == 64)
    {
        retained = value.high;
        half = UINT64_C(1) << 63;
        discarded = value.low != 0;
        relation = (value.low > half) - (value.low < half);
    }
    else if (shift < 128)
    {
        unsigned high_shift = shift - 64;
        retained = value.high >> high_shift;
        remainder = value.high & ((UINT64_C(1) << high_shift) - 1);
        half = UINT64_C(1) << (high_shift - 1);
        discarded = remainder != 0 || value.low != 0;
        relation = (remainder > half) - (remainder < half);
        if (!relation && value.low)
        {
            relation = 1;
        }
    }
    else
    {
        retained = 0;
        discarded = value.high != 0 || value.low != 0;
        relation = -1;
        if (shift == 128 && value.high >= (UINT64_C(1) << 63))
            relation = value.high == (UINT64_C(1) << 63) && !value.low ? 0 : 1;
    }
    if (increment_required(retained, discarded, relation, negative, control))
    {
        ++retained;
        *carry = retained == 0;
    }
    return retained;
}

static Ra2LegacyReal rounded(WideUnsigned exact, int32_t exponent, unsigned negative, uint16_t control)
{
    Ra2LegacyReal result = { 0, 0, negative };
    if (!exact.high && !exact.low)
    {
        return result;
    }
    unsigned top = exact.high ? highest_bit(exact.high) + 64 : highest_bit(exact.low);
    unsigned precision = precision_bits(control);
    unsigned shift = top + 1 > precision ? top + 1 - precision : 0;
    int carry;
    result.significand = shift_and_round(exact, shift, negative, control, &carry);
    result.exponent = exponent + (int32_t)shift;
    if (carry)
    {
        result.significand = UINT64_C(1) << 63;
        ++result.exponent;
    }
    return result;
}

Ra2LegacyReal ra2_real_from_i32(int32_t value)
{
    Ra2LegacyReal result = { value < 0 ? 0u - (uint32_t)value : (uint32_t)value, 0, value < 0 };
    return result;
}

Ra2LegacyReal ra2_real_from_f64(double value)
{
    uint64_t bits;
    memcpy(&bits, &value, sizeof(bits));
    unsigned exponent = (unsigned)((bits >> 52) & 2047);
    if (exponent == 2047)
    {
        unsupported_value();
    }
    Ra2LegacyReal result = { bits & UINT64_C(0xFFFFFFFFFFFFF), -1074, (unsigned)(bits >> 63) };
    if (exponent)
    {
        result.significand |= UINT64_C(1) << 52;
        result.exponent = (int32_t)exponent - 1075;
    }
    return result;
}

Ra2LegacyReal ra2_real_from_f32(float value)
{
    uint32_t bits;
    memcpy(&bits, &value, sizeof(bits));
    unsigned exponent = (bits >> 23) & 255;
    if (exponent == 255)
    {
        unsupported_value();
    }
    Ra2LegacyReal result = { bits & 0x7FFFFFu, -149, bits >> 31 };
    if (exponent)
    {
        result.significand |= UINT32_C(1) << 23;
        result.exponent = (int32_t)exponent - 150;
    }
    return result;
}

Ra2LegacyReal ra2_real_multiply(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control)
{
    uint64_t left_low = left.significand & UINT32_MAX, left_high = left.significand >> 32;
    uint64_t right_low = right.significand & UINT32_MAX, right_high = right.significand >> 32;
    uint64_t low_product = left_low * right_low;
    uint64_t middle = left_high * right_low + (low_product >> 32);
    uint64_t high_part = middle >> 32;
    middle = (middle & UINT32_MAX) + left_low * right_high;
    WideUnsigned exact = { left_high * right_high + high_part + (middle >> 32), (middle << 32) | (low_product & UINT32_MAX) };
    return rounded(exact, left.exponent + right.exponent, left.negative ^ right.negative, control);
}

/* 将最高有效位放在第 126 位，保留至少 62 位舍入余量；过小的另一操作数用末位标记剩余非零位。 */
static WideUnsigned aligned(Ra2LegacyReal value, int32_t common_exponent)
{
    WideUnsigned result = { 0, 0 };
    int32_t shift = value.exponent - common_exponent;
    if (shift >= 64)
    {
        result.high = value.significand << (shift - 64);
    }
    else if (shift > 0)
    {
        result.high = value.significand >> (64 - shift);
        result.low = value.significand << shift;
    }
    else if (!shift)
    {
        result.low = value.significand;
    }
    else if (shift <= -64)
    {
        result.low = value.significand != 0;
    }
    else
    {
        unsigned right_shift = (unsigned)-shift;
        result.low = (value.significand >> right_shift) | ((value.significand & ((UINT64_C(1) << right_shift) - 1)) != 0);
    }
    return result;
}

Ra2LegacyReal ra2_real_add(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control)
{
    if (!left.significand || !right.significand)
    {
        if (left.significand)
        {
            WideUnsigned exact = { 0, left.significand };
            return rounded(exact, left.exponent, left.negative, control);
        }
        if (right.significand)
        {
            WideUnsigned exact = { 0, right.significand };
            return rounded(exact, right.exponent, right.negative, control);
        }
        Ra2LegacyReal zero = { 0, 0, left.negative == right.negative ? left.negative : ((control >> 10) & 3) == 1 };
        return zero;
    }
    int32_t left_top = left.exponent + (int32_t)highest_bit(left.significand);
    int32_t right_top = right.exponent + (int32_t)highest_bit(right.significand);
    int32_t common = (left_top > right_top ? left_top : right_top) - 126;
    WideUnsigned a = aligned(left, common), b = aligned(right, common), exact;
    unsigned negative = left.negative;
    if (left.negative == right.negative)
    {
        exact.low = a.low + b.low;
        exact.high = a.high + b.high + (exact.low < a.low);
    }
    else
    {
        if (a.high < b.high || (a.high == b.high && a.low < b.low))
        {
            WideUnsigned temporary = a;
            a = b;
            b = temporary;
            negative = right.negative;
        }
        exact.low = a.low - b.low;
        exact.high = a.high - b.high - (a.low < b.low);
        if (!exact.high && !exact.low)
        {
            negative = ((control >> 10) & 3) == 1;
        }
    }
    return rounded(exact, common, negative, control);
}

Ra2LegacyReal ra2_real_subtract(Ra2LegacyReal left, Ra2LegacyReal right, uint16_t control)
{
    right.negative ^= 1;
    return ra2_real_add(left, right, control);
}

int32_t ra2_real_truncate_i32(Ra2LegacyReal value)
{
    /* 原版 __ftol 总是向零截断，EAX 取结果低 32 位；单位坐标/进度场景不超过有符号 32 位范围。 */
    uint64_t magnitude = value.exponent >= 0 ? (value.exponent < 64 ? value.significand << value.exponent : 0)
        : (value.exponent > -64 ? value.significand >> -value.exponent : 0);
    uint32_t bits = value.negative ? 0u - (uint32_t)magnitude : (uint32_t)magnitude;
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

int32_t ra2_real_round_i32(Ra2LegacyReal value, uint16_t control)
{
    uint64_t magnitude;
    if (value.exponent >= 0)
        magnitude = value.exponent < 64 ? value.significand << value.exponent : 0;
    else
    {
        WideUnsigned exact = { 0, value.significand };
        int carry;
        magnitude = shift_and_round(exact, (unsigned)-value.exponent, value.negative, control, &carry);
    }
    uint32_t bits = value.negative ? 0u-(uint32_t)magnitude : (uint32_t)magnitude;
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

float ra2_real_store_f32(Ra2LegacyReal value, uint16_t control)
{
    uint32_t bits = value.negative << 31;
    if (value.significand)
    {
        unsigned top = highest_bit(value.significand);
        int32_t exponent = value.exponent + (int32_t)top;
        int carry;
        WideUnsigned exact = { 0, value.significand };
        if (exponent < -126)
        {
            int32_t shift = -149 - value.exponent;
            bits |= shift > 0 ? (uint32_t)shift_and_round(exact, (unsigned)shift, value.negative, control, &carry)
                : (uint32_t)(value.significand << -shift);
        }
        else if (exponent <= 127)
        {
            uint64_t fraction = top > 23 ? shift_and_round(exact, top - 23, value.negative, control, &carry) : value.significand << (23 - top);
            if (fraction >= (UINT64_C(1) << 24))
            {
                fraction >>= 1;
                ++exponent;
            }
            if (exponent <= 127)
            {
                bits |= ((uint32_t)(exponent + 127) << 23) | ((uint32_t)fraction & 0x7FFFFFu);
            }
        }
        if (exponent > 127)
        {
            unsigned rounding = (control >> 10) & 3;
            int infinity = rounding == 0 || (rounding == 1 && value.negative) || (rounding == 2 && !value.negative);
            bits |= infinity ? 0x7F800000u : 0x7F7FFFFFu;
        }
    }
    float result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

double ra2_real_store_f64(Ra2LegacyReal value, uint16_t control)
{
    uint64_t bits = (uint64_t)value.negative << 63;
    if (value.significand)
    {
        unsigned top = highest_bit(value.significand);
        int32_t exponent = value.exponent + (int32_t)top;
        int carry;
        WideUnsigned exact = { 0, value.significand };
        if (exponent < -1022)
        {
            int32_t shift = -1074 - value.exponent;
            bits |= shift > 0 ? shift_and_round(exact, (unsigned)shift, value.negative, control, &carry)
                : value.significand << -shift;
        }
        else if (exponent <= 1023)
        {
            uint64_t fraction = top > 52 ? shift_and_round(exact, top - 52, value.negative, control, &carry)
                : value.significand << (52 - top);
            if (fraction >= (UINT64_C(1) << 53))
            {
                fraction >>= 1;
                ++exponent;
            }
            if (exponent <= 1023)
            {
                bits |= (uint64_t)(exponent + 1023) << 52;
                bits |= fraction & UINT64_C(0xFFFFFFFFFFFFF);
            }
        }
        if (exponent > 1023)
        {
            unsigned rounding = (control >> 10) & 3;
            int infinity = rounding == 0 || (rounding == 1 && value.negative) || (rounding == 2 && !value.negative);
            bits |= infinity ? UINT64_C(0x7FF0000000000000) : UINT64_C(0x7FEFFFFFFFFFFFFF);
        }
    }
    double result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}
