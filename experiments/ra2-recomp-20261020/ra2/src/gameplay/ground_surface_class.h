#pragma once
#include <stdint.h>
int ra2_ground_is_tube_entrance(int16_t connection,int32_t count,int32_t land);
int ra2_ground_is_tile_family(int32_t tile,int32_t first);
typedef struct Ra2SurfaceSupportServices
{
    void *context;
    int32_t (*base_height)(void *context);
    int (*scan_objects)(void *context);
    uintptr_t (*first_object)(void *context);
    int32_t (*object_kind)(void *context,uintptr_t object);
    uintptr_t (*next_object)(void *context,uintptr_t object);
    int32_t (*support_height)(void *context,uintptr_t object);
    int (*fallback_support)(void *context);
} Ra2SurfaceSupportServices;
/* 保留先算坡面高度、再扫描对象和回退服务的顺序。 */
int32_t ra2_ground_surface_support_height(const Ra2SurfaceSupportServices *services);
