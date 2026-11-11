#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_CALLBACK_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_CALLBACK_FIELDS_BRIDGE_H
#include <stdint.h>

/* Store three callback addresses in guest instruction order; never call them. */
void ra2_manager_constructor_callback_fields_bridge(uint32_t owner);
#endif
