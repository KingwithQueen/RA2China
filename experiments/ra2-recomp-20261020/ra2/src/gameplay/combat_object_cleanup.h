#pragma once
#include <stdint.h>

typedef struct Ra2ObjectCleanupServices {
    void *context;
    void (*begin)(void *);
    int32_t (*find)(void *);
    int32_t (*can_remove)(void *);
    int32_t (*shrink_has_following)(void *);
    int32_t (*shift_next)(void *);
} Ra2ObjectCleanupServices;

/* 仅移除查找返回的那一项，顺序搬移后继，不额外清理旧尾槽。 */
void ra2_cleanup_object_registry(const Ra2ObjectCleanupServices *services);
