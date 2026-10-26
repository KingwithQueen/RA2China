#pragma once
#include <stdint.h>
typedef enum Ra2AftermathQuery {
    RA2_AF_DEATH_MODE, RA2_AF_CURRENT_SEQUENCE, RA2_AF_SOURCE_PRESENT,
    RA2_AF_SOURCE_CLASS, RA2_AF_SOURCE_MODE_FIVE, RA2_AF_CUSTOM_COUNT,
    RA2_AF_CUSTOM_ANIMATION, RA2_AF_NOT_HUMAN, RA2_AF_FORCE_IMMEDIATE,
    RA2_AF_CARRIER_SINKABLE, RA2_AF_HAS_PASSENGERS, RA2_AF_POP_PASSENGER,
    RA2_AF_CAN_ENTER_CELL, RA2_AF_IGNORE_DEFENSES, RA2_AF_CARRIER_FLAG_7C,
    RA2_AF_UNLIMBO_PASSENGER, RA2_AF_HOUSE_CONTROLLED, RA2_AF_CARRIER_TEAM,
    RA2_AF_INHERIT_SELECTION, RA2_AF_PASSENGER_TEAM, RA2_AF_POP_RAW_PASSENGER
} Ra2AftermathQuery;
typedef enum Ra2AftermathOperation {
    RA2_AF_SET_PRESENTATION_INDEX, RA2_AF_CUSTOM_EFFECT, RA2_AF_DEFAULT_EFFECT,
    RA2_AF_DEATH_ACTION, RA2_AF_CARRIER_NOTICE, RA2_AF_BEGIN_RELEASE,
    RA2_AF_RELEASE_POSITION, RA2_AF_PLACED_NOTICE, RA2_AF_ADD_TO_TEAM,
    RA2_AF_GUARD_MISSION, RA2_AF_SELECT_PASSENGER, RA2_AF_KILL_NOTICE,
    RA2_AF_DELETE_PASSENGER, RA2_AF_END_RELEASE, RA2_AF_PEEK_PASSENGER,
    RA2_AF_LEAVE_TEAM
} Ra2AftermathOperation;
typedef struct Ra2AftermathServices {
    void *context;
    int32_t (*query)(void *context,Ra2AftermathQuery query,uint32_t index);
    void (*perform)(void *context,Ra2AftermathOperation operation,uint32_t value);
} Ra2AftermathServices;
typedef enum Ra2DeathPresentationRoute {RA2_PRESENTATION_FINISH,RA2_PRESENTATION_DEFER} Ra2DeathPresentationRoute;
Ra2DeathPresentationRoute ra2_present_infantry_death(const Ra2AftermathServices *services);
/* 载员出队后才重新判断落点；失败时通知来源并析构，成功时恢复任务/队伍。
   临时释放计数在两条分支结束后都归还，回调改变载员链后重新读取链表头。 */
void ra2_release_carrier_passengers(const Ra2AftermathServices *services);
void ra2_destroy_carrier_passengers(const Ra2AftermathServices *services);
