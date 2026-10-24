#include "ground_outcome_policy.h"

Ra2FailurePlan ra2_ground_failure_plan(Ra2PrepareFailureEntry entry, int may_retry,
    int32_t classification, int32_t rejected_direction)
{
    Ra2FailurePlan plan = {0};
    if (entry == RA2_FAILURE_CLASSIFIED_OBSTACLE && classification != 7)
        plan.clear_pending = 1;
    else if ((entry == RA2_FAILURE_REVEALED_OBSTACLE || entry == RA2_FAILURE_CLASSIFIED_OBSTACLE) && may_retry)
    {
        plan.retry = 1;
        plan.start_retry = entry == RA2_FAILURE_CLASSIFIED_OBSTACLE;
        plan.path_value = plan.start_retry ? -1 : rejected_direction;
    }
    else
    {
        plan.clear_segment = entry != RA2_FAILURE_STOP_ONLY;
        plan.saved_segment = entry == RA2_FAILURE_CLEAR_SAVED_SEGMENT
            || entry == RA2_FAILURE_CLEAR_SAVED_TAIL || entry == RA2_FAILURE_CLASSIFIED_OBSTACLE;
    }
    return plan;
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
