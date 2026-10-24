#include "ground_rebuild_result.h"
Ra2RebuildResult ra2_ground_check_rebuild_result(int rebuilt, int check_success,
    const Ra2RebuildResultServices *s)
{
    if (rebuilt && !check_success) return RA2_REBUILD_READY;
    void *c = s->context;
    if (!s->owner_exists(c)) { s->write_aborted(c); return RA2_REBUILD_NO_OWNER; }
    if (!rebuilt && !s->destination_accepted(c))
    {
        s->stop_navigation(c);
        return RA2_REBUILD_REJECTED;
    }
    return RA2_REBUILD_READY;
}
