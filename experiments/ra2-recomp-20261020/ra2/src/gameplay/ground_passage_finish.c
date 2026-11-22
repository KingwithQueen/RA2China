#include "ground_passage_finish.h"
#include "ground_outcome_policy.h"
#include "ground_collision.h"
int32_t ra2_ground_finish_passage(Ra2PassageFinishState state,
    const Ra2PassageFinishServices *services)
{
    void *context = services->context;
    int32_t result;
    Ra2OccupationRoute route = ra2_ground_occupation_route(state, &result);
    if (route == RA2_OCCUPATION_RESOLVED) return result;
    if (route == RA2_OCCUPATION_CRUSH_TARGET) {
        if (services->query(context, RA2_FINISH_CRUSH_TARGET_PRESENT) &&
            services->query(context, RA2_FINISH_CRUSH_TARGET_CRUSHABLE)) return RA2_CELL_CLEAR;
        return RA2_CELL_MOVING_OBSTACLE;
    }
    if (state.occupation_owner != -1 && services->query(context, RA2_FINISH_ALLIED_OWNER)) return RA2_CELL_MOVING_OBSTACLE;
    if (services->query(context, RA2_FINISH_CRUSHER) ||
        services->query(context, RA2_FINISH_CRUSH_ABILITY)) return RA2_CELL_CLEAR;
    if (services->query(context, RA2_FINISH_TRAIN)) return RA2_CELL_DESTROYABLE;
    if (!services->query(context, RA2_FINISH_FIRST_WEAPON_PRESENT)) return RA2_CELL_BLOCKED;
    return services->query(context, RA2_FINISH_SECOND_WEAPON_CAN_CLEAR) ? RA2_CELL_DESTROYABLE : RA2_CELL_BLOCKED;
}
