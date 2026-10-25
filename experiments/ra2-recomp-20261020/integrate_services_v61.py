"""Reversible path-result consumption, followed by direction queue and segment publication."""
from run_batch_v61 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
if sys.argv[1]=='consumer':
 p=R/'ra2/src/gameplay/ground_followup.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('Ra2FollowupResult ra2_ground_prepare_followup(')
 t=t[:a]+'''static void consume_followup_rebuild(const Ra2FollowupServices *services,void *context,
    Ra2FollowupResult *result)
{
    /* 沿用候选准备之前取得的context；回调可以改变目标、所属对象或服务表。 */
    int train=services->is_train(context);
    int rebuilt=services->rebuild_path(context,train);
    Ra2RebuildResultServices checks={context,services->owner_exists,services->write_aborted,
        services->destination_accepted,services->stop_navigation};
    if(ra2_ground_check_rebuild_result(rebuilt,0,&checks)==RA2_REBUILD_NO_OWNER) {
        result->aborted=1;
        return;
    }
    /* 拒绝目标并停止后仍重取第二方向；成功重建不额外复核owner。 */
    result->next_direction=services->next_direction(context);
}

Ra2FollowupResult ra2_ground_prepare_followup(const Ra2FollowupServices *services)
{
    void *context=services->context;
    services->prepare_candidate(context);
    Ra2FollowupResult result={services->next_direction(context),0,0};
    if(result.next_direction!=-1)return result;
    if(services->distance_to_destination(context)<=512) {
        result.force_straight=1;
        return result;
    }
    consume_followup_rebuild(services,context,&result);
    return result;
}
'''
 p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='queue':
 p=R/'ra2/src/gameplay/ground_template.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('void ra2_ground_commit_segment(')
 t=t[:a]+'''static int32_t consume_direction_queue(Ra2SegmentCommitState *state,int skip_shift,
    int32_t terminal_direction)
{
    if(!skip_shift) {
        for(unsigned i=0;i<23;++i)state->directions[i]=state->directions[i+1];
        terminal_direction=-1;
    }
    /* 保留队列的入口仍写指定尾槽；普通弹出只移动23槽，再补-1。 */
    state->directions[23]=terminal_direction;
    return terminal_direction;
}

static void prepare_segment_publication(Ra2SegmentCommitState *state,Ra2WorldPoint invalid,
    Ra2WorldPoint candidate)
{
    state->target_cell_x=(int16_t)(candidate.x/256);
    state->target_cell_y=(int16_t)(candidate.y/256);
    state->sound_pending=0;
    state->sample_index=0;
    /* 已经无效的旧段不附带改写driving；保留原状态与放行服务的交接。 */
    if(!same_position(state->movement.segment_end,invalid)) {
        state->movement.segment_end=invalid;
        state->movement.driving=0;
    }
}

static void reject_queued_segment(Ra2SegmentCommitState *state,int32_t terminal,
    const Ra2SegmentCommitServices *services)
{
    state->selector=terminal;
    state->directions[0]=terminal;
    services->set_speed_zero(services->context);
}

void ra2_ground_commit_segment(Ra2SegmentCommitState *state,Ra2WorldPoint invalid_position,
    Ra2WorldPoint candidate,int skip_shift,int32_t terminal_direction,const Ra2SegmentCommitServices *services)
{
    terminal_direction=consume_direction_queue(state,skip_shift,terminal_direction);
    prepare_segment_publication(state,invalid_position,candidate);
    const Ra2SegmentAdmissionServices admission={services->context,services->cell_accepts_owner,
        services->owner_flag_76,services->start_segment,services->owner_alive};
    if(ra2_ground_admit_segment(&state->movement.segment_end,&state->movement.driving,
        invalid_position,candidate,&admission)==RA2_SEGMENT_STARTED)return;
    reject_queued_segment(state,terminal_direction,services);
}
'''
 p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
