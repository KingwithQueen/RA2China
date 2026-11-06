#ifndef RA2_COMBAT_MANAGER_SECOND_FORWARD_BRIDGE_H
#define RA2_COMBAT_MANAGER_SECOND_FORWARD_BRIDGE_H
#include <stdint.h>
/* 保留完整helper公开元组，另行回传调用方局部TEST。 */
typedef struct Ra2ManagerSecondForwardFlags { uint32_t kind, left, right, carry; } Ra2ManagerSecondForwardFlags;
int ra2_manager_second_forward_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerSecondForwardFlags *flags);
#endif
