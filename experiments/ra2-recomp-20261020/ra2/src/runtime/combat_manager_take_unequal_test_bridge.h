#ifndef RA2_COMBAT_MANAGER_TAKE_UNEQUAL_TEST_BRIDGE_H
#define RA2_COMBAT_MANAGER_TAKE_UNEQUAL_TEST_BRIDGE_H
#include <stdint.h>

/* Independent actual ESI TEST. Four output pointers must be valid distinct slots. */
uint32_t ra2_manager_take_unequal_test_bridge(uint32_t value, uint32_t *kind, uint32_t *left, uint32_t *right, uint32_t *carry);
#endif
