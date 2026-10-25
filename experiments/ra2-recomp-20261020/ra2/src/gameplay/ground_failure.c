#include "ground_failure.h"
#include "ground_outcome_policy.h"

static uint32_t retry_failed_connection(Ra2FailurePlan plan,
    const Ra2PrepareFailureServices *s,void *c)
{
    s->clear_path(c,plan.path_value);
    if(plan.start_retry)s->start_retry(c);
    return s->prepare_again(c);
}

static uint32_t stop_failed_connection(Ra2FailurePlan plan,
    const Ra2PrepareFailureServices *s,void *c)
{
    if(plan.clear_segment)s->clear_segment(c,plan.saved_segment);
    return s->stop(c);
}

uint32_t ra2_ground_finish_failure(Ra2PrepareFailureEntry entry,int may_retry,
    int32_t classification,int32_t rejected_direction,const Ra2PrepareFailureServices *s)
{
    void *c=s->context;
    Ra2FailurePlan plan=ra2_ground_failure_plan(entry,may_retry,classification,rejected_direction);
    if(plan.clear_pending)return s->clear_pending(c);
    if(plan.retry)return retry_failed_connection(plan,s,c);
    return stop_failed_connection(plan,s,c);
}
