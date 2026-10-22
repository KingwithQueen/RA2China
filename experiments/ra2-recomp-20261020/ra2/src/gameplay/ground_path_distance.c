#include <string.h>
#include "ground_path_distance.h"
static uint32_t coordinate_difference(int16_t a,int16_t b)
{
    int32_t delta=(int32_t)a-b;
    return (uint32_t)(delta<0?-delta:delta);
}
int32_t ra2_path_squared_distance(Ra2PathPoint from,Ra2PathPoint to)
{
    uint32_t dx=coordinate_difference(from.x,to.x),dy=coordinate_difference(from.y,to.y);
    uint32_t squared=dx*dx+dy*dy;int32_t result;
    memcpy(&result,&squared,sizeof(result));return result;
}
float ra2_path_connection_distance(Ra2PathPoint from,Ra2PathPoint to)
{
    uint32_t dx=coordinate_difference(from.x,to.x),dy=coordinate_difference(from.y,to.y);
    return (float)(dx>dy?dx:dy);
}
