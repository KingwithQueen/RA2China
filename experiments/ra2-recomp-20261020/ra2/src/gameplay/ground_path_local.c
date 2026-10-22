#include "ground_path_local.h"
#include "x87_arithmetic.h"
#include <stdlib.h>

static Ra2PathPoint add(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x+b.x),(int16_t)(a.y+b.y)};}
static int distance(Ra2PathPoint p){int x=abs(p.x),y=abs(p.y);return x>y?x:y;}
static Ra2PathPoint advance(Ra2PathPoint point,int32_t direction,const Ra2LocalPathServices *v)
{return direction==8?v->connection_exit(v->context,&point):add(point,v->offsets[direction]);}
static Ra2PathPoint walk(Ra2PathPoint point,const int32_t *directions,int32_t count,const Ra2LocalPathServices *v)
{for(int32_t i=0;i<count;++i)point=advance(point,directions[i],v);return point;}
static int32_t next_level(int32_t previous,Ra2LocalPathCell cell)
{return previous-cell.ground_level==4 && (cell.flags&0x100u)?cell.ground_level+4:cell.ground_level;}
/* 不将x87中间值先写回double，避免阈值附近被再次舍入。这里的有限值相减
 * 保留精确符号；相等（包括有符号零）必须通过“大于等于”判断。 */
static int scaled_at_least(int32_t value,double factor,double threshold,uint16_t control)
{
    Ra2LegacyReal product=ra2_real_multiply(ra2_real_from_i32(value),ra2_real_from_f64(factor),control);
    Ra2LegacyReal difference=ra2_real_subtract(product,ra2_real_from_f64(threshold),0x037F);
    return !difference.significand || !difference.negative;
}
void ra2_path_find_anchor(const int32_t *directions,int32_t end,int32_t start,
    int32_t *anchor_index,Ra2PathPoint *anchor,const Ra2PathPoint offsets[8])
{
    Ra2PathPoint displacement={0,0},point=*anchor;int maximum=0,retreated=0;
    for(int32_t i=end;i>=start;--i) {
        if(directions[i]==-2)continue;
        int32_t backward=(int32_t)(((uint32_t)directions[i]-4u)&7u);
        displacement=add(displacement,offsets[backward]);point=add(point,offsets[backward]);
        int extent=distance(displacement);
        if(extent>maximum) {
            if(retreated) {
                *anchor_index=i+1;*anchor=add(point,offsets[(backward+4)&7]);return;
            }
            maximum=extent;
        } else retreated=1;
    }
    *anchor_index=start;*anchor=point;
}
int32_t ra2_path_shorten_turn(int32_t *directions,const int32_t *levels,int32_t first_count,
    int32_t second_count,Ra2PathPoint *anchor,const Ra2LocalPathServices *v)
{
    int32_t first=directions[0],second=directions[first_count];
    int32_t middle=(first+second)/2;
    if(middle+1!=first && middle+1!=second)middle=0;
    if(first==8 || second==8) {
        int32_t total=first_count+second_count;*anchor=walk(*anchor,directions,total,v);return total;
    }
    int32_t pairs=first_count<second_count?first_count:second_count;
    Ra2PathPoint origin=*anchor;
    if(second_count<first_count)origin=walk(origin,directions,first_count-second_count,v);
    double factor=v->owner_factor(v->context);uint32_t house=v->owner_house(v->context);
    for(;pairs>0;--pairs,origin=add(origin,v->offsets[first&7])) {
        int32_t remaining=pairs*2,level=levels[first_count-pairs];int blocked=0;
        Ra2PathPoint point=add(origin,v->offsets[middle&7]);
        uintptr_t cell=v->cell_at(v->context,&point);
        while(remaining>0 && !blocked) {
            blocked=v->passage(v->context,cell,middle,level)!=0;
            if(!blocked)blocked=(v->cell_properties(v->context,cell).flags&0x40000u)!=0;
            if(!blocked)blocked=scaled_at_least(v->threat(v->context,&origin,house),factor,1.0,*v->numeric_control);
            --remaining;
            /* 原版在本次已阻挡或刚到段尾时仍查询下一格并更新高度。 */
            point=add(point,v->offsets[middle&7]);cell=v->cell_at(v->context,&point);
            level=next_level(level,v->cell_properties(v->context,cell));
        }
        if(!blocked) {
            int32_t prefix=first_count-pairs;
            for(int32_t i=0;i<pairs*2;++i)directions[prefix+i]=middle;
            *anchor=walk(*anchor,directions,prefix,v);return prefix;
        }
    }
    *anchor=walk(*anchor,directions,first_count,v);return first_count;
}
int ra2_path_rewrite_segment(int32_t *directions,int32_t count,const Ra2PathPoint *anchor,
    const Ra2PathPoint *delta,int32_t level,int final_segment,const Ra2LocalPathServices *v)
{
    int32_t diagonal=delta->x<0?(delta->y<0?7:5):(delta->y<0?1:3);
    int32_t straight=delta->x-delta->y>0?(delta->x+delta->y>0?2:0):(delta->x+delta->y>0?4:6);
    int32_t x=abs(delta->x),y=abs(delta->y);
    int32_t first_count=x<y?x:y,second_count=abs(x-y),first=diagonal,second=straight;
    double factor=v->owner_factor(v->context);uint32_t house=v->owner_house(v->context);
    int use_threat=factor>0.00001;
    for(unsigned attempt=0;attempt<2;++attempt) {
        int blocked=first_count==0;Ra2PathPoint point=*anchor;int32_t current_level=level,high_threat=0;
        for(unsigned run=0;run<2 && !blocked;++run) {
            int32_t direction=run?second:first,steps=run?second_count:first_count;
            for(int32_t i=0;i<steps && !blocked;++i) {
                point=add(point,v->offsets[direction&7]);uintptr_t cell=v->cell_at(v->context,&point);
                if(use_threat && scaled_at_least(v->threat(v->context,&point,house),factor,0.01,*v->numeric_control))++high_threat;
                blocked=v->passage(v->context,cell,direction,current_level)!=0;
                Ra2LocalPathCell properties=v->cell_properties(v->context,cell);
                if(!blocked)blocked=(properties.flags&0x40000u)!=0 || high_threat>3 || (!(final_segment&255) && high_threat>0);
                current_level=next_level(current_level,properties);
            }
        }
        if(!blocked) {
            int32_t written=0;
            for(int32_t i=0;i<first_count;++i)directions[written++]=first;
            for(int32_t i=0;i<second_count;++i)directions[written++]=second;
            while(written<count)directions[written++]=-2;
            return 1;
        }
        int32_t temporary=first;first=second;second=temporary;
        temporary=first_count;first_count=second_count;second_count=temporary;
    }
    return 0;
}
