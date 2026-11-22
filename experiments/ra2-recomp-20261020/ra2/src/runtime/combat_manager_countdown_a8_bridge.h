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

/* One post-callback status read and write; flags/ECX are distinct local outputs. */
void ra2_manager_active_status_bit_bridge(uint32_t cached_esi, volatile uint32_t *cached_ecx,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);

/* Status-bit callback gate; local narrow flags only, no callback or guest store. */
int ra2_manager_status_byte_optional_gate_bridge(uint32_t cached_esi,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);

/* Status bit-3 deactivation entry and taken dword transition; no stack or callback. */
int ra2_manager_active_status_deactivation_gate_bridge(uint32_t cached_esi,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);
void ra2_manager_active_status_clear_bit_bridge(uint32_t cached_esi, volatile uint32_t *cached_eax,
    volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);

/* Ordered dword default route publication, no calls or flag edits. */
void ra2_manager_default_deactivation_routes_bridge(uint32_t cached_esi);

/* Ordered deactivation state reset prefix; no calls or flag edits. */
void ra2_manager_deactivation_state_reset_prefix_bridge(uint32_t cached_esi, uint32_t cached_edi);

/* Two ordered deactivation stores from cached registers; no guest read. */
void ra2_manager_deactivation_global_snapshot_stores_bridge(uint32_t cached_esi, uint32_t cached_edi, uint32_t cached_ecx);

/* Two ordered pre-callback state stores; no reads or calls. */
void ra2_manager_deactivation_tail_state_stores_bridge(uint32_t cached_esi, uint32_t cached_edi);

/* One post-callback state store; no reads or calls. */
void ra2_manager_deactivation_postcallback_state_store_bridge(uint32_t cached_esi, uint32_t cached_edi);

/* Success-path descriptor projection; no callback or control-flow ownership. */
void ra2_manager_descriptor_success_projection_bridge(uint32_t cached_esi, volatile uint32_t *cached_eax, volatile uint32_t *cached_ecx);

/* Fallback descriptor projection; no callback or control-flow ownership. */
void ra2_manager_descriptor_fallback_projection_bridge(uint32_t cached_esi, volatile uint32_t *cached_eax, volatile uint32_t *cached_edx);

/* Paired DEC/INC reference counters; raw carry and callbacks stay in the caller. */
void ra2_manager_linked_counter_adjustment_bridge(uint32_t cached_esi, volatile uint32_t *cached_eax, volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *kind);

/* Post-callback counter DEC/TEST; signed branch and clamp stay at their original sites. */
void ra2_manager_linked_counter_decrement_test_bridge(uint32_t cached_esi, volatile uint32_t *cached_eax, volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *kind, volatile uint32_t *carry);

/* Global publication with an intervening zero store and a fresh pointer load. */
void ra2_manager_global_publication_bridge(volatile uint32_t *cached_ecx, volatile uint32_t *cached_edx);

/* Publish ready and the original XOR state; return stays with the caller. */
void ra2_manager_global_ready_publication_bridge(volatile uint32_t *cached_eax, volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *carry, volatile uint32_t *kind);

/* Ordered counter increment and data-only callback receiver preparation. */
void ra2_manager_ready_counter_receiver_bridge(uint32_t cached_eax, volatile uint32_t *cached_ecx, volatile uint32_t *cached_edx, volatile uint32_t *lhs, volatile uint32_t *rhs, volatile uint32_t *kind);
#endif
