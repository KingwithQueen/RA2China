#include "combat_techno_cleanup.h"

void ra2_cleanup_techno_prefix(const Ra2TechnoCleanupServices *s)
{
    s->reset_tables(s->context);
    for (uint32_t member = 0; member < 4; ++member) {
        if (s->has_member(s->context, member)) {
            s->cleanup_member(s->context, member);
            s->clear_member(s->context, member);
        }
    }
}
