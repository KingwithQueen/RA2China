#include "combat_warhead_values.h"
#include "x87_arithmetic.h"

double ra2_combat_warhead_percent(int32_t percent,double percent_unit,uint16_t control)
{
    Ra2LegacyReal value=ra2_real_multiply(ra2_real_from_i32(percent),
        ra2_real_from_f64(percent_unit),control);
    return ra2_real_store_f64(value,control);
}
