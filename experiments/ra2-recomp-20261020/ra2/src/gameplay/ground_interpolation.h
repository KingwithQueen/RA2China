#pragma once
#include "unit_movement.h"

typedef struct Ra2InterpolationSurface { int32_t level; unsigned bridge; } Ra2InterpolationSurface;
typedef struct Ra2InterpolationServices
{
    void *context;
    Ra2WorldPoint (*transform)(void *context);
    Ra2WorldPoint (*position)(void *context);
    uintptr_t (*cell_at)(void *context, Ra2WorldPoint position);
    Ra2WorldPoint (*blend_delta)(void *context, Ra2WorldPoint delta);
    void (*leave)(void *context);
    void (*place)(void *context, Ra2WorldPoint position);
    Ra2InterpolationSurface (*surface)(void *context, uintptr_t cell);
    void (*set_bridge)(void *context, unsigned bridge);
    void (*enter)(void *context);
    uint8_t (*placement_flag)(void *context);
    void (*set_placement_flag)(void *context, uint8_t flag);
} Ra2InterpolationServices;

/* Advance 的不足一采样步尾部。start 是本次开始时的快照，old_x/y 是变换前保存值。
 * 找格子会调用世界服务；变换后的终点必须用重新读取的当前位置加差向量构造。 */
void ra2_ground_interpolate_advance(Ra2WorldPoint start, int32_t old_x, int32_t old_y,
    int32_t progress, const Ra2InterpolationServices *services);
