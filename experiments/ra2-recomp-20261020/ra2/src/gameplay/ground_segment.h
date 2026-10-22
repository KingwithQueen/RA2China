#pragma once
#include "ground_obstacle.h"

typedef struct Ra2CellSurface
{
    int32_t level;
    unsigned has_bridge;
} Ra2CellSurface;

typedef enum Ra2SegmentQuery
{
    RA2_SEGMENT_OWNER_BRIDGE_FLAG,
    RA2_SEGMENT_OWNER_PREDICATE_27C,
    RA2_SEGMENT_FACING_RAW,
    RA2_SEGMENT_ACTOR_IS_TRAIN,
    RA2_SEGMENT_ACTOR_IS_CRUSHER,
    RA2_SEGMENT_CELL_OVERLAY_INDEX
} Ra2SegmentQuery;

typedef struct Ra2SegmentServices
{
    void *context;
    int32_t (*query)(void *context, Ra2SegmentQuery query);
    Ra2WorldPoint (*candidate_point)(void *context, unsigned direction);
    Ra2CellSurface (*current_surface)(void *context);
    Ra2CellSurface (*surface_at)(void *context, Ra2WorldPoint position);
    void (*mark_bridge_transition)(void *context);
    int (*request_gate)(void *context, Ra2GroundCell cell);
    void (*turn_toward)(void *context, uint16_t direction);
    int32_t (*classify_cell)(void *context, Ra2GroundCell cell, int32_t direction, int32_t reference_level);
} Ra2SegmentServices;

typedef struct Ra2SegmentPreparation
{
    Ra2WorldPoint candidate;
    Ra2GroundCell cell;
    int32_t reference_level;
    int32_t passage;
} Ra2SegmentPreparation;

typedef enum Ra2SegmentPhase
{
    RA2_SEGMENT_EMPTY,
    RA2_SEGMENT_WAIT,
    RA2_SEGMENT_CLASSIFIED
} Ra2SegmentPhase;

/* 4A32CA..4A3550：新路段坐标、高度层、桥面切换、闸门许可和转向等待。
 * 查询当前格和下一格后再决定是否推进；待转向或待开闸时保持原版 true 返回值。 */
Ra2SegmentPhase ra2_ground_prepare_segment(int32_t path_head, Ra2SegmentPreparation *output, const Ra2SegmentServices *services);
