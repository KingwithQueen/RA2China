#include <string.h>
#include "ground_turn.h"
#include "ground_failure_transition.h"
#include "ground_template_transition.h"

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

typedef struct TurnGate { int32_t passage; const Ra2TurnServices *services; } TurnGate;
static int32_t gate_class(void *opaque) { return ((TurnGate *)opaque)->passage; }
static unsigned gate_type(void *opaque, unsigned crusher)
{
    const Ra2TurnServices *s = ((TurnGate *)opaque)->services;
    return (unsigned)s->query(s->context, crusher ? RA2_TURN_IS_CRUSHER : RA2_TURN_IS_TRAIN);
}
static int32_t gate_overlay(void *opaque)
{
    const Ra2TurnServices *s = ((TurnGate *)opaque)->services;
    return s->query(s->context, RA2_TURN_CELL_OVERLAY_INDEX);
}
static void gate_clear(void *opaque) { ((TurnGate *)opaque)->passage = RA2_CELL_CLEAR; }

/* 临时障碍停止失败后放弃候选；隐形/完全阻挡直接返回。服务次序共用，接续策略保留。 */
static Ra2TurnPhase stop_candidate(Ra2TurnState *state, Ra2WorldPoint invalid, int discard,
    int32_t passage, unsigned allow_recursive, const Ra2TurnServices *s)
{
    ra2_ground_invalidate_segment(&state->movement.segment_end, &state->movement.driving, invalid);
    int target = s->query(s->context, RA2_TURN_HAS_TARGET_488);
    if (ra2_ground_stop_target(target, s->context, s->cancel_target, s->stop_navigation)) return RA2_TURN_RETURN_TRUE;
    return discard ? discard_candidate(state, invalid, passage, allow_recursive, s) : RA2_TURN_RETURN_FALSE;
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
        TurnGate gate = { passage, services };
        Ra2TemplateGateServices checks = { &gate, gate_class, gate_type, gate_overlay, gate_clear };
        ra2_ground_template_gate(&checks);
        passage = gate.passage;
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
                return stop_candidate(state, invalid, 1, passage, allow_recursive, services);
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
        return stop_candidate(state, invalid, 0, passage, allow_recursive, services);
    }
    if (passage==RA2_CELL_BLOCKED)
    {
        if (allow_recursive & 255u)
        {
            state->directions[0] = -1;
            return retry(services, 0, 0, 1);
        }
        return stop_candidate(state, invalid, 0, passage, allow_recursive, services);
    }
    return discard_candidate(state, invalid, passage, allow_recursive, services);
}
