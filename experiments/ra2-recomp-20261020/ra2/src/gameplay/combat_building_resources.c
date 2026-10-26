#include "combat_building_resources.h"
#define Q(q) s->query(s->context, RA2_BR_##q)
#define DO(op, value) s->perform(s->context, RA2_BR_##op, value)

void ra2_scatter_building_resources(const Ra2BuildingResourceServices *s)
{
    if (!Q(HAS_UNIT)) return;
    DO(BEGIN, 0);
    do {
        int32_t type = Q(FIRST_TYPE);
        DO(REMOVE_BUILDING, type);
        /* 归属在扣除建筑库存后读取；不可预先冻结整批库存或归属。 */
        DO(REMOVE_OWNER, type);
        DO(SCATTER, Q(RADIUS));
        DO(PLACE, type);
    } while (Q(HAS_UNIT));
    DO(END, 0);
}
