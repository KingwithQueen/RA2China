#ifndef RA2_COMBAT_MANAGER_TAKE_DIFFERENCE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_DIFFERENCE_BRIDGE_H
#include <stdint.h>

/* Independent actual ECX/EAX SUB. State must point to a valid output object. */
typedef struct Ra2ManagerTakeDifferenceState {
    uint32_t kind, left, right, carry, value;
} Ra2ManagerTakeDifferenceState;
void ra2_manager_take_difference_bridge(uint32_t left, uint32_t right, Ra2ManagerTakeDifferenceState *state);
#endif
