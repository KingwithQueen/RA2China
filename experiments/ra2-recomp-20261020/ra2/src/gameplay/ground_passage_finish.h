#pragma once
#include <stdint.h>
typedef enum Ra2PassageFinishQuery {
    RA2_FINISH_CRUSH_TARGET_PRESENT,
    RA2_FINISH_CRUSH_TARGET_CRUSHABLE,
    RA2_FINISH_ALLIED_OWNER,
    RA2_FINISH_CRUSHER,
    RA2_FINISH_CRUSH_ABILITY,
    RA2_FINISH_TRAIN,
    RA2_FINISH_FIRST_WEAPON_PRESENT,
    RA2_FINISH_SECOND_WEAPON_CAN_CLEAR
} Ra2PassageFinishQuery;
typedef struct Ra2PassageFinishState {
    int32_t passage;
    uint8_t crush_enemy, occupation, occupied_by_vehicle;
    int32_t occupation_owner;
} Ra2PassageFinishState;
typedef struct Ra2PassageFinishServices {
    void *context;
    int (*query)(void *context, Ra2PassageFinishQuery which);
} Ra2PassageFinishServices;
/* 扫描对象后的最终通行结果。重复车辆/武器查询各有副作用，不能合并。 */
int32_t ra2_ground_finish_passage(Ra2PassageFinishState state,
    const Ra2PassageFinishServices *services);
