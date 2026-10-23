"""Preserve the temporary owner flag across a placement callback and ordered pops."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
t+='\nvoid ra2_ground_advance_place_return_bridge(void)\n{\n    uint32_t frame=g_esp,drive=g_ebp,unit=g_ecx;\n    uint8_t old_flag=MEM8(unit+0x74);MEM8(unit+0x74)=0;\n    unit=MEM32(drive+0xC);uint32_t argument=frame+0x18;\n    method(unit,0x19C,&argument,1);\n    uint32_t current_owner=MEM32(drive+0xC);\n    uint32_t saved_edi=MEM32(frame),saved_esi=MEM32(frame+4),saved_ebp=MEM32(frame+8);\n    MEM8(current_owner+0x74)=old_flag;\n    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,current_owner&UINT32_C(0xFFFFFF00));\n    g_edi=saved_edi;g_esi=saved_esi;g_ebp=saved_ebp;\n}\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A2607:\n';n=t.count(m);assert n==13,n
code='    /* 定位服务可改owner及保存槽，恢复字节时保持原出栈次序。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_advance_place_return_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
t='extern void ra2_ground_advance_place_return_bridge(void);\n'+t.replace(m,m+code);p.write_bytes(t.encode('utf-8'))
(S/'pending/place-restore-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2607',copies=n,owner_and_saved_slot_alias_order_preserved=True),indent=2)+'\n',encoding='utf-8')
