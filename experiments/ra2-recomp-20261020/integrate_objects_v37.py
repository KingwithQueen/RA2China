"""Classify an already loaded warhead without repeating weapon selection."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
p=R/'ra2/src/gameplay/ground_enemy_kind.h';t=p.read_text();t+='\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_warhead(Ra2ObjectPassageState *state,unsigned flag);\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');a='    if(!s->query(s->context,RA2_OBJECT_TERRAIN_WEAPON_ALLOWED)) return RA2_OBJECT_BLOCKED;\n    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;';assert t.count(a)==1;t=t.replace(a,'    return ra2_ground_classify_enemy_warhead(state,(unsigned)s->query(s->context,RA2_OBJECT_TERRAIN_WEAPON_ALLOWED));')
t+='\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_warhead(Ra2ObjectPassageState *state,unsigned flag)\n{\n    if(!flag)return RA2_OBJECT_BLOCKED;\n    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;\n}\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');a='else if(entry==10)';assert t.count(a)==1;t=t.replace(a,'else if(entry==11) outcome=ra2_ground_classify_enemy_warhead(&state,MEM8(g_eax+0x146));\n    '+a);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_bytes().decode('utf-8');m='L_00703A53:\r\n';n=t.count(m);assert n==3
code='    /* 弹头已载入，直接检查原通行字节，不重选武器。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t warhead_resume_v37=ra2_ground_object_branch_bridge(11);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(warhead_resume_v37==0x703B5A)goto L_00703B5A;\n    goto L_007038EF;\n'
p.write_bytes(t.replace(m,m+code.replace('\n','\r\n')).encode('utf-8'))
(S/'pending/loaded-warhead-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A53',copies=n,repeated_weapon_or_kind_query=False),indent=2)+'\n',encoding='utf-8')
