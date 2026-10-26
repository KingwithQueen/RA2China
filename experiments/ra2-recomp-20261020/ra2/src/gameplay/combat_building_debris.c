#include "combat_building_debris.h"
#define Q(q) s->query(s->context, RA2_BD_##q)
#define DO(op, value) s->perform(s->context, RA2_BD_##op, value)

void ra2_generate_building_debris(const Ra2BuildingDebrisServices *s)
{
    if (Q(MAXIMUM_GATE) <= 0) return;
    /* 原版三次类型查询和数量抽样的次序，不预先合并规则快照。 */
    Q(MAXIMUM_UPPER);
    Q(MINIMUM);
    int32_t remaining = Q(DRAW_TOTAL);
    if (Q(VOXEL_COUNT) > 0) {
        DO(BEGIN_VOXELS, 0);
        while (remaining > 0) {
            uint32_t draw = (uint32_t)Q(VOXEL_RANDOM);
            uint32_t magnitude = (int32_t)draw < 0 ? 0u - draw : draw;
            int32_t divisor = (int32_t)((uint32_t)Q(CAPTURED_VOXEL_MAXIMUM) + 1u);
            int32_t quota = (int32_t)magnitude % divisor;
            if (quota >= remaining) quota = remaining;
            DO(PUBLISH_QUOTA, quota);
            if (quota > 0) DO(EMIT_VOXELS, quota);
            remaining = (int32_t)((uint32_t)remaining - (uint32_t)quota);
            DO(ADVANCE_VOXEL, remaining);
        }
    }
    if (Q(CUSTOM_COUNT) > 0) {
        if (remaining <= 0) return;
        DO(BEGIN_CUSTOM, remaining);
        for (int32_t i = 0; i < remaining; ++i) DO(EMIT_CUSTOM, 0);
    } else if (Q(DEFAULT_ALLOWED)) {
        for (int32_t i = 0; i < remaining; ++i) DO(EMIT_DEFAULT, 0);
    }
}
