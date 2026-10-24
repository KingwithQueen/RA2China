#include "ground_reaction.h"
#include "ground_failure_transition.h"

static int stop_at_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    const Ra2ReactionServices *services)
{
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    int target = !!services->has_target_488(services->context);
    return ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation);
}

int ra2_ground_react_to_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    Ra2ReactionEntry entry, int32_t dispatch_code, int32_t passage, int allow_recursive,
    int32_t path_head, uint32_t flags, const Ra2ReactionServices *services)
{
    if (entry == RA2_REACTION_DISPATCH)
    {
        if (dispatch_code == RA2_CELL_FRIENDLY_OBSTACLE)
        {
            path_head = -1;
            flags = 0;
            entry = RA2_REACTION_ATTACK;
        }
        else
        {
            entry = dispatch_code == RA2_CELL_DESTROYABLE ? RA2_REACTION_ATTACK : RA2_REACTION_REPORT;
        }
    }
    if (entry == RA2_REACTION_REPORT)
    {
        if (services->sound_pending(services->context))
        {
            services->play_sound(services->context);
        }
    }
    else if (entry == RA2_REACTION_ATTACK)
    {
        if (allow_recursive)
        {
            return services->retry_recursively(services->context, path_head, flags);
        }
        if (services->find_object(services->context, flags))
        {
            /* 原版在判定敌我、真正攻击前分别重新取得对象；不能缓存第一次结果。 */
            uint32_t object = services->find_object(services->context, flags);
            if (!services->object_allied(services->context, object))
            {
                services->attack_object(services->context, flags);
            }
        }
        else if (services->has_overlay(services->context, path_head)
            && services->overlay_is_wall(services->context))
        {
            services->attack_wall(services->context, flags);
        }
    }
    if (passage == RA2_CELL_BLOCKED)
    {
        if (allow_recursive)
        {
            return services->retry_recursively(services->context, -1, 0);
        }
        return stop_at_obstacle(state, invalid_position, services);
    }
    services->clear_pending_and_selector(services->context);
    return 1;
}
