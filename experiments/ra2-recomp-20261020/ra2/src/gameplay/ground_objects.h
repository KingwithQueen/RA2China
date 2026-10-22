#pragma once
#include <stdint.h>

typedef enum Ra2ObjectPassageQuery
{
    RA2_OBJECT_IS_OWNER, RA2_OBJECT_RELATED_CELL_MATCHES,
    RA2_OBJECT_OWNER_ACCEPTS_LINK, RA2_OBJECT_KIND,
    RA2_OBJECT_BUILDING_OCCUPIES_CELL, RA2_OBJECT_OWNER_PAIR_FLAG_BB0,
    RA2_OBJECT_PAIR_FLAG_BB0, RA2_OBJECT_BUILDING_FOOTPRINT_TEST,
    RA2_OBJECT_IS_CELL_BUILDING, RA2_OBJECT_BUILDING_IGNORED,
    RA2_OBJECT_BUILDING_MISSION_PASSAGE, RA2_OBJECT_MISSION_STATE,
    RA2_OBJECT_BUILDING_HOUSE_PASSAGE, RA2_OBJECT_HOUSE_FLAG_142,
    RA2_OBJECT_BUILDING_NEIGHBOR_ANCHOR, RA2_OBJECT_MATCHES_NEIGHBOR_BUILDING,
    RA2_OBJECT_CLOAKED, RA2_OBJECT_OWNER_CRUSHER, RA2_OBJECT_CRUSHER_ABILITY,
    RA2_OBJECT_CRUSHABLE, RA2_OBJECT_ALLIED, RA2_OBJECT_HAS_WEAPON_ZERO,
    RA2_OBJECT_OWNER_IS_TRAIN, RA2_OBJECT_TERRAIN_WEAPON_ALLOWED,
    RA2_OBJECT_BUILDING_FLAG_1350
} Ra2ObjectPassageQuery;
typedef enum Ra2ObjectPassageOutcome
{
    RA2_OBJECT_GENERAL_COLLISION, RA2_OBJECT_CHECK_GATE,
    RA2_OBJECT_SKIP, RA2_OBJECT_CLEAR, RA2_OBJECT_CLEAR_OCCUPATION,
    RA2_OBJECT_BLOCKED, RA2_OBJECT_SCANNED
} Ra2ObjectPassageOutcome;
typedef struct Ra2ObjectPassageState
{
    int32_t passage;
    unsigned crush_enemy;
} Ra2ObjectPassageState;
typedef struct Ra2ObjectPassageServices
{
    void *context;
    int32_t (*query)(void *context, Ra2ObjectPassageQuery query);
} Ra2ObjectPassageServices;

/* 分别对应对象扫描前置、非闸门建筑、敌方对象与静止友方对象。
   移动友方的朝向/距离几何判断仍由原来的数值分支处理，不把它省略。 */
Ra2ObjectPassageOutcome ra2_ground_filter_object(const Ra2ObjectPassageServices *services);
Ra2ObjectPassageOutcome ra2_ground_filter_building(int32_t direction,const Ra2ObjectPassageServices *services);
Ra2ObjectPassageOutcome ra2_ground_classify_enemy(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);
Ra2ObjectPassageOutcome ra2_ground_classify_stationary_ally(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *services);
