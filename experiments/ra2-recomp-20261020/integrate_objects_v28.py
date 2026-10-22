"""Share the remaining category-only object entry with the main preclassifier."""
from pathlib import Path
import json
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'

def edit(path, old, new, count=1):
    data = path.read_bytes()
    nl = '\r\n' if b'\r\n' in data else '\n'
    text = data.decode('utf-8').replace('\r\n', '\n')
    assert text.count(old) == count, (path, text.count(old), count)
    path.write_bytes(text.replace(old, new).replace('\n', nl).encode('utf-8'))

header = R / 'ra2/src/gameplay/ground_object_kind.h'
assert not header.exists()
header.write_text('''#pragma once
#include "ground_objects.h"

/* 已经过自身/关联对象检查的内部接续，仍按原顺序重复查询类别。 */
Ra2ObjectPassageOutcome ra2_ground_filter_object_kind(const Ra2ObjectPassageServices *services);
''', encoding='utf-8', newline='\n')
path = R / 'ra2/src/gameplay/ground_objects.c'
edit(path, '#include "ground_objects.h"', '#include "ground_objects.h"\n#include "ground_object_kind.h"')
edit(path, '''    if(s->query(c,RA2_OBJECT_RELATED_CELL_MATCHES)) return RA2_OBJECT_CLEAR;
    if(s->query(c,RA2_OBJECT_OWNER_ACCEPTS_LINK)''', '''    if(s->query(c,RA2_OBJECT_RELATED_CELL_MATCHES)) return RA2_OBJECT_CLEAR;
    return ra2_ground_filter_object_kind(s);
}

Ra2ObjectPassageOutcome ra2_ground_filter_object_kind(const Ra2ObjectPassageServices *s)
{
    void *c = s->context;
    if(s->query(c,RA2_OBJECT_OWNER_ACCEPTS_LINK)''')
path = R / 'ra2/src/runtime/ground_objects_bridge.c'
edit(path, '#include "ground_objects.h"', '#include "ground_objects.h"\n#include "ground_object_kind.h"')
edit(path, '    else if(entry==1) outcome=', '    else if(entry==4) outcome=ra2_ground_filter_object_kind(&services);\n    else if(entry==1) outcome=')
path = R / 'ra2/src/recomp/gen_game/recomp_0046.c'
marker = 'L_007034BF:\n'
data = path.read_text(encoding='utf-8')
count = data.count(marker)
assert count == 2
edit(path, marker, marker + '''    /* 可读 C：已跳过自身/关联对象后的类别过滤接续。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t object_kind_resume_v28 = ra2_ground_object_branch_bridge(4);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (object_kind_resume_v28 == 0x7031B1) goto L_007031B1;
    if (object_kind_resume_v28 == 0x7038FD) goto L_007038FD;
    if (object_kind_resume_v28 == 0x703536) goto L_00703536;
    goto L_00703693;
''', count)
(S / 'pending/object-kind-integration.json').write_text(json.dumps(dict(passed=True, internal_entry='007034BF', overlapping_copies=count, primary_preclassifier_shared=True), indent=2)+'\n', encoding='utf-8')
print('Integrated category-only entry in main filter and two overlapping copies')
