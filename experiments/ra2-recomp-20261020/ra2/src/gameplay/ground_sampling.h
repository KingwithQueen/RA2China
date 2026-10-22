#pragma once
#include "ground_path.h"

typedef struct Ra2SamplingTemplate { int8_t normal, alternate; uint8_t facing; } Ra2SamplingTemplate;
typedef struct Ra2SamplingServices
{
    void *context;
    Ra2SamplingTemplate (*template_at)(void *context, int32_t selector);
    void (*select_table)(void *context, int32_t table);
    Ra2PathSample (*sample_at)(void *context, int32_t index);
} Ra2SamplingServices;
typedef enum Ra2SamplingPhase
{
    RA2_SAMPLING_DONE, RA2_SAMPLING_FULL_STEP, RA2_SAMPLING_REMAINDER,
    RA2_SAMPLING_INVALID_DIRECTION, RA2_SAMPLING_INTERPOLATE
} Ra2SamplingPhase;
typedef struct Ra2SamplingChoice
{
    int32_t table;
    unsigned turning;
    Ra2PathSample sample;
} Ra2SamplingChoice;
/* 初次整步采样：先选择表，再验证方向；-1和8不做转向差异判断。 */
Ra2SamplingPhase ra2_ground_choose_full_sample(int32_t progress, int32_t direction,
    int32_t selector, unsigned alternate, Ra2SamplingChoice *choice, const Ra2SamplingServices *services);
/* 消耗整步之后：先增加采样游标，余量等于7时走插值入口。 */
Ra2SamplingPhase ra2_ground_finish_sample(int32_t *index, int32_t progress);
/* 不足整步的尾部：(0,0)仅在游标非0时表示结束，保留原表的方向。 */
Ra2SamplingPhase ra2_ground_choose_remainder(int32_t progress, int32_t selector,
    unsigned alternate, int32_t index, Ra2SamplingChoice *choice, const Ra2SamplingServices *services);
