#ifndef RA2_COMBAT_MANAGER_FORWARD_FIND_BRIDGE_H
#define RA2_COMBAT_MANAGER_FORWARD_FIND_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerForwardFindFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerForwardFindFlags;

int ra2_manager_forward_find_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerForwardFindFlags *flags);

#endif
