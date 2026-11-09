#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_BACKEDGE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_BACKEDGE_BRIDGE_H
#include <stdint.h>

/* Independent entry: TEST actual cached ESI before any optional runtime yield. */
typedef struct Ra2ManagerTakeUnequalBackedgeState {
    uint32_t kind, left, right, carry;
} Ra2ManagerTakeUnequalBackedgeState;
typedef struct Ra2ManagerTakeUnequalBackedgeRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerTakeUnequalBackedgeRegisters;
int ra2_manager_take_unequal_backedge_bridge(uint32_t value, Ra2ManagerTakeUnequalBackedgeState *state);
/* Only actual yield exports GPRs; no flags synchronization or caller restoration. */
int ra2_manager_take_unequal_backedge_backedge_bridge(const Ra2ManagerTakeUnequalBackedgeRegisters *regs);
#endif
