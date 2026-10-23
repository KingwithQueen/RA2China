"""Share the weapon/train gate with the concrete enemy contact classifier."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
p=R/'ra2/src/gameplay/ground_enemy_contact.h';t=p.read_text(encoding='utf-8');t+='Ra2ObjectPassageOutcome ra2_ground_classify_enemy_weapon(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);\n';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');m='    if(!s->query(c,RA2_OBJECT_HAS_WEAPON_ZERO)';assert t.count(m)==1
t=t.replace(m,'''    return ra2_ground_classify_enemy_weapon(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_weapon(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
'''+m);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');m='    else if(entry==7)';assert t.count(m)==1;t=t.replace(m,'    else if(entry==8) outcome=ra2_ground_classify_enemy_weapon(&state,&services);\n'+m);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_text(encoding='utf-8');m='L_007039EC:\n';n=t.count(m);assert n==3
t=t.replace(m,m+'''    /* 武器查询之后按原顺序读取列车属性，再分类具体对象。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned weapon_resume_v34=ra2_ground_object_branch_bridge(8);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(weapon_resume_v34==0x703B5A)goto L_00703B5A;
    goto L_007038EF;
''');p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
(S/'pending/enemy-weapon-integration.json').write_text(json.dumps(dict(passed=True,entry='007039EC',copies=n),indent=2)+'\n',encoding='utf-8')
