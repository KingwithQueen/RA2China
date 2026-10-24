#include "ground_drive.h"
#include "ground_failure_transition.h"

static int same_position(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return left.x == right.x && left.y == right.y && left.z == right.z;
}

static int32_t query(const Ra2DriveServices *services, Ra2DriveQuery value)
{
    return services->query(services->context, value);
}


/* Prepare/Advance 都可移除单位；每次服务返回后再查存活。
   接续同帧第二段传入1，避免再次累计本帧速度；新段从0开始。 */
static int prepare_and_advance(const Ra2DriveServices *services, int continuing)
{
    if (services->prepare_segment(services->context) || !query(services, RA2_DRIVE_OWNER_ALIVE)) return 0;
    services->advance_segment(services->context, continuing);
    if (!query(services, RA2_DRIVE_OWNER_ALIVE)) return 0;
    return services->finish_frame(services->context);
}

int ra2_ground_drive_process(Ra2GroundDriveState *state, Ra2WorldPoint invalid_position, const Ra2DriveServices *services)
{
    /* 地表属性改变时保留上一属性，并重启原版的三帧过渡计时器。 */
    int32_t surface = query(services, RA2_DRIVE_CELL_SURFACE);
    if (surface != state->surface_current)
    {
        state->surface_previous = state->surface_current;
        state->surface_current = surface;
        services->restart_surface_timer(services->context);
    }

    if (state->path_selector != -1 && state->driving)
    {
        /* 先推进正在执行的路径段；路段可能在回调中耗尽，单位也可能在回调中被移除。 */
        if (services->advance_segment(services->context, 0) || !query(services, RA2_DRIVE_OWNER_ALIVE))
        {
            return 0;
        }
        if (state->path_selector != -1)
        {
            return services->finish_frame(services->context);
        }
        if (!query(services, RA2_DRIVE_IS_MOVING) && query(services, RA2_DRIVE_PATH_HEAD) == -1)
        {
            return services->finish_frame(services->context);
        }
        if (query(services, RA2_DRIVE_OWNER_CATEGORY) == 1 && query(services, RA2_DRIVE_OWNER_FLAG_5B9))
        {
            return services->finish_frame(services->context);
        }
        if (query(services, RA2_DRIVE_OWNER_CATEGORY) == 1 && query(services, RA2_DRIVE_TARGET_CATEGORY) == 15)
        {
            Ra2WorldPoint position;
            services->target_position(services->context, &position);
            if (!same_position(position, state->destination))
            {
                services->set_destination(services->context, position);
            }
        }
        return prepare_and_advance(services, 1);
    }

    /* 没有活动路段：先处理已经到达的格目标，再处理原地转向和等待任务。 */
    if (query(services, RA2_DRIVE_TARGET_CATEGORY) == 11 && query(services, RA2_DRIVE_TARGET_IS_CURRENT_CELL))
    {
        services->stop_navigation(services->context);
        return 0;
    }
    if (query(services, RA2_DRIVE_CURRENT_MISSION) == 5 && !state->driving
        && !same_position(state->destination, invalid_position) && query(services, RA2_DRIVE_POSITION_IS_DESTINATION))
    {
        services->stop_navigation(services->context);
        return 0;
    }

    if (query(services, RA2_DRIVE_IS_TURNING))
    {
        state->turn_update_pending = 1;
        return services->finish_frame(services->context);
    }
    if (state->turn_update_pending)
    {
        /* 转向结束后只刷新一次；保留世界服务在刷新过程中产生的单位失效状态。 */
        state->turn_update_pending = 0;
        services->refresh_owner_after_turn(services->context);
        if (!query(services, RA2_DRIVE_OWNER_USABLE))
        {
            return 0;
        }
    }
    if (query(services, RA2_DRIVE_EFFECTIVE_MISSION) == 5 && !query(services, RA2_DRIVE_IS_MOVING))
    {
        return services->finish_frame(services->context);
    }
    if (query(services, RA2_DRIVE_EFFECTIVE_MISSION) == 16)
    {
        return services->finish_frame(services->context);
    }

    if (!query(services, RA2_DRIVE_IS_MOVING) && query(services, RA2_DRIVE_PATH_HEAD) == -1)
    {
        /* 路径队列为空时只同步目标或停止速度，不能凭空进入新路径段。 */
        if (query(services, RA2_DRIVE_OWNER_FLAG_325))
        {
            ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
            state->desired_speed = 0.0;
            return services->finish_frame(services->context);
        }
        if (query(services, RA2_DRIVE_HAS_TARGET))
        {
            Ra2WorldPoint position;
            services->target_position(services->context, &position);
            services->set_destination(services->context, position);
        }
        return services->finish_frame(services->context);
    }

    /* 某些原版状态要求重新检查目的地；失败时先清路段，再交给任务服务停止导航。 */
    if (query(services, RA2_DRIVE_OWNER_FLAG_32D) && query(services, RA2_DRIVE_EFFECTIVE_MISSION) != 7
        && query(services, RA2_DRIVE_IS_MOVING) && !query(services, RA2_DRIVE_DESTINATION_ACCEPTED))
    {
        ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
        if (services->stop_navigation(services->context))
        {
            return 0;
        }
        return services->finish_frame(services->context);
    }
    return prepare_and_advance(services, 0);
}
