#ifndef RA2_COMBAT_MANAGER_TAKE_RESULT_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_RESULT_BRIDGE_H
#include <stdint.h>

/* Independent entry: TEST actual cached ESI before any optional runtime yield. */
typedef struct Ra2ManagerTakeResultState {
    uint32_t kind, left, right, carry;
} Ra2ManagerTakeResultState;
typedef struct Ra2ManagerTakeResultRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerTakeResultRegisters;
int ra2_manager_take_result_bridge(uint32_t value, Ra2ManagerTakeResultState *state);
/* Only actual yield exports GPRs; no flags synchronization or caller restoration. */
int ra2_manager_take_result_backedge_bridge(const Ra2ManagerTakeResultRegisters *regs);
#endif
