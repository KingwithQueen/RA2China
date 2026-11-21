#ifndef RA2_COMBAT_MANAGER_COUNTDOWN_A8_BRIDGE_H
#define RA2_COMBAT_MANAGER_COUNTDOWN_A8_BRIDGE_H
#include <stdint.h>

/* Invoke separately at both gates; do not cache or reuse a prior return. */
uint32_t ra2_manager_countdown_a8_read_bridge(uint32_t cached_esi);

/* One fresh read, DEC lazy tuple and write; carry remains caller-owned. */
void ra2_manager_countdown_a8_dec_store_bridge(uint32_t cached_esi,
    volatile uint32_t *cached_eax, volatile uint32_t *lhs,
    volatile uint32_t *rhs, volatile uint32_t *kind);

/* Candidate word only; the generated routine owns its TEST, call and post-call state. */
uint32_t ra2_manager_countdown_read_candidate168_bridge(uint32_t pre_cached_esi);

/* Reset status AL mask only; the caller preserves all jump-entry labels and stores. */
uint32_t ra2_manager_reset_status_mask_bridge(uint32_t value,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);

/* The original reset labels own address/value choice, ordering and all flags. */
void ra2_manager_reset_store_bridge(uint32_t receiver, uint32_t field_offset, uint32_t value);
#endif
