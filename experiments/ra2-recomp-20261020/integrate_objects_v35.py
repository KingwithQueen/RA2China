"""Share terrain weapon selection without repeating the object's kind query."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
p=R/'ra2/src/gameplay/ground_enemy_kind.h';t=p.read_text(encoding='utf-8');t+='\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_terrain(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');a='if(kind==36 && !s->query(c,RA2_OBJECT_TERRAIN_WEAPON_ALLOWED)) return RA2_OBJECT_BLOCKED;';assert t.count(a)==1
t=t.replace(a,'if(kind==36) return ra2_ground_classify_enemy_terrain(state,s);')
a='Ra2ObjectPassageOutcome ra2_ground_classify_stationary_ally('
b='Ra2ObjectPassageOutcome ra2_ground_classify_enemy_terrain(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)\n{\n    if(!s->query(s->context,RA2_OBJECT_TERRAIN_WEAPON_ALLOWED)) return RA2_OBJECT_BLOCKED;\n    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;\n}\n'
assert t.count(a)==1;t=t.replace(a,b+a);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');a='else if(entry==8)';assert t.count(a)==1;t=t.replace(a,'else if(entry==9) outcome=ra2_ground_classify_enemy_terrain(&state,&services);\n    '+a);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_bytes().decode('utf-8');m='L_00703A23:\r\n';n=t.count(m);assert n==3
code='    /* 地形对象已确认，武器选择与弹头门槛保留原服务顺序。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t terrain_resume_v35=ra2_ground_object_branch_bridge(9);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(terrain_resume_v35==0x703B5A)goto L_00703B5A;\n    goto L_007038EF;\n'
t=t.replace(m,m+code.replace('\n','\r\n'));p.write_bytes(t.encode('utf-8'))
(S/'pending/terrain-weapon-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A23',copies=n,repeated_kind_query=False),indent=2)+'\n',encoding='utf-8')
