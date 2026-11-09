#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_POSTCALL_RESULT_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_POSTCALL_RESULT_BRIDGE_H
#include <stdint.h>

/* Independent entry: copy actual cached EAX to ESI. Valid uint32_t output slots required. */
void ra2_manager_take_unequal_postcall_result_bridge(uint32_t value, uint32_t *output);
#endif
