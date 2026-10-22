#ifndef RA2_GROUND_PATH_SEARCH_H
#define RA2_GROUND_PATH_SEARCH_H
#include "ground_path_distance.h"
#include "ground_path_nodes.h"

typedef struct Ra2PathCell {
    Ra2PathPoint point;
    int32_t ground_level;
    unsigned has_bridge,has_region_connection;
} Ra2PathCell;

typedef struct Ra2PathSearch {
    Ra2SearchNode *current,*pending;
    uintptr_t destination,current_cell,candidate_cell;
    uint32_t expanded;
    int32_t expansion_limit;
    unsigned direction;
    uint32_t current_grid_index,candidate_grid_index;
    Ra2PathPoint candidate_point;
    int32_t candidate_region;
    unsigned lower_surface;
    float step_cost;
    unsigned ignore_soft_obstacles,continue_at_blocked_goal,restrict_to_connected_regions;
    /* 这些字段可能被引擎回调更新，使用共享视图而非复制一份旧值。 */
    int32_t *current_level,*destination_level;
    float *search_weight;
    uint8_t *movement_mode;
    uint32_t *region_cursor,*last_region_point;
    const uint16_t *region_route;
    const uint32_t *connected_regions;
    Ra2PathNodeCache cache;
    Ra2PathHeap *open;
    uint32_t grid_width;
    double cache_epsilon;
    const float *direction_bias;
    uint16_t numeric_control;
} Ra2PathSearch;

typedef struct Ra2PathSearchServices {
    void *context;
    /* 返回“地图格指针的地址”；其值为零表示该邻居不存在。第 8 项为特殊连接。 */
    uintptr_t (*neighbor)(void *,uintptr_t,unsigned);
    int (*cell)(void *,uintptr_t,Ra2PathCell *);
    int32_t (*neighbor_grid_offset)(void *,unsigned);
    int32_t (*region)(void *,const Ra2PathSearch *);
    int32_t (*passage)(void *,const Ra2PathSearch *);
    double (*traversal_cost)(void *,const Ra2PathSearch *,int32_t);
    Ra2SearchNode *(*create_node)(void *,const Ra2PathSearch *);
} Ra2PathSearchServices;

typedef enum Ra2PathSearchStop {
    RA2_SEARCH_LIMIT,RA2_SEARCH_REACHED_GOAL,RA2_SEARCH_BLOCKED_GOAL,RA2_SEARCH_EMPTY
} Ra2PathSearchStop;
/* 已连通区域通常直接通过。未标记区域仅在下层、无连接标记且启用限制时拒绝。
 * 上层和格自身的连接标记都是原版的豁免条件。 */
int ra2_path_region_allows(uint32_t region_stamp,uint32_t generation,unsigned lower_surface,
    unsigned cell_has_connection,unsigned restrict_regions);
/* 运行完整的九邻居展开和取出循环。建图、通行查询、地形代价以及节点启发式
 * 由服务提供，调用顺序属于行为兼容的一部分。 */
Ra2PathSearchStop ra2_path_search_neighbors(Ra2PathSearch *search,const Ra2PathSearchServices *services);
#endif
