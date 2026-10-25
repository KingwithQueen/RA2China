#include "ground_reaction.h"
#include "ground_failure_transition.h"

static int stop_at_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    const Ra2ReactionServices *services)
{
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    int target = !!services->has_target_488(services->context);
    return ra2_ground_stop_target(target, services->context, services->cancel_target, services->stop_navigation);
}

/* 分派码与保存的通行结果分别处理；友方障碍只改本次路径头和标志。 */
static Ra2ReactionEntry select_obstacle_response(Ra2ReactionEntry entry,
    int32_t dispatch_code,int32_t *path_head,uint32_t *flags)
{
    if(entry!=RA2_REACTION_DISPATCH)return entry;
    if(dispatch_code==RA2_CELL_FRIENDLY_OBSTACLE) {
        *path_head=-1;
        *flags=0;
        return RA2_REACTION_ATTACK;
    }
    return dispatch_code==RA2_CELL_DESTROYABLE ? RA2_REACTION_ATTACK:RA2_REACTION_REPORT;
}

static void attack_obstacle_target(int32_t path_head,uint32_t flags,
    const Ra2ReactionServices *services)
{
    if(services->find_object(services->context,flags)) {
        /* 敌我判断前重取对象；攻击服务仍自行取得当时目标，不缓存跨回调对象。 */
        uint32_t object=services->find_object(services->context,flags);
        if(!services->object_allied(services->context,object))
            services->attack_object(services->context,flags);
    } else if(services->has_overlay(services->context,path_head)
        && services->overlay_is_wall(services->context)) {
        services->attack_wall(services->context,flags);
    }
}

static int finish_obstacle_response(Ra2GroundPrepareState *state,Ra2WorldPoint invalid_position,
    int32_t passage,int allow_recursive,const Ra2ReactionServices *services)
{
    if(passage==RA2_CELL_BLOCKED) {
        if(allow_recursive)return services->retry_recursively(services->context,-1,0);
        return stop_at_obstacle(state,invalid_position,services);
    }
    services->clear_pending_and_selector(services->context);
    return 1;
}

int ra2_ground_react_to_obstacle(Ra2GroundPrepareState *state,Ra2WorldPoint invalid_position,
    Ra2ReactionEntry entry,int32_t dispatch_code,int32_t passage,int allow_recursive,
    int32_t path_head,uint32_t flags,const Ra2ReactionServices *services)
{
    entry=select_obstacle_response(entry,dispatch_code,&path_head,&flags);
    if(entry==RA2_REACTION_REPORT) {
        if(services->sound_pending(services->context))services->play_sound(services->context);
    } else if(entry==RA2_REACTION_ATTACK) {
        /* 递归即为当前出口，失败返回也不能继续落入后续收尾。 */
        if(allow_recursive)return services->retry_recursively(services->context,path_head,flags);
        attack_obstacle_target(path_head,flags,services);
    }
    return finish_obstacle_response(state,invalid_position,passage,allow_recursive,services);
}
