#include "ground_connection_numeric.h"
#include "ground_connection_trig.h"
#include "x87_arithmetic.h"

double ra2_ground_connection_angle(int32_t direction, double radians_per_turn, uint16_t control)
{
    return ra2_real_store_f64(ra2_real_multiply(ra2_real_from_i32(direction),
        ra2_real_from_f64(radians_per_turn), control), control);
}
float ra2_ground_connection_component(double angle, float index_scale, const float *table,
    int cosine, uint16_t control)
{
    int32_t quantized = ra2_real_truncate_i32(ra2_real_multiply(ra2_real_from_f64(angle),
        ra2_real_from_f32(index_scale), control));
    /* 原表先按符号向零除二，再把负余数修正到一周；奇数向下一项取样。 */
    int32_t index = quantized / 2 % 8192;
    if (index < 0) index += 8192;
    if (cosine) index += 2048;
    if (((uint32_t)quantized & 1u) && index < (cosine ? 10239 : 8191)) ++index;
    return table[index];
}

int32_t ra2_ground_connection_axis(double origin, double distance, double component,
    int subtract, uint16_t control)
{
    Ra2LegacyReal product = ra2_real_multiply(ra2_real_from_f64(component), ra2_real_from_f64(distance), control);
    Ra2LegacyReal position = ra2_real_from_f64(origin);
    Ra2LegacyReal result = subtract ? ra2_real_subtract(position, product, control)
        : ra2_real_add(product, position, control);
    return ra2_real_truncate_i32(result);
}
