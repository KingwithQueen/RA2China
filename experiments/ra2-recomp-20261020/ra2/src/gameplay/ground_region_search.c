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
static Ra2RegionLayer *prepare_layer(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    const Ra2PathPoint *start,const Ra2PathPoint *goal,unsigned layer,Ra2RegionHeap *heap,
    uint32_t *first,uint32_t *target)
{
    /* 堆在查询前取快照；地址上下界是历史记录，只清条目与计数。 */
    for(uint32_t i=0;i<=heap->count;++i)heap->items[i]=NULL;
    heap->count=0;
    *first=(uint32_t)v->region_at(v->context,start,layer);
    *target=(uint32_t)v->region_at(v->context,goal,layer);
    /* 两次区域查询之后才选取本层缓存，并分别发布起点与终点的连通代次。 */
    Ra2RegionLayer *cache=&s->layers[layer];
    cache->connected[*first]=*s->generation;cache->connected[*target]=*s->generation;
    return cache;
}

static void publish_same_region(Ra2RegionSearch *s,Ra2RegionLayer *cache,unsigned layer,uint32_t first)
{
    /* 同区域只写原先的字段，不清节点其余内容，也不查询禁行边。 */
    if(!layer){s->nodes[0].region=first;s->nodes[0].depth=0;}
    cache->route[0]=(uint16_t)first;*cache->route_count=1;
}

static void seed_layer_frontier(Ra2RegionSearch *s,Ra2RegionHeap *heap,
    Ra2RegionLayer *cache,uint32_t first)
{
    s->nodes[0]=(Ra2RegionRouteNode){-1,first,0.0f,0};offer(heap,s->nodes);
    cache->visited[first]=*s->generation;cache->costs[first]=0.0f;
}

static float proposed_edge_cost(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    unsigned layer,uint32_t house,const Ra2RegionRouteNode *current,const Ra2RegionView *adjacent,
    const Ra2RegionEdge *edge,int use_penalty,double factor)
{
    int32_t penalty=0;
    if(use_penalty) {
        penalty=v->edge_penalty(v->context,house,layer,current->region,edge->destination);
        Ra2LegacyReal weighted=ra2_real_multiply(ra2_real_from_i32(penalty),ra2_real_from_f64(factor),*s->numeric_control);
        /* 先按当时的控制字乘权重，再切换整数转换控制；后续代价沿用该控制。 */
        *s->numeric_control=s->integer_conversion_control;
        penalty=ra2_real_round_i32(weighted,*s->numeric_control);
    }
    /* 罚分服务之后才读取父代价；即使边随后被限制，也先完成代价计算。 */
    return cost(s,current->cost,adjacent->terrain,penalty,edge->surcharge);
}

static int edge_is_eligible(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    int layer,Ra2RegionLayer *cache,const Ra2RegionRouteNode *current,
    const Ra2RegionView *adjacent,const Ra2RegionEdge *edge,float proposed,int initially_unblocked)
{
    if(cache->visited[edge->destination]==*s->generation && cache->costs[edge->destination]<=proposed)return 0;
    if(layer!=2 && s->layers[layer+1].connected[adjacent->parent_region]!=*s->generation && adjacent->terrain!=1)return 0;
    if(s->terrain_allowed[adjacent->terrain]!=1)return 0;
    /* 每层首次禁行列表为空时免查；否则仅在前面限制均通过后重读列表。 */
    if(!initially_unblocked && blocked(v->blocked_edges(v->context,(unsigned)layer),current->region,edge->destination))return 0;
    return 1;
}

int ra2_region_search(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    const Ra2PathPoint *start,const Ra2PathPoint *goal,int has_owner)
{
    double factor=0.0; uint32_t house=0;
    if(has_owner){factor=v->owner_factor(v->context);house=v->owner_house(v->context);}
    int use_penalty=factor>0.00001;
    for(int layer=2;layer>=0;--layer) {
        Ra2RegionHeap *heap=s->heap;
        uint32_t first,target;
        Ra2RegionLayer *cache=prepare_layer(s,v,start,goal,(unsigned)layer,heap,&first,&target);
        if(first==target) {
            publish_same_region(s,cache,(unsigned)layer,first);continue;
        }
        seed_layer_frontier(s,heap,cache,first);
        uint32_t next_node=1;
        Ra2RegionRouteNode *current=take(heap);
        int initially_unblocked=v->blocked_edges(v->context,(unsigned)layer).count==0;
        while(current) {
            if(current->region==target)break;
            Ra2RegionView region=v->region(v->context,(unsigned)layer,current->region);
            for(int32_t i=0;i<region.edge_count;++i) {
                Ra2RegionEdge edge=region.edges[i];
                Ra2RegionView adjacent=v->region(v->context,(unsigned)layer,edge.destination);
                float proposed=proposed_edge_cost(s,v,(unsigned)layer,house,current,&adjacent,&edge,use_penalty,factor);
                if(!edge_is_eligible(s,v,layer,cache,current,&adjacent,&edge,proposed,initially_unblocked))continue;
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
