#ifndef RA2_COMBAT_MANAGER_COUNTDOWN_A8_BRIDGE_H
#define RA2_COMBAT_MANAGER_COUNTDOWN_A8_BRIDGE_H
#include <stdint.h>

/* Invoke separately at both gates; do not cache or reuse a prior return. */
uint32_t ra2_manager_countdown_a8_read_bridge(uint32_t cached_esi);

/* One fresh read, DEC lazy tuple and write; carry remains caller-owned. */
void ra2_manager_countdown_a8_dec_store_bridge(uint32_t cached_esi,
    volatile uint32_t *cached_eax, volatile uint32_t *lhs,
    volatile uint32_t *rhs, volatile uint32_t *kind);
#endif
