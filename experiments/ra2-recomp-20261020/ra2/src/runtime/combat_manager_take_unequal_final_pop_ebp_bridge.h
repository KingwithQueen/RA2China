#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_POP_EBP_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_POP_EBP_BRIDGE_H
#include <stdint.h>

/* 使用有效且独立的 ESP 和 EBP 槽。栈读取成功后，先更新 ESP，再写入 EBP。 */
void ra2_manager_take_unequal_final_pop_ebp_bridge(uint32_t *stack, uint32_t *output);
#endif
