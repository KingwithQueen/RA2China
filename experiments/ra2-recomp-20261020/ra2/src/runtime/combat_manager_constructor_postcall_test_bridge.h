#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_POSTCALL_TEST_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_POSTCALL_TEST_BRIDGE_H
#include <stdint.h>

/* The four outputs are distinct local lazy-flag storage, not guest memory. */
void ra2_manager_constructor_postcall_test_bridge(uint32_t result_eax, uint32_t *flag_a,
                                                 uint32_t *flag_b, uint32_t *carry, uint32_t *kind);
#endif
