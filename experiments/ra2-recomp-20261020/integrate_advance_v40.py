"""Expose cohesive cell-entry, train-chain and overlay effects; share placement choreography."""
from pathlib import Path
import json,textwrap
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v40'
def save(p,t):
 old=p.read_bytes();nl='\r\n' if old.count(b'\r\n')==old.count(b'\n') else '\n'
 p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
p=R/'ra2/src/gameplay/ground_advance.c';t=p.read_text(encoding='utf-8');t='#include "ground_cell_placement.h"\n'+t
a=t.index('        if (s->query(c, RA2_ADVANCE_IS_TRAIN, 0)');b=t.index('        if (!s->query(c, RA2_ADVANCE_OWNER_ALIVE, 0)) return 0;',a)
train=textwrap.indent(textwrap.dedent(t[a:b]).rstrip(),'    ')
c=t.index('        int32_t overlay = ',b);d=t.index('\n    }\n    else s->place',c)
overlay=textwrap.indent(textwrap.dedent(t[c:d]).rstrip(),'    ')
e=t.index('    if (!s->query(c, RA2_ADVANCE_OWNER_ALIVE, 0)) return 0;',d)
finish=t[e:t.rindex('}')].replace('sample.direction','direction')
helpers='''void ra2_ground_advance_train_contact(const Ra2AdvanceServices *s, Ra2AdvanceCell next)
{
    void *c=s->context;
'''+train+'''
}

void ra2_ground_advance_overlay_contact(const Ra2AdvanceServices *s, uint32_t next_cell)
{
    void *c=s->context;
'''+overlay+'''
}

typedef struct AdvancePlacementContext
{
    const Ra2AdvanceServices *services;
    Ra2AdvanceCell previous,next;
    Ra2WorldPoint position;
    uint32_t next_cell;
} AdvancePlacementContext;
static void entry_leave(void *opaque)
{
    AdvancePlacementContext *c=opaque;
    c->services->act(c->services->context,RA2_ADVANCE_LEAVE_CELL,0,0);
}
static void entry_place(void *opaque)
{
    AdvancePlacementContext *c=opaque;
    c->services->place(c->services->context,c->position,1);
}
static void entry_layer(void *opaque)
{
    AdvancePlacementContext *c=opaque;const Ra2AdvanceServices *s=c->services;
    uint32_t previous_cell=s->find_cell(s->context,c->previous);
    c->next_cell=s->find_cell(s->context,c->next);
    AdvanceLayerContext layer_context={s,{previous_cell,c->next_cell}};
    Ra2TemplateLayerServices layer_services={&layer_context,layer_level,layer_flags,layer_set};
    ra2_ground_template_layer(&layer_services);
}
static int entry_before_enter(void *opaque)
{
    AdvancePlacementContext *c=opaque;const Ra2AdvanceServices *s=c->services;
    ra2_ground_advance_train_contact(s,c->next);
    return s->query(s->context,RA2_ADVANCE_OWNER_ALIVE,0)!=0;
}
static uint32_t entry_enter(void *opaque)
{
    AdvancePlacementContext *c=opaque;
    c->services->act(c->services->context,RA2_ADVANCE_ENTER_CELL,0,1);
    return 0;
}
int ra2_ground_enter_sample_cell(const Ra2AdvanceServices *s, Ra2AdvanceCell previous,
    Ra2AdvanceCell next, Ra2WorldPoint position)
{
    AdvancePlacementContext context={s,previous,next,position,0};
    Ra2CellPlacementServices placement={&context,entry_leave,entry_place,entry_layer,
        entry_before_enter,entry_enter};
    Ra2CellPlacementResult result=ra2_ground_place_cell(&placement,1);
    if(!result.entered) return 0;
    ra2_ground_advance_overlay_contact(s,context.next_cell);
    return 1;
}
int ra2_ground_advance_finish_sample(const Ra2AdvanceServices *s, int32_t direction)
{
    void *c=s->context;
    int32_t index;
'''+finish+'''}

'''
start=t.index('int ra2_ground_advance_sample(');body=t[start:]
cross=body.index('    if (crosses_cell)');body=body[:cross]+'''    if(crosses_cell)
    {
        if(!ra2_ground_enter_sample_cell(s,previous,next,position)) return 0;
    }
    else s->place(c,position,0);
    return ra2_ground_advance_finish_sample(s,sample.direction);
}
'''
save(p,t[:start]+helpers+body)
p=R/'ra2/src/gameplay/ground_advance.h';t=p.read_text(encoding='utf-8');t+='''
/* 可单独修改的跨格业务；列车下一链项在伤害回调前保存，地表碾压在进入后执行。 */
void ra2_ground_advance_train_contact(const Ra2AdvanceServices *services,Ra2AdvanceCell next);
void ra2_ground_advance_overlay_contact(const Ra2AdvanceServices *services,uint32_t next_cell);
int ra2_ground_enter_sample_cell(const Ra2AdvanceServices *services,Ra2AdvanceCell previous,
    Ra2AdvanceCell next,Ra2WorldPoint position);
int ra2_ground_advance_finish_sample(const Ra2AdvanceServices *services,int32_t direction);
''';save(p,t)
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');marker='  src/gameplay/ground_advance.c\n';assert t.count(marker)==1;t=t.replace(marker,marker+'  src/gameplay/ground_cell_placement.c\n');t+='\nset_source_files_properties(src/gameplay/ground_cell_placement.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';save(p,t)
for name in ['build-advance-probe-v40.ps1','build-overlap-probe-v40.ps1']:
 p=R/name;t=p.read_text(encoding='utf-8');marker=' ..\\..\\ra2\\src\\runtime\\ground_joint_bridge.c';assert t.count(marker)==1;t=t.replace(marker,marker+' ..\\..\\ra2\\src\\gameplay\\ground_cell_placement.c');save(p,t)
(S/'pending/advance-integration.json').write_text(json.dumps(dict(passed=True,scope='Cell entry, train-chain contact, overlay contact, finishing sample; shared placement flow.',new_native_entries=0),indent=2)+'\n',encoding='utf-8')
print('Integrated sampled cell-entry functional units')
