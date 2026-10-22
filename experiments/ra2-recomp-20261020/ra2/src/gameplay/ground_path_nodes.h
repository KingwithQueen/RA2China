#ifndef RA2_GROUND_PATH_NODES_H
#define RA2_GROUND_PATH_NODES_H
#include "ground_path_heap.h"

typedef struct Ra2PathLink {
    void *cell_reference;
    int32_t surface_level;
    struct Ra2PathLink *parent;
} Ra2PathLink;
typedef struct Ra2PathNodeStorage {
    Ra2SearchNode *nodes;
    uint32_t *used_nodes;
    Ra2PathLink *links;
    uint32_t *used_links;
} Ra2PathNodeStorage;
typedef struct Ra2PathNodeInput {
    Ra2SearchNode *parent;
    void *cell_reference;
    int32_t cell_level;
    int32_t parent_cell_level;
    int32_t root_surface_level;
    unsigned cell_has_bridge,parent_cell_has_bridge;
    float step_cost;
} Ra2PathNodeInput;

/* 存储容量由搜索上下文保证，保持原版的追加分配及计数顺序。
 * root 从上下文继承当前表面高度；后继按桥面连接关系选择地面/桥面。 */
Ra2SearchNode *ra2_path_node_create(Ra2PathNodeStorage *storage,const Ra2PathNodeInput *input,uint16_t control);

typedef struct Ra2PathCacheLayer {
    uint32_t *stamps;
    float *costs;
} Ra2PathCacheLayer;
typedef struct Ra2PathNodeCache {
    Ra2PathCacheLayer lower,upper;
    uint32_t *generation;
} Ra2PathNodeCache;
typedef struct Ra2PathRegionCache {
    uint32_t *stamps[3];
    uint32_t count;
} Ra2PathRegionCache;

uint32_t ra2_path_cache_read_stamp(const Ra2PathNodeCache *cache,uint32_t cell,unsigned lower);
float ra2_path_cache_read_cost(const Ra2PathNodeCache *cache,uint32_t cell,unsigned lower);
void ra2_path_cache_write_cost(Ra2PathNodeCache *cache,uint32_t cell,unsigned lower,float cost);
/* 发布顺序与原版相同：先写本轮标记，再写累计代价；旧轮次的代价不清零。 */
void ra2_path_cache_publish(Ra2PathNodeCache *cache,uint32_t cell,unsigned lower,float cost);
/* 新搜索复用节点/链池及两个堆；只有 generation 回绕到零才清全部标记，随后从 1 开始。 */
void ra2_path_search_reset(Ra2PathNodeStorage *storage,Ra2PathHeap *open,Ra2PathHeap *auxiliary,
    Ra2PathNodeCache *cache,uint32_t cell_count,Ra2PathRegionCache regions[3]);
#endif
