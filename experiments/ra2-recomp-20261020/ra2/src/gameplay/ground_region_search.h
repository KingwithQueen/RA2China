#ifndef RA2_GROUND_REGION_SEARCH_H
#define RA2_GROUND_REGION_SEARCH_H
#include "ground_region_route.h"
#include "ground_path_distance.h"

typedef struct Ra2RegionEdge {uint32_t destination; uint8_t surcharge, reserved[3];} Ra2RegionEdge;
typedef struct Ra2RegionView {
    const Ra2RegionEdge *edges;
    int32_t edge_count;
    uint16_t parent_region;
    uint32_t terrain;
} Ra2RegionView;
typedef struct Ra2RegionHeap {
    uint32_t count, capacity;
    Ra2RegionRouteNode **items;
    uintptr_t highest_node_address, lowest_node_address;
} Ra2RegionHeap;
typedef struct Ra2BlockedRegionEdges {const uint32_t *pairs; int32_t count;} Ra2BlockedRegionEdges;
typedef struct Ra2RegionLayer {
    uint32_t *connected, *visited;
    float *costs;
    uint16_t *route;
    uint32_t *route_count;
} Ra2RegionLayer;
typedef struct Ra2RegionSearch {
    const uint32_t *generation;
    Ra2RegionLayer layers[3];
    Ra2RegionRouteNode *nodes;
    Ra2RegionHeap *heap;
    const int32_t *terrain_allowed;
    const float *terrain_cost;
    uint16_t *numeric_control;
    uint16_t integer_conversion_control;
} Ra2RegionSearch;
typedef struct Ra2RegionSearchServices {
    void *context;
    double (*owner_factor)(void *context);
    uint32_t (*owner_house)(void *context);
    int32_t (*region_at)(void *context, const Ra2PathPoint *point, unsigned layer);
    Ra2RegionView (*region)(void *context, unsigned layer, uint32_t id);
    int32_t (*edge_penalty)(void *context, uint32_t house, unsigned layer, uint32_t from, uint32_t to);
    Ra2BlockedRegionEdges (*blocked_edges)(void *context, unsigned layer);
} Ra2RegionSearchServices;
/* 三层由粗到细搜索，上一层连通标记约束下一层。容量及有效区域编号由原版地图保证。
 * 失败时保留已完成的粗层路线；同区域仅发布一项，不能清除其他池/缓存内容。 */
int ra2_region_search(Ra2RegionSearch *search, const Ra2RegionSearchServices *services,
    const Ra2PathPoint *start, const Ra2PathPoint *goal, int has_owner);
#endif
