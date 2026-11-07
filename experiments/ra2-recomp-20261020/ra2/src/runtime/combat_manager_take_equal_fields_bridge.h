#ifndef RA2_COMBAT_MANAGER_TAKE_EQUAL_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_EQUAL_FIELDS_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached EBP+0x14 to EDX, then cached EBX to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_equal_fields_bridge(uint32_t frame, uint32_t base, uint32_t *first, uint32_t *second);
#endif
