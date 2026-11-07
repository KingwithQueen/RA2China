#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_ADDRESS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_ADDRESS_BRIDGE_H
#include <stdint.h>

/* Independent entry: compute actual cached EBP+0x40 modulo uint32 into EAX. Valid uint32_t output slots required. */
void ra2_manager_take_equal_address_bridge(uint32_t base, uint32_t *result);
#endif
