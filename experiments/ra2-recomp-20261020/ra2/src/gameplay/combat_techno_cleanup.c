#include "combat_techno_cleanup_base.h"
#include "combat_techno_cleanup_containers.h"
#include "combat_techno_cleanup_member_registry.h"
#include "combat_techno_cleanup_registry.h"
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

void ra2_cleanup_techno_registries(const Ra2TechnoRegistryServices *s)
{
    s->perform(s->context, RA2_TCR_BEGIN);
    s->perform(s->context, RA2_TCR_CLEAR_AUXILIARY);
    s->perform(s->context, RA2_TCR_RELEASE_AUXILIARY);
    s->perform(s->context, RA2_TCR_CLEAR_STATE);
    int32_t index = s->find(s->context, 0);
    s->perform(s->context, RA2_TCR_RESTORE_SAVED);
    if (index != -1) s->remove(s->context, 0, index);
    index = s->find(s->context, 1);
    if (index != -1) s->remove(s->context, 1, index);
}

void ra2_cleanup_techno_member_registry(const Ra2TechnoMemberRegistryServices *s)
{
    if (s->has_member(s->context)) {
        s->cleanup_member(s->context);
        s->clear_member(s->context);
    }
    int32_t index = s->find(s->context);
    if (index != -1) s->remove(s->context, index);
}

void ra2_cleanup_techno_containers(const Ra2TechnoContainersServices *s)
{
    for (uint32_t member = 0; member < 3; ++member) {
        s->begin(s->context, member);
        if (s->has_data(s->context) && s->owns_data(s->context)) s->free_data(s->context);
        s->end(s->context, member);
    }
    s->finish_member118(s->context);
}

void ra2_cleanup_techno_base(const Ra2TechnoBaseCleanupServices *s)
{
    s->begin_radio(s->context);
    if (s->has_data(s->context) && s->owns_data(s->context)) s->free_data(s->context);
    s->reset_storage(s->context);
    s->begin_mission(s->context);
    s->destroy_object(s->context);
}
