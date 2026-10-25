"""Two serial reversible service steps; preserve original callback/state ordering."""
from run_batch_v67 import *
assert read(S/'traffic-baseline-scenes.json')['passed'] and read(S/'channel-observer-baseline-parity.json')['passed']
if sys.argv[1]=='reaction':
 p=R/'ra2/src/gameplay/ground_reaction.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R));t=p.read_text(encoding='utf-8');a=t.index('int ra2_ground_react_to_obstacle(')
 t=t[:a]+'''/* 分派码与保存的通行结果分别处理；友方障碍只改本次路径头和标志。 */
static Ra2ReactionEntry select_obstacle_response(Ra2ReactionEntry entry,
    int32_t dispatch_code,int32_t *path_head,uint32_t *flags)
{
    if(entry!=RA2_REACTION_DISPATCH)return entry;
    if(dispatch_code==RA2_CELL_FRIENDLY_OBSTACLE) {
        *path_head=-1;
        *flags=0;
        return RA2_REACTION_ATTACK;
    }
    return dispatch_code==RA2_CELL_DESTROYABLE ? RA2_REACTION_ATTACK:RA2_REACTION_REPORT;
}

static void attack_obstacle_target(int32_t path_head,uint32_t flags,
    const Ra2ReactionServices *services)
{
    if(services->find_object(services->context,flags)) {
        /* 敌我判断前重取对象；攻击服务仍自行取得当时目标，不缓存跨回调对象。 */
        uint32_t object=services->find_object(services->context,flags);
        if(!services->object_allied(services->context,object))
            services->attack_object(services->context,flags);
    } else if(services->has_overlay(services->context,path_head)
        && services->overlay_is_wall(services->context)) {
        services->attack_wall(services->context,flags);
    }
}

static int finish_obstacle_response(Ra2GroundPrepareState *state,Ra2WorldPoint invalid_position,
    int32_t passage,int allow_recursive,const Ra2ReactionServices *services)
{
    if(passage==RA2_CELL_BLOCKED) {
        if(allow_recursive)return services->retry_recursively(services->context,-1,0);
        return stop_at_obstacle(state,invalid_position,services);
    }
    services->clear_pending_and_selector(services->context);
    return 1;
}

int ra2_ground_react_to_obstacle(Ra2GroundPrepareState *state,Ra2WorldPoint invalid_position,
    Ra2ReactionEntry entry,int32_t dispatch_code,int32_t passage,int allow_recursive,
    int32_t path_head,uint32_t flags,const Ra2ReactionServices *services)
{
    entry=select_obstacle_response(entry,dispatch_code,&path_head,&flags);
    if(entry==RA2_REACTION_REPORT) {
        if(services->sound_pending(services->context))services->play_sound(services->context);
    } else if(entry==RA2_REACTION_ATTACK) {
        /* 递归即为当前出口，失败返回也不能继续落入后续收尾。 */
        if(allow_recursive)return services->retry_recursively(services->context,path_head,flags);
        attack_obstacle_target(path_head,flags,services);
    }
    return finish_obstacle_response(state,invalid_position,passage,allow_recursive,services);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='recovery':
 p=R/'ra2/src/gameplay/ground_recovery.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R));t=p.read_text(encoding='utf-8')
 a=t.index('static RecoveryBudgetOutcome consume_failure_budget(');b=t.index('static void notify_unaccepted_link(',a)
 t=t[:a]+'''static RecoveryBudgetOutcome finish_exhausted_budget(Ra2GroundRecoveryState *state,
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

'''+t[b:]
 a=t.index('int ra2_ground_recover_path(')
 t=t[:a]+'''static void finish_recovery_state(Ra2GroundRecoveryState *state,
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
''';p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1],mechanism_changed=False))
