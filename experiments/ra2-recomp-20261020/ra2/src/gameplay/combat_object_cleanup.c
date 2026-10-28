#include "combat_object_cleanup_members.h"
#include "combat_object_cleanup_tables.h"
#include "combat_object_cleanup.h"

void ra2_cleanup_object_registry(const Ra2ObjectCleanupServices *s)
{
    s->begin(s->context);
    if (s->find(s->context) == -1) return;
    if (!s->can_remove(s->context)) return;
    if (!s->shrink_has_following(s->context)) return;
    while (s->shift_next(s->context)) {}
}

void ra2_cleanup_object_tables(const Ra2ObjectTablesCleanupServices *s)
{
    for (uint32_t table = 0; table < 4; ++table) {
        s->select_table(s->context, table);
        ra2_cleanup_object_registry(&s->registry);
    }
}

void ra2_cleanup_object_members(const Ra2ObjectMembersCleanupServices *s)
{
    s->begin(s->context);
    for (uint32_t step = 0; step < 4; ++step) s->member_step(s->context, step);
    if (s->restore_and_has_optional(s->context)) {
        s->cleanup_optional(s->context);
        s->clear_optional(s->context);
    }
    s->cleanup_abstract(s->context);
}
