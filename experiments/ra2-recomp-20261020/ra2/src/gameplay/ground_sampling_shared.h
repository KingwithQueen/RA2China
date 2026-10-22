#pragma once
#include "ground_sampling.h"

/* 共享入口沿用调用方的方向哨兵；正常调用为 -1。选择表发生在方向校验之前。 */
Ra2SamplingPhase ra2_ground_choose_shared_full(int32_t progress, int32_t direction,
    int32_t direction_sentinel, Ra2SamplingTemplate selected, unsigned alternate,
    Ra2SamplingChoice *choice, const Ra2SamplingServices *services);
/* 模板已由调用方选定，不能再次选择普通/转弯模板，也不能重复查询路径。 */
Ra2SamplingPhase ra2_ground_choose_selected_remainder(int32_t table, int32_t index,
    int32_t end_sentinel, Ra2SamplingChoice *choice, const Ra2SamplingServices *services);
