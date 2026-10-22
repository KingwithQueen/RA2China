#include "ground_path_cache.h"
#include "x87_arithmetic.h"
int ra2_ground_path_cache_is_current(uint32_t entry_generation,uint32_t search_generation)
{return entry_generation==search_generation;}

int ra2_ground_path_cache_compare(float cached_cost,float parent_cost,double epsilon,uint16_t control)
{
    Ra2LegacyReal threshold=ra2_real_add(ra2_real_from_f32(parent_cost),ra2_real_from_f64(epsilon),control);
    Ra2LegacyReal difference=ra2_real_subtract(ra2_real_from_f32(cached_cost),threshold,control);
    if(!difference.significand)return 0;
    return difference.negative?-1:1;
}
