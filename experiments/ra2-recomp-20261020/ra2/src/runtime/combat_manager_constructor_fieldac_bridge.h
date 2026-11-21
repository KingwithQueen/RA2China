#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_FIELDAC_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_FIELDAC_BRIDGE_H
#include <stdint.h>

/* Store the actual cached ESI value through the 32-bit wrapped field-AC address. */
void ra2_manager_constructor_fieldac_bridge(uint32_t base, uint32_t value);
#endif
