#ifndef RA2_COMBAT_MANAGER_SECOND_INNER_INIT_BRIDGE_H
#define RA2_COMBAT_MANAGER_SECOND_INNER_INIT_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerSecondInnerInitFlags { uint32_t kind, left, right, carry; } Ra2ManagerSecondInnerInitFlags;

void ra2_manager_second_inner_init_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerSecondInnerInitFlags *flags);

#endif
