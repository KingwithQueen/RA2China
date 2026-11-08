#ifndef RA2_COMBAT_MANAGER_TAKE_POP_EDI_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_POP_EDI_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached old ESP, increment ESP, then assign EDI. Independent valid output slots required. */
void ra2_manager_take_pop_edi_bridge(uint32_t *stack, uint32_t *value);
#endif
