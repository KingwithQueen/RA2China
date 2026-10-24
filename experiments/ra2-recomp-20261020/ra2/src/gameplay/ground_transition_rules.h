#pragma once
#include <stdint.h>

/* 参考高度按上/下层选择；保留32位回绕，避免C有符号溢出。 */
int32_t ra2_ground_layer_reference(int32_t level, unsigned upper);
/* 只在原版允许的四级向下桥层分支写 changing_layer；失败不清旧值。 */
int32_t ra2_ground_check_height_step(int32_t from_level, int32_t to_level,
    int32_t reference, uint32_t from_flags, uint32_t to_flags,
    unsigned from_ramp, unsigned to_ramp, uint8_t *changing_layer);
