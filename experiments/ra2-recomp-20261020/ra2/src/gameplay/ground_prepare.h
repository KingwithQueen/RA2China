#pragma once
#include <stdint.h>
#include "unit_movement.h"

typedef struct Ra2GroundPrepareState
{
    Ra2WorldPoint destination;
    Ra2WorldPoint segment_end;
    unsigned driving;
    unsigned legacy_flag_61;
} Ra2GroundPrepareState;

typedef struct Ra2PathRetryTimer
{
    int32_t start_frame;
    int32_t remaining_frames;
} Ra2PathRetryTimer;

/* 未确认名称的原版谓词保留偏移/地址，避免把推测当作 MOD 规则。 */
typedef enum Ra2PrepareQuery
{
    RA2_PREPARE_EFFECTIVE_MISSION,
    RA2_PREPARE_OWNER_VIRTUAL_1BC,
    RA2_PREPARE_OWNER_VIRTUAL_1C0,
    RA2_PREPARE_TEAM_BUSY,
    RA2_PREPARE_OWNER_VIRTUAL_324,
    RA2_PREPARE_OWNER_VIRTUAL_328,
    RA2_PREPARE_TARGET_CATEGORY,
    RA2_PREPARE_DISTANCE_TO_DESTINATION,
    RA2_PREPARE_PATH_HEAD,
    RA2_PREPARE_RETRY_DELAY_FRAMES,
    RA2_PREPARE_OWNER_EXISTS,
    RA2_PREPARE_DESTINATION_ACCEPTED,
    RA2_PREPARE_OWNER_PREDICATE_4C8D60,
    RA2_PREPARE_CLOSE_ENOUGH_DISTANCE,
    RA2_PREPARE_HAS_TARGET_488,
    RA2_PREPARE_OWNER_ALIVE
} Ra2PrepareQuery;

typedef struct Ra2PrepareServices
{
    void *context;
    int32_t (*query)(void *context, Ra2PrepareQuery query);
    void (*trim_path)(void *context, int32_t end_index);
    int (*stop_navigation)(void *context, int target_variant);
    void (*write_aborted)(void *context, unsigned aborted);
    void (*restart_retry_timer)(void *context, int32_t frame, int32_t duration);
    int (*rebuild_path)(void *context);
    void (*cancel_target)(void *context);
} Ra2PrepareServices;

typedef enum Ra2PreparePhase
{
    RA2_PREPARE_RETURN_FALSE,
    RA2_PREPARE_RETURN_TRUE,
    RA2_PREPARE_RETRY_PATH,
    RA2_PREPARE_USE_QUEUED_PATH,
    RA2_PREPARE_PATH_REBUILT,
    RA2_PREPARE_INSPECT_OBSTACLE,
    RA2_PREPARE_FINISH_FAILED_ATTEMPT
} Ra2PreparePhase;

/* 准备入口：无路径/无目标、等待状态、目标距离裁剪和已有方向队列的分流。 */
Ra2PreparePhase ra2_ground_prepare_entry(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int is_moving, int32_t *cached_path_head, const Ra2PrepareServices *services);
int ra2_ground_retry_timer_ready(Ra2PathRetryTimer timer, int32_t current_frame);
/* 路径队列为空时：节流、重建、目的地复核，以及接近目标后的停止判定。 */
Ra2PreparePhase ra2_ground_retry_path(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    Ra2PathRetryTimer timer, int32_t frame, const Ra2PrepareServices *services);
