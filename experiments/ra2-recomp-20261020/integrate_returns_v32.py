"""Recover the two stop-service exits before their already shared return frames."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
void ra2_ground_prepare_stop_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,args[]={0,1};
    g_ebp=MEM32(g_ebp+0xC);
    uint32_t result=method(g_ebp,entry?0x410u:0x414u,args,2);
    if(entry)
        ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
    else
        /* Re-read the output pointer after the callback; saved slots can alias it. */
        ra2_ground_prepare_written_return_bridge(0);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_prepare_stop_return_bridge(unsigned entry);\n'+t;entries=[]
for n,a in enumerate(['004A26EC','004A2916']):
    m='L_'+a+':\n';c=t.count(m);assert c>0
    t=t.replace(m,m+f'''    /* Readable C: stop service and its ordered shared output/return frame. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_stop_return_bridge({n});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;
''');entries.append(dict(address=a,copies=c))
p.write_bytes(t.encode('utf-8'))
(S/'pending/prepare-stop-integration.json').write_text(json.dumps(dict(passed=True,entries=entries),indent=2)+'\n',encoding='utf-8');print(entries)
