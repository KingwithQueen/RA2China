#pragma once
#include <stdint.h>

typedef struct Ra2TechnoCleanupServices {
    void *context;
    void (*reset_tables)(void *);
    int32_t (*has_member)(void *, uint32_t);
    void (*cleanup_member)(void *, uint32_t);
    void (*clear_member)(void *, uint32_t);
} Ra2TechnoCleanupServices;

/* 按原顺序读取当前成员，清理回调返回后才清原槽；成员内部算法由接口承担。 */
void ra2_cleanup_techno_prefix(const Ra2TechnoCleanupServices *services);
