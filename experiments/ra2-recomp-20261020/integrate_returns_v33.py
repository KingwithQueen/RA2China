"""Share cleanup-then-owner-service and sample-service return continuations."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');assert 'ra2_ground_prepare_following_return_bridge' not in t
t+='''
void ra2_ground_prepare_following_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(entry)
    {
        uint32_t args[]={frame+0x38,1};
        result=call(0x4A0BC0,drive,args,2)&UINT32_C(0xFFFFFF00);
    }
    else
    {
        /* 第一项服务完成后重读owner，不能沿用回调前的对象。 */
        call(0x4CD9B0,g_ecx,NULL,0);
        uint32_t unit=MEM32(drive+0xC),args[]={0,1};
        result=method(unit,0x414,args,2);
    }
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_prepare_following_return_bridge(unsigned entry);\n'+t;entries=[]
for n,a in enumerate(['004A456E','004A46BD']):
    m='L_'+a+':\n';c=t.count(m);assert c>0
    t=t.replace(m,m+f'''    /* 保留服务顺序、回调后的owner重读及原返回帧。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_following_return_bridge({n});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;
''');entries.append(dict(address=a,copies=c))
p.write_bytes(t.encode())
(S/'pending/following-service-integration.json').write_text(json.dumps(dict(passed=True,entries=entries),indent=2)+'\n',encoding='utf-8');print(entries)
