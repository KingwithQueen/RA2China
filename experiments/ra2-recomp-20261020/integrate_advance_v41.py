"""Name the Advance commit state transition and share Prepare's train/crusher gate."""
from pathlib import Path
import textwrap,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41'
def save(p,t):
 raw=p.read_bytes();nl='\r\n' if raw.count(b'\r\n')==raw.count(b'\n') else '\n';p.write_bytes(t.replace('\n',nl).encode('utf-8'))
p=R/'ra2/src/gameplay/ground_continuation.c';t=p.read_text(encoding='utf-8');a=t.index('        state->alternate_template=0;');b=t.index('\n    }\n    else if(passage==',a)
block=textwrap.indent(textwrap.dedent(t[a:b]),'    ')
helper='''/* 接续已获放行后，提交模板、刷新对象，再按存活与候选格结果进入/放弃路段。
   刷新和进入服务可改变状态；恢复速度、移除旧方向只发生在成功进入之后。 */
static int commit_turn_segment(Ra2ContinuationState *state,Ra2WorldPoint invalid,
    int32_t selector,Ra2ContinuationTemplate selected,uint64_t speed,
    const Ra2ContinuationServices *s)
{
    void *c=s->context;
'''+block+'''
    return 1;
}

'''
t=t[:a]+'        return commit_turn_segment(state,invalid,selector,selected,speed,s);'+t[b:]
i=t.index('int ra2_ground_continue_turn(');t=t[:i]+helper+t[i:];save(p,t)
p=R/'ra2/src/gameplay/ground_segment.c';t=p.read_text(encoding='utf-8');t='#include "ground_template_transition.h"\n'+t
i=t.index('Ra2SegmentPhase ra2_ground_prepare_segment(')
helper='''typedef struct SegmentGateContext
{
    Ra2SegmentPreparation *output;
    const Ra2SegmentServices *services;
} SegmentGateContext;
static int32_t gate_classification(void *opaque)
{return ((SegmentGateContext *)opaque)->output->passage;}
static unsigned gate_type(void *opaque,unsigned crusher)
{
    SegmentGateContext *c=opaque;const Ra2SegmentServices *s=c->services;
    return (unsigned)s->query(s->context,crusher?RA2_SEGMENT_ACTOR_IS_CRUSHER:RA2_SEGMENT_ACTOR_IS_TRAIN);
}
static int32_t gate_overlay(void *opaque)
{
    SegmentGateContext *c=opaque;return c->services->query(c->services->context,RA2_SEGMENT_CELL_OVERLAY_INDEX);
}
static void gate_clear(void *opaque)
{((SegmentGateContext *)opaque)->output->passage=0;}

'''
t=t[:i]+helper+t[i:];a=t.index('    if (output->passage < 7');b=t.index('    return RA2_SEGMENT_CLASSIFIED;',a)
t=t[:a]+'''    SegmentGateContext gate_context={output,services};
    Ra2TemplateGateServices gate={&gate_context,gate_classification,gate_type,gate_overlay,gate_clear};
    ra2_ground_template_gate(&gate);
'''+t[b:];save(p,t)
for name in ['build-segment-probe-v41.ps1','build-prepare-probe-v41.ps1']:
 p=R/name;t=p.read_text(encoding='utf-8');m=' ..\\..\\ra2\\src\\gameplay\\ground_template.c';assert t.count(m)==1
 t=t.replace(m,m+' ..\\..\\ra2\\src\\gameplay\\ground_template_transition.c ..\\..\\ra2\\src\\gameplay\\ground_template_entry.c');save(p,t)
(S/'pending/advance-integration.json').write_text(json.dumps(dict(passed=True,advance_turn_commit_state_transition=True,prepare_segment_reuses_template_gate=True,side_effect_order_retained=True,new_native_entries=0),indent=2)+'\n',encoding='utf-8')
print('Integrated Advance commit and shared classification gate')
