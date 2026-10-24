"""Shared post-rebuild service outcome and explicit Turn rejection/commit boundaries."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parent;G=R/'ra2/src/gameplay'
def edit(name,fn):
 p=G/name;raw=p.read_bytes();eol='\r\n' if b'\r\n' in raw else '\n';s=raw.decode('utf-8').replace('\r\n','\n');t=fn(s);assert t!=s;p.write_bytes(t.replace('\n',eol).encode('utf-8'))
if sys.argv[1]=='rebuild':
 assert not (G/'ground_rebuild_result.c').exists()
 (G/'ground_rebuild_result.h').write_text('''#pragma once
/* 成功重建时是否复核owner由调用点决定；返回拒绝后是否继续取方向也由调用点决定。 */
typedef enum Ra2RebuildResult { RA2_REBUILD_READY, RA2_REBUILD_NO_OWNER, RA2_REBUILD_REJECTED } Ra2RebuildResult;
typedef struct Ra2RebuildResultServices
{
    void *context;
    int (*owner_exists)(void *);
    void (*write_aborted)(void *);
    int (*destination_accepted)(void *);
    void (*stop_navigation)(void *);
} Ra2RebuildResultServices;
Ra2RebuildResult ra2_ground_check_rebuild_result(int rebuilt, int check_success,
    const Ra2RebuildResultServices *services);
''',encoding='utf-8',newline='\n')
 (G/'ground_rebuild_result.c').write_text('''#include "ground_rebuild_result.h"
Ra2RebuildResult ra2_ground_check_rebuild_result(int rebuilt, int check_success,
    const Ra2RebuildResultServices *s)
{
    if (rebuilt && !check_success) return RA2_REBUILD_READY;
    void *c = s->context;
    if (!s->owner_exists(c)) { s->write_aborted(c); return RA2_REBUILD_NO_OWNER; }
    if (!rebuilt && !s->destination_accepted(c))
    {
        s->stop_navigation(c);
        return RA2_REBUILD_REJECTED;
    }
    return RA2_REBUILD_READY;
}
''',encoding='utf-8',newline='\n')
 def exit(s):
  s=s.replace('#include "ground_prepare_exit.h"','#include "ground_prepare_exit.h"\n#include "ground_rebuild_result.h"')
  a=s.index('        if(!s->owner_exists(c))');b=s.index('\n    }',a)
  return s[:a]+'''        Ra2RebuildResultServices checks = { c, s->owner_exists, s->write_aborted,
            s->destination_accepted, s->stop_navigation };
        if (ra2_ground_check_rebuild_result(rebuilt, 1, &checks) != RA2_REBUILD_READY) return 0;'''+s[b:]
 edit('ground_prepare_exit.c',exit)
 def followup(s):
  s=s.replace('#include "ground_followup.h"','#include "ground_followup.h"\n#include "ground_rebuild_result.h"')
  a=s.index('    if (!services->rebuild_path(context, train))');b=s.index('    result.next_direction = services->next_direction(context);',a)
  return s[:a]+'''    int rebuilt = services->rebuild_path(context, train);
    Ra2RebuildResultServices checks = { context, services->owner_exists, services->write_aborted,
        services->destination_accepted, services->stop_navigation };
    if (ra2_ground_check_rebuild_result(rebuilt, 0, &checks) == RA2_REBUILD_NO_OWNER)
    {
        result.aborted = 1;
        return result;
    }
    /* 拒绝目标并停止后仍重取第二方向；与Prepare计时出口的直接返回不同。 */
'''+s[b:]
 edit('ground_followup.c',followup)
 p=R/'ra2/CMakeLists.txt';b=p.read_bytes();eol=b'\r\n' if b'\r\n' in b else b'\n';assert b'ground_rebuild_result' not in b
 b=b.replace(b'  src/gameplay/ground_prepare_cycle.c',b'  src/gameplay/ground_rebuild_result.c'+eol+b'  src/gameplay/ground_prepare_cycle.c');b+=eol+b'set_source_files_properties(src/gameplay/ground_rebuild_result.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")'+eol;p.write_bytes(b)
elif sys.argv[1]=='turn':
 def turn(s):
  s=s.replace('#include "ground_turn.h"','#include "ground_turn.h"\n#include "ground_failure_transition.h"\n#include "ground_template_transition.h"')
  a=s.index('static void clear_segment(');b=s.index('static Ra2TurnPhase retry(',a);s=s[:a]+s[b:]
  a=s.index('Ra2TurnPhase ra2_ground_prepare_turn(')
  helpers='''typedef struct TurnGate { int32_t passage; const Ra2TurnServices *services; } TurnGate;
static int32_t gate_class(void *opaque) { return ((TurnGate *)opaque)->passage; }
static unsigned gate_type(void *opaque, unsigned crusher)
{
    const Ra2TurnServices *s = ((TurnGate *)opaque)->services;
    return (unsigned)s->query(s->context, crusher ? RA2_TURN_IS_CRUSHER : RA2_TURN_IS_TRAIN);
}
static int32_t gate_overlay(void *opaque)
{
    const Ra2TurnServices *s = ((TurnGate *)opaque)->services;
    return s->query(s->context, RA2_TURN_CELL_OVERLAY_INDEX);
}
static void gate_clear(void *opaque) { ((TurnGate *)opaque)->passage = RA2_CELL_CLEAR; }

/* 临时障碍停止失败后放弃候选；隐形/完全阻挡直接返回。服务次序共用，接续策略保留。 */
static Ra2TurnPhase stop_candidate(Ra2TurnState *state, Ra2WorldPoint invalid, int discard,
    int32_t passage, unsigned allow_recursive, const Ra2TurnServices *s)
{
    ra2_ground_invalidate_segment(&state->movement.segment_end, &state->movement.driving, invalid);
    int target = s->query(s->context, RA2_TURN_HAS_TARGET_488);
    if (ra2_ground_stop_target(target, s->context, s->cancel_target, s->stop_navigation)) return RA2_TURN_RETURN_TRUE;
    return discard ? discard_candidate(state, invalid, passage, allow_recursive, s) : RA2_TURN_RETURN_FALSE;
}

''';s=s[:a]+helpers+s[a:]
  a=s.index('        if (passage < RA2_CELL_BLOCKED');b=s.index('\n    }',a)
  s=s[:a]+'''        TurnGate gate = { passage, services };
        Ra2TemplateGateServices checks = { &gate, gate_class, gate_type, gate_overlay, gate_clear };
        ra2_ground_template_gate(&checks);
        passage = gate.passage;'''+s[b:]
  a=s.index('                clear_segment(state, invalid);');b=s.index('\n            }',a)
  s=s[:a]+'                return stop_candidate(state, invalid, 1, passage, allow_recursive, services);'+s[b:]
  s=s.replace('        clear_segment(state, invalid);\n        return stop_navigation(services) ? RA2_TURN_RETURN_TRUE : RA2_TURN_RETURN_FALSE;', '        return stop_candidate(state, invalid, 0, passage, allow_recursive, services);')
  assert 'clear_segment(state' not in s and 'stop_navigation(services)' not in s
  return s
 edit('ground_turn.c',turn)
else:raise ValueError(sys.argv[1])
print('Integrated '+sys.argv[1])
