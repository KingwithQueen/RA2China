#ifndef RA2_COMBAT_MANAGER_TAKE_FOLLOWUP_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_FOLLOWUP_FIELDS_BRIDGE_H
#include <stdint.h>

/* Independent entry: read actual cached ESP+0x14 to ESI, then cached EBX to ECX. Valid uint32_t output slots required. */
void ra2_manager_take_followup_fields_bridge(uint32_t stack, uint32_t base, uint32_t *first, uint32_t *second);
#endif
