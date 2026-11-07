#ifndef RA2_COMBAT_MANAGER_TAKE_FOLLOWUP_ARGS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_FOLLOWUP_ARGS_BRIDGE_H
#include <stdint.h>

/* Independent entry: copy actual cached ESI to EDX, then cached EBP+0x1C to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_followup_args_bridge(uint32_t data, uint32_t base, uint32_t *out_data, uint32_t *out_object);
#endif
