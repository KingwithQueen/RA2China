#pragma once
#include <stdint.h>

typedef struct Ra2BuildingDeathTimer {
    uint32_t value, elapsed;
    unsigned running, expired, pending;
} Ra2BuildingDeathTimer;

typedef enum Ra2BuildingDeathDelayQuery {
    RA2_BDD_MISSION, RA2_BDD_EXPLODES, RA2_BDD_TIMER_PENDING
} Ra2BuildingDeathDelayQuery;

typedef enum Ra2BuildingDeathDelayOperation {
    RA2_BDD_START_TIMER, RA2_BDD_CLEAR_MISSION_TIMER,
    RA2_BDD_UNINIT, RA2_BDD_POST_UNINIT
} Ra2BuildingDeathDelayOperation;

typedef struct Ra2BuildingDeathDelayServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingDeathDelayQuery);
    void (*perform)(void *, Ra2BuildingDeathDelayOperation, uint32_t);
} Ra2BuildingDeathDelayServices;

/* 到期时value保留原计数，expired决定其是否仍有剩余时间含义。 */
Ra2BuildingDeathTimer ra2_building_death_timer(uint32_t start, uint32_t duration, uint32_t now);
void ra2_initialize_building_death_delay(const Ra2BuildingDeathDelayServices *services);
/* 返回1表示本次已调度UnInit和原后处理；返回0留给原更新入口。 */
int ra2_handoff_building_death(const Ra2BuildingDeathDelayServices *services);
