#include <stdlib.h>
#include "ground_tube_progress.h"
#include "x87_arithmetic.h"

static int32_t add(int32_t a, int32_t b)
{ return (int32_t)((uint32_t)a + (uint32_t)b); }

uint32_t ra2_ground_tube_construct_approach(Ra2WorldPoint offset, int32_t rise,
    const Ra2TubeApproachServices *services)
{
    void *context = services->context;
    Ra2WorldPoint point = services->approach(context);
    point.x = add(point.x, offset.x);
    point.y = add(point.y, offset.y);
    services->construct_probe(context, point);

    uintptr_t from_handle = services->approach_center(context);
    uintptr_t to_handle = services->probe_center(context);
    Ra2WorldPoint to = services->read_center(context, to_handle);
    Ra2WorldPoint from = services->read_center(context, from_handle);
    point = services->approach(context);
    point.x = add(point.x, (int32_t)((uint32_t)to.x - (uint32_t)from.x));
    point.y = add(point.y, (int32_t)((uint32_t)to.y - (uint32_t)from.y));
    services->store_approach(context, point);
    services->increase_height(context, rise);
    return services->refresh_heading(context);
}

static unsigned top_bit(uint64_t value)
{
    unsigned top = 0;
    while (value >>= 1) ++top;
    return top;
}

/* 64位整数长除法保留余数，避免宿主double先舍入后再补偿。
   仅用于有限距离及非零步长；保持原24/53/64位精度和四种舍入模式。 */
static Ra2LegacyReal divide_distance(Ra2LegacyReal left, Ra2LegacyReal right,
    uint16_t control)
{
    unsigned precision;
    switch ((control >> 8) & 3) {
        case 0: precision = 24; break;
        case 2: precision = 53; break;
        case 3: precision = 64; break;
        default: abort();
    }
    if (!right.significand) abort();
    Ra2LegacyReal result = {0, 0, left.negative ^ right.negative};
    if (!left.significand) return result;

    unsigned left_shift = 63 - top_bit(left.significand);
    unsigned right_shift = 63 - top_bit(right.significand);
    uint64_t numerator = left.significand << left_shift;
    uint64_t denominator = right.significand << right_shift;
    int below_one = numerator < denominator;
    uint64_t remainder = below_one ? numerator - (denominator - numerator)
                                  : numerator - denominator;
    uint64_t quotient = 1;
    for (unsigned bit = 1; bit < precision; ++bit) {
        unsigned carry = (unsigned)(remainder >> 63);
        remainder <<= 1;
        quotient <<= 1;
        if (carry || remainder >= denominator) {
            remainder -= denominator;
            quotient |= 1;
        }
    }

    int increment = 0;
    if (remainder) {
        switch ((control >> 10) & 3) {
            case 0:
                increment = remainder > denominator - remainder ||
                    (remainder == denominator - remainder && (quotient & 1));
                break;
            case 1: increment = result.negative != 0; break;
            case 2: increment = result.negative == 0; break;
            default: break;
        }
    }
    result.exponent = left.exponent - (int32_t)left_shift - right.exponent +
        (int32_t)right_shift - below_one - (int32_t)(precision - 1);
    if (increment && ++quotient == 0) {
        quotient = UINT64_C(1) << 63;
        ++result.exponent;
    }
    result.significand = quotient;
    return result;
}

int32_t ra2_ground_tube_progress_height(double distance, double step_length,
    int32_t rise, int32_t base, uint16_t control, uint16_t conversion_control)
{
    Ra2LegacyReal progress = divide_distance(ra2_real_from_f64(distance),
        ra2_real_from_f64(step_length), control);
    Ra2LegacyReal change = ra2_real_multiply(progress, ra2_real_from_i32(rise), control);
    return ra2_real_round_i32(ra2_real_add(change, ra2_real_from_i32(base), control), conversion_control);
}
