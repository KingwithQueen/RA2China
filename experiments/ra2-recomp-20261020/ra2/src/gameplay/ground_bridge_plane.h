#pragma once
#include <stdint.h>

/* 原版桥面比下层高四级；按32位回绕比较，不依赖有符号加减溢出。 */
int ra2_ground_bridge_height_matches(int32_t upper_level, int32_t lower_level);
/* 进入桥面后 set_layer 可改变占格/标志；退出判断必须重新查询。 */
void ra2_ground_transition_bridge(void *context,
    int32_t (*level)(void *context, unsigned next),
    uint32_t (*flags)(void *context, unsigned next),
    void (*set_layer)(void *context, unsigned upper));
