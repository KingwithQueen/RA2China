#pragma once
#include <stdint.h>
uint32_t ra2_ground_special_obstacle_bridge(void);
uint32_t ra2_ground_template_select_bridge(unsigned entry);
void ra2_ground_template_commit_bridge(int skip_shift);

uint32_t ra2_ground_clearance_bridge(int clear_only);
uint32_t ra2_ground_traffic_wait_bridge(void);
void ra2_ground_reaction_bridge(unsigned entry);
uint32_t ra2_ground_prepare_entry_bridge(void);
uint32_t ra2_ground_retry_path_bridge(void);
uint32_t ra2_ground_observe_obstacle_bridge(int rebuilt);
uint32_t ra2_ground_prepare_segment_bridge(void);
