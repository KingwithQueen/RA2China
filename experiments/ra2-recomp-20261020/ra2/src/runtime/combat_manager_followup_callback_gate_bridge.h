#ifndef RA2_COMBAT_MANAGER_FOLLOWUP_CALLBACK_GATE_BRIDGE_H
#define RA2_COMBAT_MANAGER_FOLLOWUP_CALLBACK_GATE_BRIDGE_H
#include <stdint.h>

/* Pure call-operand read; actual indirect call stays in generated code. */
uint32_t ra2_manager_followup_callback_input_bridge(uint32_t cached_esi);

/* Set the guest CMP tuple and report equality; output pointers are distinct caller locals. */
int ra2_manager_followup_callback_cmp_bridge(uint32_t lhs, uint32_t rhs,
    uint32_t *flag_a, uint32_t *flag_b, uint32_t *carry, uint32_t *kind);

/* Ordered unequal-path guest stores only; flags and original epilogue are caller-owned. */
void ra2_manager_followup_callback_ordered_stores_bridge(uint32_t cached_esi,
    uint32_t cached_edi);

/* A descriptor read before the call and unconditional returned-word update after it. */
uint32_t ra2_manager_followup_descriptor_read_bridge(uint32_t pre_cached_esi);
void ra2_manager_followup_descriptor_publish_bridge(uint32_t post_cached_esi,
    uint32_t post_cached_eax);

/* Capture a descriptor field separately from its ordered projection.
 * The 402304 caller keeps its original POP between the operations. */
uint32_t ra2_manager_followup_descriptor_c_bridge(uint32_t descriptor_eax);
void ra2_manager_followup_descriptor_project_bridge(uint32_t cached_esi,
    volatile uint32_t *cached_eax, uint32_t pre_ecx);

/* Distinct null-result fallback; guest accesses are ordered and cache slots are distinct. */
void ra2_manager_countdown_fallback_project_bridge(uint32_t cached_esi,
    volatile uint32_t *cached_eax, volatile uint32_t *cached_edx);
#endif
