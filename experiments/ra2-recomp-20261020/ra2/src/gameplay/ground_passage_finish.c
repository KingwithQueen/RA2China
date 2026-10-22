#include "ground_passage_finish.h"
int32_t ra2_ground_finish_passage(Ra2PassageFinishState state,
    const Ra2PassageFinishServices *services)
{
    void *context = services->context;
    if (state.passage) return state.passage;
    if (state.crush_enemy) {
        if (!state.occupied_by_vehicle) return 0;
        if (services->query(context, RA2_FINISH_CRUSH_TARGET_PRESENT) &&
            services->query(context, RA2_FINISH_CRUSH_TARGET_CRUSHABLE)) return 0;
        return 2;
    }
    if (!(state.occupation & 0x3Fu)) return 0;
    if (state.occupied_by_vehicle) return 2;
    if (state.occupation_owner != -1 && services->query(context, RA2_FINISH_ALLIED_OWNER)) return 2;
    if (services->query(context, RA2_FINISH_CRUSHER) ||
        services->query(context, RA2_FINISH_CRUSH_ABILITY)) return 0;
    if (services->query(context, RA2_FINISH_TRAIN)) return 5;
    if (!services->query(context, RA2_FINISH_FIRST_WEAPON_PRESENT)) return 7;
    return services->query(context, RA2_FINISH_SECOND_WEAPON_CAN_CLEAR) ? 5 : 7;
}
