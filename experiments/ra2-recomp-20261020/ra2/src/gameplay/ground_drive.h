#pragma once
#include <stdint.h>
#include "unit_movement.h"

typedef struct Ra2GroundDriveState
{
    int32_t surface_current;
    int32_t surface_previous;
    Ra2WorldPoint destination;
    Ra2WorldPoint segment_end;
    int32_t path_selector;
    int32_t sample_index;
    int32_t sample_progress;
    double desired_speed;
    unsigned driving;
    unsigned turn_update_pending;
} Ra2GroundDriveState;

/* 暂未核实含义的原版字节保留偏移名，不把推测写成玩法定义。 */
typedef enum Ra2DriveQuery
{
    RA2_DRIVE_CELL_SURFACE,
    RA2_DRIVE_OWNER_ALIVE,
    RA2_DRIVE_OWNER_USABLE,
    RA2_DRIVE_OWNER_CATEGORY,
    RA2_DRIVE_OWNER_FLAG_5B9,
    RA2_DRIVE_OWNER_FLAG_325,
    RA2_DRIVE_OWNER_FLAG_32D,
    RA2_DRIVE_PATH_HEAD,
    RA2_DRIVE_CURRENT_MISSION,
    RA2_DRIVE_EFFECTIVE_MISSION,
    RA2_DRIVE_IS_MOVING,
    RA2_DRIVE_IS_TURNING,
    RA2_DRIVE_TARGET_CATEGORY,
    RA2_DRIVE_HAS_TARGET,
    RA2_DRIVE_TARGET_IS_CURRENT_CELL,
    RA2_DRIVE_DESTINATION_ACCEPTED,
    RA2_DRIVE_POSITION_IS_DESTINATION
} Ra2DriveQuery;

/* 回调负责世界查询、占格更新和旧引擎服务；回调返回前同步 state，允许服务改变路径或任务。 */
typedef struct Ra2DriveServices
{
    void *context;
    int32_t (*query)(void *context, Ra2DriveQuery query);
    void (*restart_surface_timer)(void *context);
    int (*advance_segment)(void *context, int skip_speed_increment);
    int (*prepare_segment)(void *context);
    void (*target_position)(void *context, Ra2WorldPoint *position);
    void (*set_destination)(void *context, Ra2WorldPoint position);
    void (*refresh_owner_after_turn)(void *context);
    int (*stop_navigation)(void *context);
    int (*finish_frame)(void *context);
} Ra2DriveServices;

/* 对应原版 DriveLocomotion::Process 的完整逐帧调度；路径搜索和单段内部碰撞由显式服务调用。 */
int ra2_ground_drive_process(Ra2GroundDriveState *state, Ra2WorldPoint invalid_position, const Ra2DriveServices *services);
