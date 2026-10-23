"""Import the remainder sample anchor in the original load/store order."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=R/'ra2/src/runtime/ground_overlap_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
uint32_t ra2_ground_sample_anchor_bridge(void)
{
    uint32_t position=MEM32(g_ebp+0xC)+0x88u;
    /* Keep each load adjacent to its store: the sample can alias the saved anchor. */
    MEM32(g_esp+0x80)=MEM32(position);
    MEM32(g_esp+0x84)=MEM32(position+4);
    MEM32(g_esp+0x88)=MEM32(position+8);
    g_ecx=MEM32(g_ecx+8);
    MEM32(g_esp+0x34)=g_ecx;
    g_eax=position;
    g_esi=MEM32(position);g_ebx=MEM32(position+4);g_edx=MEM32(position+8);
    g_flag_k=FK_ADD;g_flag_a=position-0x88u;g_flag_b=0x88u;
    g_flag_cf=position<position-0x88u;
    return 0x4A237D;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');assert b'\r\n' not in p.read_bytes()
t='extern unsigned ra2_ground_sample_anchor_bridge(void);\n'+t
marker='L_004A2347:\n';count=t.count(marker);assert count==12
t=t.replace(marker,marker+'''    /* Readable C: owner anchor and sample direction, retaining ordered aliasing. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_sample_anchor_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A237D;
''');p.write_bytes(t.encode('utf-8'))
(S/'pending/sample-anchor-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2347',copies=count),indent=2)+'\n',encoding='utf-8')
print('Integrated remainder anchor',count)
