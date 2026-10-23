"""Share the allied relation continuation, retaining geometric service order."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
(R/'ra2/src/gameplay/ground_allied_relation.h').write_text('#pragma once\n#include "ground_allied.h"\nRa2AlliedOutcome ra2_ground_classify_allied_relation(int moving,int32_t *passage,const Ra2AlliedServices *services);\n',encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_allied.c';t=p.read_text(encoding='utf-8').replace('#include "ground_allied.h"','#include "ground_allied.h"\n#include "ground_allied_relation.h"',1)
needle='    if (!s->query(c, RA2_ALLIED_OBJECT_IS_ALLIED))';assert t.count(needle)==1
t=t.replace(needle,'''    return ra2_ground_classify_allied_relation(moving,passage,s);
}

Ra2AlliedOutcome ra2_ground_classify_allied_relation(int moving,int32_t *passage,const Ra2AlliedServices *s)
{
    void *c=s->context;
'''+needle,1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_allied_bridge.c';t=p.read_text(encoding='utf-8').replace('#include "ground_allied.h"','#include "ground_allied.h"\n#include "ground_allied_relation.h"',1)
t+='''
uint32_t ra2_ground_allied_relation_bridge(void)
{
    AlliedContext c={g_esp,MEM32(g_esp+0x14),MEM32(g_esp+0x7C),g_esi};
    Ra2AlliedServices services={&c,query,heading,opposite,relative,distance,remember};
    int moving=(g_ebx&255u)!=0;
    int32_t passage=(int32_t)MEM32(c.frame+0x8C);
    g_esp=c.frame-0x100;
    Ra2AlliedOutcome outcome=ra2_ground_classify_allied_relation(moving,&passage,&services);
    MEM32(c.frame+0x8C)=(uint32_t)passage;
    g_esp=c.frame;g_ebp=c.owner;g_ebx=c.cell;g_esi=c.object;g_edi=(uint32_t)passage;
    switch(outcome)
    {
        case RA2_ALLIED_CHECK_ENEMY:return 0x70397C;
        case RA2_ALLIED_CHECK_STATIONARY:return 0x70394F;
        case RA2_ALLIED_BLOCKED:return 0x703B5A;
        default:return 0x7038EF;
    }
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';raw=p.read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');t=raw.decode('utf-8').replace('\r\n','\n')
t='extern unsigned ra2_ground_allied_relation_bridge(void);\n'+t
m='L_0070372C:\n';c=t.count(m);assert c==3
t=t.replace(m,m+'''    /* Readable C: alliance, movement and ordered facing/distance services. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned relation_v32=ra2_ground_allied_relation_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(relation_v32==0x70397C)goto L_0070397C;
    if(relation_v32==0x70394F)goto L_0070394F;
    if(relation_v32==0x703B5A)goto L_00703B5A;
    goto L_007038EF;
''');p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
(S/'pending/allied-relation-integration.json').write_text(json.dumps(dict(passed=True,entry='0070372C',copies=c),indent=2)+'\n',encoding='utf-8')
print('Integrated relation',c)
