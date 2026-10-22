#pragma once
#include "unit_movement.h"

/* 以32位回绕求曼哈顿余量，再保持原x87的运算次序。 */
int32_t ra2_ground_arrival_adjustment(Ra2WorldPoint position, Ra2WorldPoint end, uint16_t control);

typedef struct Ra2PrepareFinishServices
{
    void *context;
    void (*clear_segment)(void *context);
    void (*clear_driving)(void *context);
    int (*has_target)(void *context);
    void (*cancel_target)(void *context);
    uint32_t (*stop)(void *context, int target_cancelled);
    void (*clear_path)(void *context);
    void (*start_immediate_retry)(void *context);
    void (*finish_retry_timer)(void *context);
    uint32_t (*prepare_again)(void *context);
} Ra2PrepareFinishServices;

typedef enum Ra2PrepareFinishEntry
{
    RA2_PREPARE_STOP_EMPTY,
    RA2_PREPARE_CANCEL_TARGET,
    RA2_PREPARE_CLEAR_SEGMENT,
    RA2_PREPARE_CLEAR_SEGMENT_SAVED_OWNER,
    RA2_PREPARE_RECURSE_TIMER_TAIL,
    RA2_PREPARE_RECURSE_CLEAR_PATH,
    RA2_PREPARE_RETRY_OR_CLEAR,
    RA2_PREPARE_CLEAR_DRIVING
} Ra2PrepareFinishEntry;
/* 返回值保留目标停止/递归调用的完整32位结果；普通停止只清除低字节。 */
uint32_t ra2_ground_prepare_finish(Ra2PrepareFinishEntry entry, int may_retry,
    const Ra2PrepareFinishServices *services);
