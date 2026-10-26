#include "combat_death.h"
#define QUERY(q) s->query(s->context,RA2_DEATH_##q)
#define DO(op,v,a) s->perform(s->context,RA2_DEATH_##op,v,a)
int32_t ra2_combat_finish_damage(const Ra2CombatDeathServices *s)
{
    if(QUERY(HEALTH)<=0 && QUERY(CLASS)==15 && !QUERY(IGNORE_DEFENSES) &&
        QUERY(SPECIAL_KIND) && !QUERY(SPECIAL_POSTURE)) {
        DO(SPECIAL_EFFECT,0,0);
        int32_t health=QUERY(SPECIAL_HEALTH);
        DO(SET_HEALTH,health>1?health:1,0);DO(SET_POSTURE,1,0);
        DO(SPECIAL_ACTION,6,0);DO(SET_STATE,3,0);
    }
    int32_t state=QUERY(STATE),captured_health=QUERY(CAPTURE_HEALTH);
    unsigned attacker=QUERY(CAPTURE_ATTACKER)!=0;
    if(state==2) {
        if(attacker && QUERY(HAS_TRIGGER))DO(TRIGGER,0x27,0);
        if(!QUERY(ACTIVE))return 5;
        if(QUERY(HAS_TRIGGER))DO(TRIGGER,0x2A,0);
    }
    if(!QUERY(ACTIVE))return 5;
    if(QUERY(STATE)==3) {
        if(attacker && QUERY(HAS_TRIGGER))DO(TRIGGER,0x28,0);
        if(!QUERY(ACTIVE))return 5;
        if(QUERY(HAS_TRIGGER))DO(TRIGGER,0x2B,0);
    }
    if(!QUERY(ACTIVE))return 5;
    int32_t old_health=QUERY(OLD_HEALTH),health=QUERY(HEALTH);
    if(old_health!=health && QUERY(TYPE_PRESENT)) {
        int32_t maximum=QUERY(TYPE_STRENGTH);old_health=QUERY(OLD_HEALTH);
        if(old_health==maximum) {
            if(attacker && QUERY(HAS_TRIGGER))DO(TRIGGER,0x26,0);
            if(QUERY(HAS_TRIGGER) && QUERY(ACTIVE))DO(TRIGGER,0x29,0);
            if(QUERY(HAS_TRIGGER)) {
                if(!QUERY(ACTIVE))return 5;
                if(attacker)DO(TRIGGER,0x29,1);
            }
        }
    }
    if(!QUERY(ACTIVE))return 5;
    /* 回调已处理了由正生命转为非正生命的情况，不能再次处理同一次删除。 */
    if(captured_health>0 && QUERY(HEALTH)<=0)return 5;
    health=QUERY(HEALTH);DO(FINAL_PHASE,4,0);
    if(!health) {
        DO(ATTACKER_NOTICE,0,1);DO(SET_STATE,4,0);DO(REMOVE,1,0);
    }
    if(QUERY(ACTIVE)) {
        if(attacker && QUERY(HAS_TRIGGER) && QUERY(STATE)!=4)DO(TRIGGER,6,1);
        if(QUERY(ACTIVE)) {
            if(attacker && QUERY(HAS_TRIGGER) && QUERY(STATE)!=4)DO(TRIGGER,0x2C,1);
            if(QUERY(ACTIVE) && QUERY(STATE) && QUERY(NOTIFY_ENABLED))DO(DAMAGE_NOTICE,2,0);
        }
    }
    return QUERY(STATE);
}
