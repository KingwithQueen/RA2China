#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_STACK_RECONCILE_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_STACK_RECONCILE_BRIDGE_H
#include <stdint.h>

/* All five pointers refer to distinct local state, never guest memory. */
void ra2_manager_constructor_stack_reconcile_bridge(volatile uint32_t *cached_esp,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);
#endif
