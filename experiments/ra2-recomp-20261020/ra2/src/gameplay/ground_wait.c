#include <stdint.h>
#include <string.h>
#include "ground_wait.h"

static void clear_segment(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position)
{
    if (state->segment_end.x != invalid_position.x || state->segment_end.y != invalid_position.y
        || state->segment_end.z != invalid_position.z)
    {
        state->segment_end = invalid_position;
        state->driving = 0;
    }
}

static int32_t level_difference(int32_t left, int32_t right)
{
    uint32_t bits = (uint32_t)left - (uint32_t)right;
    if (bits & UINT32_C(0x80000000))
    {
        bits = 0u - bits;
    }
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

Ra2ClearancePhase ra2_ground_check_clearance(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int32_t passage, int32_t reference_level, int clear_only, Ra2ClearanceResult *result,
    const Ra2ClearanceServices *services)
{
    if (!clear_only)
    {
        int32_t overlay = services->query(services->context, RA2_CLEARANCE_OVERLAY_INDEX);
        if (passage == RA2_CELL_CLEAR)
        {
            if (overlay != -1 && services->query(services->context, RA2_CLEARANCE_OVERLAY_CRUSHABLE))
            {
                result->crush_overlay = 1;
            }
            int32_t level = services->query(services->context, RA2_CLEARANCE_CELL_LEVEL);
            if (level_difference(reference_level, level) >= 2)
            {
                result->target_level = reference_level;
                result->land = 1;
            }
            else
            {
                /* 原版重新查询两次；引擎服务的调用顺序是行为的一部分。 */
                result->target_level = services->query(services->context, RA2_CLEARANCE_CELL_LEVEL);
                result->land = services->query(services->context, RA2_CLEARANCE_CELL_LAND);
            }
            return RA2_CLEARANCE_TERRAIN_SPEED;
        }
        if (passage != RA2_CELL_GATE)
        {
            return RA2_CLEARANCE_SPECIAL_OBSTACLE;
        }
        services->request_gate(services->context);
    }
    clear_segment(state, invalid_position);
    return passage == RA2_CELL_MOVING_OBSTACLE ? RA2_CLEARANCE_WAIT_FOR_TRAFFIC : RA2_CLEARANCE_OTHER_OBSTACLE;
}

Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(Ra2TrafficWaitState *state,
    const Ra2TrafficWaitServices *services)
{
    if (!state->waiting)
    {
        state->waiting = 1;
        state->obstruction.start_frame = services->current_frame(services->context);
        state->obstruction.remaining_frames = services->wait_duration(services->context);
        services->start_wait(services->context, state->obstruction.start_frame, state->obstruction.remaining_frames);
    }
    int32_t frame = services->current_frame(services->context);
    if (!ra2_ground_retry_timer_ready(state->retry, frame))
    {
        return RA2_TRAFFIC_REPORT_OBSTACLE;
    }
    int mode = state->waiting && ra2_ground_retry_timer_ready(state->obstruction, frame) ? 2 : 1;
    int rebuilt = services->rebuild_path(services->context, mode);
    if (!services->owner_exists(services->context))
    {
        services->write_aborted(services->context);
        return RA2_TRAFFIC_RETURN_FALSE;
    }
    if (!rebuilt && !services->destination_accepted(services->context))
    {
        services->stop_navigation(services->context);
        return RA2_TRAFFIC_RETURN_FALSE;
    }
    /* 重建服务可能改变当前帧或对象；原版在调用后再次读取。 */
    frame = services->current_frame(services->context);
    int32_t delay = services->retry_delay(services->context);
    services->restart_retry(services->context, frame, delay);
    return RA2_TRAFFIC_RETURN_TRUE;
}
