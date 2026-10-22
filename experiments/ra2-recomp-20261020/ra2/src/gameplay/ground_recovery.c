#include "ground_recovery.h"

static void clear_segment(Ra2GroundRecoveryState *state, Ra2WorldPoint invalid_position)
{
    if (state->segment_end.x != invalid_position.x || state->segment_end.y != invalid_position.y
        || state->segment_end.z != invalid_position.z)
    {
        state->segment_end = invalid_position;
        state->driving = 0;
    }
}

int ra2_ground_recover_path(Ra2GroundRecoveryState *state, Ra2WorldPoint invalid_position,
    int finish_only, const Ra2RecoveryServices *services)
{
    if (!finish_only)
    {
        if (state->remaining_failures > 0)
        {
            --state->remaining_failures;
        }
        else
        {
            clear_segment(state, invalid_position);
            if (!services->query(services->context, RA2_RECOVERY_HAS_TARGET_488))
            {
                services->stop_navigation(services->context, 0);
            }
            else
            {
                services->cancel_target(services->context);
                if (services->stop_navigation(services->context, 1))
                {
                    return 1;
                }
            }
            if (!services->query(services->context, RA2_RECOVERY_OWNER_ALIVE))
            {
                return 0;
            }
            if (state->failure_sound_pending)
            {
                services->play_failure_sound(services->context);
            }
            state->failure_sound_pending = 0;
        }
    }

    if (!services->query(services->context, RA2_RECOVERY_IS_MOVING)
        && services->query(services->context, RA2_RECOVERY_HAS_OBJECT_228)
        && !services->query(services->context, RA2_RECOVERY_ACCEPTS_OBJECT_228))
    {
        state->legacy_flag_578 = 1;
        services->notify_linked_objects(services->context);
    }
    clear_segment(state, invalid_position);
    state->path_selector = -1;
    state->legacy_flag_61 = 0;
    return 0;
}
