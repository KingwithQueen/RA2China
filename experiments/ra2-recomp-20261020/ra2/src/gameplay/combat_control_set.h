#pragma once
#include <stdint.h>

typedef struct Ra2ControlSetServices {
    void *context;
    void (*begin)(void *);
    void (*call_first)(void *);
    void (*set_state)(void *);
    uint32_t (*restore_and_tail)(void *);
} Ra2ControlSetServices;

/* 首次回调后设置状态，再恢复保存寄存器并尾转移；内部标签交回原分派。 */
uint32_t ra2_set_control_state_and_tail(const Ra2ControlSetServices *services);
