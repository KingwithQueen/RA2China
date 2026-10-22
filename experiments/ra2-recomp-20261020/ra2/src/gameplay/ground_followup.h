#pragma once
#include <stdint.h>
#include "unit_movement.h"
#include "x87_arithmetic.h"

typedef enum Ra2SpeedQuery
{
    RA2_SPEED_TARGET_SURFACE,
    RA2_SPEED_CURRENT_SURFACE,
    RA2_SPEED_OWNER_KIND,
    RA2_SPEED_CLASS,
    RA2_SPEED_TEMPLATE_SELECTOR
} Ra2SpeedQuery;

typedef enum Ra2SpeedValue
{
    RA2_SPEED_TERRAIN_FACTOR,
    RA2_SPEED_UPHILL_CLASS_1,
    RA2_SPEED_DOWNHILL_CLASS_1,
    RA2_SPEED_UPHILL_OTHER,
    RA2_SPEED_DOWNHILL_OTHER,
    RA2_SPEED_OWNER_RATIO,
    RA2_SPEED_SLOW_RATIO_LIMIT,
    RA2_SPEED_CURRENT_UNIT_SPEED
} Ra2SpeedValue;

typedef struct Ra2GroundSpeedServices
{
    void *context;
    int32_t (*query)(void *context, Ra2SpeedQuery query);
    double (*value)(void *context, Ra2SpeedValue value);
    uint16_t (*control_word)(void *context);
    void (*store_factor)(void *context, double factor);
    void (*apply_speed)(void *context, double factor, int to_drive);
} Ra2GroundSpeedServices;

/* 地形限速、上下坡修正、零系数回退及低比例减速。
   中间写回 double 后重新装载；最后一次减速仍在原版精度下比较。
   不可把全部计算合并成一个宿主 double 表达式。 */
void ra2_ground_prepare_speed(const Ra2GroundSpeedServices *services);

typedef struct Ra2FollowupServices
{
    void *context;
    void (*prepare_candidate)(void *context);
    int32_t (*next_direction)(void *context);
    int32_t (*distance_to_destination)(void *context);
    int (*is_train)(void *context);
    int (*rebuild_path)(void *context, int train_mode);
    int (*owner_exists)(void *context);
    void (*write_aborted)(void *context);
    int (*destination_accepted)(void *context);
    void (*stop_navigation)(void *context);
} Ra2FollowupServices;

typedef struct Ra2FollowupResult
{
    int32_t next_direction;
    int force_straight;
    int aborted;
} Ra2FollowupResult;

/* 路段候选准备后，第二方向为空才按 512 距离阈值决定补建路径。
   补建失败不直接进入预算：复核/停止之后重新读取第二方向。 */
Ra2FollowupResult ra2_ground_prepare_followup(const Ra2FollowupServices *services);
