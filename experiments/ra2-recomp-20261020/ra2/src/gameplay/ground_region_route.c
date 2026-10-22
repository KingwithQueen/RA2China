#include "ground_region_route.h"
void ra2_region_route_publish(const Ra2RegionRouteNode *pool, const Ra2RegionRouteNode *end,
    uint32_t generation, uint32_t *connected, uint16_t *route, uint32_t *route_count)
{
    const Ra2RegionRouteNode *node = end;
    while (node->parent_index != -1) {
        connected[node->region] = generation;
        node = &pool[node->parent_index];
    }
    *route_count = (uint32_t)end->depth + 1;
    node = end;
    for (int32_t position = end->depth; position > 0; --position) {
        route[position] = (uint16_t)node->region;
        node = &pool[node->parent_index];
    }
    route[0] = (uint16_t)node->region;
}
