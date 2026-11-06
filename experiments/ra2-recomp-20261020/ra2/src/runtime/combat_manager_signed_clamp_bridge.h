#ifndef RA2_COMBAT_MANAGER_SIGNED_CLAMP_BRIDGE_H
#define RA2_COMBAT_MANAGER_SIGNED_CLAMP_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerSignedClampFlags { uint32_t kind, left, right, carry; } Ra2ManagerSignedClampFlags;

void ra2_manager_signed_clamp_bridge(Ra2ManagerSignedClampFlags *flags);

#endif
