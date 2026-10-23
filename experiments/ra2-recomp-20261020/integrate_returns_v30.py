"""Share three service-bearing Prepare exits while preserving callback-visible writes."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
void ra2_ground_prepare_service_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(entry==0)
    {
        uint32_t first_owner=MEM32(drive+0xC);
        MEM32(drive+0x58)=g_edi;
        MEM32(first_owner+0x4D0)=g_edi;
        uint32_t current_owner=MEM32(drive+0xC),args[]={0,0};
        g_edx=MEM32(current_owner);
        result=method(current_owner,0x4C8,args,2)&UINT32_C(0xFFFFFF00);
    }
    else
    {
        uint32_t second=entry==1?g_ebx:MEM32(frame+0x64);
        uint32_t args[]={MEM32(frame+0x60),second,1};
        result=call(0x4A2670,drive,args,3);
    }
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';raw=p.read_bytes();assert b'\r\n' not in raw;t=raw.decode('utf-8')
t='extern void ra2_ground_prepare_service_return_bridge(unsigned entry);\n'+t
entries=[]
for entry,address in [(0,'004A46FE'),(1,'004A41AE'),(2,'004A41CC')]:
    marker='L_'+address+':\n';count=t.count(marker);assert count>0
    t=t.replace(marker,marker+f'''    /* Readable C: service call and shared return, retaining callback ordering. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_service_return_bridge({entry});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;
''')
    entries.append(dict(entry=entry,address=address,copies=count))
p.write_bytes(t.encode('utf-8'))
(S/'pending/service-exit-integration.json').write_text(json.dumps(dict(passed=True,entries=entries,unique_entries=3,copies=sum(e['copies'] for e in entries)),indent=2)+'\n',encoding='utf-8')
print('Integrated service-bearing exits',entries)
