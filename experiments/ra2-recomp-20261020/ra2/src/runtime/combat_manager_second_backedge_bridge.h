#ifndef RA2_COMBAT_MANAGER_SECOND_BACKEDGE_BRIDGE_H
#define RA2_COMBAT_MANAGER_SECOND_BACKEDGE_BRIDGE_H
#include <stdint.h>

/* 401D9D回边：先保留局部GPR快照，仅实际yield时发布；不传递标志。 */
typedef struct Ra2ManagerSecondBackedgeRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerSecondBackedgeRegisters;

/* 返回是否执行了回调，调用者仅在返回非零时导入实际返回的GPR。 */
int ra2_manager_second_backedge_bridge(const Ra2ManagerSecondBackedgeRegisters *regs);
#endif
