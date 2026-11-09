#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_INDIRECT_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_FINAL_INDIRECT_FIELD_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual old cached ECX + 8, then commit ECX. Valid guest read and output slot required. */
void ra2_manager_take_unequal_final_indirect_field_bridge(uint32_t base, uint32_t *output);
#endif
