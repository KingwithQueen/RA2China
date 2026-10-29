#pragma once
#include <stdint.h>

typedef struct Ra2ReferenceCountServices {
    void *context;
    uint32_t (*read_count)(void *);
    void (*set_result)(void *, uint32_t value);
    void (*write_count)(void *, uint32_t value);
} Ra2ReferenceCountServices;

/* 先写回绕递减值，只钳位内存；返回结果和标志不随钳位改成零。 */
void ra2_decrement_reference_count(const Ra2ReferenceCountServices *services);
