#include "ground_prepare_cycle.h"

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
