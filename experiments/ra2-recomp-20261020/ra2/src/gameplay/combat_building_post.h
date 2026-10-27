#pragma once
#include <stdint.h>

typedef enum Ra2BuildingPostQuery {
    RA2_BP_LEAVE_RUBBLE, RA2_BP_IMAGE_OUT_PRESENT, RA2_BP_LOAD_IMAGE,
    RA2_BP_IMAGE_FRAME_COUNT, RA2_BP_CRATE_BENEATH, RA2_BP_CRATE_MONEY
} Ra2BuildingPostQuery;
typedef enum Ra2BuildingPostOperation {
    RA2_BP_PUBLISH_HALF_FRAMES, RA2_BP_PUBLISH_RUBBLE_LEVEL,
    RA2_BP_CRATE_POSITION, RA2_BP_PLACE_CRATE
} Ra2BuildingPostOperation;
typedef struct Ra2BuildingPostServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingPostQuery);
    void (*perform)(void *, Ra2BuildingPostOperation, int32_t);
} Ra2BuildingPostServices;

/* 只判断留废墟资格并发布原输出；格改写与失效通知继续委托。 */
int ra2_prepare_building_rubble(const Ra2BuildingPostServices *services);
void ra2_schedule_building_crate(const Ra2BuildingPostServices *services);
int16_t ra2_building_post_cell(int32_t coordinate);
