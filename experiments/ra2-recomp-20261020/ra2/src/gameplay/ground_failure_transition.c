#include "ground_failure_transition.h"
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid)
{
    if (end->x != invalid.x || end->y != invalid.y || end->z != invalid.z)
    {
        *end = invalid;
        *driving = 0;
    }
}
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *), int (*stop)(void *, int))
{
    if (variant) cancel(context);
    int stopped = stop(context, variant);
    return variant ? stopped : 0;
}
