#ifndef RA2_COMBAT_MANAGER_EMPTY_CALL_BRIDGE_H
#define RA2_COMBAT_MANAGER_EMPTY_CALL_BRIDGE_H
#include <stdint.h>

/* 使用实际ESI+1C计算结果；调用者先更新ECX和guest ESP。 */
typedef struct Ra2ManagerEmptyCallRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerEmptyCallRegisters;

/* guest压槽成功后公开缓存，执行完整408450；返回实际原caller。 */
uint32_t ra2_manager_empty_call_bridge(const Ra2ManagerEmptyCallRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
