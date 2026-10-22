#pragma once
#include "unit_movement.h"

typedef struct Ra2GroundArrivalState
{
    Ra2WorldPoint destination;
    Ra2WorldPoint segment_end;
    int32_t path_selector;
    int32_t sample_index;
    unsigned driving;
} Ra2GroundArrivalState;

typedef enum Ra2ArrivalQuery
{
    RA2_ARRIVAL_TARGET_IS_CURRENT_CELL,
    RA2_ARRIVAL_OWNER_REFERENCE_Z,
    RA2_ARRIVAL_OWNER_USABLE,
    RA2_ARRIVAL_EFFECTIVE_MISSION,
    RA2_ARRIVAL_OWNER_UPDATE,
    RA2_ARRIVAL_OWNER_ALIVE
} Ra2ArrivalQuery;

typedef struct Ra2ArrivalServices
{
    void *context;
    int32_t (*query)(void *context, Ra2ArrivalQuery query);
    void (*relocate)(void *context, int crosses_cell);
    void (*refresh_owner)(void *context);
    void (*cancel_target_and_path)(void *context);
    int (*stop_move_mission)(void *context);
} Ra2ArrivalServices;

typedef enum Ra2ArrivalOutcome
{
    RA2_ARRIVAL_CONTINUE,
    RA2_ARRIVAL_RETURN_FALSE,
    RA2_ARRIVAL_RETURN_TRUE
} Ra2ArrivalOutcome;

/* 对应原版一段路径耗尽后的完整落位与任务收尾，0x4A2034..0x4A22F9。
   进度余量的 x87 算术在 unit_movement.c 中；调用本函数前已按原顺序结算。 */
Ra2ArrivalOutcome ra2_ground_finish_segment(Ra2GroundArrivalState *state, Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position, int32_t level_height, const Ra2ArrivalServices *services);
