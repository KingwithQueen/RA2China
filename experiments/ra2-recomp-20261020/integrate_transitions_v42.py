"""Two bounded state/service extractions; original generated entry glue stays unchanged."""
from pathlib import Path
import sys,re
R=Path(__file__).resolve().parent;G=R/'ra2/src/gameplay'
def edit(name,fn):
 p=G/name;raw=p.read_bytes();eol='\r\n' if b'\r\n' in raw else '\n';text=raw.decode('utf-8').replace('\r\n','\n');after=fn(text);assert after!=text,name;p.write_bytes(after.replace('\n',eol).encode('utf-8'))
def replace(s,a,b):
 assert s.count(a)==1,a;return s.replace(a,b)
def clear(s,typename):
 s=s.replace('#include "'+typename+'.h"','#include "'+typename+'.h"\n#include "ground_failure_transition.h"')
 a=s.index('static void clear_segment(');b=s.index('\n}\n',a)+3
 return s[:a]+s[b:]
if sys.argv[1]=='prepare':
 assert not (G/'ground_failure_transition.c').exists()
 (G/'ground_failure_transition.h').write_text('''#pragma once
#include "ground_prepare.h"
/* 清除有效路段；原本已无路段时，不额外改变 driving。 */
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid);
/* 调用者在清除路段后查询实时目标。取消目标服务可改变对象，随后再调用停止服务。 */
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *),
    int (*stop)(void *, int));
''',encoding='utf-8',newline='\n')
 (G/'ground_failure_transition.c').write_text('''#include "ground_failure_transition.h"
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid)
{
    if (end->x != invalid.x || end->y != invalid.y || end->z != invalid.z)
    {
        *end = invalid;
        *driving = 0;
    }
}
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *), int (*stop)(void *, int))
{
    if (variant) cancel(context);
    int stopped = stop(context, variant);
    return variant ? stopped : 0;
}
''',encoding='utf-8',newline='\n')
 def reaction(s):
  s=s.replace('#include "ground_reaction.h"','#include "ground_reaction.h"\n#include "ground_failure_transition.h"')
  a=s.index('    if (state->segment_end.x');b=s.index('\n}\n',a)
  return s[:a]+'''    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    int target = !!services->has_target_488(services->context);
    return ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation);'''+s[b:]
 edit('ground_reaction.c',reaction)
 def obstacle(s):
  s=clear(s,'ground_obstacle').replace('clear_segment(state, invalid_position);','ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);')
  a=s.index('                if (target_variant)');b=s.index('                return target_variant',a)
  return s[:a]+'''                int stopped = ra2_ground_stop_target(target_variant, context,
                    services->cancel_target, services->stop_navigation);
'''+s[b:]
 edit('ground_obstacle.c',obstacle)
 def recovery(s):
  s=clear(s,'ground_recovery').replace('clear_segment(state, invalid_position);','ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);')
  a=s.index('            if (!services->query(services->context, RA2_RECOVERY_HAS_TARGET_488))');b=s.index('            if (!services->query(services->context, RA2_RECOVERY_OWNER_ALIVE))',a)
  return s[:a]+'''            int target = !!services->query(services->context, RA2_RECOVERY_HAS_TARGET_488);
            if (ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation))
            {
                return 1;
            }
'''+s[b:]
 edit('ground_recovery.c',recovery)
 p=R/'ra2/CMakeLists.txt';raw=p.read_bytes();assert b'ground_failure_transition' not in raw
 eol=b'\r\n' if b'\r\n' in raw else b'\n';raw=raw.replace(b'  src/gameplay/ground_prepare_cycle.c',b'  src/gameplay/ground_failure_transition.c'+eol+b'  src/gameplay/ground_prepare_cycle.c')
 raw+=eol+b'set_source_files_properties(src/gameplay/ground_failure_transition.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")'+eol;p.write_bytes(raw)
elif sys.argv[1]=='advance':
 def wait(s):
  s=clear(s,'ground_wait').replace('#include "ground_failure_transition.h"','#include "ground_failure_transition.h"\n#include "ground_prepare_exit.h"')
  s=s.replace('clear_segment(state, invalid_position);','ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);')
  a=s.index('    if (!services->owner_exists(services->context))')
  return s[:a]+'''    /* 重建服务可替换对象或推进帧；统一出口在服务返回后重新查询。 */
    Ra2PrepareExitServices exit_services = { services->context, services->owner_exists,
        services->write_aborted, services->destination_accepted, services->stop_navigation,
        services->current_frame, services->retry_delay, services->restart_retry };
    return ra2_ground_prepare_after_rebuild(rebuilt, 0, &exit_services)
        ? RA2_TRAFFIC_RETURN_TRUE : RA2_TRAFFIC_RETURN_FALSE;
}
'''
 edit('ground_wait.c',wait)
 def continuation(s):
  s=clear(s,'ground_continuation')
  return s.replace('clear_segment(state,invalid);','ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid);')
 edit('ground_continuation.c',continuation)
else:raise ValueError(sys.argv[1])
print('Integrated '+sys.argv[1])
