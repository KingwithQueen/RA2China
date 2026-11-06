#ifndef RA2_COMBAT_MANAGER_POST_CLAMP_FORWARD_BRIDGE_H
#define RA2_COMBAT_MANAGER_POST_CLAMP_FORWARD_BRIDGE_H
#include <stdint.h>
/* helper公开标志与调用方局部TEST分别保存。 */
typedef struct Ra2ManagerPostClampForwardFlags { uint32_t kind, left, right, carry; } Ra2ManagerPostClampForwardFlags;
int ra2_manager_post_clamp_forward_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerPostClampForwardFlags *flags);
#endif
