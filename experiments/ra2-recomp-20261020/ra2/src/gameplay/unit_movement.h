#pragma once
#include <stdint.h>

typedef struct Ra2WorldPoint
{
    /* 原版整数世界坐标，一格为 256 个单位；Z 是独立高度。 */
    int32_t x;
    int32_t y;
    int32_t z;
} Ra2WorldPoint;

/* 当前恢复的是原版地面行走的路径采样参数；修改时必须同步检查路径采样表与原版对照。 */
typedef struct Ra2GroundPathSampling
{
    /* 一段路径采样的进度单位数；不是一格所需的模拟帧数。 */
    int32_t progress_steps_per_sample;
    double reciprocal_progress_steps;
    double reciprocal_arrival_distance;
} Ra2GroundPathSampling;

typedef enum Ra2PathTransform
{
    RA2_PATH_SWAP_XY = 1,
    RA2_PATH_FLIP_X = 2,
    RA2_PATH_FLIP_Y = 4
} Ra2PathTransform;

extern const Ra2GroundPathSampling ra2_original_ground_path_sampling;

/* 路段内部的速度爬升/回落；乘法、加减和落盘均遵守原版控制字。 */
double ra2_ground_add_acceleration(double current_speed, double acceleration, uint16_t control);
double ra2_ground_apply_deceleration(double current_speed, int32_t elapsed, double deceleration, uint16_t control);

/* control 参数是原版的数值兼容设置，制作规则 MOD 时应保留；正常输入为有限系数和原版坐标/进度范围。 */
int32_t ra2_ground_scale_speed(int32_t base_speed, double speed_factor, uint16_t precision);
int32_t ra2_ground_arrival_progress_adjustment(int32_t remaining_distance, const Ra2GroundPathSampling *sampling, uint16_t precision);
float ra2_ground_progress_fraction(int32_t progress, const Ra2GroundPathSampling *sampling, uint16_t precision);
/* 原版第一次整数转换后会切换控制字；第二、三轴沿用切换后的状态，反比例保留第一次计算结果。 */
Ra2WorldPoint ra2_ground_interpolate_position(Ra2WorldPoint start, Ra2WorldPoint finish, float fraction,
    uint16_t initial_control, uint16_t conversion_control);
Ra2WorldPoint ra2_ground_transform_path_sample(Ra2WorldPoint local_sample, Ra2WorldPoint origin, uint32_t transform_flags, uint32_t *direction);
