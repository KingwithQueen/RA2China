#ifndef RA2_COMBAT_MANAGER_TAKE_COMPARE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_COMPARE_BRIDGE_H
#include <stdint.h>

/* Independent actual EAX/ESI CMP. State must point to a valid output object. */
typedef struct Ra2ManagerTakeCompareState {
    uint32_t kind, left, right, carry;
} Ra2ManagerTakeCompareState;
int ra2_manager_take_compare_bridge(uint32_t left, uint32_t right, Ra2ManagerTakeCompareState *state);
#endif
