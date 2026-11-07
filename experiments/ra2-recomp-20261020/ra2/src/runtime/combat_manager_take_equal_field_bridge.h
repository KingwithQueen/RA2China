#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_FIELD_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached ESP+0x18 to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_equal_field_bridge(uint32_t stack, uint32_t *value);
#endif
