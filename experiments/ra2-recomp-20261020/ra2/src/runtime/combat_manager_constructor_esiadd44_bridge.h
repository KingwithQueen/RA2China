#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_ESIADD44_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_ESIADD44_BRIDGE_H
#include <stdint.h>

typedef struct {
    uint32_t value;
    uint32_t carry;
} ra2_manager_constructor_esiadd44_result;

ra2_manager_constructor_esiadd44_result ra2_manager_constructor_esiadd44_bridge(uint32_t source);
#endif
