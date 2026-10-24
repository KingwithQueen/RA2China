#include <stdint.h>
#include <string.h>
#include "ground_arrival.h"
#include "ground_failure_transition.h"


static int same_cell(Ra2WorldPoint left, Ra2WorldPoint right)
{
    /* 原版先向零取整，再截取 16 位格坐标；不能用负数右移代替除法。 */
    return (uint16_t)(left.x / 256) == (uint16_t)(right.x / 256)
        && (uint16_t)(left.y / 256) == (uint16_t)(right.y / 256);
}

static int32_t signed_bits(uint32_t bits)
{
    int32_t value;
    memcpy(&value, &bits, sizeof(value));
    return value;
}

static int32_t wrapped_distance(int32_t left, int32_t right)
{
    uint32_t difference = (uint32_t)left - (uint32_t)right;
    if (difference & 0x80000000u)
    {
        difference = 0u - difference;
    }
    return signed_bits(difference);
}


/* 刷新后重新检查可用性；停止任务/更新服务均可结束本帧或移除所有者。 */
static Ra2ArrivalOutcome finish_after_refresh(int reached_target, const Ra2ArrivalServices *services)
{
    services->refresh_owner(services->context);
    if (!services->query(services->context, RA2_ARRIVAL_OWNER_USABLE))
    {
        return RA2_ARRIVAL_RETURN_TRUE;
    }
    if (reached_target)
    {
        services->cancel_target_and_path(services->context);
        if (services->query(services->context, RA2_ARRIVAL_EFFECTIVE_MISSION) == 2
            && services->stop_move_mission(services->context))
        {
            return RA2_ARRIVAL_RETURN_TRUE;
        }
    }
    if (services->query(services->context, RA2_ARRIVAL_OWNER_UPDATE))
    {
        return RA2_ARRIVAL_RETURN_TRUE;
    }
    if (!services->query(services->context, RA2_ARRIVAL_OWNER_ALIVE))
    {
        return RA2_ARRIVAL_RETURN_FALSE;
    }
    return RA2_ARRIVAL_CONTINUE;
}

Ra2ArrivalOutcome ra2_ground_finish_segment(Ra2GroundArrivalState *state, Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position, int32_t level_height, const Ra2ArrivalServices *services)
{
    services->relocate(services->context, !same_cell(owner_position, state->segment_end));
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    state->path_selector = -1;
    state->sample_index = 0;

    int reached_target = 0;
    if (services->query(services->context, RA2_ARRIVAL_TARGET_IS_CURRENT_CELL))
    {
        int32_t owner_z = services->query(services->context, RA2_ARRIVAL_OWNER_REFERENCE_Z);
        int32_t tolerance = signed_bits((uint32_t)level_height * 2u);
        if (wrapped_distance(owner_z, state->destination.z) < tolerance)
        {
            reached_target = 1;
            state->destination = invalid_position;
            ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
            state->driving = 0;
        }
    }

    return finish_after_refresh(reached_target, services);
}
