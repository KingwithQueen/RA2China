#pragma once
#include <stdint.h>

typedef struct Ra2ControlTailServices {
    void *context;
    void (*begin)(void *);
    void (*call_first)(void *);
    void (*clear_state)(void *);
    uint32_t (*restore_and_tail)(void *);
} Ra2ControlTailServices;

/* 首次回调后清状态，再恢复保存寄存器并尾转移；返回值供原内部标签分派。 */
uint32_t ra2_clear_control_state_and_tail(const Ra2ControlTailServices *services);
