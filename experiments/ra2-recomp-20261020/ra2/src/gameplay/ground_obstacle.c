#include <stdint.h>
#include "ground_obstacle.h"
#include "ground_failure_transition.h"

static int32_t wrapped_absolute_difference(int32_t left, int32_t right)
{
    uint32_t difference = (uint32_t)left - (uint32_t)right;
    return (int32_t)((int32_t)difference < 0 ? 0u - difference : difference);
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
        direction = services->query(context, rebuilt ? RA2_OBSTACLE_PATH_HEAD : RA2_OBSTACLE_FACING_DIRECTION);
        int passage = services->can_enter(context, cell, direction);
        if (passage == 3)
        {
            services->request_gate(context, cell);
        }
        else if (passage == 6 && services->find_allied_blocker(context, cell)
            && !services->query(context, RA2_OBSTACLE_TRAIN))
        {
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
            if (close_to_destination)
            {
                ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
                int target_variant = services->query(context, RA2_OBSTACLE_HAS_TARGET_488);
                int stopped = ra2_ground_stop_target(target_variant, context,
                    services->cancel_target, services->stop_navigation);
                return target_variant && stopped ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE;
            }
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
    }
    if (rebuilt)
    {
        services->reset_failure_budget(context, 10);
        *path_head = services->query(context, RA2_OBSTACLE_PATH_HEAD);
        return RA2_PREPARE_USE_QUEUED_PATH;
    }
    return RA2_PREPARE_FINISH_FAILED_ATTEMPT;
}
