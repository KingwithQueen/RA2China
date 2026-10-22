#pragma once
#include <stdint.h>
#include "ground_collision.h"

typedef enum Ra2AlliedQuery
{
    RA2_ALLIED_OWNER_MISSION, RA2_ALLIED_IS_OWNER_DESTINATION,
    RA2_ALLIED_OBJECT_KIND, RA2_ALLIED_IS_OWNER_TARGET,
    RA2_ALLIED_OBJECT_HAS_MOVEMENT, RA2_ALLIED_OBJECT_HAS_DESTINATION,
    RA2_ALLIED_OBJECT_IS_TURNING, RA2_ALLIED_OBJECT_IS_MOVING,
    RA2_ALLIED_OBJECT_IS_ALLIED, RA2_ALLIED_OBJECT_FLAG_5A0,
    RA2_ALLIED_OBJECT_WANTS_MOVING_PASSAGE
} Ra2AlliedQuery;

typedef enum Ra2AlliedOutcome
{
    RA2_ALLIED_CLEAR, RA2_ALLIED_BLOCKED, RA2_ALLIED_CHECK_ENEMY,
    RA2_ALLIED_CHECK_STATIONARY, RA2_ALLIED_SCANNED
} Ra2AlliedOutcome;

typedef struct Ra2AlliedServices
{
    void *context;
    int32_t (*query)(void *context, Ra2AlliedQuery query);
    /* 原版八方向量化及近距离判断由适配层保留数值约定。 */
    unsigned (*owner_heading)(void *context);
    unsigned (*opposite_object_heading)(void *context);
    unsigned (*relative_heading)(void *context);
    int32_t (*distance)(void *context);
    void (*remember_moving_object)(void *context, int present);
} Ra2AlliedServices;

/* 包括敌我分流；敌方和静止友方交回已有独立分类函数。 */
Ra2AlliedOutcome ra2_ground_classify_allied_motion(int32_t *passage,
    const Ra2AlliedServices *services);
