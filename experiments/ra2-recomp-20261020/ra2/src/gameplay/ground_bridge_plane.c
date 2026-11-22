#include "ground_bridge_plane.h"

int ra2_ground_bridge_height_matches(int32_t upper_level, int32_t lower_level)
{ return (uint32_t)upper_level==(uint32_t)lower_level+4u; }

static void enter_upper_bridge(int32_t previous,int32_t next,void *context,
    uint32_t (*flags)(void *,unsigned),void (*set_layer)(void *,unsigned))
{
    if(ra2_ground_bridge_height_matches(previous,next) && ra2_ground_bridge_cell_flag_present(flags(context,1)))
        set_layer(context,1);
}

static void leave_upper_bridge(void *context,uint32_t (*flags)(void *,unsigned),
    void (*set_layer)(void *,unsigned))
{
    /* 上层写回可以改变格标志；独立复核离桥条件，不能与入桥组成else。 */
    if(!ra2_ground_bridge_cell_flag_present(flags(context,1)) && ra2_ground_bridge_cell_flag_present(flags(context,0)))
        set_layer(context,0);
}

void ra2_ground_transition_bridge(void *context,
    int32_t (*level)(void *context, unsigned next),
    uint32_t (*flags)(void *context, unsigned next),
    void (*set_layer)(void *context, unsigned upper))
{
    int32_t previous=level(context,0);
    int32_t next=level(context,1);
    enter_upper_bridge(previous,next,context,flags,set_layer);
    leave_upper_bridge(context,flags,set_layer);
}
