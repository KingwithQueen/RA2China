"""Remaining Prepare stop branches and Process/Arrival service boundaries, in two parts."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parent;G=R/'ra2/src/gameplay'
def edit(name,fn):
 p=G/name;raw=p.read_bytes();eol='\r\n' if b'\r\n' in raw else '\n';s=raw.decode('utf-8').replace('\r\n','\n');t=fn(s);assert t!=s;p.write_bytes(t.replace('\n',eol).encode('utf-8'))
def clear(s,name):
 s=s.replace('#include "'+name+'.h"','#include "'+name+'.h"\n#include "ground_failure_transition.h"')
 a=s.index('static void clear_segment(');b=s.index('\n}\n',a)+3
 return (s[:a]+s[b:]).replace('clear_segment(state, invalid_position);','ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);')
if sys.argv[1]=='prepare':
 def prepare(s):
  s=clear(s,'ground_prepare');a=s.index('            if (!query(services, RA2_PREPARE_HAS_TARGET_488))');b=s.index('            return query(services, RA2_PREPARE_OWNER_ALIVE)',a)
  return s[:a]+'''            int target = !!query(services, RA2_PREPARE_HAS_TARGET_488);
            if (ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation))
            {
                return RA2_PREPARE_RETURN_TRUE;
            }
'''+s[b:]
 edit('ground_prepare.c',prepare)
 def special(s):
  s=clear(s,'ground_special');a=s.index('    if (target_variant) services->cancel_target');b=s.index('\n}',a)
  return s[:a]+'''    return !!ra2_ground_stop_target(target_variant, services->context,
        services->cancel_target, services->stop_navigation);'''+s[b:]
 edit('ground_special.c',special)
elif sys.argv[1]=='process':
 def drive(s):
  s=clear(s,'ground_drive');a=s.index('int ra2_ground_drive_process(')
  helper='''/* Prepare/Advance 都可移除单位；每次服务返回后再查存活。
   接续同帧第二段传入1，避免再次累计本帧速度；新段从0开始。 */
static int prepare_and_advance(const Ra2DriveServices *services, int continuing)
{
    if (services->prepare_segment(services->context) || !query(services, RA2_DRIVE_OWNER_ALIVE)) return 0;
    services->advance_segment(services->context, continuing);
    if (!query(services, RA2_DRIVE_OWNER_ALIVE)) return 0;
    return services->finish_frame(services->context);
}

''';s=s[:a]+helper+s[a:]
  # Extract the two service sequences without changing their preceding branch queries.
  a=s.index('        if (services->prepare_segment(');b=s.index('\n    }',a)
  s=s[:a]+'        return prepare_and_advance(services, 1);'+s[b:]
  a=s.rindex('    if (services->prepare_segment(');s=s[:a]+'    return prepare_and_advance(services, 0);\n}\n'
  return s
 edit('ground_drive.c',drive)
 def arrival(s):
  s=clear(s,'ground_arrival');a=s.index('static int same_position(');b=s.index('\n}\n',a)+3;s=s[:a]+s[b:];a=s.index('    services->refresh_owner(services->context);');tail=s[a:]
  # Followup depends on refreshed world services, not a cached owner or state snapshot.
  helper='/* 刷新后重新检查可用性；停止任务/更新服务均可结束本帧或移除所有者。 */\nstatic Ra2ArrivalOutcome finish_after_refresh(int reached_target, const Ra2ArrivalServices *services)\n{\n'+tail
  s=s[:a]+'    return finish_after_refresh(reached_target, services);\n}\n'
  a=s.index('Ra2ArrivalOutcome ra2_ground_finish_segment(')
  return s[:a]+helper+'\n'+s[a:]
 edit('ground_arrival.c',arrival)
else:raise ValueError(sys.argv[1])
print('Integrated '+sys.argv[1])
