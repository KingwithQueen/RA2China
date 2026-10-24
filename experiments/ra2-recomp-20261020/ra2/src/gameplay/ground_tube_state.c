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

static uint32_t place_at_free_exit(const Ra2TubeExitServices *services, void *context)
{
    services->place_at_exit(context);
    services->enter_cell(context);
    /* 入格服务后再判断目标，不能把格指针查询挪到落位前。 */
    if (services->goal_is_exit_cell(context))
        services->request_self_clearance(context);
    services->restore_mission(context);
    services->set_speed(context, 0);
    return services->face_next_connection(context);
}

uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services)
{
    void *context = services->context;
    uintptr_t object = services->exit_occupants(context);
    if (!object) return place_at_free_exit(services, context);
    /* 完成原链快照后才发让路请求；速度服务之后统一释放快照。 */
    snapshot_exit_chain(services, context, object);
    request_snapshot_clearance(services, context);
    services->set_speed(context, 1);
    return services->end_snapshot(context);
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
