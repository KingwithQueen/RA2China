#pragma once
#include "unit_movement.h"
typedef struct Ra2ObjectScanServices
{
    void *context;
    int (*enabled)(void *context);
    uintptr_t (*head)(void *context, int upper);
    int32_t (*kind)(void *context, uintptr_t object);
    uintptr_t (*next)(void *context, uintptr_t object);
    uintptr_t (*fallback)(void *context);
} Ra2ObjectScanServices;
uintptr_t ra2_ground_find_kind(int upper, int32_t kind, const Ra2ObjectScanServices *services);
/* 优先底层步兵，其次原对象服务，最后重新检查开关并查底层地形对象。 */
uintptr_t ra2_ground_find_blocking_object(const Ra2ObjectScanServices *services);
uintptr_t ra2_ground_cell_connection(int16_t index, int32_t count, const uint32_t *connections);
typedef struct Ra2HeightServices
{
    void *context;
    int32_t (*cell_level)(void *context);
    unsigned (*bridge_layer)(void *context);
    Ra2WorldPoint (*position)(void *context);
    int32_t (*ground_height)(void *context, Ra2WorldPoint position);
    int32_t (*bridge_height)(void *context);
} Ra2HeightServices;
int32_t ra2_ground_surface_level(const Ra2HeightServices *services);
int32_t ra2_ground_height_above_surface(const Ra2HeightServices *services);
