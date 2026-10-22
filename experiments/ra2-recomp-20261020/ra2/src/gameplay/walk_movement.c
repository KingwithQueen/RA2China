#include "walk_movement.h"
#include "x87_arithmetic.h"

int32_t ra2_walk_advance_axis(int32_t origin,double direction_component,double speed,
    unsigned subtract_step,uint16_t arithmetic_control,uint16_t conversion_control)
{
    Ra2LegacyReal step=ra2_real_multiply(ra2_real_from_f64(direction_component),
        ra2_real_from_f64(speed),arithmetic_control);
    Ra2LegacyReal coordinate=ra2_real_from_i32(origin);
    coordinate=subtract_step?ra2_real_subtract(coordinate,step,arithmetic_control)
        :ra2_real_add(coordinate,step,arithmetic_control);
    /* 极小负位移也须先按原版舍入相加，不能提前由宿主 double 舍回整数起点。 */
    return ra2_real_round_i32(coordinate,conversion_control);
}
