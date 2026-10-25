"""Reversible per-unit recovery scheduling, then retry-deadline publication."""
from run_batch_v66 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
assert read(S/'channel-observer-baseline-parity.json')['passed']
if sys.argv[1]=='scheduling':
 p=R/'ra2/src/gameplay/ground_wait.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(')
 t=t[:a]+'''/* 先通过短重试门禁，再按同一帧判断长等待；此选择本身不重置已有等待起点。 */
static int traffic_rebuild_mode(const Ra2TrafficWaitState *state,int32_t frame)
{
    if(!ra2_ground_retry_timer_ready(state->retry,frame))return 0;
    return state->waiting && ra2_ground_retry_timer_ready(state->obstruction,frame) ? 2:1;
}

Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(Ra2TrafficWaitState *state,
    const Ra2TrafficWaitServices *services)
{
    if(!state->waiting)start_traffic_wait_once(state,services);
    int32_t frame=services->current_frame(services->context);
    int mode=traffic_rebuild_mode(state,frame);
    if(!mode)return RA2_TRAFFIC_REPORT_OBSTACLE;
    return rebuild_after_traffic_wait(mode,services);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
 p=R/'ra2/src/gameplay/ground_prepare_cycle.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_prepare_cycle.h"

/* 只有入口确认队列耗尽后才取计时器；取帧时继续读取服务当时的context。 */
static Ra2PreparePhase schedule_empty_queue_retry(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,const Ra2PrepareCycleServices *s)
{
    Ra2PathRetryTimer timer=s->retry_timer(s->context);
    int32_t frame=s->current_frame(s->context);
    return ra2_ground_retry_path(state,invalid_position,timer,frame,s->prepare);
}

Ra2PreparePhase ra2_ground_prepare_cycle(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,int is_moving,int32_t *cached_path_head,
    const Ra2PrepareCycleServices *s)
{
    Ra2PreparePhase phase=ra2_ground_prepare_entry(state,invalid_position,
        is_moving,cached_path_head,s->prepare);
    if(phase!=RA2_PREPARE_RETRY_PATH)return phase;
    return schedule_empty_queue_retry(state,invalid_position,s);
}
''',encoding='utf-8',newline='\n')
elif sys.argv[1]=='publication':
 p=R/'ra2/src/gameplay/ground_prepare_exit.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_prepare_exit.h"
#include "ground_rebuild_result.h"

static int accept_rebuild_for_retry(int rebuilt,const Ra2PrepareExitServices *s,void *c)
{
    Ra2RebuildResultServices checks={c,s->owner_exists,s->write_aborted,
        s->destination_accepted,s->stop_navigation};
    return ra2_ground_check_rebuild_result(rebuilt,1,&checks)==RA2_REBUILD_READY;
}

static void publish_retry_deadline(const Ra2PrepareExitServices *s,void *c)
{
    /* 先取当前帧，再换算延迟；换算服务可改变控制字，随后实时调用重启。 */
    int32_t frame=s->current_frame(c);
    int32_t delay=s->retry_delay(c);
    s->restart_timer(c,frame,delay);
}

int ra2_ground_prepare_after_rebuild(int rebuilt,int timer_only,const Ra2PrepareExitServices *s)
{
    void *c=s->context;
    if(!timer_only && !accept_rebuild_for_retry(rebuilt,s,c))return 0;
    publish_retry_deadline(s,c);
    return 1;
}

void ra2_ground_prepare_clear_pending(Ra2PreparePendingState *state)
{state->sound_pending=0;state->selector=-1;}
''',encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1],mechanism_changed=False))
