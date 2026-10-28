#pragma once
#include <stdint.h>

enum { RA2_REFERENCE_CONTINUE, RA2_REFERENCE_EARLY, RA2_REFERENCE_INVALID };
typedef struct Ra2ReferencePrefixServices {
    void *context;
    void (*begin)(void *);
    int32_t (*active)(void *);
    int32_t (*manager_matches)(void *);
    int32_t (*has_reference)(void *);
    int32_t (*first_stamp_matches)(void *);
    int32_t (*second_stamp_matches)(void *);
    int32_t (*is_dead)(void *);
} Ra2ReferencePrefixServices;

/* 检查按原顺序短路；两类失败由原函数各自的清理出口处理。 */
uint32_t ra2_check_reference_prefix(const Ra2ReferencePrefixServices *services);
