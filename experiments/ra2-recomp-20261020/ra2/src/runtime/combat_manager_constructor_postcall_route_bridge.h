#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_POSTCALL_ROUTE_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_POSTCALL_ROUTE_BRIDGE_H
#include <stdint.h>

/* Outputs are distinct local flag slots; a nonzero result takes the existing equal edge. */
int ra2_manager_constructor_postcall_route_bridge(uint32_t cached_ebx, uint32_t cached_ebp,
                                                  uint32_t *flag_a, uint32_t *flag_b, uint32_t *carry, uint32_t *kind);
#endif
