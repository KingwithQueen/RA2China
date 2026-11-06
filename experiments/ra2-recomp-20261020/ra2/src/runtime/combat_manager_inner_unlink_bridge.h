#ifndef RA2_COMBAT_MANAGER_INNER_UNLINK_BRIDGE_H
#define RA2_COMBAT_MANAGER_INNER_UNLINK_BRIDGE_H
#include <stdint.h>

/* 调用者先按实际EDI更新缓存ECX/ESP；guest压槽成功后才公开快照。 */
typedef struct Ra2ManagerInnerUnlinkRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerInnerUnlinkRegisters;

/* 返回实际原caller；导入GPR后恢复caller，再导入helper公开标志。 */
uint32_t ra2_manager_inner_unlink_bridge(const Ra2ManagerInnerUnlinkRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
