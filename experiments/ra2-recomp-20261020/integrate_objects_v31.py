"""Share the moving-allied flag, kind and locomotor tail."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=R/'ra2/src/gameplay/ground_moving_tail.h';p.write_text('#pragma once\n#include "ground_allied.h"\nRa2AlliedOutcome ra2_ground_classify_moving_tail(int32_t *passage,const Ra2AlliedServices *services);\n',encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_allied.c';t=p.read_text(encoding='utf-8');needle='    /* 5A0';assert t.count(needle)==1
t=t.replace('#include "ground_allied.h"','#include "ground_allied.h"\n#include "ground_moving_tail.h"')
t=t.replace(needle,'''    return ra2_ground_classify_moving_tail(passage,s);
}

Ra2AlliedOutcome ra2_ground_classify_moving_tail(int32_t *passage,const Ra2AlliedServices *s)
{
    void *c=s->context;
'''+needle);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_allied_bridge.c';t=p.read_text(encoding='utf-8').replace('#include "ground_allied.h"','#include "ground_allied.h"\n#include "ground_moving_tail.h"')
t+='''
uint32_t ra2_ground_moving_tail_bridge(void)
{
    uint32_t frame=g_esp,object=g_esi;
    AlliedContext c={frame,MEM32(frame+0x14),MEM32(frame+0x7C),MEM32(frame+0x20)};
    Ra2AlliedServices services={&c,query,heading,opposite,relative,distance,remember};
    g_esp=frame-0x100;
    /* The locomotor callback can update the caller's passage slot. */
    ra2_ground_classify_moving_tail((int32_t *)(uintptr_t)ADDR(frame+0x8C),&services);
    g_esp=frame;g_ebp=MEM32(frame+0x14);g_esi=object;g_edi=c.object;
    return 0x7038EF;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';raw=p.read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');t=raw.decode('utf-8').replace('\r\n','\n')
t='extern unsigned ra2_ground_moving_tail_bridge(void);\n'+t
marker='L_00703895:\n';count=t.count(marker);assert count==3
t=t.replace(marker,marker+'''    /* Readable C: remembered moving-object kind and locomotor passage. */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_moving_tail_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_007038EF;
''');p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
(S/'pending/moving-tail-integration.json').write_text(json.dumps(dict(passed=True,entry='00703895',copies=count),indent=2)+'\n',encoding='utf-8')
print('Integrated moving tail',count)
