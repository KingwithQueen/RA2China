#ifndef RA2_COMBAT_MANAGER_POST_FORWARD_PAYLOAD_BRIDGE_H
#define RA2_COMBAT_MANAGER_POST_FORWARD_PAYLOAD_BRIDGE_H
#include <stdint.h>
/* 只回传调用方局部TEST，前向helper的公开标志保持原值。 */
typedef struct Ra2ManagerPostForwardPayloadFlags { uint32_t kind, left, right, carry; } Ra2ManagerPostForwardPayloadFlags;
int ra2_manager_post_forward_payload_bridge(Ra2ManagerPostForwardPayloadFlags *flags);
#endif
