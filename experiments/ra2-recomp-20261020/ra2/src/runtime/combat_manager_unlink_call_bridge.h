#ifndef RA2_COMBAT_MANAGER_UNLINK_CALL_BRIDGE_H
#define RA2_COMBAT_MANAGER_UNLINK_CALL_BRIDGE_H
#include <stdint.h>

/* 调用者先更新缓存ECX/ESP；guest写槽成功后才公开该快照。 */
typedef struct Ra2ManagerUnlinkCallRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerUnlinkCallRegisters;

/* 返回实际原caller；调用者导入GPR后恢复caller，再导入公开标志。 */
uint32_t ra2_manager_unlink_call_bridge(const Ra2ManagerUnlinkCallRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
