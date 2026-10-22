#include <stdint.h>
#include <string.h>
#include "unit_movement.h"
#include "x87_arithmetic.h"

/* 数值分别来自本机 1.006 的 0x7A05C8、0x7A05C0、0x7A05D0，保留原版常量的精确二进制值。 */
const Ra2GroundPathSampling ra2_original_ground_path_sampling = { 7, 0.14285714285714285, 0.09090909090909091 };

double ra2_ground_add_acceleration(double current_speed, double acceleration, uint16_t control)
{
    Ra2LegacyReal sum = ra2_real_add(ra2_real_from_f64(acceleration), ra2_real_from_f64(current_speed), control);
    return ra2_real_store_f64(sum, control);
}

double ra2_ground_apply_deceleration(double current_speed, int32_t elapsed, double deceleration, uint16_t control)
{
    Ra2LegacyReal step = ra2_real_multiply(ra2_real_from_i32(elapsed), ra2_real_from_f64(deceleration), control);
    Ra2LegacyReal difference = ra2_real_subtract(ra2_real_from_f64(current_speed), step, control);
    return ra2_real_store_f64(difference, control);
}

int32_t ra2_ground_scale_speed(int32_t base_speed, double speed_factor, uint16_t precision)
{
    /* 原版先按当前 x87 精度/舍入方式计算乘积，再用 __ftol 向零截断；合并成宿主 double 会改变整数边界。 */
    Ra2LegacyReal scaled = ra2_real_multiply(ra2_real_from_i32(base_speed), ra2_real_from_f64(speed_factor), precision);
    return ra2_real_truncate_i32(scaled);
}

int32_t ra2_ground_arrival_progress_adjustment(int32_t remaining_distance, const Ra2GroundPathSampling *sampling, uint16_t precision)
{
    /* 原版公式：(1 - 剩余曼哈顿距离 / 11) * 7，最后向零截断；每一步都保留原版舍入语义。 */
    Ra2LegacyReal distance = ra2_real_from_i32(remaining_distance);
    Ra2LegacyReal distance_in_samples = ra2_real_multiply(distance, ra2_real_from_f64(sampling->reciprocal_arrival_distance), precision);
    Ra2LegacyReal remaining_fraction = ra2_real_subtract(ra2_real_from_i32(1), distance_in_samples, precision);
    Ra2LegacyReal adjustment = ra2_real_multiply(remaining_fraction, ra2_real_from_i32(sampling->progress_steps_per_sample), precision);
    return ra2_real_truncate_i32(adjustment);
}

float ra2_ground_progress_fraction(int32_t progress, const Ra2GroundPathSampling *sampling, uint16_t precision)
{
    Ra2LegacyReal fraction = ra2_real_multiply(ra2_real_from_i32(progress), ra2_real_from_f64(sampling->reciprocal_progress_steps), precision);
    return ra2_real_store_f32(fraction, precision);
}

static int32_t interpolate_axis(int32_t start, int32_t finish, Ra2LegacyReal fraction, Ra2LegacyReal inverse_fraction, uint16_t precision)
{
    /* 位置 = 起点 * (1 - 比例) + 终点 * 比例；运算顺序与原版向量插值保持一致。 */
    Ra2LegacyReal finish_component = ra2_real_multiply(ra2_real_from_i32(finish), fraction, precision);
    Ra2LegacyReal start_component = ra2_real_multiply(ra2_real_from_i32(start), inverse_fraction, precision);
    return ra2_real_truncate_i32(ra2_real_add(finish_component, start_component, precision));
}

Ra2WorldPoint ra2_ground_interpolate_position(Ra2WorldPoint start, Ra2WorldPoint finish, float fraction,
    uint16_t initial_control, uint16_t conversion_control)
{
    Ra2LegacyReal blend = ra2_real_from_f32(fraction);
    Ra2LegacyReal inverse = ra2_real_subtract(ra2_real_from_i32(1), blend, initial_control);
    Ra2WorldPoint result;
    result.x = interpolate_axis(start.x, finish.x, blend, inverse, initial_control);
    result.y = interpolate_axis(start.y, finish.y, blend, inverse, conversion_control);
    result.z = interpolate_axis(start.z, finish.z, blend, inverse, conversion_control);
    return result;
}

static int32_t signed_bits(uint32_t bits)
{
    int32_t value;
    memcpy(&value, &bits, sizeof(value));
    return value;
}

Ra2WorldPoint ra2_ground_transform_path_sample(Ra2WorldPoint local_sample, Ra2WorldPoint origin, uint32_t transform_flags, uint32_t *direction)
{
    uint32_t facing = *direction;
    uint32_t x = (uint32_t)local_sample.x, y = (uint32_t)local_sample.y;
    if (transform_flags & RA2_PATH_SWAP_XY)
    {
        uint32_t temporary = x;
        x = y;
        y = temporary;
        facing = (0u - 64u - facing) & 255u;
    }
    if (transform_flags & RA2_PATH_FLIP_X)
    {
        x = 0u - x;
        facing = (0u - facing) & 255u;
    }
    if (transform_flags & RA2_PATH_FLIP_Y)
    {
        y = 0u - y;
        facing = (0u - 128u - facing) & 255u;
    }
    *direction = facing;
    Ra2WorldPoint result = { signed_bits((uint32_t)origin.x + x), signed_bits((uint32_t)origin.y + y), local_sample.z };
    return result;
}
