"""Extract allied-blocker and recovery phases without moving live service reads."""
from run_batch_v53 import *
name=sys.argv[1]
if name=='obstacle':
 p=R/'ra2/src/gameplay/ground_obstacle.c';assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_obstacle.c')
 t=p.read_text(encoding='utf-8')
 start=t.index('            int32_t distance = services->query');stop=t.index('\n        }\n    }\n    if (rebuilt)',start)
 old=t[start:stop]
 a=old.index('            int bridge_layer = 0;');near=old[:a];notify=old[a:]
 c=near.index('            if (close_to_destination)\n            {\n                ra2_ground_invalidate_segment')
 check=near[:c];finish=near[c:]
 # Keep the original decision body and its short-circuit order byte-for-byte apart from indentation.
 check='\n'.join(line[8:] if line.startswith('        ') else line for line in check.splitlines())+'\n'
 check+='    return close_to_destination;\n'
 notify='\n'.join(line[8:] if line.startswith('        ') else line for line in notify.splitlines())+'\n'
 helper='''static int close_to_allied_blocker(Ra2GroundPrepareState *state,
    const Ra2ObstacleServices *services, void *context)
{
    Ra2WorldPoint position;
'''+check+'''}

static void notify_allied_blocker(const Ra2ObstacleServices *services, void *context)
{
    Ra2WorldPoint position;
'''+notify+'''}

'''
 replacement='''            /* 友军查询和列车过滤之后才判断距离；桥层查询只在不结束目标时执行。 */
            if (close_to_allied_blocker(state, services, context))
            {
                ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
                int target_variant = services->query(context, RA2_OBSTACLE_HAS_TARGET_488);
                int stopped = ra2_ground_stop_target(target_variant, context,
                    services->cancel_target, services->stop_navigation);
                return target_variant && stopped ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE;
            }
            notify_allied_blocker(services, context);'''
 t=t[:start]+replacement+t[stop:];t=t.replace('Ra2PreparePhase ra2_ground_observe_obstacle(',helper+'Ra2PreparePhase ra2_ground_observe_obstacle(',1)
elif name=='recovery':
 p=R/'ra2/src/gameplay/ground_recovery.c';assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_recovery.c')
 t='''#include "ground_recovery.h"
#include "ground_failure_transition.h"

typedef enum RecoveryBudgetOutcome
{
    RA2_RECOVERY_CONTINUE,
    RA2_RECOVERY_TARGET_STOPPED,
    RA2_RECOVERY_OWNER_REMOVED
} RecoveryBudgetOutcome;

static RecoveryBudgetOutcome consume_failure_budget(Ra2GroundRecoveryState *state,
    Ra2WorldPoint invalid_position, const Ra2RecoveryServices *services)
{
    if (state->remaining_failures > 0)
    {
        --state->remaining_failures;
        return RA2_RECOVERY_CONTINUE;
    }
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    int target = !!services->query(services->context, RA2_RECOVERY_HAS_TARGET_488);
    if (ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation))
        return RA2_RECOVERY_TARGET_STOPPED;
    /* 停止服务可移除对象；存活检查必须先于音效和共享收尾。 */
    if (!services->query(services->context, RA2_RECOVERY_OWNER_ALIVE))
        return RA2_RECOVERY_OWNER_REMOVED;
    if (state->failure_sound_pending)
        services->play_failure_sound(services->context);
    state->failure_sound_pending = 0;
    return RA2_RECOVERY_CONTINUE;
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

int ra2_ground_recover_path(Ra2GroundRecoveryState *state, Ra2WorldPoint invalid_position,
    int finish_only, const Ra2RecoveryServices *services)
{
    if (!finish_only)
    {
        RecoveryBudgetOutcome result = consume_failure_budget(state, invalid_position, services);
        if (result != RA2_RECOVERY_CONTINUE) return result == RA2_RECOVERY_TARGET_STOPPED;
    }
    notify_unaccepted_link(state, services);
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    state->path_selector = -1;
    state->legacy_flag_61 = 0;
    return 0;
}
'''
else:raise ValueError(name)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,phase=name,source=p.relative_to(R).as_posix(),sha256=sha(p)))
