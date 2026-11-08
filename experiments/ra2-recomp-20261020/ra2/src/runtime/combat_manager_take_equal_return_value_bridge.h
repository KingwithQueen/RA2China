#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_RETURN_VALUE_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_RETURN_VALUE_BRIDGE_H
#include <stdint.h>

/* Independent entry: copy actual cached EBP to EAX. Valid uint32_t output slots required. */
void ra2_manager_take_equal_return_value_bridge(uint32_t value, uint32_t *output);
#endif
