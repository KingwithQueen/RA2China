#ifndef RA2_COMBAT_MANAGER_NEIGHBOR_FIRST_CALL_STATE_BRIDGE_H
#define RA2_COMBAT_MANAGER_NEIGHBOR_FIRST_CALL_STATE_BRIDGE_H
#include <stdint.h>

/* All outputs refer to distinct caller locals; only the snapshot reads guest memory. */
void ra2_manager_neighbor_first_call_state_bridge(uint32_t cached_esi,
    volatile uint32_t *cached_ebp, volatile uint32_t *cached_edi, volatile uint32_t *cached_ecx);
#endif
