#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_CALL_ARG_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_CALL_ARG_BRIDGE_H
#include <stdint.h>

/* Independent entry: copy actual cached EDI to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_unequal_call_arg_bridge(uint32_t value, uint32_t *output);
#endif
