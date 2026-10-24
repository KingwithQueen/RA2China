#pragma once
#include "ground_prepare.h"
#include "ground_path.h"

typedef struct Ra2AdvanceCell { int16_t x, y; } Ra2AdvanceCell;
typedef enum Ra2AdvanceQuery
{
    RA2_ADVANCE_NEEDS_POSITION_MARK, RA2_ADVANCE_SAMPLE_INDEX,
    RA2_ADVANCE_CELL_LEVEL, RA2_ADVANCE_CELL_HAS_BRIDGE,
    RA2_ADVANCE_IS_TRAIN, RA2_ADVANCE_TRAIN_FLAG_5B8,
    RA2_ADVANCE_BRIDGE_LAYER, RA2_ADVANCE_GROUND_HEIGHT,
    RA2_ADVANCE_OBJECT_HEAD_LOWER, RA2_ADVANCE_OBJECT_HEAD_UPPER, RA2_ADVANCE_OBJECT_NEXT,
    RA2_ADVANCE_OBJECT_CRUSHABLE, RA2_ADVANCE_OWNER_ALIVE,
    RA2_ADVANCE_OVERLAY_INDEX, RA2_ADVANCE_CRUSHING_ENABLED,
    RA2_ADVANCE_IS_CRUSHER, RA2_ADVANCE_CRUSHER_ABILITY,
    RA2_ADVANCE_OVERLAY_LAND_TYPE, RA2_ADVANCE_CRUSH_SLOWDOWN,
    RA2_ADVANCE_TRANSITION_SAMPLE
} Ra2AdvanceQuery;
typedef enum Ra2AdvanceAction
{
    RA2_ADVANCE_MARK_POSITION, RA2_ADVANCE_CLEAR_SAMPLE_FLAGS,
    RA2_ADVANCE_LEAVE_CELL, RA2_ADVANCE_SET_BRIDGE_LAYER,
    RA2_ADVANCE_ENTER_CELL, RA2_ADVANCE_TRAIN_DAMAGE,
    RA2_ADVANCE_MARK_CRUSHING, RA2_ADVANCE_APPLY_CRUSH_SLOWDOWN,
    RA2_ADVANCE_REFRESH_PLACEMENT, RA2_ADVANCE_SET_FACING
} Ra2AdvanceAction;

typedef struct Ra2AdvanceServices
{
    void *context;
    int32_t (*query)(void *context, Ra2AdvanceQuery query, uint32_t object);
    void (*act)(void *context, Ra2AdvanceAction action, uint32_t object, int32_t value);
    Ra2WorldPoint (*raw_position)(void *context);
    Ra2AdvanceCell (*current_cell)(void *context);
    Ra2PathSample (*sample)(void *context, int32_t index, int previous);
    Ra2WorldPoint (*transform_sample)(void *context, Ra2PathSample *sample, int previous);
    uint32_t (*find_cell)(void *context, Ra2AdvanceCell cell);
    void (*place)(void *context, Ra2WorldPoint position, int crosses_cell);
} Ra2AdvanceServices;

/* 每个采样先完成坐标变换和放置，再更新桥面、列车碰撞和朝向。
   回调可能伤害/移除单位，所以存活检查与世界查询必须保留原有顺序。 */
int ra2_ground_advance_sample(const Ra2AdvanceServices *services);

/* 可单独修改的跨格业务；列车下一链项在伤害回调前保存，地表碾压在进入后执行。 */
void ra2_ground_advance_train_contact(const Ra2AdvanceServices *services,Ra2AdvanceCell next);
void ra2_ground_advance_overlay_contact(const Ra2AdvanceServices *services,uint32_t next_cell);
int ra2_ground_enter_sample_cell(const Ra2AdvanceServices *services,Ra2AdvanceCell previous,
    Ra2AdvanceCell next,Ra2WorldPoint position);
int ra2_ground_advance_finish_sample(const Ra2AdvanceServices *services,int32_t direction);
