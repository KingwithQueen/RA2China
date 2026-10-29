#pragma once
#include <stdint.h>

typedef struct Ra2ControlDispatchServices {
    void *context;
    void (*begin)(void *);
    void (*call_first)(void *);
    int32_t (*needs_optional)(void *);
    void (*call_optional)(void *);
    void (*call_last)(void *);
    int32_t (*has_callback)(void *);
    void (*call_callback)(void *);
    void (*finish)(void *);
} Ra2ControlDispatchServices;

/* 回调后才读取状态、当前函数表和可选指针，最后清理原状态槽。 */
void ra2_dispatch_control_cleanup(const Ra2ControlDispatchServices *services);
