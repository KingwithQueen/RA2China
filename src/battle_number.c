#include "battle_number.h"
#include <stdbool.h>
#include <limits.h>

#define SIGN UINT64_C(0x8000000000000000)
#define FRACTION UINT64_C(0x000fffffffffffff)
#define HIDDEN UINT64_C(0x0010000000000000)

static battle_real pack(uint64_t sign, int exponent, uint64_t significand)
{
    if (!significand || exponent < -1022) return 0;
    if (exponent > 1023) return sign | UINT64_C(0x7fefffffffffffff);
    return sign | (uint64_t)(exponent + 1023) << 52 | (significand & FRACTION);
}
static int exponent(battle_real a)
{
    return (int)((a >> 52) & 2047) - 1023;
}
static uint64_t significand(battle_real a)
{
    return (a & FRACTION) | HIDDEN;
}

battle_real battle_real_ratio(uint32_t numerator, uint32_t denominator)
{
    uint64_t n = numerator, d = denominator, value = 1;
    int e = 0;
    if (!n || !d) return 0;
    while (n < d)
    {
        n <<= 1;
        --e;
    }
    while (n >= d * 2)
    {
        d <<= 1;
        ++e;
    }
    uint64_t remainder = n - d;
    for (unsigned i = 0; i < 52; ++i)
    {
        remainder <<= 1;
        value <<= 1;
        if (remainder >= d)
        {
            remainder -= d;
            value |= 1;
        }
    }
    /* 规则十进制输入按最近偶数编码；之后的原版计算才使用向零截断。 */
    if (remainder * 2 > d || (remainder * 2 == d && (value & 1)))
    {
        if (++value == (HIDDEN << 1))
        {
            value >>= 1;
            ++e;
        }
    }
    return pack(0, e, value);
}
battle_real battle_real_int(int32_t value)
{
    uint32_t magnitude = (uint32_t)(value < 0 ? -(int64_t)value : value);
    return battle_real_ratio(magnitude, 1) | (value < 0 ? SIGN : 0);
}
battle_real battle_real_float(uint32_t value)
{
    if (!(value & 0x7fffffffu)) return 0;
    /* 游戏数值域只产生正规单精度数，不接受 NaN、无穷或非正规输入。 */
    int e = (int)((value >> 23) & 255) - 127;
    return pack((uint64_t)(value & 0x80000000u) << 32, e, ((uint64_t)(value & 0x7fffffu) | 0x800000u) << 29);
}
uint32_t battle_real_float_bits(battle_real value)
{
    int e = exponent(value);
    if (!value || e < -126) return 0;
    if (e > 127) return (uint32_t)(value >> 32) & 0x80000000u;
    return ((uint32_t)(value >> 32) & 0x80000000u) | (uint32_t)(e + 127) << 23 | (uint32_t)((value & FRACTION) >> 29);
}
static void multiply(uint64_t a, uint64_t b, uint64_t *high, uint64_t *low)
{
    uint64_t p0 = (uint64_t)(uint32_t)a * (uint32_t)b, p1 = (a >> 32) * (uint32_t)b;
    uint64_t p2 = (uint64_t)(uint32_t)a * (b >> 32), p3 = (a >> 32) * (b >> 32);
    uint64_t middle = (p0 >> 32) + (uint32_t)p1 + (uint32_t)p2;
    *low = (middle << 32) | (uint32_t)p0;
    *high = p3 + (p1 >> 32) + (p2 >> 32) + (middle >> 32);
}
battle_real battle_real_mul(battle_real a, battle_real b)
{
    uint64_t high, low;
    unsigned shift;
    if (!(a & ~SIGN) || !(b & ~SIGN)) return 0;
    multiply(significand(a), significand(b), &high, &low);
    shift = high >= (UINT64_C(1) << 41) ? 53 : 52;
    return pack((a ^ b) & SIGN, exponent(a) + exponent(b) + (int)shift - 52, (high << (64 - shift)) | (low >> shift));
}
battle_real battle_real_add(battle_real a, battle_real b)
{
    uint64_t av, bv, result, sign;
    unsigned distance, top = 0;
    bool lost;
    if (!(a & ~SIGN)) return b;
    if (!(b & ~SIGN)) return a;
    if ((a & ~SIGN) < (b & ~SIGN))
    {
        battle_real swap = a;
        a = b;
        b = swap;
    }
    distance = (unsigned)(exponent(a) - exponent(b));
    av = significand(a) << 10;
    bv = significand(b) << 10;
    lost = distance >= 64 ? bv != 0 : distance && (bv & ((UINT64_C(1) << distance) - 1)) != 0;
    bv = distance >= 64 ? 0 : bv >> distance;
    sign = a & SIGN;
    /* 异号减法必须传播被丢弃尾数的借位，否则 1 - 连续减速量会错误跨过整数边界。 */
    result = ((a ^ b) & SIGN) ? av - bv - (lost ? 1 : 0) : av + bv;
    if (!result) return 0;
    for (uint64_t bits = result; bits >>= 1;) ++top;
    return pack(sign, exponent(a) + (int)top - 62, top > 52 ? result >> (top - 52) : result << (52 - top));
}
battle_real battle_real_sub(battle_real a, battle_real b)
{
    return battle_real_add(a, b ^ ((b & ~SIGN) ? SIGN : 0));
}
battle_real battle_real_div(battle_real a, battle_real b)
{
    uint64_t n, d, value = 1;
    int e;
    if (!(a & ~SIGN) || !(b & ~SIGN)) return 0;
    n = significand(a);
    d = significand(b);
    e = exponent(a) - exponent(b);
    if (n < d)
    {
        n <<= 1;
        --e;
    }
    uint64_t remainder = n - d;
    for (unsigned i = 0; i < 52; ++i)
    {
        value <<= 1;
        remainder <<= 1;
        if (remainder >= d)
        {
            remainder -= d;
            value |= 1;
        }
    }
    return pack((a ^ b) & SIGN, e, value);
}
battle_real battle_real_sqrt(battle_real a)
{
    uint64_t high, low, root = 0, remainder = 0;
    int e;
    if (!a || (a & SIGN)) return 0;
    e = exponent(a);
    uint64_t value = significand(a) << (e & 1);
    multiply(value, HIDDEN, &high, &low);
    for (int pair = 52; pair >= 0; --pair)
    {
        unsigned shift = (unsigned)pair * 2;
        uint64_t bits = shift >= 64 ? high >> (shift - 64) : low >> shift;
        remainder = (remainder << 2) | (bits & 3);
        uint64_t trial = (root << 2) | 1;
        root <<= 1;
        if (remainder >= trial)
        {
            remainder -= trial;
            root |= 1;
        }
    }
    return pack(0, e < 0 ? (e - (e & 1)) / 2 : e / 2, root);
}
int32_t battle_real_integer(battle_real a)
{
    int e = exponent(a);
    uint64_t value;
    if (!a || e < 0) return 0;
    if (e > 30) return a & SIGN ? INT32_MIN : INT32_MAX;
    value = significand(a) >> (52 - e);
    return a & SIGN ? -(int32_t)value : (int32_t)value;
}
int battle_real_compare(battle_real a, battle_real b)
{
    if (!(a & ~SIGN)) a = 0;
    if (!(b & ~SIGN)) b = 0;
    if (a == b) return 0;
    if ((a ^ b) & SIGN) return a & SIGN ? -1 : 1;
    return a & SIGN ? (a < b ? 1 : -1) : (a < b ? -1 : 1);
}
