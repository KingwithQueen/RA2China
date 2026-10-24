#include "ground_recovery.h"
#include "ground_failure_transition.h"


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
            ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
            int target = !!services->query(services->context, RA2_RECOVERY_HAS_TARGET_488);
            if (ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation))
            {
                return 1;
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
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    state->path_selector = -1;
    state->legacy_flag_61 = 0;
    return 0;
}
