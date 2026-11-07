#ifndef RA2_COMBAT_MANAGER_TAKE_DISPATCH_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_DISPATCH_FIELDS_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached ESP+0x14 to EDX, then compute cached ESI+0x1C to EDI. */
void ra2_manager_take_dispatch_fields_bridge(uint32_t stack, uint32_t value, uint32_t *data, uint32_t *target);
#endif
