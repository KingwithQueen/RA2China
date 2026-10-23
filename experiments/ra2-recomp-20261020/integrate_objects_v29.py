"""Share the building-flag continuation after the footprint gate."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
(R/'ra2/src/gameplay/ground_building_flags.h').write_text('''#pragma once
#include "ground_objects.h"
Ra2ObjectPassageOutcome ra2_ground_filter_building_flags(const Ra2ObjectPassageServices *services);
''',encoding='utf-8')
p=R/'ra2/src/gameplay/ground_objects.c';t=p.read_text(encoding='utf-8');t=t.replace('#include "ground_object_kind.h"','#include "ground_object_kind.h"\n#include "ground_building_flags.h"')
marker='    if(s->query(c,RA2_OBJECT_BUILDING_IGNORED)) return RA2_OBJECT_SKIP;';assert t.count(marker)==1
t=t.replace(marker,'''    return ra2_ground_filter_building_flags(s);
}
Ra2ObjectPassageOutcome ra2_ground_filter_building_flags(const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
'''+marker);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8');t=t.replace('#include "ground_object_kind.h"','#include "ground_object_kind.h"\n#include "ground_building_flags.h"')
t=t.replace('    else if(entry==1)', '    else if(entry==5) outcome=ra2_ground_filter_building_flags(&services);\n    else if(entry==1)');p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';data=p.read_bytes();assert data.count(b'\n')==data.count(b'\r\n');t=data.decode().replace('\r\n','\n');marker='L_007035DF:\n';count=t.count(marker);assert count>0
t=t.replace(marker,marker+'''    /* 可读 C：建筑标志内部接续，与完整建筑筛选共享。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t building_resume_v29=ra2_ground_object_branch_bridge(5);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(building_resume_v29==0x703B5A)goto L_00703B5A;
    if(building_resume_v29==0x7038FD)goto L_007038FD;
    goto L_00703693;
''');p.write_bytes(t.replace('\n','\r\n').encode())
(S/'pending/object-kind-integration.json').write_text(json.dumps(dict(passed=True,entry='007035DF',copies=count,main_and_internal_share_flags=True),indent=2)+'\n',encoding='utf-8')
print('Integrated building continuation',count)
