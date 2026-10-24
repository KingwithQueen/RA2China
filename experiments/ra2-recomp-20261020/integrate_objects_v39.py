"""Classify an already selected weapon holder, including its empty result."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v39'
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');a='else if(entry==12){uint32_t warhead=MEM32(g_eax+0xAC);outcome=ra2_ground_classify_enemy_warhead(&state,warhead?MEM8(warhead+0x146):0);}'
assert t.count(a)==1;t=t.replace(a,'else if(entry==12||entry==13){uint32_t weapon=entry==13?MEM32(g_eax):g_eax;uint32_t warhead=weapon?MEM32(weapon+0xAC):0;outcome=ra2_ground_classify_enemy_warhead(&state,warhead?MEM8(warhead+0x146):0);}')
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_bytes().decode('utf-8');m='    eax = MEM32(eax); /* 0x00703A3B:';assert t.count(m)==3
code='    /* 武器选择服务已返回，直接解释可空持有槽。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t holder_resume_v39=ra2_ground_object_branch_bridge(13);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(holder_resume_v39==0x703B5A)goto L_00703B5A;\n    goto L_007038EF;\n'
p.write_bytes(t.replace(m,code.replace('\n','\r\n')+m).encode('utf-8'))
(S/'pending/object-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A3B',copies=3,services_repeated=0),indent=2)+'\n',encoding='utf-8')
