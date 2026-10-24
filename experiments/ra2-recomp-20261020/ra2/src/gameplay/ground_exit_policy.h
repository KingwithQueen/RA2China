#pragma once
#include "ground_completion.h"

typedef struct Ra2PrepareExitPlan
{
    unsigned clear_path, start_retry, finish_timer, recurse;
    unsigned clear_segment, clear_driving, cancel_target;
} Ra2PrepareExitPlan;

/* 计划只解释入口，不读取世界。目标及owner仍在执行服务时查询。 */
Ra2PrepareExitPlan ra2_ground_prepare_exit_plan(Ra2PrepareFinishEntry entry, int may_retry);
/* 原连接的非零时长约定；32位高差回绕后向零整除。 */
int32_t ra2_ground_connection_height(int32_t start, int32_t finish, int32_t duration);
