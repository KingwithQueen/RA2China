#pragma once
#include "ground_prepare.h"

typedef struct Ra2GroundCell
{
    int16_t x;
    int16_t y;
} Ra2GroundCell;

typedef enum Ra2ObstacleQuery
{
    RA2_OBSTACLE_PATH_HEAD,
    RA2_OBSTACLE_FACING_DIRECTION,
    RA2_OBSTACLE_TRAIN,
    RA2_OBSTACLE_DISTANCE_TO_DESTINATION,
    RA2_OBSTACLE_CLOSE_ENOUGH_DISTANCE,
    RA2_OBSTACLE_PREDICATE_636F10,
    RA2_OBSTACLE_HEIGHT_PER_LEVEL,
    RA2_OBSTACLE_CURRENT_LAND,
    RA2_OBSTACLE_CELL_HAS_BRIDGE,
    RA2_OBSTACLE_CELL_LEVEL,
    RA2_OBSTACLE_HAS_TARGET_488
} Ra2ObstacleQuery;

typedef struct Ra2ObstacleServices
{
    void *context;
    int32_t (*query)(void *context, Ra2ObstacleQuery query);
    Ra2WorldPoint (*position)(void *context, int virtual_position);
    Ra2GroundCell (*neighbor)(void *context, Ra2GroundCell cell, unsigned direction);
    int (*inside_map)(void *context, Ra2GroundCell cell);
    int (*can_enter)(void *context, Ra2GroundCell cell, int32_t direction);
    void (*request_gate)(void *context, Ra2GroundCell cell);
    int (*find_allied_blocker)(void *context, Ra2GroundCell cell);
    void (*notify_blocker)(void *context, int bridge_layer);
    void (*cancel_target)(void *context);
    int (*stop_navigation)(void *context, int target_variant);
    void (*reset_failure_budget)(void *context, int32_t remaining);
} Ra2ObstacleServices;

/* 4A2A83..4A2DFD 与 4A2F7A..4A32CA：观察相邻格并处理闸门和友军阻挡。
 * rebuilt 区分路径重建后的复核与重建失败后的观察；后者随后扣除失败预算。
 * 世界查询仍由原版提供，地图、寻路器与对象占用不在此处模拟。 */
Ra2PreparePhase ra2_ground_observe_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int rebuilt, int32_t *path_head, const Ra2ObstacleServices *services);
