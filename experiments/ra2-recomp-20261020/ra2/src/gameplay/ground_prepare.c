#include <stdint.h>
#include <string.h>
#include "ground_prepare.h"
#include "ground_failure_transition.h"

static int same_position(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return left.x == right.x && left.y == right.y && left.z == right.z;
}

static int32_t signed_bits(uint32_t bits)
{
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}


static int32_t query(const Ra2PrepareServices *services, Ra2PrepareQuery value)
{
    return services->query(services->context, value);
}

Ra2PreparePhase ra2_ground_prepare_entry(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int is_moving, int32_t *cached_path_head, const Ra2PrepareServices *services)
{
    if (!is_moving && *cached_path_head == -1)
    {
        state->legacy_flag_61 = 0;
        ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
        if (query(services, RA2_PREPARE_EFFECTIVE_MISSION) == 2)
        {
            unsigned aborted = (unsigned)services->stop_navigation(services->context, 1);
            services->write_aborted(services->context, aborted);
        }
        return RA2_PREPARE_RETURN_FALSE;
    }
    if (same_position(state->destination, invalid_position))
    {
        return RA2_PREPARE_RETURN_FALSE;
    }
    if (query(services, RA2_PREPARE_OWNER_VIRTUAL_1BC) || query(services, RA2_PREPARE_OWNER_VIRTUAL_1C0))
    {
        return RA2_PREPARE_RETURN_FALSE;
    }
    if (query(services, RA2_PREPARE_TEAM_BUSY))
    {
        return RA2_PREPARE_RETURN_TRUE;
    }
    if (query(services, RA2_PREPARE_OWNER_VIRTUAL_324) || query(services, RA2_PREPARE_OWNER_VIRTUAL_328))
    {
        return RA2_PREPARE_RETURN_TRUE;
    }

    if (*cached_path_head != -1)
    {
        /* 原版只对这两类目标按距离裁剪；两个类别查询的短路顺序也保留。 */
        if (query(services, RA2_PREPARE_TARGET_CATEGORY) == 1 || query(services, RA2_PREPARE_TARGET_CATEGORY) == 15)
        {
            int32_t distance_in_cells = query(services, RA2_PREPARE_DISTANCE_TO_DESTINATION) / 256;
            if (distance_in_cells < 24)
            {
                services->trim_path(services->context, distance_in_cells);
                *cached_path_head = query(services, RA2_PREPARE_PATH_HEAD);
            }
        }
        if (*cached_path_head != -1)
        {
            return RA2_PREPARE_USE_QUEUED_PATH;
        }
    }
    return RA2_PREPARE_RETRY_PATH;
}

int ra2_ground_retry_timer_ready(Ra2PathRetryTimer timer, int32_t current_frame)
{
    int32_t remaining = timer.remaining_frames;
    if (timer.start_frame != -1)
    {
        int32_t elapsed = signed_bits((uint32_t)current_frame - (uint32_t)timer.start_frame);
        if (elapsed >= remaining)
        {
            return 1;
        }
        remaining = signed_bits((uint32_t)remaining - (uint32_t)elapsed);
    }
    return remaining == 0;
}

Ra2PreparePhase ra2_ground_retry_path(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    Ra2PathRetryTimer timer, int32_t frame, const Ra2PrepareServices *services)
{
    if (!ra2_ground_retry_timer_ready(timer, frame))
    {
        return RA2_PREPARE_RETURN_FALSE;
    }
    int32_t delay = query(services, RA2_PREPARE_RETRY_DELAY_FRAMES);
    services->restart_retry_timer(services->context, frame, delay);
    if (services->rebuild_path(services->context))
    {
        return RA2_PREPARE_PATH_REBUILT;
    }
    if (!query(services, RA2_PREPARE_OWNER_EXISTS))
    {
        services->write_aborted(services->context, 1);
        return RA2_PREPARE_RETURN_FALSE;
    }
    if (!query(services, RA2_PREPARE_DESTINATION_ACCEPTED))
    {
        services->stop_navigation(services->context, 0);
        return RA2_PREPARE_RETURN_FALSE;
    }
    if (same_position(state->destination, invalid_position))
    {
        return RA2_PREPARE_RETURN_FALSE;
    }

    if (!query(services, RA2_PREPARE_OWNER_PREDICATE_4C8D60))
    {
        int32_t distance = query(services, RA2_PREPARE_DISTANCE_TO_DESTINATION);
        int32_t threshold = query(services, RA2_PREPARE_CLOSE_ENOUGH_DISTANCE);
        if (distance >= threshold)
        {
            return RA2_PREPARE_INSPECT_OBSTACLE;
        }
        /* 两次任务查询照原版执行；服务可能带有可观察副作用，不能合并成一次。 */
        if (query(services, RA2_PREPARE_EFFECTIVE_MISSION) == 2 || query(services, RA2_PREPARE_EFFECTIVE_MISSION) == 11)
        {
            ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
            int target = !!query(services, RA2_PREPARE_HAS_TARGET_488);
            if (ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation))
            {
                return RA2_PREPARE_RETURN_TRUE;
            }
            return query(services, RA2_PREPARE_OWNER_ALIVE)
                ? RA2_PREPARE_FINISH_FAILED_ATTEMPT : RA2_PREPARE_RETURN_FALSE;
        }
    }
    return RA2_PREPARE_INSPECT_OBSTACLE;
}
