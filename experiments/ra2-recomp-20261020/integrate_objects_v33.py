"""Share concrete enemy contact services after the independently classified cloak."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
p=R/'ra2/src/gameplay/ground_enemy_contact.h';assert not p.exists()
p.write_text('#pragma once\n#include "ground_objects.h"\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_contact(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);\n',encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');m='    if((s->query(c,RA2_OBJECT_OWNER_CRUSHER)';assert t.count(m)==1
t=t.replace('#include "ground_objects.h"','#include "ground_objects.h"\n#include "ground_enemy_contact.h"',1)
t=t.replace(m,'''    return ra2_ground_classify_enemy_contact(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_contact(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
'''+m,1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8').replace('#include "ground_objects.h"','#include "ground_objects.h"\n#include "ground_enemy_contact.h"',1)
t=t.replace('    else if(entry==6)', '    else if(entry==7) outcome=ra2_ground_classify_enemy_contact(&state,&services);\n    else if(entry==6)',1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';raw=p.read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');t=raw.decode().replace('\r\n','\n')
m='L_0070399A:\n';c=t.count(m);assert c==3
t=t.replace(m,m+'''    /* 敌方具体对象：碾压能力、可碾压属性、阵营重查与武器门槛。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned enemy_contact_v33=ra2_ground_object_branch_bridge(7);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(enemy_contact_v33==0x703B5A)goto L_00703B5A;
    goto L_007038EF;
''');p.write_bytes(t.replace('\n','\r\n').encode())
(S/'pending/enemy-contact-integration.json').write_text(json.dumps(dict(passed=True,entry='0070399A',copies=c),indent=2)+'\n',encoding='utf-8');print('Integrated enemy contact',c)
