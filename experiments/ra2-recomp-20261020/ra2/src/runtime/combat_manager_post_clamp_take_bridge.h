#ifndef RA2_COMBAT_MANAGER_POST_CLAMP_TAKE_BRIDGE_H
#define RA2_COMBAT_MANAGER_POST_CLAMP_TAKE_BRIDGE_H
#include <stdint.h>
/* 调用方局部TEST与完整池helper的公开标志分别保存。 */
typedef struct Ra2ManagerPostClampTakeFlags { uint32_t kind, left, right, carry; } Ra2ManagerPostClampTakeFlags;
int ra2_manager_post_clamp_take_bridge(uint32_t kind, uint32_t left, uint32_t right, uint32_t carry, Ra2ManagerPostClampTakeFlags *flags);
#endif
