#pragma once
#include <stdint.h>

typedef enum Ra2BuildingResourceQuery {
    RA2_BR_HAS_UNIT, RA2_BR_FIRST_TYPE, RA2_BR_RADIUS
} Ra2BuildingResourceQuery;

typedef enum Ra2BuildingResourceOperation {
    RA2_BR_BEGIN, RA2_BR_REMOVE_BUILDING, RA2_BR_REMOVE_OWNER,
    RA2_BR_SCATTER, RA2_BR_PLACE, RA2_BR_END
} Ra2BuildingResourceOperation;

typedef struct Ra2BuildingResourceServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingResourceQuery);
    void (*perform)(void *, Ra2BuildingResourceOperation, int32_t);
} Ra2BuildingResourceServices;

/* 每次消耗一个库存单位；坐标散动和单元格资源规则由原服务承担。 */
void ra2_scatter_building_resources(const Ra2BuildingResourceServices *services);
