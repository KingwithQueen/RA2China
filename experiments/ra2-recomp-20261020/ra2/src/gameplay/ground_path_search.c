#include <string.h>
#include "ground_path_search.h"
#include "ground_path_cache.h"
#include "ground_path_cost.h"

static uint32_t level_difference(int32_t a,int32_t b)
{
    /* 与原版 SUB/CDQ/XOR/SUB 相同，避免有符号溢出。有效高度差远小于 INT32_MAX。 */
    uint32_t delta=(uint32_t)a-(uint32_t)b;
    return delta&0x80000000u?0u-delta:delta;
}
int ra2_path_region_allows(uint32_t stamp,uint32_t generation,unsigned lower,unsigned connection,unsigned restrict_regions)
{return stamp==generation || !lower || connection || !restrict_regions;}

static int cached_candidate_is_cheaper(const Ra2PathSearch *s)
{
    if(ra2_path_cache_read_stamp(&s->cache,s->candidate_grid_index,s->lower_surface)!=*s->cache.generation)return 0;
    return ra2_ground_path_cache_compare(ra2_path_cache_read_cost(&s->cache,s->candidate_grid_index,s->lower_surface),
        s->current->accumulated_cost,s->cache_epsilon,s->numeric_control)<0;
}
static void publish_candidate(Ra2PathSearch *s,const Ra2PathSearchServices *v)
{
    Ra2SearchNode *node=v->create_node(v->context,s);
    s->pending=ra2_path_heap_offer(s->open,s->pending,node);
    ra2_path_cache_publish(&s->cache,s->candidate_grid_index,s->lower_surface,node->accumulated_cost);
    /* 原版将 itinerary 项零扩展，而 candidate_region 来自有符号 short。 */
    if(s->candidate_region==(int32_t)s->region_route[*s->region_cursor]) {
        ++*s->region_cursor;
        memcpy(s->last_region_point,&s->candidate_point,sizeof(s->candidate_point));
    }
}
Ra2PathSearchStop ra2_path_search_neighbors(Ra2PathSearch *s,const Ra2PathSearchServices *v)
{
    for(;;) {
        if((int32_t)s->expanded>=s->expansion_limit)return RA2_SEARCH_LIMIT;
        Ra2PathLink *link=s->current->path_link;
        s->current_cell=(uintptr_t)link->cell_reference;
        if(s->current_cell==s->destination && link->surface_level==*s->destination_level)return RA2_SEARCH_REACHED_GOAL;
        Ra2PathCell current;
        v->cell(v->context,s->current_cell,&current);
        s->current_grid_index=(uint32_t)current.point.y*s->grid_width+(uint32_t)(int32_t)current.point.x;
        s->pending=NULL;
        for(s->direction=0;s->direction<=8;++s->direction) {
            s->candidate_cell=v->neighbor(v->context,s->current_cell,s->direction);
            Ra2PathCell candidate;
            if(!v->cell(v->context,s->candidate_cell,&candidate))continue;
            s->candidate_point=candidate.point;
            s->candidate_grid_index=s->direction==8?
                (uint32_t)candidate.point.y*s->grid_width+(uint32_t)(int32_t)candidate.point.x:
                s->current_grid_index+(uint32_t)v->neighbor_grid_offset(v->context,s->direction);
            s->lower_surface=!candidate.has_bridge || level_difference(*s->current_level,candidate.ground_level)<=1;
            s->candidate_region=v->region(v->context,s);
            v->cell(v->context,s->candidate_cell,&candidate);
            if(!ra2_path_region_allows(s->connected_regions[s->candidate_region],*s->cache.generation,
                s->lower_surface,candidate.has_region_connection,s->restrict_to_connected_regions))continue;
            if(cached_candidate_is_cheaper(s))continue;
            int32_t passage=v->passage(v->context,s);
            if(s->ignore_soft_obstacles && passage<7)passage=0;
            if(s->direction==8) {
                v->cell(v->context,s->current_cell,&current);
                v->cell(v->context,s->candidate_cell,&candidate);
                s->step_cost=ra2_path_connection_distance(current.point,candidate.point);
            } else {
                double cost=v->traversal_cost(v->context,s,passage);
                s->step_cost=ra2_ground_score_path_step(cost,*s->search_weight,s->direction_bias[s->direction],s->numeric_control);
            }
            if(passage<7) {
                /* 通行/代价服务可能已发布该格，必须在建节点前再读一次标记。 */
                if(ra2_path_cache_read_stamp(&s->cache,s->candidate_grid_index,s->lower_surface)==*s->cache.generation)continue;
                publish_candidate(s,v);
            } else if(s->candidate_cell==s->destination && !s->continue_at_blocked_goal &&
                level_difference(*s->current_level,*s->destination_level)<=1)return RA2_SEARCH_BLOCKED_GOAL;
        }
        s->current=ra2_path_heap_take(s->open,s->pending);
        if(s->current)*s->current_level=((Ra2PathLink *)s->current->path_link)->surface_level;
        ++s->expanded;
        if(!s->current)return RA2_SEARCH_EMPTY;
    }
}
