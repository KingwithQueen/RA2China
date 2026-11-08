#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_MARK_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_MARK_BRIDGE_H
#include <stdint.h>

/* Independent entry: store constant one at actual cached EBP+0x18; guest write semantics. */
void ra2_manager_take_equal_mark_bridge(uint32_t base);
#endif
