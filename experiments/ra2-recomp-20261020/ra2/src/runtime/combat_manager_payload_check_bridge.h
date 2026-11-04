#ifndef RA2_COMBAT_MANAGER_PAYLOAD_CHECK_BRIDGE_H
#define RA2_COMBAT_MANAGER_PAYLOAD_CHECK_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerPayloadFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerPayloadFlags;

int ra2_manager_payload_check_bridge(Ra2ManagerPayloadFlags *flags);

#endif
