#ifndef RA2_COMBAT_MANAGER_FRONT_CALL_BRIDGE_H
#define RA2_COMBAT_MANAGER_FRONT_CALL_BRIDGE_H
#include <stdint.h>

/* 先完成缓存LEA/ECX/ESP，压槽成功后再公开实际快照。 */
typedef struct Ra2ManagerFrontCallRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerFrontCallRegisters;

/* 导入实际返回GPR后恢复此caller，再导入helper公开标志。 */
uint32_t ra2_manager_front_call_bridge(const Ra2ManagerFrontCallRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
