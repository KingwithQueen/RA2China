#pragma once
#include "unit_movement.h"
typedef struct Ra2TubeExitServices
{
    void *context;
    uintptr_t (*exit_occupants)(void *context);
    void (*begin_snapshot)(void *context);
    void (*append_snapshot)(void *context, uintptr_t object);
    uintptr_t (*next_occupant)(void *context, uintptr_t object);
    int32_t (*snapshot_count)(void *context);
    uintptr_t (*snapshot_object)(void *context, int32_t index);
    int32_t (*object_kind)(void *context, uintptr_t object);
    int (*object_moving)(void *context, uintptr_t object);
    void (*request_object_clearance)(void *context, uintptr_t object);
    void (*set_speed)(void *context, int blocked);
    uint32_t (*end_snapshot)(void *context);
    void (*place_at_exit)(void *context);
    void (*enter_cell)(void *context);
    int (*goal_is_exit_cell)(void *context);
    void (*request_self_clearance)(void *context);
    void (*restore_mission)(void *context);
    uint32_t (*face_next_connection)(void *context);
} Ra2TubeExitServices;
/* 出口有人时先保存对象快照，再按原顺序处理，避免让路回调改变链表。 */
uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services);
typedef struct Ra2TubeWaypointServices
{
    void *context;
    void (*advance_and_snap)(void *context);
    int (*finished_after_snap)(void *context);
} Ra2TubeWaypointServices;
typedef enum Ra2TubeWaypointResult {RA2_TUBE_KEEP_STEP,RA2_TUBE_NEXT_STEP,RA2_TUBE_EXIT} Ra2TubeWaypointResult;
Ra2TubeWaypointResult ra2_ground_tube_waypoint(int32_t distance, int32_t speed,
    const Ra2TubeWaypointServices *services);
