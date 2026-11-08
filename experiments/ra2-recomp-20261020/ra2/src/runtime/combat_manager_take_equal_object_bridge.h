#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_OBJECT_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_OBJECT_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached EBX to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_equal_object_bridge(uint32_t object, uint32_t *value);
#endif
