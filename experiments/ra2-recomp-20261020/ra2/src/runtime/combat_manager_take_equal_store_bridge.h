#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_STORE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_STORE_BRIDGE_H
#include <stdint.h>

/* Independent entry: store actual cached ECX at actual cached ESP+0x18; guest write semantics. */
void ra2_manager_take_equal_store_bridge(uint32_t stack, uint32_t value);
#endif
