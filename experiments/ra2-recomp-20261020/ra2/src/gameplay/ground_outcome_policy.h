#pragma once
#include "ground_failure.h"
#include "ground_passage_finish.h"

typedef struct Ra2FailurePlan
{
    unsigned clear_pending, retry, start_retry, clear_segment, saved_segment;
    int32_t path_value;
} Ra2FailurePlan;
Ra2FailurePlan ra2_ground_failure_plan(Ra2PrepareFailureEntry entry, int may_retry,
    int32_t classification, int32_t rejected_direction);

typedef enum Ra2OccupationRoute
{
    RA2_OCCUPATION_RESOLVED,
    RA2_OCCUPATION_CRUSH_TARGET,
    RA2_OCCUPATION_QUERY_OWNER
} Ra2OccupationRoute;
/* 只解释已扫描状态；联盟、能力、武器等世界服务仍由调用者按序查询。 */
Ra2OccupationRoute ra2_ground_occupation_route(Ra2PassageFinishState state, int32_t *result);
