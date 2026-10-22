#include <string.h>
#include "ground_turn.h"

static int32_t signed_bits(uint32_t bits)
{
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

static int32_t absolute_difference(int32_t left, int32_t right)
{
    uint32_t bits = (uint32_t)left - (uint32_t)right;
    if (bits & UINT32_C(0x80000000)) bits = 0u - bits;
    return signed_bits(bits);
}

static void clear_segment(Ra2TurnState *state, Ra2WorldPoint invalid)
{
    Ra2WorldPoint end = state->movement.segment_end;
    if (end.x!=invalid.x || end.y!=invalid.y || end.z!=invalid.z)
    {
        state->movement.segment_end = invalid;
        state->movement.driving = 0;
    }
}

static int stop_navigation(const Ra2TurnServices *services)
{
    void *context = services->context;
    int has_target = services->query(context, RA2_TURN_HAS_TARGET_488);
    if (has_target) services->cancel_target(context);
    int result = services->stop_navigation(context, has_target);
    return has_target && result;
}

static Ra2TurnPhase retry(const Ra2TurnServices *services, unsigned allow_recursive,
    unsigned prevent_turn, int restart_timer)
{
    return services->retry(services->context, allow_recursive, prevent_turn, restart_timer)
        ? RA2_TURN_RETURN_TRUE : RA2_TURN_RETURN_FALSE;
}

static Ra2TurnPhase discard_candidate(Ra2TurnState *state, Ra2WorldPoint invalid,
    int32_t passage, unsigned allow_recursive, const Ra2TurnServices *services)
{
    state->directions[0] = -1;
    state->selector = -1;
    state->candidate = invalid;
    if (passage==RA2_CELL_DESTROYABLE || passage==RA2_CELL_FRIENDLY_OBSTACLE)
    {
        return retry(services, allow_recursive, 1, 0);
    }
    return RA2_TURN_COMMIT_WITHOUT_SHIFT;
}

Ra2TurnPhase ra2_ground_prepare_turn(Ra2TurnState *state, Ra2WorldPoint invalid,
    int32_t next_direction, unsigned allow_recursive, const Ra2TurnServices *services)
{
    void *context = services->context;
    int32_t passage = RA2_CELL_BLOCKED;
    if (services->cell_accepts_owner(context) || services->query(context, RA2_TURN_OWNER_FLAG_76))
    {
        if (!services->query(context, RA2_TURN_OWNER_ALIVE)) return RA2_TURN_RETURN_FALSE;
        Ra2WorldPoint step = services->direction_offset(context, next_direction);
        state->candidate.x = signed_bits((uint32_t)state->candidate.x + (uint32_t)step.x);
        state->candidate.y = signed_bits((uint32_t)state->candidate.y + (uint32_t)step.y);
        passage = services->probe_passage(context, next_direction);
        if (passage < RA2_CELL_BLOCKED && services->query(context, RA2_TURN_IS_TRAIN))
        {
            passage = RA2_CELL_CLEAR;
        }
        else if ((passage==RA2_CELL_FRIENDLY_OBSTACLE || passage==RA2_CELL_DESTROYABLE)
            && services->query(context, RA2_TURN_IS_CRUSHER)
            && services->query(context, RA2_TURN_CELL_OVERLAY_INDEX)==0)
        {
            passage = RA2_CELL_CLEAR;
        }
    }
    else if (!services->query(context, RA2_TURN_OWNER_ALIVE)) return RA2_TURN_RETURN_FALSE;
    services->classified(context, passage);
    if (!services->query(context, RA2_TURN_OWNER_ALIVE)) return RA2_TURN_RETURN_FALSE;
    if (passage==RA2_CELL_CLEAR)
    {
        for (unsigned i=0; i<22; ++i) state->directions[i] = state->directions[i+2];
        state->directions[22] = -1;
        state->bridge_transition_pending = 1;
        return RA2_TURN_COMMIT_WITHOUT_SHIFT;
    }
    if (passage==RA2_CELL_GATE)
    {
        services->request_gate(context);
        return discard_candidate(state, invalid, passage, allow_recursive, services);
    }
    if (passage==RA2_CELL_MOVING_OBSTACLE) return retry(services, allow_recursive, 1, 0);
    if (passage==RA2_CELL_TEMPORARY_OBSTACLE)
    {
        if (services->query(context, RA2_TURN_IS_TRAIN))
        {
            return discard_candidate(state, invalid, passage, allow_recursive, services);
        }
        if (allow_recursive & 255u)
        {
            state->directions[0] = -1;
            return retry(services, 0, 0, 1);
        }
        int32_t distance = services->query(context, RA2_TURN_DISTANCE_TO_DESTINATION);
        int32_t close_enough = services->query(context, RA2_TURN_CLOSE_ENOUGH);
        if (distance < close_enough)
        {
            Ra2WorldPoint position = services->raw_position(context);
            int32_t height = services->query(context, RA2_TURN_HEIGHT_PER_LEVEL);
            if (absolute_difference(state->movement.destination.z, position.z) < signed_bits((uint32_t)height*2u)
                && services->query(context, RA2_TURN_CURRENT_LAND)!=10)
            {
                clear_segment(state, invalid);
                if (stop_navigation(services)) return RA2_TURN_RETURN_TRUE;
                return discard_candidate(state, invalid, passage, allow_recursive, services);
            }
        }
        int bridge_layer = 0;
        if (services->query(context, RA2_TURN_CELL_HAS_BRIDGE))
        {
            Ra2WorldPoint position = services->raw_position(context);
            int32_t height = services->query(context, RA2_TURN_HEIGHT_PER_LEVEL);
            int32_t level = services->query(context, RA2_TURN_CELL_LEVEL);
            bridge_layer = absolute_difference(position.z/height,level)>2;
        }
        services->notify_cell(context, bridge_layer);
        return discard_candidate(state, invalid, passage, allow_recursive, services);
    }
    if (passage==RA2_CELL_CLOAKED_OBSTACLE)
    {
        services->reveal_cell(context);
        if (allow_recursive & 255u)
        {
            state->directions[0] = -1;
            return retry(services, 0, 0, 0);
        }
        clear_segment(state, invalid);
        return stop_navigation(services) ? RA2_TURN_RETURN_TRUE : RA2_TURN_RETURN_FALSE;
    }
    if (passage==RA2_CELL_BLOCKED)
    {
        if (allow_recursive & 255u)
        {
            state->directions[0] = -1;
            return retry(services, 0, 0, 1);
        }
        clear_segment(state, invalid);
        return stop_navigation(services) ? RA2_TURN_RETURN_TRUE : RA2_TURN_RETURN_FALSE;
    }
    return discard_candidate(state, invalid, passage, allow_recursive, services);
}
