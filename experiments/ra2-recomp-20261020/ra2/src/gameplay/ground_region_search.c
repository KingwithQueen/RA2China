#include "ground_region_search.h"
#include "x87_arithmetic.h"
#include <stddef.h>

/* 区域堆直接入队；格子搜索的 pending 节点规则不适用于这里。平分时保留原先顺序。 */
static void offer(Ra2RegionHeap *heap, Ra2RegionRouteNode *node)
{
    uint32_t slot=heap->count+1;
    if(slot>=heap->capacity)return;
    while(slot>1 && heap->items[slot/2]->cost>node->cost) {
        heap->items[slot]=heap->items[slot/2]; slot/=2;
    }
    heap->items[slot]=node; ++heap->count;
    uintptr_t address=(uintptr_t)node;
    if(address>heap->highest_node_address)heap->highest_node_address=address;
    if(address<heap->lowest_node_address)heap->lowest_node_address=address;
}
static Ra2RegionRouteNode *take(Ra2RegionHeap *heap)
{
    if(!heap->count)return NULL;
    Ra2RegionRouteNode *result=heap->items[1];
    heap->items[1]=heap->items[heap->count]; heap->items[heap->count--]=NULL;
    for(uint32_t slot=1;;) {
        uint32_t chosen=slot,left=slot*2,right=left+1;
        if(left<=heap->count && heap->items[chosen]->cost>heap->items[left]->cost)chosen=left;
        if(right<=heap->count && heap->items[chosen]->cost>heap->items[right]->cost)chosen=right;
        if(chosen==slot)break;
        Ra2RegionRouteNode *temporary=heap->items[slot];
        heap->items[slot]=heap->items[chosen]; heap->items[chosen]=temporary; slot=chosen;
    }
    return result;
}
static int blocked(Ra2BlockedRegionEdges list,uint32_t from,uint32_t to)
{
    uint32_t a=(uint16_t)from,b=(uint16_t)to;
    uint32_t pair=a<b?(a<<16)|b:(b<<16)|a;
    for(int32_t i=list.count;i>0;)if(list.pairs[--i]==pair)return 1;
    return 0;
}
static float cost(const Ra2RegionSearch *s,float parent,uint32_t terrain,int32_t penalty,unsigned surcharge)
{
    Ra2LegacyReal value=ra2_real_add(ra2_real_from_f32(s->terrain_cost[terrain]),ra2_real_from_f32(parent),*s->numeric_control);
    value=ra2_real_add(value,ra2_real_from_i32(penalty),*s->numeric_control);
    value=ra2_real_add(value,ra2_real_from_f64(surcharge?0.001:0.0),*s->numeric_control);
    return ra2_real_store_f32(value,*s->numeric_control);
}
int ra2_region_search(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    const Ra2PathPoint *start,const Ra2PathPoint *goal,int has_owner)
{
    double factor=0.0; uint32_t house=0;
    if(has_owner){factor=v->owner_factor(v->context);house=v->owner_house(v->context);}
    int use_penalty=factor>0.00001;
    for(int layer=2;layer>=0;--layer) {
        Ra2RegionHeap *heap=s->heap;
        for(uint32_t i=0;i<=heap->count;++i)heap->items[i]=NULL;
        heap->count=0; /* 地址上下界是历史记录，不随一层搜索清空。 */
        uint32_t first=(uint32_t)v->region_at(v->context,start,(unsigned)layer);
        uint32_t target=(uint32_t)v->region_at(v->context,goal,(unsigned)layer);
        Ra2RegionLayer *cache=&s->layers[layer];
        cache->connected[first]=*s->generation; cache->connected[target]=*s->generation;
        if(first==target) {
            if(!layer){s->nodes[0].region=first;s->nodes[0].depth=0;}
            cache->route[0]=(uint16_t)first;*cache->route_count=1;continue;
        }
        s->nodes[0]=(Ra2RegionRouteNode){-1,first,0.0f,0};offer(heap,s->nodes);
        cache->visited[first]=*s->generation;cache->costs[first]=0.0f;
        uint32_t next_node=1;
        Ra2RegionRouteNode *current=take(heap);
        int initially_unblocked=v->blocked_edges(v->context,(unsigned)layer).count==0;
        while(current) {
            if(current->region==target)break;
            Ra2RegionView region=v->region(v->context,(unsigned)layer,current->region);
            for(int32_t i=0;i<region.edge_count;++i) {
                Ra2RegionEdge edge=region.edges[i];
                Ra2RegionView adjacent=v->region(v->context,(unsigned)layer,edge.destination);
                int32_t penalty=0;
                if(use_penalty) {
                    penalty=v->edge_penalty(v->context,house,(unsigned)layer,current->region,edge.destination);
                    Ra2LegacyReal weighted=ra2_real_multiply(ra2_real_from_i32(penalty),ra2_real_from_f64(factor),*s->numeric_control);
                    /* 77F110 会切换整数转换控制字且不恢复，后续区域代价也沿用它。 */
                    *s->numeric_control=s->integer_conversion_control;
                    penalty=ra2_real_round_i32(weighted,*s->numeric_control);
                }
                float proposed=cost(s,current->cost,adjacent.terrain,penalty,edge.surcharge);
                if(cache->visited[edge.destination]==*s->generation && cache->costs[edge.destination]<=proposed)continue;
                if(layer!=2 && s->layers[layer+1].connected[adjacent.parent_region]!=*s->generation && adjacent.terrain!=1)continue;
                if(s->terrain_allowed[adjacent.terrain]!=1)continue;
                if(!initially_unblocked && blocked(v->blocked_edges(v->context,(unsigned)layer),current->region,edge.destination))continue;
                Ra2RegionRouteNode *node=&s->nodes[next_node];
                *node=(Ra2RegionRouteNode){(int32_t)(current-s->nodes),edge.destination,proposed,current->depth+1};
                offer(heap,node);
                /* 原版即使堆满仍发布访问代价并消耗池槽位。 */
                cache->visited[edge.destination]=*s->generation;cache->costs[edge.destination]=proposed;++next_node;
            }
            current=take(heap);
        }
        if(!current)return 0;
        ra2_region_route_publish(s->nodes,current,*s->generation,cache->connected,cache->route,cache->route_count);
    }
    return 1;
}
