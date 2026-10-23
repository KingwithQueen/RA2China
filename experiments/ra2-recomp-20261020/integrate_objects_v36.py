"""Classify a confirmed enemy building without another kind query."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
p=R/'ra2/src/gameplay/ground_enemy_kind.h';t=p.read_text(encoding='utf-8');t+='\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_building(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');a='if(kind==6 && s->query(c,RA2_OBJECT_BUILDING_FLAG_1350)) return RA2_OBJECT_BLOCKED;';assert t.count(a)==1;t=t.replace(a,'if(kind==6) return ra2_ground_classify_enemy_building(state,s);')
t+='\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_building(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)\n{\n    if(s->query(s->context,RA2_OBJECT_BUILDING_FLAG_1350)) return RA2_OBJECT_BLOCKED;\n    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;\n}\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');a='else if(entry==9)';assert t.count(a)==1;t=t.replace(a,'else if(entry==10) outcome=ra2_ground_classify_enemy_building(&state,&services);\n    '+a);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_bytes().decode('utf-8');m='L_00703A7F:\r\n';n=t.count(m);assert n==3,n
code='    /* 建筑类型已确认，只读取当前建筑通行标志。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t building_resume_v36=ra2_ground_object_branch_bridge(10);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(building_resume_v36==0x703B5A)goto L_00703B5A;\n    goto L_007038EF;\n'
t=t.replace(m,m+code.replace('\n','\r\n'));p.write_bytes(t.encode('utf-8'))
(S/'pending/building-gate-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A7F',copies=n,repeated_kind_query=False),indent=2)+'\n',encoding='utf-8')
