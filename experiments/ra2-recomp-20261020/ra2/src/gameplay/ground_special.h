#pragma once
#include "ground_prepare.h"
#include "ground_collision.h"

typedef enum Ra2SpecialQuery
{
    RA2_SPECIAL_IS_TRAIN,
    RA2_SPECIAL_DISTANCE_TO_TARGET,
    RA2_SPECIAL_CLOSE_ENOUGH,
    RA2_SPECIAL_HEIGHT_PER_LEVEL,
    RA2_SPECIAL_CURRENT_LAND,
    RA2_SPECIAL_CELL_HAS_BRIDGE,
    RA2_SPECIAL_CELL_LEVEL,
    RA2_SPECIAL_HAS_TARGET_488
} Ra2SpecialQuery;

typedef struct Ra2SpecialServices
{
    void *context;
    int32_t (*query)(void *context, Ra2SpecialQuery query);
    Ra2WorldPoint (*raw_position)(void *context);
    int (*retry)(void *context, int32_t path_head, int restart_timer);
    void (*reveal_cell)(void *context);
    void (*notify_cell)(void *context, int bridge_layer);
    void (*cancel_target)(void *context);
    int (*stop_navigation)(void *context, int target_variant);
} Ra2SpecialServices;

typedef enum Ra2SpecialPhase
{
    RA2_SPECIAL_RETURN_FALSE,
    RA2_SPECIAL_RETURN_TRUE,
    RA2_SPECIAL_CLEAR_SEGMENT
} Ra2SpecialPhase;

/* 4A36ED..4A39C8。临时障碍允许一次带计时器重置的递归；隐形障碍先揭露对象，
   再递归且不重置计时器。不能把这两个相似分支合并成同一重试动作。 */
Ra2SpecialPhase ra2_ground_handle_special_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int32_t passage, int allow_recursive, int32_t path_head, const Ra2SpecialServices *services);
