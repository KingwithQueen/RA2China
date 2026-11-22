#pragma once
#include <stdint.h>

/* Integer constant expressions shared with the opt-in bridge value contract. */
#define RA2_GROUND_BRIDGE_FLAG_VALUE(flags) (((uint32_t)(flags) & 0x100u) != 0u)
#define RA2_GROUND_BRIDGE_HEIGHT_VALUE(upper, lower) ((uint32_t)(upper) == (uint32_t)(lower) + 4u)

/* Test the bridge-present bit without interpreting the other cell flags. */
static inline int ra2_ground_bridge_cell_flag_present(uint32_t flags)
{ return RA2_GROUND_BRIDGE_FLAG_VALUE(flags); }

/* 原版桥面比下层高四级；按32位回绕比较，不依赖有符号加减溢出。 */
int ra2_ground_bridge_height_matches(int32_t upper_level, int32_t lower_level);
/* 进入桥面后 set_layer 可改变占格/标志；退出判断必须重新查询。 */
void ra2_ground_transition_bridge(void *context,
    int32_t (*level)(void *context, unsigned next),
    uint32_t (*flags)(void *context, unsigned next),
    void (*set_layer)(void *context, unsigned upper));
