#pragma once
#include <stdint.h>

typedef struct Ra2ShakeAmplitude {
    int32_t quotient, remainder;
    unsigned division_valid;
} Ra2ShakeAmplitude;

typedef struct Ra2BuildingShakeServices {
    void *context;
    int32_t threshold;
    int32_t (*cost)(void *);
    int32_t (*divisor)(void *);
    void (*publish)(void *, Ra2ShakeAmplitude);
    void (*dispatch)(void *, int32_t);
} Ra2BuildingShakeServices;

Ra2ShakeAmplitude ra2_building_shake_amplitude(int32_t cost, int32_t divisor);
void ra2_schedule_building_shake(const Ra2BuildingShakeServices *services);
/* 本机原版1.006的共用入口只有RET，不写相机或震屏状态。 */
void ra2_legacy_screen_shake(int32_t amplitude);
