#pragma once
#include <stdint.h>

/* 编号与本机 1.006 通行返回值一致；编号越大通常表示限制越强，不能按布尔值处理。 */
typedef enum Ra2CellPassage
{
    RA2_CELL_CLEAR = 0,
    RA2_CELL_CLOAKED_OBSTACLE = 1,
    RA2_CELL_MOVING_OBSTACLE = 2,
    RA2_CELL_GATE = 3,
    RA2_CELL_FRIENDLY_OBSTACLE = 4,
    RA2_CELL_DESTROYABLE = 5,
    RA2_CELL_TEMPORARY_OBSTACLE = 6,
    RA2_CELL_BLOCKED = 7
} Ra2CellPassage;

typedef struct Ra2CellOccupation
{
    int32_t previous_result;
    uint8_t occupation_flags;
    unsigned vehicle_present;
    int32_t infantry_owner_index;
    unsigned crushable_enemy_seen;
    unsigned actor_is_crusher;
    unsigned actor_is_train;
} Ra2CellOccupation;

typedef enum Ra2OccupationQuery
{
    RA2_OCCUPATION_INFANTRY_ALLIED,
    RA2_OCCUPATION_CRUSHER_ABILITY,
    RA2_OCCUPATION_HAS_WEAPON,
    RA2_OCCUPATION_WEAPON_CAN_CLEAR,
    RA2_OCCUPATION_VEHICLE_CRUSHABLE
} Ra2OccupationQuery;

typedef int (*Ra2OccupationQueryFunction)(void *context, Ra2OccupationQuery query);

int ra2_ground_uses_bridge_occupation(unsigned has_bridge, int32_t reference_level, int32_t cell_level);
uint8_t ra2_ground_remove_self_occupation(uint8_t flags);
Ra2CellPassage ra2_ground_resolve_occupation(const Ra2CellOccupation *occupation, void *context, Ra2OccupationQueryFunction query);
