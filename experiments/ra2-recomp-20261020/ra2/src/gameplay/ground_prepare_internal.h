#pragma once
#include "unit_movement.h"

typedef struct Ra2PrepareInternalServices
{
    void *context;
    uint32_t (*rebuild)(void *context, uint32_t destination_cell, unsigned attempts);
    void (*clear_segment)(void *context, int32_t first_coordinate);
} Ra2PrepareInternalServices;
/* 有符号坐标除以 256 向零截断，再按原版 CellStruct 的两个 int16 打包。 */
uint32_t ra2_ground_prepare_destination_cell(Ra2WorldPoint destination);
/* 普通重建一次；携带非零重试标记的内部接续允许两次。 */
uint32_t ra2_ground_prepare_rebuild_internal(Ra2WorldPoint destination, unsigned retry,
    const Ra2PrepareInternalServices *services);
void ra2_ground_prepare_clear_internal(int32_t first_coordinate,
    const Ra2PrepareInternalServices *services);
