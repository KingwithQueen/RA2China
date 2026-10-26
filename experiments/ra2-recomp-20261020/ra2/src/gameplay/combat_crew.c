#include <string.h>
#include "combat_crew.h"
#include "x87_arithmetic.h"

static unsigned top_bit(uint64_t value){unsigned n=0;while(value>>=1)++n;return n;}
static int compare(Ra2LegacyReal a,Ra2LegacyReal b)
{
    if(!a.significand)a.negative=0;
    if(!b.significand)b.negative=0;
    if(a.negative!=b.negative)return a.negative?-1:1;
    int magnitude;
    if(!a.significand || !b.significand)magnitude=(a.significand!=0)-(b.significand!=0);
    else {
        unsigned at=top_bit(a.significand),bt=top_bit(b.significand);
        int32_t ae=a.exponent+(int32_t)at,be=b.exponent+(int32_t)bt;
        if(ae!=be)magnitude=(ae>be)-(ae<be);
        else {uint64_t av=a.significand<<(63-at),bv=b.significand<<(63-bt);magnitude=(av>bv)-(av<bv);}
    }
    return a.negative?-magnitude:magnitude;
}
int ra2_crew_roll_succeeds(int32_t draw,double unit,double chance,uint16_t control)
{
    uint64_t bits;memcpy(&bits,&chance,sizeof(bits));
    /* 原fcomp的无序结果置C0，屏蔽异常时与“小于”一起进入生成分支。 */
    if((bits&UINT64_C(0x7FF0000000000000))==UINT64_C(0x7FF0000000000000))
        return (bits&UINT64_C(0xFFFFFFFFFFFFF))!=0 || !(bits>>63);
    Ra2LegacyReal value=ra2_real_multiply(ra2_real_from_i32(draw),ra2_real_from_f64(unit),control);
    return compare(value,ra2_real_from_f64(chance))<0;
}
Ra2CrewSelection ra2_select_crew_type(const Ra2CrewServices *s)
{
    Ra2CrewSelection result={0,0};
    if(!s->query(s->context,RA2_CQ_CREWED))return result;
    result.eligible=1;s->perform(s->context,RA2_CO_SAVE_SELECTION_REGISTER,0);
    uint32_t kind=s->query(s->context,RA2_CQ_HOUSE_KIND);
    result.type=s->query(s->context,kind==0?RA2_CQ_ALLIED:kind==1?RA2_CQ_SOVIET:RA2_CQ_TECHNICIAN);
    s->perform(s->context,RA2_CO_PUBLISH_SELECTION,result.type);
    if(!s->query(s->context,RA2_CQ_COUNTRY_VALID))result.type=s->query(s->context,RA2_CQ_TECHNICIAN);
    else if((s->query(s->context,RA2_CQ_TECHNICIAN_GATE)&255) && (int32_t)s->query(s->context,RA2_CQ_RANDOM_100)<15)
        result.type=s->query(s->context,RA2_CQ_CURRENT_TECHNICIAN);
    return result;
}
