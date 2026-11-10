#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_ZERO_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_ZERO_BRIDGE_H
#include <stdint.h>

/* 五个输出指针必须指向有效且独立的槽；只更新传入的EAX与私有lazy flags。 */
void ra2_manager_take_unequal_final_zero_bridge(uint32_t *output, uint32_t *kind, uint32_t *left, uint32_t *right, uint32_t *carry);
#endif
