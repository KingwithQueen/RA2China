#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_VALUE_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_VALUE_FIELDS_BRIDGE_H
#include <stdint.h>

/* Store the actual cached EBP value, without assuming it is zero. */
void ra2_manager_constructor_value_fields_bridge(uint32_t owner, uint32_t value);
#endif
