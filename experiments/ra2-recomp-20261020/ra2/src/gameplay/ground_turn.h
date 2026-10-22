#pragma once
#include "ground_prepare.h"
#include "ground_collision.h"

typedef struct Ra2TurnState
{
    Ra2GroundPrepareState movement;
    Ra2WorldPoint candidate;
    int32_t directions[24];
    int32_t selector;
    unsigned bridge_transition_pending;
} Ra2TurnState;

typedef enum Ra2TurnQuery
{
    RA2_TURN_OWNER_ALIVE,
    RA2_TURN_OWNER_FLAG_76,
    RA2_TURN_IS_TRAIN,
    RA2_TURN_IS_CRUSHER,
    RA2_TURN_CELL_OVERLAY_INDEX,
    RA2_TURN_DISTANCE_TO_DESTINATION,
    RA2_TURN_CLOSE_ENOUGH,
    RA2_TURN_HEIGHT_PER_LEVEL,
    RA2_TURN_CURRENT_LAND,
    RA2_TURN_CELL_HAS_BRIDGE,
    RA2_TURN_CELL_LEVEL,
    RA2_TURN_HAS_TARGET_488
} Ra2TurnQuery;

typedef struct Ra2TurnServices
{
    void *context;
    int32_t (*query)(void *context, Ra2TurnQuery query);
    int (*cell_accepts_owner)(void *context);
    Ra2WorldPoint (*direction_offset)(void *context, int32_t direction);
    int32_t (*probe_passage)(void *context, int32_t direction);
    void (*classified)(void *context, int32_t passage);
    void (*request_gate)(void *context);
    int (*retry)(void *context, unsigned allow_recursive, unsigned prevent_turn, int restart_timer);
    Ra2WorldPoint (*raw_position)(void *context);
    void (*notify_cell)(void *context, int bridge_layer);
    void (*reveal_cell)(void *context);
    void (*cancel_target)(void *context);
    int (*stop_navigation)(void *context, int target_variant);
} Ra2TurnServices;

typedef enum Ra2TurnPhase
{
    RA2_TURN_RETURN_FALSE,
    RA2_TURN_RETURN_TRUE,
    RA2_TURN_COMMIT_WITHOUT_SHIFT
} Ra2TurnPhase;

/* 转弯模板的第二格碰撞及后续状态。成功消耗两个方向；失败按通行原因
   决定开闸、一次重试、揭露或停止，不把通行码简化为 true/false。 */
Ra2TurnPhase ra2_ground_prepare_turn(Ra2TurnState *state, Ra2WorldPoint invalid_position,
    int32_t next_direction, unsigned allow_recursive, const Ra2TurnServices *services);
