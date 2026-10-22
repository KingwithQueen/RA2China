#pragma once
#include "unit_movement.h"

typedef struct Ra2SlopePlane
{
    double x_gradient, y_gradient, offset, ceiling, extra_height;
} Ra2SlopePlane;
typedef struct Ra2SlopeCache
{
    uint8_t initialized;
    double level_height, world_scale;
    Ra2SlopePlane planes[20];
} Ra2SlopeCache;
/* 三个初始化位分别保护高度、每世界单位比例和20种坡面参数。 */
void ra2_ground_initialize_slopes(Ra2SlopeCache *cache, int32_t level_height, uint16_t control);
/* 返回后x87转换控制字沿用原版；坡型0是平地，1..20对应坡面表。 */
int32_t ra2_ground_slope_height(const Ra2SlopeCache *cache, int32_t level_height,
    int8_t level, uint8_t slope, Ra2WorldPoint position, uint16_t initial_control, uint16_t conversion_control);
