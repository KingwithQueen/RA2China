"""Share the enemy building/terrain/other-kind tail with its internal C copies."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
p=R/'ra2/src/gameplay/ground_enemy_kind.h';p.write_text('#pragma once\n#include "ground_objects.h"\nRa2ObjectPassageOutcome ra2_ground_classify_enemy_kind(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);\n',encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');needle='    int32_t kind=s->query(c,RA2_OBJECT_KIND);';assert t.count(needle)==1
t=t.replace('#include "ground_objects.h"','#include "ground_objects.h"\n#include "ground_enemy_kind.h"');t=t.replace(needle,'''    return ra2_ground_classify_enemy_kind(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_kind(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
'''+needle);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');needle='    else if(entry==2) outcome=';assert t.count(needle)==1
t=t.replace('#include "ground_objects.h"','#include "ground_objects.h"\n#include "ground_enemy_kind.h"');t=t.replace(needle,'    else if(entry==6) outcome=ra2_ground_classify_enemy_kind(&state,&services);\n'+needle);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';raw=p.read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');t=raw.decode('utf-8').replace('\r\n','\n')
marker='L_00703A12:\n';count=t.count(marker);assert count>0
t=t.replace(marker,marker+'''    /* Readable C: concrete enemy object kinds and selected terrain weapon. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t enemy_kind_resume_v30=ra2_ground_object_branch_bridge(6);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(enemy_kind_resume_v30==0x703B5A)goto L_00703B5A;
    goto L_007038EF;
''');p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
(S/'pending/enemy-kind-integration.json').write_text(json.dumps(dict(passed=True,entry='00703A12',copies=count),indent=2)+'\n',encoding='utf-8')
p=S/'objects_probe.c';t=p.read_text(encoding='utf-8').replace('0x7034BF,0x7035DF','0x7034BF,0x7035DF,0x703A12').replace('phase>5','phase>6');p.write_text(t,encoding='utf-8',newline='\n')
print('Integrated concrete enemy-kind continuation',count)
