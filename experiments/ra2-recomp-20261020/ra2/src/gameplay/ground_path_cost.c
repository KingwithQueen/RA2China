#include "ground_path_cost.h"
#include "x87_arithmetic.h"

float ra2_ground_accumulate_path_cost(float previous_cost, float step_cost, uint16_t control)
{
    /* 原版 1.006：先按当前 x87 精度相加，再按当前舍入方式写回 float。
     * 默认的就近舍入会把缓存代价抬高一位，改变重寻路的内部查询次数。 */
    Ra2LegacyReal accumulated = ra2_real_add(ra2_real_from_f32(step_cost),
        ra2_real_from_f32(previous_cost), control);
    return ra2_real_store_f32(accumulated, control);
}

float ra2_ground_score_path_step(double traversal_cost,float search_weight,float direction_bias,uint16_t control)
{
    Ra2LegacyReal weighted=ra2_real_multiply(ra2_real_from_f64(traversal_cost),ra2_real_from_f32(search_weight),control);
    return ra2_real_store_f32(ra2_real_add(weighted,ra2_real_from_f32(direction_bias),control),control);
}

float ra2_ground_path_priority(double approximate_distance,float accumulated_cost,uint16_t control)
{
    Ra2LegacyReal priority=ra2_real_add(ra2_real_from_f64(approximate_distance),ra2_real_from_f32(accumulated_cost),control);
    return ra2_real_store_f32(priority,control);
}
