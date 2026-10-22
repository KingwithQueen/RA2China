#pragma once
#include "ground_prepare.h"
#include "ground_collision.h"

typedef struct Ra2ContinuationState
{
    Ra2WorldPoint segment_end, candidate;
    int32_t selector, sample_index;
    unsigned alternate_template, driving, orientation_mismatch;
} Ra2ContinuationState;
typedef struct Ra2ContinuationTemplate
{
    int32_t selector, sample_kind, entry_index;
} Ra2ContinuationTemplate;
typedef enum Ra2ContinuationQuery
{
    RA2_CONTINUATION_TRANSITION_INDEX, RA2_CONTINUATION_TEMPLATE_HEADING,
    RA2_CONTINUATION_OWNER_KIND, RA2_CONTINUATION_TYPE_FLAG_BA4,
    RA2_CONTINUATION_OWNER_ALIVE, RA2_CONTINUATION_OWNER_FLAG_76,
    RA2_CONTINUATION_OWNER_FLAG_7A, RA2_CONTINUATION_CELL_HAS_BRIDGE,
    RA2_CONTINUATION_CELL_LEVEL, RA2_CONTINUATION_HEIGHT_PER_LEVEL
} Ra2ContinuationQuery;
typedef struct Ra2ContinuationServices
{
    void *context;
    int32_t (*query)(void *context, Ra2ContinuationQuery query);
    Ra2ContinuationTemplate (*find_template)(void *context, int32_t selector);
    Ra2WorldPoint (*direction_offset)(void *context, int32_t direction);
    uint64_t (*save_speed)(void *context);
    int32_t (*probe_passage)(void *context, Ra2WorldPoint candidate, int32_t direction);
    void (*classified)(void *context, int32_t passage);
    void (*commit_template)(void *context, Ra2ContinuationTemplate selected);
    void (*refresh_owner)(void *context);
    int (*candidate_accepts_owner)(void *context);
    void (*start_segment)(void *context);
    void (*restore_speed)(void *context, uint64_t speed);
    void (*shift_direction)(void *context);
    void (*reveal_candidate)(void *context);
    void (*request_gate)(void *context);
    Ra2WorldPoint (*raw_position)(void *context);
    void (*notify_segment_cell)(void *context, int bridge_layer);
} Ra2ContinuationServices;

/* 已推进到模板过渡采样时，尝试接上下一转弯模板。返回 0 仅表示
   原版要求立即结束本次 Advance；普通受阻仍允许既有采样继续收尾。 */
int ra2_ground_continue_turn(Ra2ContinuationState *state, Ra2WorldPoint invalid,
    int32_t direction, const Ra2ContinuationServices *services);
