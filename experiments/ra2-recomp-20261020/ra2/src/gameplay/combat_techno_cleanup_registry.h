#pragma once
#include <stdint.h>

typedef enum Ra2TechnoRegistryOperation {
    RA2_TCR_BEGIN, RA2_TCR_CLEAR_AUXILIARY, RA2_TCR_RELEASE_AUXILIARY,
    RA2_TCR_CLEAR_STATE, RA2_TCR_RESTORE_SAVED
} Ra2TechnoRegistryOperation;

typedef struct Ra2TechnoRegistryServices {
    void *context;
    void (*perform)(void *, Ra2TechnoRegistryOperation);
    int32_t (*find)(void *, uint32_t);
    void (*remove)(void *, uint32_t, int32_t);
} Ra2TechnoRegistryServices;

/* 辅助成员的两次清理先完成；两个登记表逐个查询，只跳过返回 -1 的项。 */
void ra2_cleanup_techno_registries(const Ra2TechnoRegistryServices *services);
