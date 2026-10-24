#include "ground_internal_next.h"
#include "ground_transition_rules.h"

int ra2_ground_full_sample_exhausted(int32_t index, int32_t x, int32_t y)
{ return x == 0 && y == 0 && index != 0; }

static Ra2WorldPoint displaced(Ra2WorldPoint point, Ra2WorldPoint offset)
{
    point.x = (int32_t)((uint32_t)point.x + (uint32_t)offset.x);
    point.y = (int32_t)((uint32_t)point.y + (uint32_t)offset.y);
    return point;
}

int ra2_ground_prepare_approach(int32_t *level, const Ra2PrepareApproachServices *services)
{
    void *context = services->context;
    services->reset_budget(context);
    if (services->direction(context) == 8) return 1;

    Ra2WorldPoint point = services->position(context);
    services->construct_target(context, displaced(point, services->offset(context)));
    services->store_probe(context, services->position(context));
    uintptr_t cell = services->probe_cell(context);
    *level = ra2_ground_layer_reference(services->cell_level(context, cell),services->upper_layer(context));

    /* 首次查询可能改变单位、坐标或偏移表，不能沿用上面的缓存。 */
    point = services->position(context);
    services->construct_probe(context, displaced(point, services->offset(context)));
    cell = services->probe_cell(context);
    uint32_t flags = services->cell_flags(context, cell);
    if (((flags >> 8) & 1u) ^ services->upper_layer(context))
        services->mark_transition(context);
    return 0;
}
