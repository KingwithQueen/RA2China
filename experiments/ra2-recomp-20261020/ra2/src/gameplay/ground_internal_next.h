#pragma once
#include "unit_movement.h"

int ra2_ground_full_sample_exhausted(int32_t index, int32_t x, int32_t y);
typedef struct Ra2PrepareApproachServices {
    void *context;
    void (*reset_budget)(void *context);
    int32_t (*direction)(void *context);
    Ra2WorldPoint (*position)(void *context);
    Ra2WorldPoint (*offset)(void *context);
    void (*construct_target)(void *context, Ra2WorldPoint point);
    void (*store_probe)(void *context, Ra2WorldPoint point);
    uintptr_t (*probe_cell)(void *context);
    int32_t (*cell_level)(void *context, uintptr_t cell);
    unsigned (*upper_layer)(void *context);
    void (*construct_probe)(void *context, Ra2WorldPoint point);
    uint32_t (*cell_flags)(void *context, uintptr_t cell);
    void (*mark_transition)(void *context);
} Ra2PrepareApproachServices;
/* 返回1进入既有连接分支；否则写出当前有效高度层。位置和桥面标志须重新读取。 */
int ra2_ground_prepare_approach(int32_t *level, const Ra2PrepareApproachServices *services);
