"""Share the remaining direct stop service using the incoming object register."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+='''
void ra2_ground_prepare_owner_stop_return_bridge(void)
{
    uint32_t frame=g_esp,unit=g_ecx,args[]={0,1};
    uint32_t result=method(unit,0x410,args,2);
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A449B:\n';n=t.count(m);assert n==7
t='extern void ra2_ground_prepare_owner_stop_return_bridge(void);\n'+t.replace(m,m+'''    /* 服务对象来自ECX；保留回调写回、EAX高位与返回帧。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_owner_stop_return_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;
''');p.write_bytes(t.encode('utf-8'))
(S/'pending/owner-stop-integration.json').write_text(json.dumps(dict(passed=True,entry='004A449B',copies=n,object_source='incoming ECX'),indent=2)+'\n',encoding='utf-8')
