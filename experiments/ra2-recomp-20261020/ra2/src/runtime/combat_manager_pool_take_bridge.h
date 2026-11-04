#ifndef RA2_COMBAT_MANAGER_POOL_TAKE_BRIDGE_H
#define RA2_COMBAT_MANAGER_POOL_TAKE_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerPoolTakeFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerPoolTakeFlags;

int ra2_manager_pool_take_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerPoolTakeFlags *flags);

#endif
