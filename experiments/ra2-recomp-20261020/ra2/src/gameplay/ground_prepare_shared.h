#pragma once
#include <stdint.h>
typedef struct Ra2PrepareSharedServices
{
    void *context;
    void (*reset_failure_budget)(void *context, int32_t budget);
    int32_t (*read_path_head)(void *context);
    uint32_t (*prepare_segment)(void *context, int32_t head);
} Ra2PrepareSharedServices;
/* 重建成功入口会恢复十次失败预算并重新取队首；已有队列入口使用传入的缓存值。 */
uint32_t ra2_ground_prepare_shared(int rebuilt, int32_t cached_head, const Ra2PrepareSharedServices *services);
