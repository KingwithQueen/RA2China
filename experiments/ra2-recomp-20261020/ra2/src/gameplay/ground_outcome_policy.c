#include "ground_outcome_policy.h"
#include "ground_failure_policy.h"
#include "ground_collision.h"

Ra2FailurePlan ra2_ground_failure_plan(Ra2PrepareFailureEntry entry, int may_retry,
    int32_t classification, int32_t rejected_direction)
{
    switch (RA2_GROUND_FAILURE_DECISION_VALUE(entry, may_retry, classification))
    {
        case RA2_FAILURE_PLAN_CLEAR_PENDING:
            return (Ra2FailurePlan){.clear_pending = 1};
        case RA2_FAILURE_PLAN_RETRY_REVEALED:
            return (Ra2FailurePlan){.retry = 1,
                .path_value = RA2_GROUND_FAILURE_RETRY_PATH_VALUE(RA2_FAILURE_PLAN_RETRY_REVEALED, rejected_direction)};
        case RA2_FAILURE_PLAN_RETRY_CLASSIFIED:
            return (Ra2FailurePlan){.retry = 1, .start_retry = 1,
                .path_value = RA2_GROUND_FAILURE_RETRY_PATH_VALUE(RA2_FAILURE_PLAN_RETRY_CLASSIFIED, rejected_direction)};
        case RA2_FAILURE_PLAN_STOP_DIRECT:
            return (Ra2FailurePlan){.clear_segment = 1};
        case RA2_FAILURE_PLAN_STOP_SAVED:
            return (Ra2FailurePlan){.clear_segment = 1, .saved_segment = 1};
        case RA2_FAILURE_PLAN_STOP_ONLY:
            break;
    }
    return (Ra2FailurePlan){0};
}

Ra2OccupationRoute ra2_ground_occupation_route(Ra2PassageFinishState state, int32_t *result)
{
    *result = state.passage;
    if (state.passage) return RA2_OCCUPATION_RESOLVED;
    if (state.crush_enemy)
        return state.occupied_by_vehicle ? RA2_OCCUPATION_CRUSH_TARGET : RA2_OCCUPATION_RESOLVED;
    if (!(state.occupation & 0x3Fu)) return RA2_OCCUPATION_RESOLVED;
    if (state.occupied_by_vehicle)
    {
        *result = 2;
        return RA2_OCCUPATION_RESOLVED;
    }
    return RA2_OCCUPATION_QUERY_OWNER;
}
