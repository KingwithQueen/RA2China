#ifndef RA2_GROUND_REGION_ROUTE_H
#define RA2_GROUND_REGION_ROUTE_H
#include <stdint.h>
typedef struct Ra2RegionRouteNode {
    int32_t parent_index;
    uint32_t region;
    float cost;
    int32_t depth;
} Ra2RegionRouteNode;
/* 终点父链转换成从起点到终点的区域序列。
 * 连接标记不包含根区域；输出路径包含根，保留区域编号的低16位。
 * 池、路径及标记容量由调用者按原版合法搜索结果保证。 */
void ra2_region_route_publish(const Ra2RegionRouteNode *pool, const Ra2RegionRouteNode *end,
    uint32_t generation, uint32_t *connected, uint16_t *route, uint32_t *route_count);
#endif
