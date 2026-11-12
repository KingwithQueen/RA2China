#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_OWNER_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_OWNER_FIELD_BRIDGE_H
#include <stdint.h>

/* Store the actual cached EBP value through the 32-bit wrapped owner address. */
void ra2_manager_constructor_owner_field_bridge(uint32_t base, uint32_t value);
#endif
