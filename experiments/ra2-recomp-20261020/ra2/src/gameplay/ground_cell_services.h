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

typedef struct Ra2MapArea
{
    int32_t width, local_x, local_y, local_width, local_height;
} Ra2MapArea;
/* 可用地图是等距投影的菱形，不是有地形数据就能接收移动目标。
   adjust_height关闭时传0高度/坡度；开启时由适配层读取真实格或备用格。 */
typedef enum Ra2MapAreaEdge {
    RA2_MAP_AREA_INSIDE, RA2_MAP_AREA_ABOVE, RA2_MAP_AREA_BELOW,
    RA2_MAP_AREA_RIGHT, RA2_MAP_AREA_LEFT
} Ra2MapAreaEdge;
Ra2MapAreaEdge ra2_cell_area_boundary(const Ra2MapArea *area,Ra2ServiceCell cell,
    int32_t level,unsigned slope);
int ra2_cell_usable_area(const Ra2MapArea *area, Ra2ServiceCell cell,
    int32_t level, unsigned slope);
