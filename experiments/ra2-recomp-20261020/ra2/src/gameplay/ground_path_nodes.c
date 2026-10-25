#include "ground_path_nodes.h"
#include "ground_path_cost.h"
#include <stddef.h>
#include <string.h>

static void initialize_node_state(Ra2SearchNode *node,Ra2PathLink *link,
    const Ra2PathNodeInput *input,uint16_t control)
{
    if(!input->parent) {
        link->surface_level=input->root_surface_level;
        node->accumulated_cost=0;
        node->path_length=1;
    } else {
        link->surface_level=input->cell_level;
        if(input->cell_has_bridge) {
            if(input->parent_cell_has_bridge) {
                if(link->parent->surface_level==input->parent_cell_level+4)link->surface_level+=4;
            } else {
                int32_t difference=input->cell_level-link->parent->surface_level+3;
                if(difference>=-1 && difference<=1)link->surface_level+=4;
            }
        }
        node->accumulated_cost=ra2_ground_accumulate_path_cost(input->parent->accumulated_cost,input->step_cost,control);
        /* 原版长度字段以 32 位加法更新。 */
        uint32_t length=(uint32_t)input->parent->path_length+1u;
        memcpy(&node->path_length,&length,sizeof(length));
    }
}

Ra2SearchNode *ra2_path_node_create(Ra2PathNodeStorage *storage,const Ra2PathNodeInput *input,uint16_t control)
{
    /* 容量由搜索上下文保证；节点先于链分配，各计数仍在取址时递增。 */
    Ra2SearchNode *node=&storage->nodes[(*storage->used_nodes)++];
    Ra2PathLink *link=&storage->links[(*storage->used_links)++];
    link->cell_reference=input->cell_reference;
    link->parent=input->parent?(Ra2PathLink *)input->parent->path_link:NULL;
    initialize_node_state(node,link,input,control);
    /* 链与节点状态就绪后再发布关联；priority仍留待距离服务生成。 */
    node->path_link=link;
    /* priority 稍后由原距离近似服务与累计代价生成，不改写池中的旧值。 */
    return node;
}

static const Ra2PathCacheLayer *layer(const Ra2PathNodeCache *cache,unsigned lower)
{ return lower?&cache->lower:&cache->upper; }

uint32_t ra2_path_cache_read_stamp(const Ra2PathNodeCache *cache,uint32_t cell,unsigned lower)
{ return layer(cache,lower)->stamps[cell]; }
float ra2_path_cache_read_cost(const Ra2PathNodeCache *cache,uint32_t cell,unsigned lower)
{ return layer(cache,lower)->costs[cell]; }
void ra2_path_cache_write_cost(Ra2PathNodeCache *cache,uint32_t cell,unsigned lower,float cost)
{ layer(cache,lower)->costs[cell]=cost; }
void ra2_path_cache_publish(Ra2PathNodeCache *cache,uint32_t cell,unsigned lower,float cost)
{
    layer(cache,lower)->stamps[cell]=*cache->generation;
    layer(cache,lower)->costs[cell]=cost;
}

static void clear_wrapped_generation(Ra2PathNodeCache *cache,uint32_t cell_count,
    Ra2PathRegionCache regions[3])
{
    /* 只清代次标记，不清代价、节点旧内容或历史堆地址界限。 */
    for(uint32_t i=0;i<cell_count;++i)cache->lower.stamps[i]=cache->upper.stamps[i]=0;
    for(unsigned group=0;group<3;++group)
        for(uint32_t i=0;i<regions[group].count;++i)
            for(unsigned side=0;side<3;++side)regions[group].stamps[side][i]=0;
}

void ra2_path_search_reset(Ra2PathNodeStorage *storage,Ra2PathHeap *open,Ra2PathHeap *auxiliary,
    Ra2PathNodeCache *cache,uint32_t cell_count,Ra2PathRegionCache regions[3])
{
    *storage->used_links=0;
    *storage->used_nodes=0;
    ra2_path_heap_clear(open);
    ra2_path_heap_clear(auxiliary);
    ++*cache->generation;
    if(*cache->generation)return;
    clear_wrapped_generation(cache,cell_count,regions);
    ++*cache->generation;
}
