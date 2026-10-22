#pragma once
#include "unit_movement.h"

typedef struct Ra2TubeApproachServices {
    void *context;
    Ra2WorldPoint (*approach)(void *context);
    void (*construct_probe)(void *context, Ra2WorldPoint point);
    uintptr_t (*approach_center)(void *context);
    uintptr_t (*probe_center)(void *context);
    Ra2WorldPoint (*read_center)(void *context, uintptr_t center);
    void (*store_approach)(void *context, Ra2WorldPoint point);
    void (*increase_height)(void *context, int32_t increment);
    uint32_t (*refresh_heading)(void *context);
} Ra2TubeApproachServices;

/* 两次格查询完成后才读取中心坐标；查询回调可能改变前一次返回的数据。 */
uint32_t ra2_ground_tube_construct_approach(Ra2WorldPoint offset, int32_t rise,
    const Ra2TubeApproachServices *services);
/* 逐次舍入：distance / step_length * rise + base，再使用原转换控制字。
   原版默认转换向零；测试也覆盖转换控制字与运算控制字不同的情况。 */
int32_t ra2_ground_tube_progress_height(double distance, double step_length,
    int32_t rise, int32_t base, uint16_t control, uint16_t conversion_control);
