#include "ground_barrier.h"
#include "ground_collision.h"

static Ra2BarrierResult result(Ra2BarrierOutcome outcome, int32_t passage)
{
    Ra2BarrierResult value = { outcome, passage };
    return value;
}

static int32_t raise_priority(int32_t current, int32_t minimum)
{
    return current < minimum ? minimum : current;
}

Ra2BarrierResult ra2_ground_check_overlay(Ra2OverlayBarrier overlay, int32_t previous_result,
    void *context, Ra2BarrierQueryFunction query)
{
    if (!overlay.present)
    {
        return result(RA2_BARRIER_CONTINUE, previous_result);
    }
    if (overlay.is_crate && !query(context, RA2_BARRIER_HOUSE_CRATE_PERMISSION)
        && !query(context, RA2_BARRIER_GLOBAL_CRATE_MODE))
    {
        return result(RA2_BARRIER_BLOCKED, RA2_CELL_BLOCKED);
    }
    if (!overlay.is_wall)
    {
        return result(RA2_BARRIER_CONTINUE, previous_result);
    }
    if (overlay.is_crushable && (overlay.actor_is_crusher || query(context, RA2_BARRIER_CRUSHER_ABILITY)))
    {
        /* 可碾压的敌方墙不提高等级；友方墙仍保留原版等级 4。 */
        if (query(context, RA2_BARRIER_WALL_OWNER_ALLIED))
        {
            previous_result = raise_priority(previous_result, RA2_CELL_FRIENDLY_OBSTACLE);
        }
        return result(RA2_BARRIER_CONTINUE, previous_result);
    }
    if (!query(context, RA2_BARRIER_ACTOR_CAN_ATTACK))
    {
        return result(RA2_BARRIER_BLOCKED, RA2_CELL_BLOCKED);
    }
    int weapon_flags = query(context, RA2_BARRIER_WEAPON_WALL_FLAGS);
    if (!(weapon_flags & 1) && (!(weapon_flags & 2) || overlay.armor != 6))
    {
        return result(RA2_BARRIER_BLOCKED, RA2_CELL_BLOCKED);
    }
    int32_t priority = query(context, RA2_BARRIER_WALL_OWNER_ALLIED) ? RA2_CELL_FRIENDLY_OBSTACLE : RA2_CELL_DESTROYABLE;
    return result(RA2_BARRIER_CONTINUE, raise_priority(previous_result, priority));
}

Ra2BarrierResult ra2_ground_check_gate(unsigned is_gate, int32_t previous_result,
    void *context, Ra2BarrierQueryFunction query)
{
    if (!is_gate)
    {
        return result(RA2_BARRIER_NOT_GATE, previous_result);
    }
    if (query(context, RA2_BARRIER_GATE_PASSABLE))
    {
        return result(RA2_BARRIER_SKIP_OBJECT, previous_result);
    }
    if (query(context, RA2_BARRIER_GATE_OWNER_ALLIED))
    {
        return result(RA2_BARRIER_SKIP_OBJECT, raise_priority(previous_result, RA2_CELL_GATE));
    }
    if (!query(context, RA2_BARRIER_ACTOR_CAN_ATTACK))
    {
        return result(RA2_BARRIER_BLOCKED, RA2_CELL_BLOCKED);
    }
    return result(RA2_BARRIER_SKIP_OBJECT, raise_priority(previous_result, RA2_CELL_DESTROYABLE));
}
