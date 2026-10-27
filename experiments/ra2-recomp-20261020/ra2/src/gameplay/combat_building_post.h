#pragma once
#include <stdint.h>

typedef enum Ra2BuildingPostQuery {
    RA2_BP_LEAVE_RUBBLE, RA2_BP_IMAGE_OUT_PRESENT, RA2_BP_LOAD_IMAGE,
    RA2_BP_IMAGE_FRAME_COUNT, RA2_BP_CRATE_BENEATH, RA2_BP_CRATE_MONEY,
    RA2_BP_FOUNDATION_END
} Ra2BuildingPostQuery;
typedef enum Ra2BuildingPostOperation {
    RA2_BP_PUBLISH_HALF_FRAMES, RA2_BP_PUBLISH_RUBBLE_LEVEL,
    RA2_BP_CRATE_POSITION, RA2_BP_PLACE_CRATE,
    RA2_BP_RUBBLE_FOUNDATION, RA2_BP_RUBBLE_POSITION, RA2_BP_RUBBLE_CELL,
    RA2_BP_CLEAR_CELL, RA2_BP_PUBLISH_RUBBLE_CELL, RA2_BP_RECALCULATE_CELL,
    RA2_BP_REFRESH_MAP_CELL, RA2_BP_REFRESH_PASSABILITY, RA2_BP_FINISH_CELL,
    RA2_BP_RUBBLE_ANCHOR, RA2_BP_FIRST_RECTANGLE, RA2_BP_SECOND_RECTANGLE,
    RA2_BP_PREPARE_INVALIDATION, RA2_BP_INVALIDATE_RECTANGLE,
    RA2_BP_FIND_CURRENT_ANCHOR, RA2_BP_INVALIDATE_ANCHOR
} Ra2BuildingPostOperation;
typedef struct Ra2BuildingPostServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingPostQuery);
    void (*perform)(void *, Ra2BuildingPostOperation, int32_t);
} Ra2BuildingPostServices;

/* 资格、格改写和通知分别调度；矩形提供及合并算法继续原接口。 */
int ra2_prepare_building_rubble(const Ra2BuildingPostServices *services);
void ra2_schedule_building_crate(const Ra2BuildingPostServices *services);
int16_t ra2_building_post_cell(int32_t coordinate);
void ra2_rewrite_building_rubble(const Ra2BuildingPostServices *services);
void ra2_invalidate_building_rubble(const Ra2BuildingPostServices *services);
