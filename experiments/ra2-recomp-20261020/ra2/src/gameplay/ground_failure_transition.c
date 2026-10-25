#include "ground_failure_transition.h"
#include <string.h>
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid)
{
    if (end->x != invalid.x || end->y != invalid.y || end->z != invalid.z)
    {
        *end = invalid;
        *driving = 0;
    }
}
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *), int (*stop)(void *, int))
{
    if (variant) cancel(context);
    int stopped = stop(context, variant);
    return variant ? stopped : 0;
}

int ra2_ground_within_stop_distance(int32_t distance,int32_t close_enough)
{
    return distance<close_enough;
}
int32_t ra2_ground_axis_distance(int32_t left,int32_t right)
{
    uint32_t bits=(uint32_t)left-(uint32_t)right;
    if(bits&0x80000000u)bits=0u-bits;
    int32_t value;memcpy(&value,&bits,sizeof(value));return value;
}
int ra2_ground_within_stop_height(int32_t left,int32_t right,int32_t level_height)
{
    uint32_t bits=2u*(uint32_t)level_height;
    int32_t threshold;memcpy(&threshold,&bits,sizeof(threshold));
    return ra2_ground_axis_distance(left,right)<threshold;
}
