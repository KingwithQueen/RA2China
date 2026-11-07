#ifndef RA2_COMBAT_MANAGER_NEXT_FRONT_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEXT_FRONT_BRIDGE_H
#include <stdint.h>

/* 使用上一调用实际返回的EBX；调用者先更新ECX和guest ESP。 */
typedef struct Ra2ManagerNextFrontRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerNextFrontRegisters;

/* guest压槽成功后公开缓存，执行完整4073A0；返回实际原caller。 */
uint32_t ra2_manager_next_front_bridge(const Ra2ManagerNextFrontRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
