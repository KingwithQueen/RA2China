"""Share the internal table fallback with the main template selector."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
p=R/'ra2/src/gameplay/ground_template_table.h'
p.write_text('''#pragma once
#include "ground_template.h"
Ra2TemplateSelection ra2_ground_template_table(int32_t direction, int32_t next_direction,
    unsigned crushing, const Ra2TemplateServices *services);
''',encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_template.c';t=p.read_text(encoding='utf-8');t=t.replace('#include "ground_template.h"','#include "ground_template.h"\n#include "ground_template_table.h"')
needle='    int32_t selector = signed_bits((uint32_t)next_direction + (uint32_t)direction * 8u);'
assert t.count(needle)==1
t=t.replace(needle,'''    return ra2_ground_template_table(direction, next_direction, crushing, services);
}

Ra2TemplateSelection ra2_ground_template_table(int32_t direction, int32_t next_direction,
    unsigned crushing, const Ra2TemplateServices *services)
{
'''+needle)
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_overlap_bridge.c';t=p.read_text(encoding='utf-8');t+='''
/* 4A3FE3 internal continuation: neighbor crushing was already resolved. */
#include "ground_template_table.h"
static uint8_t table_byte(void *opaque, int32_t selector, Ra2TemplateByte field)
{
    (void)opaque;
    return MEM8(0x7A0180u+(uint32_t)selector*12u+(field==RA2_TEMPLATE_FLAGS?8u:0u));
}
uint32_t ra2_ground_template_table_bridge(void)
{
    uint32_t selector=g_esi+g_ebx*8u;
    unsigned fallback=!table_byte(NULL,(int32_t)selector,RA2_TEMPLATE_ENTRY_TAG);
    Ra2TemplateServices services={NULL,NULL,table_byte};
    Ra2TemplateSelection result=ra2_ground_template_table((int32_t)g_ebx,(int32_t)g_esi,
        MEM8(g_ebp+0x64),&services);
    MEM8(g_ebp+0x60)=0;
    MEM32(g_ebp+0x58)=(uint32_t)result.selector;
    g_ecx=selector*3u;
    if(fallback)g_edx=g_ebx*9u;
    g_eax=(uint32_t)result.selector*3u;
    g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=(uint32_t)result.flags<<24;
    g_flag_b=8u<<24;g_flag_cf=0;
    return result.flags&8u?0x4A4015:0x4A45B7;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
# Declare beside existing overlap ABI declarations without touching prior headers.
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';data=p.read_bytes();assert b'\r\n' not in data;t=data.decode('utf-8')
t='extern unsigned ra2_ground_template_table_bridge(void);\n'+t
marker='L_004A3FE3:\n';count=t.count(marker);assert count>0
t=t.replace(marker,marker+'''    /* 可读 C：内部模板表选择与直行回退。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t table_resume_v29=ra2_ground_template_table_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(table_resume_v29==0x4A4015)goto L_004A4015;
    goto L_004A45B7;
''');p.write_bytes(t.encode('utf-8'))
(S/'pending/template-integration.json').write_text(json.dumps(dict(passed=True,entry='004A3FE3',copies=count,main_and_internal_share_table=True),indent=2)+'\n',encoding='utf-8')
print('Integrated template table',count)
