#include "ground_tube_state.h"

static void snapshot_exit_chain(const Ra2TubeExitServices *services, void *context, uintptr_t object)
{
    services->begin_snapshot(context);
    do {
        services->append_snapshot(context, object);
        object = services->next_occupant(context, object);
    } while (object);
}

static void request_snapshot_clearance(const Ra2TubeExitServices *services, void *context)
{
    /* 数量可随让路回调改变；非类别1仍要再次查类别，不能预读或缓存。 */
    for (int32_t index = 0; index < services->snapshot_count(context); ++index) {
        uintptr_t object = services->snapshot_object(context, index);
        if (services->object_kind(context, object) == 1 ||
            services->object_kind(context, object) == 15) {
            if (!services->object_moving(context, object))
                services->request_object_clearance(context, object);
        }
    }
}

/* 落位和入格完成后才查目标；恢复任务、速度和后继连接保持实时顺序。 */
static uint32_t restore_exit_navigation(const Ra2TubeExitServices *services,void *context)
{
    if(services->goal_is_exit_cell(context))
        services->request_self_clearance(context);
    services->restore_mission(context);
    services->set_speed(context,0);
    return services->face_next_connection(context);
}

static uint32_t place_at_free_exit(const Ra2TubeExitServices *services,void *context)
{
    services->place_at_exit(context);
    services->enter_cell(context);
    return restore_exit_navigation(services,context);
}

static uint32_t wait_for_occupied_exit(const Ra2TubeExitServices *services,
    void *context,uintptr_t object)
{
    /* 先完成原链快照，再让路；速度回调结束后才释放快照并传回结果。 */
    snapshot_exit_chain(services,context,object);
    request_snapshot_clearance(services,context);
    services->set_speed(context,1);
    return services->end_snapshot(context);
}

uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services)
{
    void *context=services->context;
    uintptr_t object=services->exit_occupants(context);
    if(object)return wait_for_occupied_exit(services,context,object);
    return place_at_free_exit(services,context);
}

Ra2TubeWaypointResult ra2_ground_tube_waypoint(int32_t distance, int32_t speed,
    const Ra2TubeWaypointServices *services)
{
    if (distance > speed)
        return RA2_TUBE_KEEP_STEP;

    /* 对齐到路点的回调可能改变结束标志，必须在回调后读取。 */
    services->advance_and_snap(services->context);
    return services->finished_after_snap(services->context)
        ? RA2_TUBE_EXIT : RA2_TUBE_NEXT_STEP;
}
