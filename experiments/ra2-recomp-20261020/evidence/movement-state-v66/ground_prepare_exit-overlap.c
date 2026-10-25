#include "ground_prepare_exit.h"
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
