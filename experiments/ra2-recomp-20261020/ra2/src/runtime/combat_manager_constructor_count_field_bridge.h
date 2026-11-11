#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_COUNT_FIELD_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_COUNT_FIELD_BRIDGE_H
#include <stdint.h>

/* Initialize the count using the actual cached owner, without reading old data. */
void ra2_manager_constructor_count_field_bridge(uint32_t owner);
#endif
