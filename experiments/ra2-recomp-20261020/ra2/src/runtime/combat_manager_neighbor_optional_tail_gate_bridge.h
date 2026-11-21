#ifndef RA2_COMBAT_MANAGER_NEIGHBOR_OPTIONAL_TAIL_GATE_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEIGHBOR_OPTIONAL_TAIL_GATE_BRIDGE_H
#include <stdint.h>

/* Reviewed sites use +0x94/+0x98/+0x9C from ESI or +0xE8 from returned EBP; outputs are distinct locals. */
int ra2_manager_neighbor_optional_tail_gate_bridge(uint32_t cached_base, uint32_t field_offset,
    volatile uint32_t *cached_edx, volatile uint32_t *lhs, volatile uint32_t *rhs,
    volatile uint32_t *carry, volatile uint32_t *kind);

void ra2_manager_neighbor_ebp_tail_call_inputs_bridge(uint32_t pre_ebp, uint32_t pre_edi,
    volatile uint32_t *cached_edx, volatile uint32_t *cached_ecx);
#endif
