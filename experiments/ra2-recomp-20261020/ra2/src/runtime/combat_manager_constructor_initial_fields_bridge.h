#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_INITIAL_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_INITIAL_FIELDS_BRIDGE_H
#include <stdint.h>

/* Six valid, distinct output slots outside both guest fields. Volatile stores
 * preserve completed XOR state before either guest write can fault. */
void ra2_manager_constructor_initial_fields_bridge(uint32_t owner, volatile uint32_t *base, volatile uint32_t *member, volatile uint32_t *kind, volatile uint32_t *left, volatile uint32_t *right, volatile uint32_t *carry);
#endif
