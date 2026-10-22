#pragma once
#include <stdint.h>
#include "unit_movement.h"

/* 隧道入口按原顺序请求距离、路段、朝向、速度及两端地形高度。
   服务可修改单位或返回别名，因此这些请求不能合并。 */
typedef struct Ra2TubeEntryServices {
    void *context;
    int32_t (*distance)(void *);
    void (*select_route)(void *);
    uint32_t (*heading)(void *);
    int32_t (*speed)(void *);
    void (*endpoints)(void *);
    int32_t (*entrance_height)(void *);
    int32_t (*exit_height)(void *);
    int32_t (*segment_count)(void *);
} Ra2TubeEntryServices;
typedef struct Ra2TubeEntryPreparation { int32_t distance, step, rise; uint32_t heading; } Ra2TubeEntryPreparation;
Ra2TubeEntryPreparation ra2_ground_tube_prepare_entry(const Ra2TubeEntryServices *services);
int32_t ra2_ground_tube_step(int32_t speed, double scale, uint16_t operation, uint16_t conversion);

typedef struct Ra2TubeHorizontalInput {
    Ra2WorldPoint origin;
    int32_t heading, distance;
    double radians_per_turn;
    float sine_scale, cosine_scale;
    const float *table;
    uint16_t operation, conversion;
} Ra2TubeHorizontalInput;
typedef struct Ra2TubeHorizontalResult { Ra2WorldPoint point; double angle; } Ra2TubeHorizontalResult;
/* 朝向先有符号扩展低16位，再减四分之一周；Y减正弦，X加余弦。 */
Ra2TubeHorizontalResult ra2_ground_tube_horizontal(Ra2TubeHorizontalInput input);
