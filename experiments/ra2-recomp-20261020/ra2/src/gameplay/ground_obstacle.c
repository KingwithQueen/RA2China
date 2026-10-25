#include <stdint.h>
#include "ground_obstacle.h"
#include "ground_failure_transition.h"

static int32_t wrapped_absolute_difference(int32_t left, int32_t right)
{
    uint32_t difference = (uint32_t)left - (uint32_t)right;
    return (int32_t)((int32_t)difference < 0 ? 0u - difference : difference);
}


static int close_to_allied_blocker(Ra2GroundPrepareState *state,
    const Ra2ObstacleServices *services, void *context)
{
    Ra2WorldPoint position;
    int32_t distance = services->query(context, RA2_OBSTACLE_DISTANCE_TO_DESTINATION);
    int32_t close_enough = services->query(context, RA2_OBSTACLE_CLOSE_ENOUGH_DISTANCE);
    int close_to_destination = distance < close_enough;
    if (close_to_destination && !services->query(context, RA2_OBSTACLE_PREDICATE_636F10))
    {
        position = services->position(context, 0);
        int32_t height = services->query(context, RA2_OBSTACLE_HEIGHT_PER_LEVEL);
        int32_t two_levels = (int32_t)((uint32_t)height * 2u);
        close_to_destination = wrapped_absolute_difference(state->destination.z, position.z) < two_levels;
        if (close_to_destination)
        {
            close_to_destination = services->query(context, RA2_OBSTACLE_CURRENT_LAND) != 10;
        }
    }
    else
    {
        close_to_destination = 0;
    }
    return close_to_destination;
}

static void notify_allied_blocker(const Ra2ObstacleServices *services, void *context)
{
    Ra2WorldPoint position;
    int bridge_layer = 0;
    if (services->query(context, RA2_OBSTACLE_CELL_HAS_BRIDGE))
    {
        position = services->position(context, 0);
        int32_t height = services->query(context, RA2_OBSTACLE_HEIGHT_PER_LEVEL);
        int32_t level = services->query(context, RA2_OBSTACLE_CELL_LEVEL);
        bridge_layer = wrapped_absolute_difference(position.z / height, level) > 2;
    }
    services->notify_blocker(context, bridge_layer);
}

/* 越界检查之后重读朝向/队首，保留首次捕获的障碍服务context。 */
static int observe_neighbor_passage(Ra2GroundCell cell,int rebuilt,
    const Ra2ObstacleServices *services,void *context)
{
    int32_t direction=services->query(context,rebuilt ? RA2_OBSTACLE_PATH_HEAD:RA2_OBSTACLE_FACING_DIRECTION);
    return services->can_enter(context,cell,direction);
}

static Ra2PreparePhase finish_near_allied_blocker(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,const Ra2ObstacleServices *services,void *context)
{
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    int target_variant = services->query(context, RA2_OBSTACLE_HAS_TARGET_488);
    int stopped = ra2_ground_stop_target(target_variant, context,
        services->cancel_target, services->stop_navigation);
    return target_variant && stopped ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE;
}

/* 障碍复核完成才重置失败预算，再读取可能由回调改写的实时队首。 */
static Ra2PreparePhase publish_recovered_queue(int32_t *path_head,
    const Ra2ObstacleServices *services,void *context)
{
    services->reset_failure_budget(context, 10);
    *path_head = services->query(context, RA2_OBSTACLE_PATH_HEAD);
    return RA2_PREPARE_USE_QUEUED_PATH;
}

Ra2PreparePhase ra2_ground_observe_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int rebuilt, int32_t *path_head, const Ra2ObstacleServices *services)
{
    void *context = services->context;
    int32_t direction = services->query(context, rebuilt ? RA2_OBSTACLE_PATH_HEAD : RA2_OBSTACLE_FACING_DIRECTION);
    if (rebuilt && direction == 8)
    {
        return RA2_PREPARE_RETURN_FALSE;
    }
    Ra2WorldPoint position = services->position(context, 1);
    Ra2GroundCell cell = { (int16_t)(position.x / 256), (int16_t)(position.y / 256) };
    cell = services->neighbor(context, cell, (uint32_t)direction & 7u);
    if (services->inside_map(context, cell))
    {
        /* 失败路径会再次取实时朝向，重建成功路径则再次读队列头；不能复用上次查询值。 */
        int passage=observe_neighbor_passage(cell,rebuilt,services,context);
        if (passage == 3)
        {
            services->request_gate(context, cell);
        }
        else if (passage == 6 && services->find_allied_blocker(context, cell)
            && !services->query(context, RA2_OBSTACLE_TRAIN))
        {
            /* 友军查询和列车过滤之后才判断距离；桥层查询只在不结束目标时执行。 */
            if (close_to_allied_blocker(state, services, context))
            {
                return finish_near_allied_blocker(state,invalid_position,services,context);
            }
            notify_allied_blocker(services, context);
        }
    }
    if (rebuilt)
    {
        return publish_recovered_queue(path_head,services,context);
    }
    return RA2_PREPARE_FINISH_FAILED_ATTEMPT;
}
