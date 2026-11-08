#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_COMPARE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_COMPARE_BRIDGE_H
#include <stdint.h>

/* Independent MEM32(actual EBP+4) / actual EBP CMP. State must point to a valid output object. */
typedef struct Ra2ManagerTakeUnequalCompareState {
    uint32_t kind, left, right, carry;
} Ra2ManagerTakeUnequalCompareState;
int ra2_manager_take_unequal_compare_bridge(uint32_t base, Ra2ManagerTakeUnequalCompareState *state);
#endif
