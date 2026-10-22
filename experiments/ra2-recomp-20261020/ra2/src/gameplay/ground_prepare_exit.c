#include "ground_prepare_exit.h"
int ra2_ground_prepare_after_rebuild(int rebuilt, int timer_only, const Ra2PrepareExitServices *s)
{
    void *c=s->context;
    if(!timer_only)
    {
        if(!s->owner_exists(c)){s->write_aborted(c);return 0;}
        if(!rebuilt && !s->destination_accepted(c)){s->stop_navigation(c);return 0;}
    }
    /* 当前帧先于延迟换算读取；延迟服务会改变原x87控制字，之后重新取单位。 */
    int32_t frame=s->current_frame(c);
    int32_t delay=s->retry_delay(c);
    s->restart_timer(c,frame,delay);
    return 1;
}
void ra2_ground_prepare_clear_pending(Ra2PreparePendingState *state)
{state->sound_pending=0;state->selector=-1;}
