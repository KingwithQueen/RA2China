#ifndef RA2_COMBAT_CONTROL_WALK_H
#define RA2_COMBAT_CONTROL_WALK_H

#include <stdint.h>

typedef struct Ra2ControlWalkServices {
    void *context;
    void (*begin)(void *context);
    void (*first)(void *context);
    int32_t (*has_current)(void *context);
    int32_t (*is_active)(void *context);
    int32_t (*type_matches)(void *context);
    void (*change)(void *context);
    void (*next)(void *context);
    int32_t (*backedge_and_continue)(void *context);
    void (*finish)(void *context);
} Ra2ControlWalkServices;

void ra2_walk_control_states(const Ra2ControlWalkServices *services);

#endif
