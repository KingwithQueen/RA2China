"""Preserve the mark-enter callback result and return frame."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+='\nvoid ra2_ground_advance_mark_return_bridge(void)\n{\n    uint32_t frame=g_esp,unit=MEM32(g_ebp+0xC),argument=1;\n    g_ebp=unit;g_edx=MEM32(unit);\n    uint32_t result=method(unit,0x11C,&argument,1);\n    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,result&UINT32_C(0xFFFFFF00));\n}\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A25E8:\n';n=t.count(m);assert n==13
code='    /* 进入服务允许改写保存槽；完成后按原顺序出栈。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_advance_mark_return_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
p.write_bytes(('extern void ra2_ground_advance_mark_return_bridge(void);\n'+t.replace(m,m+code)).encode('utf-8'))
(S/'pending/mark-enter-integration.json').write_text(json.dumps(dict(passed=True,entry='004A25E8',copies=n,callback_saved_slots_preserved=True),indent=2)+'\n',encoding='utf-8')
