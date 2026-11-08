#ifndef RA2_COMBAT_MANAGER_TAKE_STACK_ADJUST_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_STACK_ADJUST_BRIDGE_H
#include <stdint.h>

/* Independent actual ESP plus 0xC ADD. State must point to a valid output object. */
typedef struct Ra2ManagerTakeStackAdjustState {
    uint32_t kind, left, right, carry, value;
} Ra2ManagerTakeStackAdjustState;
void ra2_manager_take_stack_adjust_bridge(uint32_t stack, Ra2ManagerTakeStackAdjustState *state);
#endif
