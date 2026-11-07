#ifndef RA2_COMBAT_MANAGER_NEXT_RESULT_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEXT_RESULT_BRIDGE_H
#include <stdint.h>

/* 401DDD：完整结果位值及局部TEST；不修改公开状态。 */
typedef struct Ra2ManagerNextResultState {
    uint32_t value, kind, left, right, carry;
} Ra2ManagerNextResultState;

typedef struct Ra2ManagerNextResultRegisters {
    uint32_t ax, cx, dx, bx, sp, si, di, bp;
} Ra2ManagerNextResultRegisters;

int ra2_manager_next_result_bridge(uint32_t result, Ra2ManagerNextResultState *state);
/* 返回是否实际yield；不导出flags，不恢复caller。 */
int ra2_manager_next_result_backedge_bridge(const Ra2ManagerNextResultRegisters *regs);
#endif
