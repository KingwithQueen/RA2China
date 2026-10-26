#include "combat_building_crew.h"

uint32_t ra2_select_building_crew(const Ra2BuildingCrewServices *s)
{
    if (!s->query(s->context, RA2_BCQ_SPECIAL_DISABLED)) {
        int32_t draw = (int32_t)s->query(s->context, RA2_BCQ_RANDOM_100);
        if (draw < 25 && s->query(s->context, RA2_BCQ_FACTORY_KIND) == 7)
            return s->query(s->context, RA2_BCQ_CURRENT_ENGINEER);
    }
    return s->query(s->context, RA2_BCQ_GENERIC_CREW);
}

uint32_t ra2_create_building_evacuee(const Ra2BuildingEvacuationServices *s)
{
    uint32_t type = s->select_type(s->context);
    if (!type) return 0;
    uint32_t storage = s->allocate(s->context, 0x5D8);
    if (!storage) return 0;
    return s->construct(s->context, storage, type);
}

uint32_t ra2_select_building_sale_crew(const Ra2BuildingCrewRetryServices *s)
{
    uint32_t type = s->select_type(s->context);
    if (!s->is_engineer(s->context, type)) return type;
    while (s->engineer_already_selected(s->context)) {
        type = s->select_type(s->context);
        if (!s->is_engineer(s->context, type)) break;
    }
    if (s->is_engineer(s->context, type)) s->mark_engineer_selected(s->context);
    return type;
}
