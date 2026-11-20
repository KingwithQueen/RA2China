#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_FIELD168_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_FIELD168_BRIDGE_H
#include <stdint.h>

/* Store the actual cached EBP value through the 32-bit wrapped field168 address. */
void ra2_manager_constructor_field168_bridge(uint32_t base, uint32_t value);
#endif
