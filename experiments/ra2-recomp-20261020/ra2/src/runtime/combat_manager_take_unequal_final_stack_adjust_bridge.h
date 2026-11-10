#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_STACK_ADJUST_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_STACK_ADJUST_BRIDGE_H
#include <stdint.h>

/* 五个指针必须指向有效且独立的槽；使用旧ESP，按原顺序更新结果与私有lazy flags。 */
void ra2_manager_take_unequal_final_stack_adjust_bridge(uint32_t *stack, uint32_t *kind, uint32_t *left, uint32_t *right, uint32_t *carry);
#endif
