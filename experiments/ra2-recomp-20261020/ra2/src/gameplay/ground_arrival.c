#include <stdint.h>
#include <string.h>
#include "ground_arrival.h"
#include "ground_failure_transition.h"
#include "ground_owner_boundary.h"


static int same_cell(Ra2WorldPoint left, Ra2WorldPoint right)
{
    /* 原版先向零取整，再截取 16 位格坐标；不能用负数右移代替除法。 */
    return (uint16_t)(left.x / 256) == (uint16_t)(right.x / 256)
        && (uint16_t)(left.y / 256) == (uint16_t)(right.y / 256);
}



/* 适配查询接口；服务仍在原有实时上下文执行，不缓存刷新前的任务或存活状态。 */
static void refresh(void *context)
{ const Ra2ArrivalServices *s=context; s->refresh_owner(s->context); }
static int usable(void *context)
{ const Ra2ArrivalServices *s=context; return s->query(s->context,RA2_ARRIVAL_OWNER_USABLE); }
static void cancel(void *context)
{ const Ra2ArrivalServices *s=context; s->cancel_target_and_path(s->context); }
static int mission(void *context)
{ const Ra2ArrivalServices *s=context; return s->query(s->context,RA2_ARRIVAL_EFFECTIVE_MISSION); }
static int stop_move(void *context)
{ const Ra2ArrivalServices *s=context; return s->stop_move_mission(s->context); }
static int update(void *context)
{ const Ra2ArrivalServices *s=context; return s->query(s->context,RA2_ARRIVAL_OWNER_UPDATE); }
static int alive(void *context)
{ const Ra2ArrivalServices *s=context; return s->query(s->context,RA2_ARRIVAL_OWNER_ALIVE); }

static Ra2ArrivalOutcome finish_after_refresh(int reached_target,const Ra2ArrivalServices *s)
{
    const Ra2OwnerCompletionServices completion={{(void *)s,refresh,usable},cancel,mission,stop_move,update,alive};
    switch(ra2_ground_complete_owner(reached_target,&completion))
    {
        case RA2_OWNER_RETURN_TRUE: return RA2_ARRIVAL_RETURN_TRUE;
        case RA2_OWNER_RETURN_FALSE: return RA2_ARRIVAL_RETURN_FALSE;
        default: return RA2_ARRIVAL_CONTINUE;
    }
}

static void publish_arrived_segment(Ra2GroundArrivalState *state,Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position,const Ra2ArrivalServices *services)
{
    /* relocate可回写状态；先落位，再废弃旧段并清选择器、采样下标。 */
    services->relocate(services->context,!same_cell(owner_position,state->segment_end));
    ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
    state->path_selector=-1;
    state->sample_index=0;
}

static int mark_reached_destination(Ra2GroundArrivalState *state,Ra2WorldPoint invalid_position,
    int32_t level_height,const Ra2ArrivalServices *services)
{
    if(services->query(services->context,RA2_ARRIVAL_TARGET_IS_CURRENT_CELL)) {
        int32_t owner_z=services->query(services->context,RA2_ARRIVAL_OWNER_REFERENCE_Z);
        /* 目的地高度在查询后读取，保留严格小于和32位回绕距离。 */
        if(ra2_ground_within_stop_height(owner_z,state->destination.z,level_height)) {
            state->destination=invalid_position;
            ra2_ground_invalidate_segment(&state->segment_end,&state->driving,invalid_position);
            state->driving=0;
            return 1;
        }
    }
    return 0;
}

Ra2ArrivalOutcome ra2_ground_finish_segment(Ra2GroundArrivalState *state,Ra2WorldPoint owner_position,
    Ra2WorldPoint invalid_position,int32_t level_height,const Ra2ArrivalServices *services)
{
    publish_arrived_segment(state,owner_position,invalid_position,services);
    int reached_target=mark_reached_destination(state,invalid_position,level_height,services);
    return finish_after_refresh(reached_target,services);
}
