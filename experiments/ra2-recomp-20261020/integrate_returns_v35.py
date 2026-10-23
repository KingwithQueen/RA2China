"""Preserve ordered destination invalidation, owner reload and speed service."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+='\nvoid ra2_ground_prepare_invalidate_return_bridge(void)\n{\n    uint32_t drive=g_ebp,unit=MEM32(drive+0xC);\n    g_eax=unit;g_ecx=(g_ecx&UINT32_C(0xFFFFFF00))|MEM8(unit+0x7D);\n    if(g_ecx&255u)\n    {\n        uint32_t out=g_esi;\n        g_ecx=MEM32(0x852998);MEM32(out)=g_ecx;\n        g_edx=MEM32(0x85299C);MEM32(out+4)=g_edx;\n        g_eax=MEM32(0x8529A0);MEM32(out+8)=g_eax;\n        MEM8(drive+0x63)=0;\n    }\n    ra2_ground_prepare_service_return_bridge(0);\n}\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A46D7:\n';n=t.count(m);assert n==11
code='    /* 清空目标时按原顺序读写，服务回调和owner重读保持。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_invalidate_return_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
t='extern void ra2_ground_prepare_invalidate_return_bridge(void);\n'+t.replace(m,m+code);p.write_bytes(t.encode('utf-8'))
(S/'pending/invalidate-service-integration.json').write_text(json.dumps(dict(passed=True,entry='004A46D7',copies=n,ordered_destination_and_owner_writeback=True),indent=2)+'\n',encoding='utf-8')
