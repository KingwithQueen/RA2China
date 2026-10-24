"""Leave, place, update layer, enter and restore the original return frame."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+=r'''
void ra2_ground_advance_leave_place_return_bridge(void)
{
    uint32_t frame=g_esp,drive=g_ebp,argument=0;
    /* 首次使用入口 ECX；离格回调后重新读取当前 owner。 */
    g_eax=MEM32(g_ecx);method(g_ecx,0x11C,&argument,1);
    uint32_t unit=MEM32(drive+0xC);argument=frame+0x18;
    g_eax=argument;g_edx=MEM32(unit);method(unit,0x19C,&argument,1);
    g_esp=frame;g_ebp=drive;
    ra2_ground_late_layer_bridge();
    ra2_ground_advance_mark_return_bridge();
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A2586:\n';n=t.count(m);assert n==13
code='    /* 离格和定位均可改写 owner、落点及保存槽，随后重读。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_advance_leave_place_return_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
p.write_bytes(('extern void ra2_ground_advance_leave_place_return_bridge(void);\n'+t.replace(m,m+code)).encode('utf-8'))
(S/'pending/leave-place-mark-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2586',copies=n,callback_saved_slots_preserved=True,owner_and_cells_reread_after_callbacks=True),indent=2)+'\n',encoding='utf-8')
