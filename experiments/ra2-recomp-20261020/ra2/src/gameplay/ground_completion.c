#include <string.h>
#include "ground_completion.h"
#include "ground_exit_policy.h"

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
    Ra2PrepareExitPlan plan = ra2_ground_prepare_exit_plan(entry, may_retry);
    if (plan.clear_path) s->clear_path(s->context);
    if (plan.start_retry) s->start_immediate_retry(s->context);
    if (plan.finish_timer) s->finish_retry_timer(s->context);
    if (plan.recurse) return s->prepare_again(s->context);
    if (plan.clear_segment) s->clear_segment(s->context);
    if (plan.clear_driving) s->clear_driving(s->context);
    /* 取消入口短路目标查询；其他入口在清理服务之后再查询。 */
    if (plan.cancel_target || s->has_target(s->context))
    {
        s->cancel_target(s->context);
        return s->stop(s->context, 1);
    }
    return s->stop(s->context, 0) & 0xFFFFFF00u;
}
