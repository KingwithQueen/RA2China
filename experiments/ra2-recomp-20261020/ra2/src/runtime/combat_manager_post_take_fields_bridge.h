#ifndef RA2_COMBAT_MANAGER_POST_TAKE_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_POST_TAKE_FIELDS_BRIDGE_H
#include <stdint.h>

/* Independent entry: read current local stack to EBX, then copy cached EAX to ESI. */
void ra2_manager_post_take_fields_bridge(uint32_t stack, uint32_t value, uint32_t *owner, uint32_t *data);
#endif
