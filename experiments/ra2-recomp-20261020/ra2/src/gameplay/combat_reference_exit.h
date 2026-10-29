#pragma once
#include <stdint.h>

typedef struct Ra2ReferenceExitServices {
    void *context;
    void (*clear_field)(void *, uint32_t offset);
    void (*restore_and_return)(void *);
} Ra2ReferenceExitServices;

/* 早退保留首引用；第二种成员终结还须清管理器，之后才读取保存帧。 */
void ra2_finish_reference_cleanup(const Ra2ReferenceExitServices *services,
    uint32_t clear_reference, uint32_t clear_manager);
