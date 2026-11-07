#ifndef RA2_COMBAT_MANAGER_INNER_RETURN_BRIDGE_H
#define RA2_COMBAT_MANAGER_INNER_RETURN_BRIDGE_H
#include <stdint.h>

/* 调用者有序完成两次字段读取及EDX更新；压槽成功后才公开缓存。 */
typedef struct Ra2ManagerInnerReturnRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerInnerReturnRegisters;

/* 返回实际原caller；完整407460及其现有边界合同保持。 */
uint32_t ra2_manager_inner_return_bridge(const Ra2ManagerInnerReturnRegisters *regs, uint32_t kind, uint32_t left, uint32_t right, uint32_t carry);
#endif
