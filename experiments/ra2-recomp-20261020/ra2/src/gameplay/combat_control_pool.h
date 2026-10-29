#ifndef RA2_COMBAT_CONTROL_POOL_H
#define RA2_COMBAT_CONTROL_POOL_H

#include <stdint.h>

typedef struct Ra2ControlPoolServices {
    void *context;
    void (*begin)(void *context);
    void (*allocate)(void *context);
    int32_t (*has_allocation)(void *context);
    int32_t (*start_links)(void *context);
    void (*begin_links)(void *context);
    void (*write_link)(void *context);
    int32_t (*backedge_and_continue)(void *context);
    void (*end_links)(void *context);
    void (*finish)(void *context);
} Ra2ControlPoolServices;

typedef struct Ra2ControlPoolReleaseServices {
    void *context;
    void (*begin)(void *context);
    void (*release)(void *context);
    void (*finish)(void *context);
} Ra2ControlPoolReleaseServices;

void ra2_initialize_control_pool(const Ra2ControlPoolServices *services);
void ra2_release_control_pool(const Ra2ControlPoolReleaseServices *services);

#endif
