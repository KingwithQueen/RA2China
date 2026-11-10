#ifndef RA2_COMBAT_MANAGER_REFERENCE_INCREMENT_BRIDGE_H
#define RA2_COMBAT_MANAGER_REFERENCE_INCREMENT_BRIDGE_H
#include <stdint.h>

/* Four valid, distinct output slots outside the guest counter. Volatile stores
 * preserve completed register/flag updates before a failing guest write. */
void ra2_manager_reference_increment_bridge(uint32_t receiver, volatile uint32_t *value, volatile uint32_t *kind, volatile uint32_t *left, volatile uint32_t *right);
#endif
