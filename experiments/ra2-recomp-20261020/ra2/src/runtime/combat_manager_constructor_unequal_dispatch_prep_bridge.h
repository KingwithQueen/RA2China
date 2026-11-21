#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_UNEQUAL_DISPATCH_PREP_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_UNEQUAL_DISPATCH_PREP_BRIDGE_H
#include <stdint.h>

/* Distinct caller locals: preserve both cache assignments between the two volatile reads. */
uint32_t ra2_manager_constructor_unequal_dispatch_prep_bridge(uint32_t cached_ebx,
    volatile uint32_t *cached_edx, volatile uint32_t *cached_ecx);
#endif
