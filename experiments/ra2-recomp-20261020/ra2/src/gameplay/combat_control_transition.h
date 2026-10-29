#pragma once
#include <stdint.h>

typedef struct Ra2ControlTransitionServices {
    void *context;
    void (*begin)(void *);
    void (*call_first)(void *);
    int32_t (*needs_change)(void *);
    void (*clear_active)(void *);
    void (*call_change)(void *);
    void (*finish_change)(void *);
    uint32_t (*restore_and_tail)(void *);
} Ra2ControlTransitionServices;

/* 条件在首回调后读取，状态和函数表在各回调后重新读取。 */
uint32_t ra2_transition_control_state(const Ra2ControlTransitionServices *services);
