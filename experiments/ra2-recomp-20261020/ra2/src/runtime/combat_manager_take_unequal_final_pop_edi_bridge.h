#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_POP_EDI_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_POP_EDI_BRIDGE_H
#include <stdint.h>

/* Independent entry: Read actual old ESP, increment ESP by 4, then commit EDI. Valid independent stack/value output slots required. */
void ra2_manager_take_unequal_final_pop_edi_bridge(uint32_t *stack, uint32_t *output);
#endif
