#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_ADDRESS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_ADDRESS_BRIDGE_H
#include <stdint.h>

/* Independent entry: compute actual cached EBP + 0x24 modulo uint32 to EDI. Valid uint32_t output slots required. */
void ra2_manager_take_unequal_address_bridge(uint32_t value, uint32_t *output);
#endif
