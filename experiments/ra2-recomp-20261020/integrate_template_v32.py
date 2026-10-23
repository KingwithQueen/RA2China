"""Recover both destination-coordinate continuations without removing raw labels."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
uint32_t ra2_ground_template_destination_bridge(unsigned alternate)
{
    uint32_t frame=g_esp,drive=g_ebp,offset=alternate?0x24u:0x74u;
    uint32_t x=MEM32(frame+offset),y=MEM32(frame+offset+4),z=MEM32(frame+offset+8);
    MEM32(frame+0x18)=x;MEM32(frame+0x1C)=y;MEM32(frame+0x20)=z;
    MEM32(frame+0xD0)=x;MEM32(frame+0xD4)=y;MEM32(frame+0xD8)=z;
    uint32_t pointer=frame+0xD0;
    uint32_t result=call(0x548000,0x8324E0,&pointer,1);
    /* The map service may replace the drive's owner. Read it after the call. */
    g_ecx=MEM32(drive+0xC);MEM32(frame+0x54)=result;
    g_eax=result;g_edx=g_ecx+0x88u;g_ebx=z;
    return 0x4A2528;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');assert b'\r\n' not in p.read_bytes()
t='extern unsigned ra2_ground_template_destination_bridge(unsigned alternate);\n'+t
import re
parts=re.split(r'(?=^void sub_)',t,flags=re.M);entries=[]
for n,a in enumerate(['004A24C6','004A24DC']):
    m='L_'+a+':\n';count=skipped=0
    for j,body in enumerate(parts):
        if m not in body:continue
        if 'L_004A2528:' not in body:skipped+=1;continue
        count+=body.count(m)
        parts[j]=body.replace(m,m+f"    /* Readable C: template destination and map service. */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_destination_bridge({n});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A2528;\n")
    assert count==8 and skipped==4,(count,skipped)
    entries.append(dict(address=a,copies=count,unintercepted_without_continuation_label=skipped))
p.write_bytes(''.join(parts).encode('utf-8'))
(S/'pending/destination-integration.json').write_text(json.dumps(dict(passed=True,entries=entries),indent=2)+'\n',encoding='utf-8')
print(entries)
