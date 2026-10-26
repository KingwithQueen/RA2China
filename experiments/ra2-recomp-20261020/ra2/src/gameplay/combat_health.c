#include "combat_health.h"
#include "x87_arithmetic.h"
#include <string.h>

static int32_t subtract_wrapped(int32_t left,int32_t right)
{
    uint32_t bits=(uint32_t)left-(uint32_t)right;
    int32_t value;memcpy(&value,&bits,sizeof(value));return value;
}
static unsigned leading_bit(uint64_t value)
{
    unsigned bit=0;while(value>>1){value>>=1;++bit;}return bit;
}
/* 比较兼容数值的实际尾数/指数，不提前保存为double而丢失临界位。 */
static int compare_real(Ra2LegacyReal a,Ra2LegacyReal b)
{
    if(!a.significand && !b.significand)return 0;
    unsigned an=a.significand && a.negative,bn=b.significand && b.negative;
    if(an!=bn)return an?-1:1;
    int result;
    if(!a.significand)result=-1;
    else if(!b.significand)result=1;
    else {
        unsigned ab=leading_bit(a.significand),bb=leading_bit(b.significand);
        int32_t ae=a.exponent+(int32_t)ab,be=b.exponent+(int32_t)bb;
        if(ae!=be)result=ae<be?-1:1;
        else {
            uint64_t av=a.significand<<(63u-ab),bv=b.significand<<(63u-bb);
            result=av==bv?0:av<bv?-1:1;
        }
    }
    return an?-result:result;
}
Ra2CombatHealthStep ra2_combat_receive_health(Ra2CombatHealthState *state,
    unsigned ignore_defenses,const Ra2CombatHealthServices *s)
{
    Ra2CombatHealthStep step={0};step.original_health=state->health;
    if(state->health<=0 || !s->query(s->context,RA2_HEALTH_DAMAGE))return step;
    if(!ignore_defenses && s->query(s->context,RA2_HEALTH_TYPE_IMMUNE))return step;
    step.maximum_health=s->query(s->context,RA2_HEALTH_MAXIMUM);step.maximum_queried=1;
    if(!ignore_defenses) {
        int32_t armor=s->query(s->context,RA2_HEALTH_ARMOR);
        int32_t damage=s->adjust_damage(s->context,armor);
        s->store_damage(s->context,damage);
    }
    int32_t damage=s->query(s->context,RA2_HEALTH_DAMAGE);
    step.effective_damage=damage;
    if(!damage)return step;
    if(damage<0) {
        int32_t before=state->health;
        state->health=subtract_wrapped(before,damage);
        if(state->health>step.maximum_health)state->health=step.maximum_health;
        if(state->health!=before)s->refresh_health(s->context);
        return step;
    }
    step.damage_state=1;
    if(step.original_health<=damage)s->store_damage(s->context,step.original_health);
    else {
        int32_t half=step.maximum_health/2;
        if(step.maximum_health<0 && step.maximum_health%2)--half;
        if(step.original_health>=half && subtract_wrapped(step.original_health,damage)<half)
            step.damage_state=2;
    }
    double ratio=s->critical_ratio(s->context);
    Ra2LegacyReal threshold=ra2_real_multiply(ra2_real_from_i32(step.maximum_health),
        ra2_real_from_f64(ratio),s->operation_control(s->context));
    if(compare_real(ra2_real_from_i32(step.original_health),threshold)>0) {
        step.critical_comparison_ran=1;
        step.comparison_health=subtract_wrapped(step.original_health,s->query(s->context,RA2_HEALTH_DAMAGE));
        if(compare_real(ra2_real_from_i32(step.comparison_health),threshold)<0)step.damage_state=3;
    }
    state->health=subtract_wrapped(step.original_health,s->query(s->context,RA2_HEALTH_DAMAGE));
    step.outcome=RA2_HEALTH_CONTINUE_DAMAGE;return step;
}
