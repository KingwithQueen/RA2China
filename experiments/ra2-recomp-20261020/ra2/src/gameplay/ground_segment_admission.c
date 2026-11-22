#include "ground_segment_admission.h"
#include "ground_world_point.h"

Ra2SegmentAdmission ra2_ground_admit_segment(Ra2WorldPoint *end, unsigned *driving,
    Ra2WorldPoint invalid, Ra2WorldPoint candidate, const Ra2SegmentAdmissionServices *s)
{
    void *c=s->context;
    if(ra2_ground_same_world_point(candidate,invalid))
        return RA2_SEGMENT_NO_CANDIDATE;
    *end=candidate; *driving=1;
    if(s->accepts_owner(c,candidate) && !s->owner_restricted(c))
    {
        s->start_segment(c,candidate);
        return RA2_SEGMENT_STARTED;
    }
    if(!s->owner_alive(c)) return RA2_SEGMENT_OWNER_REMOVED;
    *end=invalid; *driving=0;
    return RA2_SEGMENT_REJECTED_ALIVE;
}
