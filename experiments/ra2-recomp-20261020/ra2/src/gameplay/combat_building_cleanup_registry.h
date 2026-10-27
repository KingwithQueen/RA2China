#pragma once
#include <stdint.h>

typedef enum Ra2BuildingRegistryQuery {
    RA2_BCG_HAS_MEMBER, RA2_BCG_FIND
} Ra2BuildingRegistryQuery;

typedef enum Ra2BuildingRegistryOperation {
    RA2_BCG_DELETE_MEMBER, RA2_BCG_CLEAR_MEMBER, RA2_BCG_REMOVE
} Ra2BuildingRegistryOperation;

typedef struct Ra2BuildingRegistryServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingRegistryQuery, uint32_t);
    void (*perform)(void *, Ra2BuildingRegistryOperation, uint32_t);
} Ra2BuildingRegistryServices;

/* 成员删除后清零；逐表实时查找，命中才委托原按索引移除接口。 */
void ra2_cleanup_building_registries(const Ra2BuildingRegistryServices *services);
