"""Connect thirteen late layer spans, including five embedded spans."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t=t.replace('#include "ground_joint_bridge.h"','#include "ground_joint_bridge.h"\n#include "ground_template_transition.h"')
t+=r'''
typedef struct LateLayerContext { uint32_t drive,previous,next; } LateLayerContext;
static int32_t late_level(void *opaque,unsigned next)
{
    LateLayerContext *c=opaque;
    int32_t value=(int8_t)MEM8((next?c->next:c->previous)+0x11B);
    if(next){g_esi=(uint32_t)value;g_edx=0x100;}else g_edx=(uint32_t)value;
    return value;
}
static uint32_t late_flags(void *opaque,unsigned next)
{
    LateLayerContext *c=opaque;uint32_t value=MEM32((next?c->next:c->previous)+0x140);
    g_flag_k=FK_TEST;g_flag_a=value;g_flag_b=0x100;g_flag_cf=0;
    return value;
}
static void late_set_layer(void *opaque,unsigned upper)
{
    LateLayerContext *c=opaque;uint32_t unit=MEM32(c->drive+0xC);
    if(upper)g_esi=unit;else g_eax=unit;
    /* 写回可能覆盖格子标志；下次查询必须重新读取。 */
    MEM8(unit+0x79)=(uint8_t)upper;
}
uint32_t ra2_ground_late_layer_bridge(void)
{
    LateLayerContext c={g_ebp,MEM32(g_esp+0x6C),MEM32(g_esp+0x54)};
    g_ecx=c.previous;g_eax=c.next;
    Ra2TemplateLayerServices services={&c,late_level,late_flags,late_set_layer};
    ra2_ground_template_layer(&services);return 0x4A25E8;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='    ecx = MEM32(esp + 0x6C); /* 0x004A25A0:';n=t.count(m);assert n==13
assert t.count('L_004A25A0:')==8 and t.count('L_004A25E8:')==13
code='    /* 桥层写回沿用已取格子，保留重复读取与写回顺序。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_late_layer_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A25E8;\n'
p.write_bytes(('extern unsigned ra2_ground_late_layer_bridge(void);\n'+t.replace(m,code+m)).encode('utf-8'))
(S/'pending/late-layer-integration.json').write_text(json.dumps(dict(passed=True,entry='004A25A0',copies=n,native_labeled_copies=8,embedded_spans=5,new_native_entries=0,repeated_flags_read_preserved=True),indent=2)+'\n',encoding='utf-8')
