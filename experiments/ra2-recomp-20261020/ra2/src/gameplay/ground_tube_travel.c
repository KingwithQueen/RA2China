#include "ground_tube_travel.h"
#include "ground_connection_trig.h"
#include "ground_connection_numeric.h"
#include "x87_arithmetic.h"

int32_t ra2_ground_tube_step(int32_t speed, double scale, uint16_t operation, uint16_t conversion)
{
    return ra2_real_round_i32(ra2_real_multiply(ra2_real_from_i32(speed),
        ra2_real_from_f64(scale), operation), conversion);
}
Ra2TubeEntryPreparation ra2_ground_tube_prepare_entry(const Ra2TubeEntryServices *s)
{
    void *c=s->context; Ra2TubeEntryPreparation result;
    result.distance=s->distance(c);
    s->select_route(c);
    result.heading=s->heading(c);
    result.step=s->speed(c);
    s->endpoints(c);
    /* 两端查询都有副作用，先入口后出口；差值按原32位回绕。 */
    int32_t entrance=s->entrance_height(c);
    int32_t exit=s->exit_height(c);
    int32_t difference=(int32_t)((uint32_t)exit-(uint32_t)entrance);
    int32_t count=s->segment_count(c);
    result.rise=count ? (int32_t)((int64_t)difference/count) : 0;
    return result;
}
static float component(double angle,float scale,const float *table,int cosine,uint16_t operation,uint16_t conversion)
{
    int32_t quantized=ra2_real_round_i32(ra2_real_multiply(ra2_real_from_f64(angle),
        ra2_real_from_f32(scale),operation),conversion);
    int32_t index=quantized/2%8192;
    if(index<0)index+=8192;
    if(cosine)index+=2048;
    if(((uint32_t)quantized&1u)&&index<(cosine?10239:8191))++index;
    return table[index];
}
static int32_t coordinate(int32_t origin,int32_t distance,float direction,int subtract,uint16_t control)
{
    Ra2LegacyReal step=ra2_real_multiply(ra2_real_from_f32(direction),ra2_real_from_i32(distance),control);
    Ra2LegacyReal start=ra2_real_from_i32(origin);
    return ra2_real_round_i32(subtract?ra2_real_subtract(start,step,control):ra2_real_add(step,start,control),control);
}
Ra2TubeHorizontalResult ra2_ground_tube_horizontal(Ra2TubeHorizontalInput in)
{
    Ra2TubeHorizontalResult out; out.point=in.origin;
    int32_t turn=(int32_t)(int16_t)(uint16_t)in.heading-0x3FFF;
    out.angle=ra2_ground_connection_angle(turn,in.radians_per_turn,in.operation);
    float sine=component(out.angle,in.sine_scale,in.table,0,in.operation,in.conversion);
    /* 查表服务返回后，原版恢复独立转换控制字，后续运算服从它。 */
    out.point.y=coordinate(in.origin.y,in.distance,sine,1,in.conversion);
    float cosine=component(out.angle,in.cosine_scale,in.table,1,in.conversion,in.conversion);
    out.point.x=coordinate(in.origin.x,in.distance,cosine,0,in.conversion);
    return out;
}
