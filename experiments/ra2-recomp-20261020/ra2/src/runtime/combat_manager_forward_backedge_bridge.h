#ifndef RA2_COMBAT_MANAGER_FORWARD_BACKEDGE_BRIDGE_H
#define RA2_COMBAT_MANAGER_FORWARD_BACKEDGE_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerForwardBackedgeFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerForwardBackedgeFlags;

int ra2_manager_forward_backedge_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerForwardBackedgeFlags *flags);

#endif
