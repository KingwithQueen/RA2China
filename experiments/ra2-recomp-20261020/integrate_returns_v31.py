"""Share Advance's service exits and its original still-alive continuation."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
uint32_t ra2_ground_advance_service_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(!entry)
    {
        uint32_t unit=MEM32(drive+0xC),args[]={0,1};
        result=method(unit,0x414,args,2);
        if(result&255u)
        {
            ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,(result&UINT32_C(0xFFFFFF00))|1u);
            return 0;
        }
    }
    uint32_t unit=MEM32(drive+0xC);
    g_edx=MEM32(unit);
    result=method(unit,0x490,NULL,0);
    if(result&255u)
    {
        ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,(result&UINT32_C(0xFFFFFF00))|1u);
        return 0;
    }
    unit=MEM32(drive+0xC);unsigned alive=MEM8(unit+0x7D);
    g_eax=unit;g_ecx=(g_ecx&UINT32_C(0xFFFFFF00))|alive;
    if(alive)
    {
        g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=alive<<24;g_flag_b=alive<<24;g_flag_cf=0;
        return 0x4A1FA1;
    }
    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,unit&UINT32_C(0xFFFFFF00));
    return 0;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');assert b'\r\n' not in p.read_bytes()
t='extern unsigned ra2_ground_advance_service_return_bridge(unsigned entry);\n'+t;entries=[]
for entry,address in [(0,'004A229C'),(1,'004A22BE')]:
    marker='L_'+address+':\n';count=t.count(marker);assert count==7
    t=t.replace(marker,marker+f'''    /* Readable C: service return or original alive-owner remainder continuation. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned advance_exit_v31_{entry}=ra2_ground_advance_service_return_bridge({entry});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(advance_exit_v31_{entry})goto L_004A1FA1; return;
''');entries.append(dict(entry=entry,address=address,copies=count))
p.write_bytes(t.encode('utf-8'))
(S/'pending/advance-service-integration.json').write_text(json.dumps(dict(passed=True,entries=entries,unique_entries=2,copies=14),indent=2)+'\n',encoding='utf-8')
print('Integrated Advance service exits',entries)
