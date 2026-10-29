#pragma once
#include <stdint.h>

typedef struct Ra2ControlSwitchServices {
    void *context;
    void (*begin)(void *);
    void (*call_first)(void *);
    int32_t (*needs_change)(void *);
    void (*call_change)(void *);
    void (*clear_changed)(void *);
    void (*activate_state)(void *);
    uint32_t (*restore_and_tail)(void *);
} Ra2ControlSwitchServices;

/* 先回调，再按原顺序重读、清位和置位，保留EAX与写回值的区别。 */
uint32_t ra2_switch_control_state(const Ra2ControlSwitchServices *services);
