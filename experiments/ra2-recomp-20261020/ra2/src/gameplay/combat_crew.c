#include <string.h>
#include "combat_crew.h"
#include "combat_real_compare.h"
#include "combat_crew_percent.h"

int ra2_crew_roll_succeeds(int32_t draw,double unit,double chance,uint16_t control)
{
    uint64_t bits;memcpy(&bits,&chance,sizeof(bits));
    /* 原fcomp的无序结果置C0，屏蔽异常时与“小于”一起进入生成分支。 */
    if((bits&UINT64_C(0x7FF0000000000000))==UINT64_C(0x7FF0000000000000))
        return (bits&UINT64_C(0xFFFFFFFFFFFFF))!=0 || !(bits>>63);
    Ra2LegacyReal value=ra2_real_multiply(ra2_real_from_i32(draw),ra2_real_from_f64(unit),control);
    return ra2_combat_compare_legacy_real(value,ra2_real_from_f64(chance))<0;
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
    else if((s->query(s->context,RA2_CQ_TECHNICIAN_GATE)&255) &&
        ra2_crew_percent_roll_below((int32_t)s->query(s->context,RA2_CQ_RANDOM_100), RA2_CREW_TECHNICIAN_PERCENT))
        result.type=s->query(s->context,RA2_CQ_CURRENT_TECHNICIAN);
    return result;
}
