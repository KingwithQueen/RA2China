#pragma once
#include <stdint.h>

typedef struct Ra2ReferenceControllerServices {
    void *context;
    int32_t (*has_controller)(void *);
    int32_t (*owns_reference)(void *);
    int32_t (*needs_cancel)(void *);
    void (*cancel)(void *);
    void (*release_current)(void *);
    void (*clear_current_field)(void *, uint32_t offset);
    void (*clear_reference_link)(void *);
} Ra2ReferenceControllerServices;

/* 回调和各次存储都使用当前关联，不把最初的控制对象缓存到清理尾部。 */
void ra2_cleanup_reference_controller(const Ra2ReferenceControllerServices *services);
