#pragma once
#include "unit_movement.h"
typedef struct Ra2ServiceCell { int16_t x, y; } Ra2ServiceCell;
typedef struct Ra2CellGrid
{
    const uint32_t *cells;
    int32_t count;
    uintptr_t fallback;
    Ra2ServiceCell *fallback_point;
} Ra2CellGrid;
/* 通行服务共用的格子读取。越界/空槽返回同一个备用格，并更新其坐标。 */
uintptr_t ra2_cell_at_world(const Ra2CellGrid *grid, Ra2WorldPoint point);
uintptr_t ra2_cell_at_point(const Ra2CellGrid *grid, Ra2ServiceCell point);
/* 原版这个内部入口不检查范围；调用者必须已保证索引有效。 */
int ra2_cell_slot_present(const uint32_t *cells, Ra2ServiceCell point);
int32_t ra2_cell_threat_index(Ra2ServiceCell actual_cell);
