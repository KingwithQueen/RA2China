"""Reversible exhausted-queue retry/drive service phase, then segment arrival publication."""
from run_batch_v62 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
def inner(block):
 body=block[block.index('{')+2:block.rfind('}')]
 return '\n'.join(line[4:] if line.startswith('    ') else line for line in body.splitlines()).rstrip()+'\n'
if sys.argv[1]=='retry':
 p=R/'ra2/src/gameplay/ground_drive.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');head=t.index('int ra2_ground_drive_process(')
 a=t.index('    if (state->path_selector != -1 && state->driving)',head);b=t.index('\n    /* 没有活动路段',a);active=t[a:b]
 t=t[:a]+'''    if(state->path_selector!=-1 && state->driving)
        return resume_exhausted_segment(state,services);
'''+t[b:]
 a=t.index('    if (query(services, RA2_DRIVE_TARGET_CATEGORY) == 11',head);b=t.index('    if (query(services, RA2_DRIVE_IS_TURNING))',a);reached=t[a:b]
 t=t[:a]+'''    if(stop_if_already_arrived(state,invalid_position,services))return 0;

'''+t[b:]
 a=t.rindex('    if (!query(services, RA2_DRIVE_IS_MOVING) && query(services, RA2_DRIVE_PATH_HEAD) == -1)');b=t.index('    /* 某些原版状态',a);empty=t[a:b]
 t=t[:a]+'''    if(!query(services,RA2_DRIVE_IS_MOVING) && query(services,RA2_DRIVE_PATH_HEAD)==-1)
        return handle_empty_queue(state,invalid_position,services);

'''+t[b:]
 helpers='''/* 推进和存活检查先于耗尽接续；同帧第二段传1，不重复累计速度。 */
static int resume_exhausted_segment(Ra2GroundDriveState *state,const Ra2DriveServices *services)
{
'''+inner(active)+'''}

static int stop_if_already_arrived(Ra2GroundDriveState *state,Ra2WorldPoint invalid_position,
    const Ra2DriveServices *services)
{
'''+reached.replace('return 0;','return 1;')+'''    return 0;
}

/* 空队列只同步目标或清速度；新的Prepare由外层有路径分支负责。 */
static int handle_empty_queue(Ra2GroundDriveState *state,Ra2WorldPoint invalid_position,
    const Ra2DriveServices *services)
{
'''+inner(empty)+'''}

'''
 t=t[:head]+helpers+t[head:];p.write_text(t,encoding='utf-8',newline='\n')
 p=R/'ra2/src/gameplay/ground_prepare.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('Ra2PreparePhase ra2_ground_retry_path(')
 t=t[:a]+'''static Ra2PreparePhase restart_and_rebuild_path(Ra2GroundPrepareState *state,
    Ra2WorldPoint invalid_position,int32_t frame,const Ra2PrepareServices *services)
{
    int32_t delay=query(services,RA2_PREPARE_RETRY_DELAY_FRAMES);
    services->restart_retry_timer(services->context,frame,delay);
    if(services->rebuild_path(services->context))return RA2_PREPARE_PATH_REBUILT;
    /* 重建可移除owner或改写目标；失败判断继续使用回调之后的实时状态。 */
    return finish_failed_rebuild(state,invalid_position,services);
}

Ra2PreparePhase ra2_ground_retry_path(Ra2GroundPrepareState *state,Ra2WorldPoint invalid_position,
    Ra2PathRetryTimer timer,int32_t frame,const Ra2PrepareServices *services)
{
    if(!ra2_ground_retry_timer_ready(timer,frame))return RA2_PREPARE_RETURN_FALSE;
    return restart_and_rebuild_path(state,invalid_position,frame,services);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='arrival':
 p=R/'ra2/src/gameplay/ground_arrival.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');a=t.index('Ra2ArrivalOutcome ra2_ground_finish_segment(')
 t=t[:a]+'''static void publish_arrived_segment(Ra2GroundArrivalState *state,Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position,const Ra2ArrivalServices *services)
{
    /* relocate可回写状态；先落位，再废弃旧段并清选择器、采样下标。 */
    services->relocate(services->context,!same_cell(owner_position,state->segment_end));
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
    state->path_selector=-1;
    state->sample_index=0;
}

static int mark_reached_destination(Ra2GroundArrivalState *state,Ra2WorldPoint invalid_position,
    int32_t level_height,const Ra2ArrivalServices *services)
{
    if(services->query(services->context,RA2_ARRIVAL_TARGET_IS_CURRENT_CELL)) {
        int32_t owner_z=services->query(services->context,RA2_ARRIVAL_OWNER_REFERENCE_Z);
        int32_t tolerance=signed_bits((uint32_t)level_height*2u);
        /* 目的地高度在查询后读取，保留严格小于和32位回绕距离。 */
        if(wrapped_distance(owner_z,state->destination.z)<tolerance) {
            state->destination=invalid_position;
            ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
            state->driving=0;
            return 1;
        }
    }
    return 0;
}

Ra2ArrivalOutcome ra2_ground_finish_segment(Ra2GroundArrivalState *state,Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position,int32_t level_height,const Ra2ArrivalServices *services)
{
    publish_arrived_segment(state,owner_position,invalid_position,services);
    int reached_target=mark_reached_destination(state,invalid_position,level_height,services);
    return finish_after_refresh(reached_target,services);
}
''';p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
