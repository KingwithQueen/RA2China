#ifndef RA2_COMBAT_MANAGER_NEIGHBOR_OPTIONAL_TAIL_GATE_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEIGHBOR_OPTIONAL_TAIL_GATE_BRIDGE_H
#include <stdint.h>

/* Only original +0x94/+0x98/+0x9C sites; output pointers are distinct caller locals. */
int ra2_manager_neighbor_optional_tail_gate_bridge(uint32_t cached_esi, uint32_t field_offset,
    volatile uint32_t *cached_edx, volatile uint32_t *lhs, volatile uint32_t *rhs,
    volatile uint32_t *carry, volatile uint32_t *kind);
#endif
