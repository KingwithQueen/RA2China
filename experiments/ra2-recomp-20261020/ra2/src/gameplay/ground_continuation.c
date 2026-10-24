#include <string.h>
#include "ground_continuation.h"
#include "ground_failure_transition.h"
#include "ground_segment_admission.h"

static int32_t signed_bits(uint32_t bits)
{ int32_t result; memcpy(&result,&bits,4); return result; }
static int32_t absolute_difference(int32_t a,int32_t b)
{
    uint32_t bits=(uint32_t)a-(uint32_t)b;
    if(bits&UINT32_C(0x80000000)) bits=0u-bits;
    return signed_bits(bits);
}
/* 接续服务按实时上下文读取候选，不能改成 Prepare 的按值位置参数。
   接受服务可能移除 owner 或改写状态；成功后仍按原顺序恢复速度、弹出方向。 */
static int continuation_accept(void *context,Ra2WorldPoint candidate)
{
    const Ra2ContinuationServices *s=context; (void)candidate;
    return s->candidate_accepts_owner(s->context);
}
static int continuation_restricted(void *context)
{
    const Ra2ContinuationServices *s=context;
    return s->query(s->context,RA2_CONTINUATION_OWNER_FLAG_76);
}
static int continuation_alive(void *context)
{
    const Ra2ContinuationServices *s=context;
    return s->query(s->context,RA2_CONTINUATION_OWNER_ALIVE);
}
static void continuation_start(void *context,Ra2WorldPoint candidate)
{
    const Ra2ContinuationServices *s=context; (void)candidate;
    s->start_segment(s->context);
}

/* 接续已获放行后，提交模板、刷新对象，再按存活与候选格结果进入/放弃路段。
   刷新和进入服务可改变状态；恢复速度、移除旧方向只发生在成功进入之后。 */
static int commit_turn_segment(Ra2ContinuationState *state,Ra2WorldPoint invalid,
    int32_t selector,Ra2ContinuationTemplate selected,uint64_t speed,
    const Ra2ContinuationServices *s)
{
    void *c=s->context;
    state->alternate_template=0; state->selector=selector;
    state->orientation_mismatch=0;
    state->sample_index=signed_bits((uint32_t)selected.entry_index-1u);
    s->commit_template(c,selected);
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid);
    state->driving=1;
    s->refresh_owner(c);
    state->driving=0;
    if(!s->query(c,RA2_CONTINUATION_OWNER_ALIVE) || s->query(c,RA2_CONTINUATION_OWNER_FLAG_76)
        || s->query(c,RA2_CONTINUATION_OWNER_FLAG_7A)) return 0;
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid);
    const Ra2SegmentAdmissionServices admission={(void *)s,continuation_accept,
        continuation_restricted,continuation_start,continuation_alive};
    if(ra2_ground_admit_segment(&state->segment_end,&state->driving,invalid,
        state->candidate,&admission)==RA2_SEGMENT_STARTED)
    {
        s->restore_speed(c,speed);
        s->shift_direction(c);
    }
    return 1;
}

int ra2_ground_continue_turn(Ra2ContinuationState *state,Ra2WorldPoint invalid,
    int32_t direction,const Ra2ContinuationServices *s)
{
    void *c=s->context;
    if(direction==8 || direction==-1 || !state->orientation_mismatch) return 1;
    if(state->sample_index!=s->query(c,RA2_CONTINUATION_TRANSITION_INDEX) || !state->sample_index) return 1;
    unsigned heading=(unsigned)s->query(c,RA2_CONTINUATION_TEMPLATE_HEADING)&255u;
    unsigned facing=(((heading>>4)+1u)>>1)&7u;
    int32_t selector=signed_bits((uint32_t)direction+facing*8u);
    Ra2ContinuationTemplate selected=s->find_template(c,selector);
    if(!selected.sample_kind || !selected.entry_index) return 1;
    uint64_t speed=s->save_speed(c);
    Ra2WorldPoint step=s->direction_offset(c,direction);
    state->candidate=state->segment_end;
    state->candidate.x=signed_bits((uint32_t)state->candidate.x+(uint32_t)step.x);
    state->candidate.y=signed_bits((uint32_t)state->candidate.y+(uint32_t)step.y);
    int32_t passage=s->probe_passage(c,state->candidate,direction);
    s->classified(c,passage);
    if(passage==RA2_CELL_CLEAR || passage==RA2_CELL_MOVING_OBSTACLE)
    {
        /* 这里原版允许移动障碍接续，与 Prepare 的让路重试分支不同。 */
        if(s->query(c,RA2_CONTINUATION_OWNER_KIND)==1 && !s->query(c,RA2_CONTINUATION_TYPE_FLAG_BA4)) return 1;
        return commit_turn_segment(state,invalid,selector,selected,speed,s);
    }
    else if(passage==RA2_CELL_CLOAKED_OBSTACLE) s->reveal_candidate(c);
    else if(passage==RA2_CELL_GATE) s->request_gate(c);
    else if(passage==RA2_CELL_TEMPORARY_OBSTACLE)
    {
        int bridge_layer=0;
        if(s->query(c,RA2_CONTINUATION_CELL_HAS_BRIDGE))
        {
            Ra2WorldPoint raw=s->raw_position(c);
            int32_t level=s->query(c,RA2_CONTINUATION_CELL_LEVEL);
            int32_t height=s->query(c,RA2_CONTINUATION_HEIGHT_PER_LEVEL);
            bridge_layer=absolute_difference(raw.z/height,level)>2;
        }
        s->notify_segment_cell(c,bridge_layer);
    }
    return 1;
}
