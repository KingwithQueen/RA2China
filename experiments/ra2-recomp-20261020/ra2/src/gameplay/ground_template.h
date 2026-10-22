#pragma once
#include "ground_prepare.h"

typedef enum Ra2TemplateByte
{
    RA2_TEMPLATE_ENTRY_TAG,
    RA2_TEMPLATE_FLAGS
} Ra2TemplateByte;

typedef struct Ra2TemplateServices
{
    void *context;
    int (*neighbor_overlay_crushable)(void *context, int32_t direction);
    uint8_t (*template_byte)(void *context, int32_t selector, Ra2TemplateByte field);
} Ra2TemplateServices;

typedef struct Ra2TemplateSelection
{
    int32_t next_direction;
    int32_t selector;
    unsigned crushing;
    unsigned flags;
} Ra2TemplateSelection;

/* 4A3F8B..4A4015：第二个方向无效、递归屏蔽转弯或可碾压覆盖物都可能强制直行。
   表项首字节为 0 才回退到 direction*9；不能改成“整个指针为空”。 */
Ra2TemplateSelection ra2_ground_choose_template(int32_t direction, int32_t next_direction,
    int prevent_turn, int crush_current_overlay, int normalize_directions, const Ra2TemplateServices *services);

typedef struct Ra2SegmentCommitState
{
    Ra2GroundPrepareState movement;
    int32_t directions[24];
    int32_t selector;
    int32_t sample_index;
    unsigned sound_pending;
    int16_t target_cell_x;
    int16_t target_cell_y;
} Ra2SegmentCommitState;

typedef struct Ra2SegmentCommitServices
{
    void *context;
    int (*cell_accepts_owner)(void *context, Ra2WorldPoint position);
    int (*owner_flag_76)(void *context);
    int (*owner_alive)(void *context);
    void (*start_segment)(void *context, Ra2WorldPoint position);
    void (*set_speed_zero)(void *context);
} Ra2SegmentCommitServices;

/* 4A45B7..4A4725；skip_shift 对应共享入口 4A45D0，不重复弹出方向队列。 */
void ra2_ground_commit_segment(Ra2SegmentCommitState *state, Ra2WorldPoint invalid_position,
    Ra2WorldPoint candidate, int skip_shift, int32_t terminal_direction, const Ra2SegmentCommitServices *services);
