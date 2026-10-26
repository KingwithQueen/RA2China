#pragma once
#include <stdint.h>

typedef enum Ra2BuildingDebrisQuery {
    RA2_BD_MAXIMUM_GATE, RA2_BD_MAXIMUM_UPPER, RA2_BD_MINIMUM,
    RA2_BD_DRAW_TOTAL, RA2_BD_VOXEL_COUNT, RA2_BD_VOXEL_RANDOM,
    RA2_BD_CAPTURED_VOXEL_MAXIMUM, RA2_BD_CUSTOM_COUNT, RA2_BD_DEFAULT_ALLOWED
} Ra2BuildingDebrisQuery;

typedef enum Ra2BuildingDebrisOperation {
    RA2_BD_BEGIN_VOXELS, RA2_BD_PUBLISH_QUOTA, RA2_BD_EMIT_VOXELS,
    RA2_BD_ADVANCE_VOXEL, RA2_BD_BEGIN_CUSTOM, RA2_BD_EMIT_CUSTOM,
    RA2_BD_EMIT_DEFAULT
} Ra2BuildingDebrisOperation;

typedef struct Ra2BuildingDebrisServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingDebrisQuery);
    void (*perform)(void *, Ra2BuildingDebrisOperation, int32_t);
} Ra2BuildingDebrisServices;

/* 只决策数量、类型与直接生成顺序；飞行、落地及伤害由原生成器承担。 */
void ra2_generate_building_debris(const Ra2BuildingDebrisServices *services);
