#pragma once
#include <stdint.h>

typedef struct Ra2TechnoBaseCleanupServices {
    void *context;
    void (*begin_radio)(void *);
    int32_t (*has_data)(void *);
    int32_t (*owns_data)(void *);
    void (*free_data)(void *);
    void (*reset_storage)(void *);
    void (*begin_mission)(void *);
    void (*destroy_object)(void *);
} Ra2TechnoBaseCleanupServices;

/* 先退出Radio存储，再进入Mission并调度Object；底层Object实现保持委托。 */
void ra2_cleanup_techno_base(const Ra2TechnoBaseCleanupServices *services);
