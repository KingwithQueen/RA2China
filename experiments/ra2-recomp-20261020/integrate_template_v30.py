"""Share the selected normal/alternate template index with an internal continuation."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
p=R/'ra2/src/gameplay/ground_sampling_shared.h';t=p.read_text(encoding='utf-8')
t+='\nint32_t ra2_ground_template_index(Ra2SamplingTemplate selected, unsigned alternate);\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_sampling_shared.c';t=p.read_text(encoding='utf-8')
needle='    choice->table = alternate ? selected.alternate : selected.normal;';assert t.count(needle)==1
t=t.replace(needle,'    choice->table = ra2_ground_template_index(selected, alternate);')
t+='\nint32_t ra2_ground_template_index(Ra2SamplingTemplate selected, unsigned alternate)\n{ return alternate ? selected.alternate : selected.normal; }\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_overlap_bridge.c';t=p.read_text(encoding='utf-8')
t+='''
#include "ground_sampling_shared.h"
uint32_t ra2_ground_template_index_bridge(void)
{
    uint32_t scaled=g_eax*3u, table=0x7A0180u+scaled*4u;
    unsigned alternate=MEM8(g_ebp+0x60);
    Ra2SamplingTemplate selected={(int8_t)MEM8(table),(int8_t)MEM8(table+1),0};
    g_eax=(uint32_t)ra2_ground_template_index(selected,alternate);
    g_ecx=(scaled&UINT32_C(0xFFFFFF00))|alternate;
    g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=alternate<<24;g_flag_b=alternate<<24;g_flag_cf=0;
    return 0x4A2311;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';raw=p.read_bytes();assert b'\r\n' not in raw;t=raw.decode('utf-8')
t='extern unsigned ra2_ground_template_index_bridge(void);\n'+t
marker='L_004A1FBE:\n';count=t.count(marker);assert count>0
t=t.replace(marker,marker+'''    /* Readable C: selected template index, retaining AL-width test and signed table bytes. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_index_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A2311;
''');p.write_bytes(t.encode('utf-8'))
(S/'pending/template-remainder-integration.json').write_text(json.dumps(dict(passed=True,entry='004A1FBE',copies=count),indent=2)+'\n',encoding='utf-8')
print('Integrated template remainder index',count)
