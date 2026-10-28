#include "combat_reference_prefix.h"
#include "combat_object_cleanup_base.h"
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

void ra2_detach_object_association(const Ra2ObjectBaseCleanupServices *s)
{
    uint32_t owner = s->association_owner(s->context);
    if (owner) {
        /* 必须先清关联对象，再清成员；两处可能重叠，不重新读取owner。 */
        s->clear_owner_link(s->context, owner);
        s->clear_member_link(s->context);
    }
}

void ra2_reset_abstract_tables(const Ra2ObjectBaseCleanupServices *s)
{
    static const uint32_t tables[] = {0x79ADD8, 0x79ADBC, 0x79ADB4, 0x79ADAC};
    for (uint32_t i = 0; i < 4; ++i) s->write_abstract_table(s->context, i * 4, tables[i]);
}

uint32_t ra2_check_reference_prefix(const Ra2ReferencePrefixServices *s)
{
    s->begin(s->context);
    if (!s->active(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->manager_matches(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->has_reference(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->first_stamp_matches(s->context)) return RA2_REFERENCE_INVALID;
    if (!s->second_stamp_matches(s->context)) return RA2_REFERENCE_INVALID;
    if (s->is_dead(s->context)) return RA2_REFERENCE_INVALID;
    return RA2_REFERENCE_CONTINUE;
}
