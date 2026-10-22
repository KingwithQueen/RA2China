#pragma once
#include "ground_cell_services.h"

typedef struct Ra2PassageCell
{
    int32_t level;
    unsigned ramp;
    uint32_t flags;
} Ra2PassageCell;

/* 0为允许，7为不可进入。level与changing_layer只在原版指定的分支写入。 */
int32_t ra2_ground_classify_transition(const Ra2PassageCell *destination,
    const Ra2PassageCell *origin, int32_t direction, int32_t *level, uint8_t *changing_layer);

typedef struct Ra2BasePassageServices
{
    void *context;
    int (*has_locomotor)(void *context);
    int32_t (*locomotor_can_enter)(void *context);
} Ra2BasePassageServices;
int32_t ra2_ground_base_can_enter(unsigned check_locomotor, const Ra2BasePassageServices *services);

typedef struct Ra2GroundHeightServices
{
    void *context;
    uintptr_t (*cell_at_world)(void *context, Ra2WorldPoint point);
    int32_t (*height_in_cell)(void *context, uintptr_t cell, Ra2WorldPoint point);
} Ra2GroundHeightServices;
/* 坐标保留完整32位；越界格复用原版后备格，之后交给坡面高度服务。 */
int32_t ra2_ground_height_at(Ra2WorldPoint point, const Ra2GroundHeightServices *services);
