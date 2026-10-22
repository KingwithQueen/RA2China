#include <stdint.h>
#include <string.h>
#include "ground_special.h"

static int32_t absolute_difference(int32_t left, int32_t right)
{
    uint32_t bits = (uint32_t)left - (uint32_t)right;
    if (bits & UINT32_C(0x80000000)) bits = 0u - bits;
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

static void clear_segment(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position)
{
    if (state->segment_end.x != invalid_position.x || state->segment_end.y != invalid_position.y
        || state->segment_end.z != invalid_position.z)
    {
        state->segment_end = invalid_position;
        state->driving = 0;
    }
}

static int stop_navigation(const Ra2SpecialServices *services)
{
    int target_variant = services->query(services->context, RA2_SPECIAL_HAS_TARGET_488);
    if (target_variant) services->cancel_target(services->context);
    int stopped = services->stop_navigation(services->context, target_variant);
    return target_variant && stopped;
}

Ra2SpecialPhase ra2_ground_handle_special_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int32_t passage, int allow_recursive, int32_t path_head, const Ra2SpecialServices *services)
{
    void *context = services->context;
    if (passage == RA2_CELL_CLOAKED_OBSTACLE)
    {
        services->reveal_cell(context);
        if (allow_recursive)
        {
            return services->retry(context, path_head, 0) ? RA2_SPECIAL_RETURN_TRUE : RA2_SPECIAL_RETURN_FALSE;
        }
        clear_segment(state, invalid_position);
        return stop_navigation(services) ? RA2_SPECIAL_RETURN_TRUE : RA2_SPECIAL_RETURN_FALSE;
    }
    if (passage != RA2_CELL_TEMPORARY_OBSTACLE || services->query(context, RA2_SPECIAL_IS_TRAIN))
    {
        return RA2_SPECIAL_CLEAR_SEGMENT;
    }
    if (allow_recursive)
    {
        return services->retry(context, path_head, 1) ? RA2_SPECIAL_RETURN_TRUE : RA2_SPECIAL_RETURN_FALSE;
    }
    int32_t distance = services->query(context, RA2_SPECIAL_DISTANCE_TO_TARGET);
    int32_t close_enough = services->query(context, RA2_SPECIAL_CLOSE_ENOUGH);
    if (distance < close_enough)
    {
        Ra2WorldPoint position = services->raw_position(context);
        int32_t height = services->query(context, RA2_SPECIAL_HEIGHT_PER_LEVEL);
        if (absolute_difference(state->destination.z, position.z) < (int32_t)((uint32_t)height * 2u)
            && services->query(context, RA2_SPECIAL_CURRENT_LAND) != 10)
        {
            clear_segment(state, invalid_position);
            if (stop_navigation(services)) return RA2_SPECIAL_RETURN_TRUE;
            return RA2_SPECIAL_CLEAR_SEGMENT;
        }
    }
    int bridge_layer = 0;
    if (services->query(context, RA2_SPECIAL_CELL_HAS_BRIDGE))
    {
        Ra2WorldPoint position = services->raw_position(context);
        int32_t height = services->query(context, RA2_SPECIAL_HEIGHT_PER_LEVEL);
        int32_t level = services->query(context, RA2_SPECIAL_CELL_LEVEL);
        bridge_layer = absolute_difference(position.z / height, level) > 2;
    }
    services->notify_cell(context, bridge_layer);
    return RA2_SPECIAL_CLEAR_SEGMENT;
}
