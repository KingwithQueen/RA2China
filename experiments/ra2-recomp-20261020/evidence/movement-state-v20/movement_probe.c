#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include "unit_movement.h"
#include "x87_arithmetic.h"

/* 这些汇编仅用于对照本机 x86 CPU，生产移动模块及兼容运算全部使用 C17。 */
static int32_t reference_scale(int32_t speed, double factor, uint16_t control)
{
    uint16_t saved, chop = control | 0x0C00;
    int64_t result;
    __asm
    {
        fnstcw saved
        fldcw control
        fild speed
        fmul factor
        fldcw chop
        fistp qword ptr result
        fldcw saved
    }
    return (int32_t)result;
}

static int32_t reference_arrival(int32_t distance, uint16_t control)
{
    double reciprocal = 0.09090909090909091, one = 1.0, steps = 7.0;
    uint16_t saved, chop = control | 0x0C00;
    int64_t result;
    __asm
    {
        fnstcw saved
        fldcw control
        fild distance
        fmul reciprocal
        fsubr one
        fmul steps
        fldcw chop
        fistp qword ptr result
        fldcw saved
    }
    return (int32_t)result;
}

static float reference_fraction(int32_t progress, uint16_t control)
{
    double reciprocal = 0.14285714285714285;
    uint16_t saved;
    float result;
    __asm
    {
        fnstcw saved
        fldcw control
        fild progress
        fmul reciprocal
        fstp result
        fldcw saved
    }
    return result;
}

static int32_t reference_axis(int32_t start, int32_t finish, float fraction, uint16_t control)
{
    double one = 1.0;
    uint16_t saved, chop = control | 0x0C00;
    int64_t result;
    __asm
    {
        fnstcw saved
        fldcw control
        fld fraction
        fsubr one
        fild finish
        fmul fraction
        fild start
        fmul st(0), st(2)
        faddp st(1), st(0)
        fldcw chop
        fistp qword ptr result
        fstp st(0)
        fldcw saved
    }
    return (int32_t)result;
}

static float reference_operation(double left, double right, unsigned operation, uint16_t control)
{
    uint16_t saved;
    float result;
    __asm
    {
        fnstcw saved
        fldcw control
        fld left
    }
    if (operation == 0) { __asm fadd right }
    else if (operation == 1) { __asm fsub right }
    else { __asm fmul right }
    __asm
    {
        fstp result
        fldcw saved
    }
    return result;
}

static uint32_t bits(float value)
{
    uint32_t result;
    memcpy(&result, &value, 4);
    return result;
}

static uint32_t seed = 0x61247;
static uint32_t random_word(void)
{
    seed = seed * 1664525u + 1013904223u;
    return seed;
}

static double random_finite(void)
{
    uint64_t raw = ((uint64_t)random_word() << 32) | random_word();
    raw = (raw & UINT64_C(0x800FFFFFFFFFFFFF)) | ((uint64_t)(random_word() % 2047) << 52);
    double result;
    memcpy(&result, &raw, 8);
    return result;
}

int main(void)
{
    const unsigned precisions[] = { 0, 2, 3 };
    const double factors[] = { 0, 1, -1, 0.1, 0.2, 0.5, 0.9, 0.8999999999999999, 0.92, 0.9199999999999999,
        0.99, 1.01, 1.5, 2.0, 0.14285714285714285 };
    const int32_t progress_values[] = { INT32_MIN, -100001, -21, -7, -1, 0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 100001, INT32_MAX };
    unsigned scale_count = 0, arrival_count = 0, fraction_count = 0, interpolation_count = 0, arithmetic_count = 0;
    if (reference_scale(10, 0.8999999999999999, 0x0E7F) != 8
        || ra2_ground_scale_speed(10, 0.8999999999999999, 0x0E7F) != 8)
    {
        puts("frame 2247 captured operands regression failed");
        return 1;
    }
    for (unsigned p = 0; p < 3; ++p)
    {
        for (unsigned rounding = 0; rounding < 4; ++rounding)
        {
            uint16_t control = (uint16_t)(0x007F | (precisions[p] << 8) | (rounding << 10));
            for (int32_t speed = -128; speed <= 512; ++speed)
            {
                for (unsigned f = 0; f < sizeof(factors) / sizeof(*factors); ++f)
                {
                    int32_t want = reference_scale(speed, factors[f], control);
                    int32_t got = ra2_ground_scale_speed(speed, factors[f], control);
                    if (want != got) { printf("scale failure cw=%x speed=%d factor=%.17g want=%d got=%d\n", control, speed, factors[f], want, got); return 1; }
                    ++scale_count;
                }
            }
            for (int32_t distance = -64; distance <= 4096; ++distance)
            {
                int32_t want = reference_arrival(distance, control);
                int32_t got = ra2_ground_arrival_progress_adjustment(distance, &ra2_original_ground_path_sampling, control);
                if (want != got) { printf("arrival failure cw=%x distance=%d want=%d got=%d\n", control, distance, want, got); return 1; }
                ++arrival_count;
            }
            for (unsigned i = 0; i < sizeof(progress_values) / sizeof(*progress_values); ++i)
            {
                uint32_t want = bits(reference_fraction(progress_values[i], control));
                uint32_t got = bits(ra2_ground_progress_fraction(progress_values[i], &ra2_original_ground_path_sampling, control));
                if (want != got) { printf("fraction failure cw=%x progress=%d want=%08x got=%08x\n", control, progress_values[i], want, got); return 1; }
                ++fraction_count;
            }
            for (unsigned i = 0; i < 10000; ++i)
            {
                Ra2WorldPoint start, finish;
                start.x = (int32_t)(random_word() % 131073) - 65536;
                start.y = (int32_t)(random_word() % 131073) - 65536;
                start.z = (int32_t)(random_word() % 4097) - 2048;
                finish.x = (int32_t)(random_word() % 131073) - 65536;
                finish.y = (int32_t)(random_word() % 131073) - 65536;
                finish.z = (int32_t)(random_word() % 4097) - 2048;
                float fraction = reference_fraction((int32_t)(i % 8), control);
                Ra2WorldPoint got = ra2_ground_interpolate_position(start, finish, fraction, control, control);
                if (got.x != reference_axis(start.x, finish.x, fraction, control)
                    || got.y != reference_axis(start.y, finish.y, fraction, control)
                    || got.z != reference_axis(start.z, finish.z, fraction, control))
                {
                    printf("interpolation failure cw=%x case=%u\n", control, i);
                    return 1;
                }
                interpolation_count += 3;
                double left = random_finite(), right = i % 10 == 0 ? 0.0 : random_finite();
                for (unsigned operation = 0; operation < 3; ++operation)
                {
                    Ra2LegacyReal a = ra2_real_from_f64(left), b = ra2_real_from_f64(right), result;
                    if (operation == 0) result = ra2_real_add(a, b, control);
                    else if (operation == 1) result = ra2_real_subtract(a, b, control);
                    else result = ra2_real_multiply(a, b, control);
                    uint32_t want = bits(reference_operation(left, right, operation, control));
                    uint32_t actual = bits(ra2_real_store_f32(result, control));
                    if (want != actual)
                    {
                        printf("arithmetic failure cw=%x op=%u left=%.17g right=%.17g want=%08x got=%08x\n", control, operation, left, right, want, actual);
                        return 1;
                    }
                    ++arithmetic_count;
                }
            }
        }
    }
    printf("{\"passed\":true,\"scale\":%u,\"arrival\":%u,\"fraction\":%u,\"interpolated_axes\":%u,\"arithmetic\":%u,\"precision_modes\":3,\"rounding_modes\":4}\n",
        scale_count, arrival_count, fraction_count, interpolation_count, arithmetic_count);
    return 0;
}
