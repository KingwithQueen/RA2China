#include <string.h>
#include "ground_completion.h"

static uint32_t absolute_difference(int32_t left, int32_t right)
{
    uint32_t difference = (uint32_t)left - (uint32_t)right;
    return difference & 0x80000000u ? 0u - difference : difference;
}

int32_t ra2_ground_arrival_adjustment(Ra2WorldPoint position, Ra2WorldPoint end, uint16_t control)
{
    uint32_t bits = absolute_difference(end.x, position.x) + absolute_difference(end.y, position.y);
    int32_t distance;
    memcpy(&distance, &bits, sizeof(distance));
    return ra2_ground_arrival_progress_adjustment(distance, &ra2_original_ground_path_sampling, control);
}

uint32_t ra2_ground_prepare_finish(Ra2PrepareFinishEntry entry, int may_retry,
    const Ra2PrepareFinishServices *s)
{
    if (entry == RA2_PREPARE_RECURSE_TIMER_TAIL)
    {
        s->finish_retry_timer(s->context);
        return s->prepare_again(s->context);
    }
    if (entry == RA2_PREPARE_RECURSE_CLEAR_PATH)
    {
        s->clear_path(s->context);
        return s->prepare_again(s->context);
    }
    if (entry == RA2_PREPARE_RETRY_OR_CLEAR && may_retry)
    {
        s->clear_path(s->context);
        s->start_immediate_retry(s->context);
        s->finish_retry_timer(s->context);
        return s->prepare_again(s->context);
    }
    if (entry == RA2_PREPARE_CLEAR_SEGMENT || entry == RA2_PREPARE_CLEAR_SEGMENT_SAVED_OWNER
        || entry == RA2_PREPARE_RETRY_OR_CLEAR)
    {
        s->clear_segment(s->context);
    }
    if (entry == RA2_PREPARE_CLEAR_DRIVING)
    {
        s->clear_driving(s->context);
    }
    if (entry == RA2_PREPARE_CANCEL_TARGET || s->has_target(s->context))
    {
        s->cancel_target(s->context);
        return s->stop(s->context, 1);
    }
    return s->stop(s->context, 0) & 0xFFFFFF00u;
}
