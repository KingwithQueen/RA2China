#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_AFTERLOOP_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_AFTERLOOP_FIELD_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached EBP+0x3C to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_unequal_afterloop_field_bridge(uint32_t base, uint32_t *value);
#endif
