#ifndef RA2_GROUND_PATH_HEAP_H
#define RA2_GROUND_PATH_HEAP_H
#include <stdint.h>

typedef struct Ra2SearchNode {
    void *path_link;
    float accumulated_cost;
    float priority;
    int32_t path_length;
} Ra2SearchNode;

/* 原版一基下标堆。capacity 包含闲置的 0 号槽，最多容纳 capacity-1 个节点。
 * 地址上下界只记录曾经入堆的节点，不参与评分，也不在出堆时缩小。 */
typedef struct Ra2PathHeap {
    uint32_t count;
    uint32_t capacity;
    Ra2SearchNode **items;
    uintptr_t highest_node_address;
    uintptr_t lowest_node_address;
} Ra2PathHeap;

/* pending 表示单独暂存的候选，不保证分数最优。
 * 原版 427939 的 INC 覆盖了此前的评分比较标志：合法堆计数下总是把旧候选入堆，暂存最新候选。
 * 满堆时旧候选入堆失败，仍暂存最新候选。这里保留原版行为，不改成标准的仅保留最优值。 */
Ra2SearchNode *ra2_path_heap_offer(Ra2PathHeap *heap,Ra2SearchNode *pending,Ra2SearchNode *candidate);
/* pending 与堆根同分时先取堆根；下沉时相等则不交换，左右同分优先左侧。 */
Ra2SearchNode *ra2_path_heap_take(Ra2PathHeap *heap,Ra2SearchNode *pending);
/* 旧版内部共享入口的接续接口：调用者已经完成上浮或选择了首次交换位置。 */
void ra2_path_heap_finish_offer(Ra2PathHeap *heap,Ra2SearchNode *node,uint32_t slot);
void ra2_path_heap_swap_and_sift(Ra2PathHeap *heap,uint32_t parent,uint32_t child);
/* 清空 0..count，保留容量、存储和历史地址界限。 */
void ra2_path_heap_clear(Ra2PathHeap *heap);
#endif
