"""Second checkpoint: preserve live candidate reads and post-start continuation services."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parent
assert sys.argv[1:]==['continuation']
p=R/'ra2/src/gameplay/ground_continuation.c';s=p.read_text(encoding='utf-8')
assert 'ground_segment_admission.h' not in s
s=s.replace('#include "ground_failure_transition.h"','#include "ground_failure_transition.h"\n#include "ground_segment_admission.h"')
a=s.index('static int valid_point(');b=s.index('static int32_t absolute_difference',a);s=s[:a]+s[b:]
a=s.index('/* 接续已获放行')
adapters='/* 接续服务按实时上下文读取候选，不能改成 Prepare 的按值位置参数。\n   接受服务可能移除 owner 或改写状态；成功后仍按原顺序恢复速度、弹出方向。 */\nstatic int continuation_accept(void *context,Ra2WorldPoint candidate)\n{\n    const Ra2ContinuationServices *s=context; (void)candidate;\n    return s->candidate_accepts_owner(s->context);\n}\nstatic int continuation_restricted(void *context)\n{\n    const Ra2ContinuationServices *s=context;\n    return s->query(s->context,RA2_CONTINUATION_OWNER_FLAG_76);\n}\nstatic int continuation_alive(void *context)\n{\n    const Ra2ContinuationServices *s=context;\n    return s->query(s->context,RA2_CONTINUATION_OWNER_ALIVE);\n}\nstatic void continuation_start(void *context,Ra2WorldPoint candidate)\n{\n    const Ra2ContinuationServices *s=context; (void)candidate;\n    s->start_segment(s->context);\n}\n\n'
s=s[:a]+adapters+s[a:]
a=s.index('    if(!valid_point(state->candidate,invalid))');b=s.index('\n    return 1;\n}',a)+1
s=s[:a]+'    const Ra2SegmentAdmissionServices admission={(void *)s,continuation_accept,\n        continuation_restricted,continuation_start,continuation_alive};\n    if(ra2_ground_admit_segment(&state->segment_end,&state->driving,invalid,\n        state->candidate,&admission)==RA2_SEGMENT_STARTED)\n    {\n        s->restore_speed(c,speed);\n        s->shift_direction(c);\n    }\n'+s[b:]
p.write_text(s,encoding='utf-8',newline='\n')
print('Integrated live-candidate continuation admission')
