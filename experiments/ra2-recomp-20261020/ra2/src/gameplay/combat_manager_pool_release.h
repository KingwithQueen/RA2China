#ifndef RA2_COMBAT_MANAGER_POOL_RELEASE_H
#define RA2_COMBAT_MANAGER_POOL_RELEASE_H

#include <stdint.h>

typedef struct Ra2ManagerPoolReleaseServices {
    void *context;
    int32_t (*load_pool)(void *context, uint32_t offset);
    void (*release_pool)(void *context);
    void (*release_manager)(void *context);
    void (*finish)(void *context);
} Ra2ManagerPoolReleaseServices;

void ra2_release_manager_pools(const Ra2ManagerPoolReleaseServices *services);

#endif
