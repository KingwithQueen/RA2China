#pragma once
#include <stdint.h>
#include "ground_return_plan.h"
uint32_t ra2_ground_template_entry_bridge(unsigned entry);
uint32_t ra2_ground_passage_entry_bridge(void);
void ra2_ground_return_frame(uint32_t frame,Ra2GroundFrameKind kind,uint32_t result);
