#include "ground_prepare_shared.h"
uint32_t ra2_ground_prepare_shared(int rebuilt, int32_t cached_head, const Ra2PrepareSharedServices *s)
{
    if (rebuilt)
    {
        s->reset_failure_budget(s->context, 10);
        cached_head = s->read_path_head(s->context);
    }
    return s->prepare_segment(s->context, cached_head);
}
