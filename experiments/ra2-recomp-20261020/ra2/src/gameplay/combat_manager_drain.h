#ifndef RA2_COMBAT_MANAGER_DRAIN_H
#define RA2_COMBAT_MANAGER_DRAIN_H

#include <stdint.h>

typedef struct Ra2ManagerDrainServices {
    void *context;
    void (*begin)(void *context);
    void (*first_outer)(void *context);
    int32_t (*has_outer)(void *context);
    void (*save_extra)(void *context);
    int32_t (*outer_needs_detach)(void *context);
    void (*detach_outer)(void *context);
    void (*first_inner)(void *context);
    int32_t (*has_inner)(void *context);
    void (*detach_inner)(void *context);
    void (*cleanup_inner)(void *context);
    void (*return_inner)(void *context);
    void (*next_inner)(void *context);
    int32_t (*backedge_and_continue)(void *context);
    void (*cleanup_outer)(void *context);
    void (*return_outer)(void *context);
    void (*next_outer)(void *context);
    void (*restore_extra)(void *context);
} Ra2ManagerDrainServices;

void ra2_drain_manager_lists(const Ra2ManagerDrainServices *services);

#endif
