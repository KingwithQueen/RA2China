#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_CLEANUP_ARG_PUSH_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_CLEANUP_ARG_PUSH_BRIDGE_H
#include <stdint.h>

/* cached_esp points to the private caller local, not guest memory. */
void ra2_manager_constructor_cleanup_arg_push_bridge(volatile uint32_t *cached_esp, uint32_t cached_ebx);
#endif
