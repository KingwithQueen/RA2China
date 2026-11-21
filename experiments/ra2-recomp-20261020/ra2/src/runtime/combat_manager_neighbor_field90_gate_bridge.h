#ifndef RA2_COMBAT_MANAGER_NEIGHBOR_FIELD90_GATE_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEIGHBOR_FIELD90_GATE_BRIDGE_H
#include <stdint.h>

/* Distinct local outputs. The later reread belongs to the original continuation. */
int ra2_manager_neighbor_field90_gate_bridge(uint32_t cached_esi, volatile uint32_t *cached_edx,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);
#endif
