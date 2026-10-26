#include "combat_aftermath.h"
#define Q(q,i) s->query(s->context,RA2_AF_##q,i)
#define DO(op,v) s->perform(s->context,RA2_AF_##op,v)
Ra2DeathPresentationRoute ra2_present_infantry_death(const Ra2AftermathServices *s)
{
    int32_t mode=Q(DEATH_MODE,0);
    if(Q(CURRENT_SEQUENCE,0)==0x21)mode=3;
    DO(SET_PRESENTATION_INDEX,(uint32_t)mode);
    if(Q(SOURCE_PRESENT,0) && Q(SOURCE_CLASS,0)==6 && Q(SOURCE_MODE_FIVE,0)) {
        mode=5;DO(SET_PRESENTATION_INDEX,5);
    }
    int32_t count=Q(CUSTOM_COUNT,0);
    if(count>0) {
        if(mode<0 || mode>=count || !Q(CUSTOM_ANIMATION,(uint32_t)mode)) {
            mode=0;DO(SET_PRESENTATION_INDEX,0);
        }
        if(Q(CUSTOM_ANIMATION,(uint32_t)mode))DO(CUSTOM_EFFECT,(uint32_t)mode);
        return RA2_PRESENTATION_FINISH;
    }
    if(Q(NOT_HUMAN,0))DO(DEATH_ACTION,11);
    else {
        uint32_t index=(uint32_t)mode-1;DO(SET_PRESENTATION_INDEX,index);
        if(index>6)return RA2_PRESENTATION_FINISH;
        if(index>=2){DO(DEFAULT_EFFECT,index);return RA2_PRESENTATION_FINISH;}
        DO(DEATH_ACTION,index?12:11);
    }
    return Q(FORCE_IMMEDIATE,0)?RA2_PRESENTATION_FINISH:RA2_PRESENTATION_DEFER;
}
void ra2_release_carrier_passengers(const Ra2AftermathServices *s)
{
    DO(CARRIER_NOTICE,0);
    if(Q(CARRIER_SINKABLE,0))return;
    while(Q(HAS_PASSENGERS,0)) {
        if(!Q(POP_PASSENGER,0))break;
        int allowed=Q(CAN_ENTER_CELL,0);
        DO(BEGIN_RELEASE,0);DO(RELEASE_POSITION,0);
        if(!Q(IGNORE_DEFENSES,0) && !Q(CARRIER_FLAG_7C,0) && allowed && Q(UNLIMBO_PASSENGER,0)) {
            DO(PLACED_NOTICE,0);
            if(!Q(HOUSE_CONTROLLED,0)) {
                if(Q(CARRIER_TEAM,0))DO(ADD_TO_TEAM,0);
                else DO(GUARD_MISSION,15);
            }
            if(Q(INHERIT_SELECTION,0))DO(SELECT_PASSENGER,0);
        }else {DO(KILL_NOTICE,0);DO(DELETE_PASSENGER,1);}
        DO(END_RELEASE,0);
    }
}
void ra2_destroy_carrier_passengers(const Ra2AftermathServices *s)
{
    while(Q(HAS_PASSENGERS,0)) {
        DO(PEEK_PASSENGER,0);
        if(Q(PASSENGER_TEAM,0))DO(LEAVE_TEAM,0);
        if(Q(POP_RAW_PASSENGER,0)){DO(KILL_NOTICE,0);DO(DELETE_PASSENGER,1);}
    }
}
