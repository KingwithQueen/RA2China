#include "ground_tube_state.h"

uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services)
{
    void *context = services->context;
    uintptr_t object = services->exit_occupants(context);

    if (object) {
        /* 先复制出口对象链。让路请求可能修改原链表，不能边遍历边请求。 */
        services->begin_snapshot(context);
        do {
            services->append_snapshot(context, object);
            object = services->next_occupant(context, object);
        } while (object);

        /* 每次重读快照数量；类别不为1时必须再查一次，保留回调副作用。 */
        for (int32_t index = 0; index < services->snapshot_count(context); ++index) {
            object = services->snapshot_object(context, index);
            if (services->object_kind(context, object) == 1 ||
                services->object_kind(context, object) == 15) {
                if (!services->object_moving(context, object))
                    services->request_object_clearance(context, object);
            }
        }
        services->set_speed(context, 1);
        return services->end_snapshot(context);
    }

    /* 出口已空：落位、登记入格，再恢复任务与速度。目标判断是格指针相等。 */
    services->place_at_exit(context);
    services->enter_cell(context);
    if (services->goal_is_exit_cell(context))
        services->request_self_clearance(context);
    services->restore_mission(context);
    services->set_speed(context, 0);
    return services->face_next_connection(context);
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
