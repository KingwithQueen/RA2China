#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_GLOBAL_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_GLOBAL_FIELD_BRIDGE_H
#include <stdint.h>

/* Store the actual cached EAX value through the 32-bit wrapped owner address. */
void ra2_manager_constructor_global_field_bridge(uint32_t base, uint32_t value);
#endif
