#pragma once
#include <stdint.h>

typedef struct Ra2CellPlacementServices
{
    void *context;
    void (*leave)(void *context);
    void (*place)(void *context);
    void (*update_layer)(void *context);
    /* 列车碰撞等处理可能移除移动单位；返回0时不再执行占格。可为空。 */
    int (*before_enter)(void *context);
    uint32_t (*enter)(void *context);
} Ra2CellPlacementServices;

typedef struct Ra2CellPlacementResult
{
    unsigned entered;
    uint32_t value;
} Ra2CellPlacementResult;

/* 离格是否已经完成由调用方说明。各阶段依次执行，不缓存回调中的对象/世界状态。 */
Ra2CellPlacementResult ra2_ground_place_cell(const Ra2CellPlacementServices *services,
    unsigned needs_leave);
