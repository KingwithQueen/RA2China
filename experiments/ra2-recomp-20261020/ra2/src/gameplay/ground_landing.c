#include "ground_exit_policy.h"
#include "ground_landing.h"

static int admit_connection(int32_t index,const Ra2LandingServices *s,void *c)
{
    if(!s->connection_exists(c,index)) {
        s->reject_connection(c);
        return 0;
    }
    s->start_connection(c,index);
    s->set_approach_point(c);
    return 1;
}

static void publish_connection_height(const Ra2LandingServices *s,void *c)
{
    int32_t start=s->current_ground_height(c),duration;
    int32_t finish=s->target_ground_height(c,&duration);
    /* 先两次实时高度服务，再计算和发布；不提前缓存owner或端点。 */
    int32_t height=ra2_ground_connection_height(start,finish,duration);
    s->finish_connection(c,height);
}

int ra2_ground_land_connection(const Ra2LandingServices *s)
{
    void *c=s->context;
    if(s->selector(c)!=-1)return 1;
    s->leave_cell(c);
    s->clear_segment(c);
    int32_t index=s->connection_index(c);
    if(!admit_connection(index,s,c))return 0;
    publish_connection_height(s,c);
    return 0;
}

void ra2_ground_reject_direction(int32_t *path_head, int32_t rejected_value)
{ *path_head = rejected_value; }
