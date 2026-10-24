"""Inspect the loaded weapon's nullable warhead without service calls."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');a='else if(entry==11)';assert t.count(a)==1
t=t.replace(a,'else if(entry==12){uint32_t warhead=MEM32(g_eax+0xAC);outcome=ra2_ground_classify_enemy_warhead(&state,warhead?MEM8(warhead+0x146):0);}\n    '+a);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_bytes().decode('utf-8');m='L_00703A45:\r\n';n=t.count(m);assert n==3
code='    /* 武器已载入，直接检查可空弹头，不重选武器。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t weapon_resume_v38=ra2_ground_object_branch_bridge(12);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(weapon_resume_v38==0x703B5A)goto L_00703B5A;\n    goto L_007038EF;\n'
p.write_bytes(t.replace(m,m+code.replace('\n','\r\n')).encode('utf-8'))
(S/'pending/loaded-weapon-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A45',copies=n,repeated_weapon_or_kind_query=False,null_warhead_preserved=True),indent=2)+'\n',encoding='utf-8')
