"""Two reversible waiting and released-obstacle service phases; existing ABI/glue retained."""
from run_batch_v63 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
def unindent(s):return '\n'.join(l[4:] if l.startswith('    ') else l for l in s.splitlines())+'\n'
if sys.argv[1]=='wait':
 p=R/'ra2/src/gameplay/ground_wait.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('            if (overlay != -1');b=t.index('            return RA2_CLEARANCE_TERRAIN_SPEED;',a)
 body=t[a:b]
 body='\n'.join(l[12:] if l.startswith('            ') else l for l in body.splitlines())
 helper='''/* 通行后才解析可碾覆盖和层高；每次查询仍使用当时的context。 */
static void resolve_clear_terrain(int32_t overlay,int32_t reference_level,
    Ra2ClearanceResult *result,const Ra2ClearanceServices *services)
{
'''+''.join('    '+l+'\n' for l in body.splitlines())+'''}

'''
 t=t[:a]+'            resolve_clear_terrain(overlay,reference_level,result,services);\n'+t[b:]
 head=t.index('Ra2ClearancePhase ra2_ground_check_clearance(');t=t[:head]+helper+t[head:]
 a=t.index('Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(')
 old=t[a:];start=old.index('        state->waiting = 1;');end=old.index('\n    }',start)
 start_body=unindent(old[start:end])
 rebuild=old[old.index('    int rebuilt ='):old.rfind('}')]
 t=t[:a]+'''/* 首次阻塞只启动一次；start_wait可改写计时或waiting，调用后不覆盖。 */
static void start_traffic_wait_once(Ra2TrafficWaitState *state,const Ra2TrafficWaitServices *services)
{
'''+start_body+'''}

static Ra2TrafficWaitPhase rebuild_after_traffic_wait(int mode,const Ra2TrafficWaitServices *services)
{
'''+rebuild+'''}

Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(Ra2TrafficWaitState *state,
    const Ra2TrafficWaitServices *services)
{
    if(!state->waiting)start_traffic_wait_once(state,services);
    int32_t frame=services->current_frame(services->context);
    if(!ra2_ground_retry_timer_ready(state->retry,frame))return RA2_TRAFFIC_REPORT_OBSTACLE;
    /* 重试门禁先于长等待判断；保留回绕计时和mode 1/2的原版选择。 */
    int mode=state->waiting && ra2_ground_retry_timer_ready(state->obstruction,frame) ? 2:1;
    return rebuild_after_traffic_wait(mode,services);
}
'''
 p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='release':
 p=R/'ra2/src/gameplay/ground_obstacle.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');head=t.index('Ra2PreparePhase ra2_ground_observe_obstacle(')
 a=t.index('                ra2_ground_invalidate_segment(',head);b=t.index('\n            }',a)
 finish=t[a:b];finish='\n'.join(l[12:] if l.startswith('            ') else l for l in finish.splitlines())+'\n'
 t=t[:a]+'                return finish_near_allied_blocker(state,invalid_position,services,context);'+t[b:]
 a=t.index('        direction = services->query(',head);b=t.index('\n        if (passage == 3)',a)
 t=t[:a]+'        int passage=observe_neighbor_passage(cell,rebuilt,services,context);'+t[b:]
 a=t.index('        services->reset_failure_budget(',head);b=t.index('\n    }',a)
 publish=t[a:b];publish=unindent(publish)
 t=t[:a]+'        return publish_recovered_queue(path_head,services,context);'+t[b:]
 helpers='''/* 越界检查之后重读朝向/队首，保留首次捕获的障碍服务context。 */
static int observe_neighbor_passage(Ra2GroundCell cell,int rebuilt,
    const Ra2ObstacleServices *services,void *context)
{
    int32_t direction=services->query(context,rebuilt ? RA2_OBSTACLE_PATH_HEAD:RA2_OBSTACLE_FACING_DIRECTION);
    return services->can_enter(context,cell,direction);
}

static Ra2PreparePhase finish_near_allied_blocker(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,const Ra2ObstacleServices *services,void *context)
{
'''+finish+'''}

/* 障碍复核完成才重置失败预算，再读取可能由回调改写的实时队首。 */
static Ra2PreparePhase publish_recovered_queue(int32_t *path_head,
    const Ra2ObstacleServices *services,void *context)
{
'''+publish+'''}

'''
 t=t[:head]+helpers+t[head:];p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
