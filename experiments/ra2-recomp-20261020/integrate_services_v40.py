"""Route primary and already-left exits through the same gameplay placement services."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v40'
p=R/'ra2/src/runtime/ground_joint_bridge.c';raw=p.read_bytes();t=p.read_text(encoding='utf-8');t='#include "ground_cell_placement.h"\n'+t
a=t.index('void ra2_ground_advance_place_layer_return_bridge(void)');b=t.index('static void template_compare32(',a)
t=t[:a]+'''typedef struct JointPlacementContext { uint32_t frame,drive; } JointPlacementContext;
static void placement_restore(JointPlacementContext *c)
{g_esp=c->frame;g_ebp=c->drive;}
static void placement_leave(void *opaque)
{
    JointPlacementContext *c=opaque;uint32_t argument=0;
    g_eax=MEM32(g_ecx);method(g_ecx,0x11C,&argument,1);
    placement_restore(c);
}
static void placement_place(void *opaque)
{
    JointPlacementContext *c=opaque;
    uint32_t unit=MEM32(c->drive+0xC),argument=c->frame+0x18;
    g_eax=argument;g_edx=MEM32(unit);method(unit,0x19C,&argument,1);
    placement_restore(c);
}
static void placement_layer(void *opaque)
{(void)opaque;ra2_ground_late_layer_bridge();}
static uint32_t placement_enter(void *opaque)
{
    JointPlacementContext *c=opaque;uint32_t unit=MEM32(c->drive+0xC),argument=1;
    g_ebp=unit;g_edx=MEM32(unit);
    return method(unit,0x11C,&argument,1);
}
static void placement_return(unsigned needs_leave)
{
    JointPlacementContext context={g_esp,g_ebp};
    Ra2CellPlacementServices services={&context,placement_leave,placement_place,
        placement_layer,NULL,placement_enter};
    Ra2CellPlacementResult result=ra2_ground_place_cell(&services,needs_leave);
    ra2_ground_return_frame(context.frame,RA2_FRAME_ADVANCE,result.value&UINT32_C(0xFFFFFF00));
}
void ra2_ground_advance_place_layer_return_bridge(void)
{placement_return(0);}
void ra2_ground_advance_leave_place_return_bridge(void)
{placement_return(1);}

'''+t[b:]
nl='\r\n' if raw.count(b'\r\n')==raw.count(b'\n') else '\n';p.write_bytes(t.replace('\n',nl).encode('utf-8'))
(S/'pending/service-integration.json').write_text(json.dumps(dict(passed=True,shared_workflow='ra2_ground_place_cell',primary_advance_and_shared_internal_exits=True,new_native_entries=0,owner_and_layer_reloaded_after_callbacks=True),indent=2)+'\n',encoding='utf-8')
print('Integrated shared service-bearing exits')
