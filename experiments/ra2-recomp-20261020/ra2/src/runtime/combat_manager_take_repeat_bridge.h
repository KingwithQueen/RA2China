#ifndef RA2_COMBAT_MANAGER_TAKE_REPEAT_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_REPEAT_BRIDGE_H
#include <stdint.h>

/* Independent lazy-operand JNE. Neither helper changes the cached flags tuple. */
typedef struct Ra2ManagerTakeRepeatRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerTakeRepeatRegisters;
int ra2_manager_take_repeat_bridge(uint32_t left, uint32_t right);
/* Only actual yield exports GPRs; no flags synchronization or caller restoration. */
int ra2_manager_take_repeat_backedge_bridge(const Ra2ManagerTakeRepeatRegisters *regs);
#endif
