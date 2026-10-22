#pragma once
#include "unit_movement.h"

typedef struct Ra2GroundRecoveryState
{
    Ra2WorldPoint segment_end;
    int32_t path_selector;
    int32_t remaining_failures;
    unsigned driving;
    unsigned legacy_flag_61;
    unsigned legacy_flag_578;
    unsigned failure_sound_pending;
} Ra2GroundRecoveryState;

typedef enum Ra2RecoveryQuery
{
    RA2_RECOVERY_HAS_TARGET_488,
    RA2_RECOVERY_OWNER_ALIVE,
    RA2_RECOVERY_IS_MOVING,
    RA2_RECOVERY_HAS_OBJECT_228,
    RA2_RECOVERY_ACCEPTS_OBJECT_228
} Ra2RecoveryQuery;

typedef struct Ra2RecoveryServices
{
    void *context;
    int (*query)(void *context, Ra2RecoveryQuery query);
    int (*stop_navigation)(void *context, int target_variant);
    void (*cancel_target)(void *context);
    void (*play_failure_sound)(void *context);
    void (*notify_linked_objects)(void *context);
} Ra2RecoveryServices;

/* 0x4A2DFD..0x4A2F7A：寻路失败预算、停止任务、一次性提示与路径状态清理。
   finish_only 对应原版 0x4A2EAC 的共享入口，不再扣预算或重复停止。 */
int ra2_ground_recover_path(Ra2GroundRecoveryState *state, Ra2WorldPoint invalid_position,
    int finish_only, const Ra2RecoveryServices *services);
