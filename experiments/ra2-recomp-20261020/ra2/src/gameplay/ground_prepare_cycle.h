#pragma once
#include "ground_prepare.h"

typedef struct Ra2PrepareCycleServices
{
    const Ra2PrepareServices *prepare;
    void *context;
    Ra2PathRetryTimer (*retry_timer)(void *context);
    int32_t (*current_frame)(void *context);
} Ra2PrepareCycleServices;

/* 入口先处理已有路径和服务状态；确需重寻路时才读取当前owner的计时器和帧。 */
Ra2PreparePhase ra2_ground_prepare_cycle(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,int is_moving,int32_t *cached_path_head,
    const Ra2PrepareCycleServices *services);
