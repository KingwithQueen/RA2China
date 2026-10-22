#include "ground_failure.h"

uint32_t ra2_ground_finish_failure(Ra2PrepareFailureEntry entry, int may_retry,
    int32_t classification, int32_t rejected_direction, const Ra2PrepareFailureServices *s)
{
    void *c = s->context;
    if (entry == RA2_FAILURE_CLASSIFIED_OBSTACLE && classification != 7)
        return s->clear_pending(c);
    if ((entry == RA2_FAILURE_REVEALED_OBSTACLE || entry == RA2_FAILURE_CLASSIFIED_OBSTACLE) && may_retry)
    {
        s->clear_path(c, entry == RA2_FAILURE_REVEALED_OBSTACLE ? rejected_direction : -1);
        if (entry == RA2_FAILURE_CLASSIFIED_OBSTACLE) s->start_retry(c);
        return s->prepare_again(c);
    }
    if (entry != RA2_FAILURE_STOP_ONLY)
        s->clear_segment(c, entry == RA2_FAILURE_CLEAR_SAVED_SEGMENT || entry == RA2_FAILURE_CLEAR_SAVED_TAIL
            || entry == RA2_FAILURE_CLASSIFIED_OBSTACLE);
    return s->stop(c);
}
