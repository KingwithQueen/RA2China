#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_INDIRECT_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_INDIRECT_FIELD_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached EAX+4 to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_unequal_indirect_field_bridge(uint32_t base, uint32_t *value);
#endif
