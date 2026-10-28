#pragma once
#include "combat_object_cleanup.h"

typedef struct Ra2ObjectTablesCleanupServices {
    void *context;
    void (*select_table)(void *, uint32_t);
    Ra2ObjectCleanupServices registry;
} Ra2ObjectTablesCleanupServices;

/* 逐表完成后再进入下一表，复用首表的单项顺序移除规则。 */
void ra2_cleanup_object_tables(const Ra2ObjectTablesCleanupServices *services);
