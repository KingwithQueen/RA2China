#ifndef RA2_COMBAT_MANAGER_TAKE_DISPATCH_ARGS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_DISPATCH_ARGS_BRIDGE_H
#include <stdint.h>

/* Independent entry: copy actual cached EDI to EDX, then cached ESI to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_dispatch_args_bridge(uint32_t data, uint32_t object, uint32_t *out_data, uint32_t *out_object);
#endif
