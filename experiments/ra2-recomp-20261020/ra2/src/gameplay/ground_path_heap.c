#include "ground_path_heap.h"
#include <stddef.h>

void ra2_path_heap_finish_offer(Ra2PathHeap *heap,Ra2SearchNode *node,uint32_t slot)
{
    heap->items[slot]=node;
    ++heap->count;
    uintptr_t address=(uintptr_t)node;
    if(address>heap->highest_node_address)heap->highest_node_address=address;
    if(address<heap->lowest_node_address)heap->lowest_node_address=address;
}

static int has_free_slot(const Ra2PathHeap *heap)
{
    /* capacity包含闲置的0号槽；先比较再加一，零容量和计数回绕均不能发布。 */
    return heap->capacity>0 && heap->count<heap->capacity-1u;
}

static int try_push(Ra2PathHeap *heap,Ra2SearchNode *node)
{
    if(!has_free_slot(heap))return 0;
    uint32_t slot=heap->count+1;
    while(slot>1) {
        uint32_t parent=slot/2;
        if(!(heap->items[parent]->priority>node->priority))break;
        heap->items[slot]=heap->items[parent];
        slot=parent;
    }
    ra2_path_heap_finish_offer(heap,node,slot);
    return 1;
}

Ra2SearchNode *ra2_path_heap_offer(Ra2PathHeap *heap,Ra2SearchNode *pending,Ra2SearchNode *candidate)
{
    if(!pending)return candidate;
    if(try_push(heap,pending))return candidate;
    /* 用户允许寻路改进：满堆不增加内存，保留两候选中分数较低者；同分仍选新的。 */
    return pending->priority<candidate->priority?pending:candidate;
}

static void swap(Ra2PathHeap *heap,uint32_t a,uint32_t b)
{
    Ra2SearchNode *temporary=heap->items[a];
    heap->items[a]=heap->items[b];
    heap->items[b]=temporary;
}

static void sift_down(Ra2PathHeap *heap,uint32_t slot)
{
    for(;;) {
        uint32_t chosen=slot,left=slot*2,right=left+1;
        if(left<=heap->count && heap->items[chosen]->priority>heap->items[left]->priority)chosen=left;
        if(right<=heap->count && heap->items[chosen]->priority>heap->items[right]->priority)chosen=right;
        if(chosen==slot)return;
        swap(heap,slot,chosen);
        slot=chosen;
    }
}

void ra2_path_heap_swap_and_sift(Ra2PathHeap *heap,uint32_t parent,uint32_t child)
{
    swap(heap,parent,child);
    sift_down(heap,child);
}

Ra2SearchNode *ra2_path_heap_take(Ra2PathHeap *heap,Ra2SearchNode *pending)
{
    if(pending) {
        if(!heap->count || heap->items[1]->priority>pending->priority)return pending;
        Ra2SearchNode *result=heap->items[1];
        heap->items[1]=pending;
        sift_down(heap,1);
        return result;
    }
    if(!heap->count)return NULL;
    Ra2SearchNode *result=heap->items[1];
    heap->items[1]=heap->items[heap->count];
    heap->items[heap->count]=NULL;
    --heap->count;
    sift_down(heap,1);
    return result;
}

void ra2_path_heap_clear(Ra2PathHeap *heap)
{
    for(uint32_t i=0;i<=heap->count;++i)heap->items[i]=NULL;
    heap->count=0;
}
