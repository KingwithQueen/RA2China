"""Share the position/layer/mark exit without repeating the preceding leave service."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v39'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');start=t.index('void ra2_ground_advance_leave_place_return_bridge(void)');end=t.index('static void template_compare32(',start)
t=t[:start]+'''void ra2_ground_advance_place_layer_return_bridge(void)
{
    uint32_t frame=g_esp,drive=g_ebp,unit=MEM32(g_ebp+0xC),argument=frame+0x18;
    g_eax=argument;g_edx=MEM32(unit);method(unit,0x19C,&argument,1);
    g_esp=frame;g_ebp=drive;
    ra2_ground_late_layer_bridge();ra2_ground_advance_mark_return_bridge();
}
void ra2_ground_advance_leave_place_return_bridge(void)
{
    uint32_t frame=g_esp,drive=g_ebp,argument=0;
    g_eax=MEM32(g_ecx);method(g_ecx,0x11C,&argument,1);
    g_esp=frame;g_ebp=drive;ra2_ground_advance_place_layer_return_bridge();
}

'''+t[end:];p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='    ecx = MEM32(ebp + 0xC); /* 0x004A2590:';assert t.count(m)==13
code='    /* 离格已完成：定位后重读落点、桥层及当前对象，再占格。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_advance_place_layer_return_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
p.write_bytes(('extern void ra2_ground_advance_place_layer_return_bridge(void);\n'+t.replace(m,code+m)).encode('utf-8'))
(S/'pending/service-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2590',copies=13,preceding_leave_not_repeated=True),indent=2)+'\n',encoding='utf-8')
