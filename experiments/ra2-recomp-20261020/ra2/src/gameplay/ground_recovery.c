#include "ground_recovery.h"
#include "ground_failure_transition.h"

typedef enum RecoveryBudgetOutcome
{
    RA2_RECOVERY_CONTINUE,
    RA2_RECOVERY_TARGET_STOPPED,
    RA2_RECOVERY_OWNER_REMOVED
} RecoveryBudgetOutcome;

static RecoveryBudgetOutcome finish_exhausted_budget(Ra2GroundRecoveryState *state,
    Ra2WorldPoint invalid_position,const Ra2RecoveryServices *services)
{
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
    int target=!!services->query(services->context,RA2_RECOVERY_HAS_TARGET_488);
    if(ra2_ground_stop_target(target,services->context,services->cancel_target,services->stop_navigation))
        return RA2_RECOVERY_TARGET_STOPPED;
    /* 停止服务可能移除owner；先实时查存活，再处理声音与共享收尾。 */
    if(!services->query(services->context,RA2_RECOVERY_OWNER_ALIVE))
        return RA2_RECOVERY_OWNER_REMOVED;
    if(state->failure_sound_pending)services->play_failure_sound(services->context);
    state->failure_sound_pending=0;
    return RA2_RECOVERY_CONTINUE;
}

static RecoveryBudgetOutcome consume_failure_budget(Ra2GroundRecoveryState *state,
    Ra2WorldPoint invalid_position,const Ra2RecoveryServices *services)
{
    if(state->remaining_failures>0) {
        --state->remaining_failures;
        return RA2_RECOVERY_CONTINUE;
    }
    return finish_exhausted_budget(state,invalid_position,services);
}

static void notify_unaccepted_link(Ra2GroundRecoveryState *state,
    const Ra2RecoveryServices *services)
{
    /* 每次保留原调用点的context读取；前序服务可改变关联对象或移动状态。 */
    if (!services->query(services->context, RA2_RECOVERY_IS_MOVING)
        && services->query(services->context, RA2_RECOVERY_HAS_OBJECT_228)
        && !services->query(services->context, RA2_RECOVERY_ACCEPTS_OBJECT_228))
    {
        state->legacy_flag_578 = 1;
        services->notify_linked_objects(services->context);
    }
}

static void finish_recovery_state(Ra2GroundRecoveryState *state,
    Ra2WorldPoint invalid_position,const Ra2RecoveryServices *services)
{
    notify_unaccepted_link(state,services);
    /* 通知后再复位本段；通知回调对状态的修改仍按原顺序可见。 */
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
    state->path_selector=-1;
    state->legacy_flag_61=0;
}

int ra2_ground_recover_path(Ra2GroundRecoveryState *state,Ra2WorldPoint invalid_position,
    int finish_only,const Ra2RecoveryServices *services)
{
    if(!finish_only) {
        RecoveryBudgetOutcome result=consume_failure_budget(state,invalid_position,services);
        if(result!=RA2_RECOVERY_CONTINUE)return result==RA2_RECOVERY_TARGET_STOPPED;
    }
    finish_recovery_state(state,invalid_position,services);
    return 0;
}
