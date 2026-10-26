#include "combat_lifecycle.h"
#define Q(q,i) s->query(s->context,RA2_LIFE_##q,i)
#define DO(op,i) s->perform(s->context,RA2_LIFE_##op,i)
Ra2DerivedDeathRoute ra2_unit_damage_handoff(const Ra2LifecycleServices *s,int32_t state)
{
    if(state==5)return RA2_DEATH_RETURN;
    if(state!=4)return RA2_DEATH_LIVE_EFFECTS;
    if(Q(DEATH_FRAMES,0)>0) {
        if(Q(DEATH_FRAME_UNSET,0)){DO(BEGIN_DEATH_FRAME,0);DO(CREDIT_KILL,0);}
        DO(REVIVE_DELAYED,0);return RA2_DEATH_DELAYED_EFFECTS;
    }
    return RA2_DEATH_EFFECTS;
}
Ra2DerivedDeathRoute ra2_infantry_damage_handoff(const Ra2LifecycleServices *s,int32_t state)
{
    if(!state || state==5)return RA2_DEATH_RETURN;
    if(state!=4)return RA2_DEATH_LIVE_EFFECTS;
    DO(CREDIT_KILL,0);DO(CLEAR_OCCUPATION,0);DO(STOP_MOTION,0);
    DO(CLEAR_MISSION,0);DO(DEATH_MISSION,0);DO(COMMIT_MISSION,0);DO(NOTIFY_DEATH,0);
    return RA2_DEATH_EFFECTS;
}
void ra2_finish_derived_death(const Ra2LifecycleServices *s,int unit)
{
    if(Q(SINKABLE,0)){if(Q(START_SINK,0))return;}
    else if(unit && Q(DEATH_DEFERRED,0))return;
    DO(UNINIT,0);
}
void ra2_uninit_foot(const Ra2LifecycleServices *s)
{
    if(Q(HAS_ATTACHED,0))DO(CANCEL_ATTACHED,0);
    if(Q(HAS_TEAM,0))DO(LEAVE_TEAM,0);
    DO(OBJECT_UNINIT,0);
}
void ra2_uninit_object(const Ra2LifecycleServices *s)
{
    if(Q(HAS_TIMER,0))DO(CANCEL_TIMER,0);
    DO(DETACH_REFERENCES,0);DO(LIMBO,0);DO(MARK_INACTIVE,0);
    if(Q(QUEUE_ROOM,0) || (Q(QUEUE_CAN_GROW,0) && Q(QUEUE_GROW,0)))DO(APPEND_DELETE,0);
}
void ra2_drain_object_deletions(const Ra2LifecycleServices *s)
{
    if(!Q(QUEUE_NONEMPTY,0))return;
    uint32_t index=0;
    do {
        DO(SELECT_CURRENT,index);
        if(!Q(READY_TO_DELETE,0))++index;
        else {
            for(;;) {
                uint32_t found=(uint32_t)Q(FIND_CURRENT,0);
                if(!Q(VALID_INDEX,found))break;
                DO(DECREMENT_COUNT,found);
                for(uint32_t next=found+1;Q(SHIFT_MORE,next);++next)DO(SHIFT_ITEM,next);
            }
            if(Q(IS_OBJECT,0)) {
                if(Q(KEEP_ACTIVE_TYPE,0))DO(MARK_CURRENT_ACTIVE,0);
                DO(DELETE_CURRENT,0);
            }
        }
    }while(Q(QUEUE_MORE,index));
}
