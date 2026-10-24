#include "ground_exit_policy.h"
#include <string.h>

Ra2PrepareExitPlan ra2_ground_prepare_exit_plan(Ra2PrepareFinishEntry entry, int may_retry)
{
    Ra2PrepareExitPlan plan = {0};
    switch (entry)
    {
        case RA2_PREPARE_RECURSE_TIMER_TAIL:
            plan.finish_timer = plan.recurse = 1;
            break;
        case RA2_PREPARE_RECURSE_CLEAR_PATH:
            plan.clear_path = plan.recurse = 1;
            break;
        case RA2_PREPARE_RETRY_OR_CLEAR:
            if (may_retry)
                plan.clear_path = plan.start_retry = plan.finish_timer = plan.recurse = 1;
            else plan.clear_segment = 1;
            break;
        case RA2_PREPARE_CLEAR_SEGMENT:
        case RA2_PREPARE_CLEAR_SEGMENT_SAVED_OWNER:
            plan.clear_segment = 1;
            break;
        case RA2_PREPARE_CLEAR_DRIVING:
            plan.clear_driving = 1;
            break;
        case RA2_PREPARE_CANCEL_TARGET:
            plan.cancel_target = 1;
            break;
        default:
            break;
    }
    return plan;
}

int32_t ra2_ground_connection_height(int32_t start, int32_t finish, int32_t duration)
{
    uint32_t bits = (uint32_t)finish - (uint32_t)start;
    int32_t difference, height;
    memcpy(&difference, &bits, sizeof(bits));
    bits = (uint32_t)(difference / duration) + (uint32_t)start;
    memcpy(&height, &bits, sizeof(bits));
    return height;
}
