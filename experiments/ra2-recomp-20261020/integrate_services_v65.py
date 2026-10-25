"""Reversible Tube exit transaction, then connection admission/retry recovery services."""
from run_batch_v65 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
if sys.argv[1]=='exit':
 p=R/'ra2/src/gameplay/ground_tube_state.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('static uint32_t place_at_free_exit(');b=t.index('Ra2TubeWaypointResult ra2_ground_tube_waypoint(',a)
 t=t[:a]+'''/* 落位和入格完成后才查目标；恢复任务、速度和后继连接保持实时顺序。 */
static uint32_t restore_exit_navigation(const Ra2TubeExitServices *services,void *context)
{
    if(services->goal_is_exit_cell(context))
        services->request_self_clearance(context);
    services->restore_mission(context);
    services->set_speed(context,0);
    return services->face_next_connection(context);
}

static uint32_t place_at_free_exit(const Ra2TubeExitServices *services,void *context)
{
    services->place_at_exit(context);
    services->enter_cell(context);
    return restore_exit_navigation(services,context);
}

static uint32_t wait_for_occupied_exit(const Ra2TubeExitServices *services,
    void *context,uintptr_t object)
{
    /* 先完成原链快照，再让路；速度回调结束后才释放快照并传回结果。 */
    snapshot_exit_chain(services,context,object);
    request_snapshot_clearance(services,context);
    services->set_speed(context,1);
    return services->end_snapshot(context);
}

uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services)
{
    void *context=services->context;
    uintptr_t object=services->exit_occupants(context);
    if(object)return wait_for_occupied_exit(services,context,object);
    return place_at_free_exit(services,context);
}

'''+t[b:];p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='recovery':
 p=R/'ra2/src/gameplay/ground_landing.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('int ra2_ground_land_connection(');b=t.index('void ra2_ground_reject_direction(',a)
 t=t[:a]+'''static int admit_connection(int32_t index,const Ra2LandingServices *s,void *c)
{
    if(!s->connection_exists(c,index)) {
        s->reject_connection(c);
        return 0;
    }
    s->start_connection(c,index);
    s->set_approach_point(c);
    return 1;
}

static void publish_connection_height(const Ra2LandingServices *s,void *c)
{
    int32_t start=s->current_ground_height(c),duration;
    int32_t finish=s->target_ground_height(c,&duration);
    /* 先两次实时高度服务，再计算和发布；不提前缓存owner或端点。 */
    int32_t height=ra2_ground_connection_height(start,finish,duration);
    s->finish_connection(c,height);
}

int ra2_ground_land_connection(const Ra2LandingServices *s)
{
    void *c=s->context;
    if(s->selector(c)!=-1)return 1;
    s->leave_cell(c);
    s->clear_segment(c);
    int32_t index=s->connection_index(c);
    if(!admit_connection(index,s,c))return 0;
    publish_connection_height(s,c);
    return 0;
}

'''+t[b:];p.write_text(t,encoding='utf-8',newline='\n')
 p=R/'ra2/src/gameplay/ground_failure.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_failure.h"
#include "ground_outcome_policy.h"

static uint32_t retry_failed_connection(Ra2FailurePlan plan,
    const Ra2PrepareFailureServices *s,void *c)
{
    s->clear_path(c,plan.path_value);
    if(plan.start_retry)s->start_retry(c);
    return s->prepare_again(c);
}

static uint32_t stop_failed_connection(Ra2FailurePlan plan,
    const Ra2PrepareFailureServices *s,void *c)
{
    if(plan.clear_segment)s->clear_segment(c,plan.saved_segment);
    return s->stop(c);
}

uint32_t ra2_ground_finish_failure(Ra2PrepareFailureEntry entry,int may_retry,
    int32_t classification,int32_t rejected_direction,const Ra2PrepareFailureServices *s)
{
    void *c=s->context;
    Ra2FailurePlan plan=ra2_ground_failure_plan(entry,may_retry,classification,rejected_direction);
    if(plan.clear_pending)return s->clear_pending(c);
    if(plan.retry)return retry_failed_connection(plan,s,c);
    return stop_failed_connection(plan,s,c);
}
''',encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
