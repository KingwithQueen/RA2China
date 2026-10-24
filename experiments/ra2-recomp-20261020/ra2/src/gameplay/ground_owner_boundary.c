#include "ground_owner_boundary.h"

int ra2_ground_refresh_owner(const Ra2OwnerRefreshServices *s)
{
    s->refresh(s->context);
    return s->usable(s->context)!=0;
}

Ra2OwnerCompletion ra2_ground_complete_owner(int reached_target,
    const Ra2OwnerCompletionServices *s)
{
    void *c=s->refresh.context;
    if(!ra2_ground_refresh_owner(&s->refresh)) return RA2_OWNER_RETURN_TRUE;
    if(reached_target)
    {
        s->cancel_target_and_path(c);
        if(s->effective_mission(c)==2 && s->stop_move_mission(c))
            return RA2_OWNER_RETURN_TRUE;
    }
    if(s->update_owner(c)) return RA2_OWNER_RETURN_TRUE;
    if(!s->alive(c)) return RA2_OWNER_RETURN_FALSE;
    return RA2_OWNER_CONTINUE;
}
