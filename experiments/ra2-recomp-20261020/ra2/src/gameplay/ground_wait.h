#pragma once
#include "ground_prepare.h"
#include "ground_collision.h"

typedef enum Ra2ClearanceQuery
{
    RA2_CLEARANCE_OVERLAY_INDEX,
    RA2_CLEARANCE_OVERLAY_CRUSHABLE,
    RA2_CLEARANCE_CELL_LEVEL,
    RA2_CLEARANCE_CELL_LAND
} Ra2ClearanceQuery;

typedef struct Ra2ClearanceServices
{
    void *context;
    int32_t (*query)(void *context, Ra2ClearanceQuery query);
    void (*request_gate)(void *context);
} Ra2ClearanceServices;

typedef enum Ra2ClearancePhase
{
    RA2_CLEARANCE_TERRAIN_SPEED,
    RA2_CLEARANCE_SPECIAL_OBSTACLE,
    RA2_CLEARANCE_WAIT_FOR_TRAFFIC,
    RA2_CLEARANCE_OTHER_OBSTACLE
} Ra2ClearancePhase;

typedef struct Ra2ClearanceResult
{
    int32_t target_level;
    int32_t land;
    unsigned crush_overlay;
} Ra2ClearanceResult;

/* 0x4A3550..0x4A364F。clear_only 对应共享入口 0x4A35FE。
   通行值 1/6 的特殊处理在后续阶段完成，不能在这里当成普通阻塞。 */
Ra2ClearancePhase ra2_ground_check_clearance(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int32_t passage, int32_t reference_level, int clear_only, Ra2ClearanceResult *result,
    const Ra2ClearanceServices *services);

typedef struct Ra2TrafficWaitState
{
    unsigned waiting;
    Ra2PathRetryTimer retry;
    Ra2PathRetryTimer obstruction;
} Ra2TrafficWaitState;

typedef struct Ra2TrafficWaitServices
{
    void *context;
    int32_t (*current_frame)(void *context);
    int32_t (*wait_duration)(void *context);
    void (*start_wait)(void *context, int32_t frame, int32_t duration);
    int (*rebuild_path)(void *context, int mode);
    int (*owner_exists)(void *context);
    int (*destination_accepted)(void *context);
    void (*write_aborted)(void *context);
    void (*stop_navigation)(void *context);
    int32_t (*retry_delay)(void *context);
    void (*restart_retry)(void *context, int32_t frame, int32_t duration);
} Ra2TrafficWaitServices;

typedef enum Ra2TrafficWaitPhase
{
    RA2_TRAFFIC_RETURN_FALSE,
    RA2_TRAFFIC_RETURN_TRUE,
    RA2_TRAFFIC_REPORT_OBSTACLE
} Ra2TrafficWaitPhase;

/* 0x4A364F..0x4A36ED，0x4A39C8..0x4A3A8E。
   短计时器限制寻路频率；长计时器到期后将原版搜索模式从 1 提升为 2。
   两者都沿用原版有符号回绕计时，不能替换成无符号比较。 */
Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(Ra2TrafficWaitState *state,
    const Ra2TrafficWaitServices *services);
