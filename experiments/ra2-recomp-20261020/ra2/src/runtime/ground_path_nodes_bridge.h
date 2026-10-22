#ifndef RA2_GROUND_PATH_NODES_BRIDGE_H
#define RA2_GROUND_PATH_NODES_BRIDGE_H
#include <stdint.h>
void ra2_path_node_create_bridge(void);
uint32_t ra2_path_cache_stamp_bridge(uint32_t context,unsigned lower,uint32_t byte_offset);
float ra2_path_cache_cost_bridge(uint32_t context,unsigned lower,uint32_t byte_offset);
void ra2_path_cache_publish_bridge(unsigned cost_only);
void ra2_path_search_reset_bridge(void);
#endif
