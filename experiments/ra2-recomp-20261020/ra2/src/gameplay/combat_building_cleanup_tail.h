#pragma once
#include <stdint.h>

typedef enum Ra2BuildingTailQuery {
    RA2_BCT_HAS_DATA, RA2_BCT_OWNS_DATA
} Ra2BuildingTailQuery;

typedef enum Ra2BuildingTailOperation {
    RA2_BCT_CLEAR_STATE, RA2_BCT_CLEAR_CONTAINER, RA2_BCT_RESIZE_CONTAINER,
    RA2_BCT_BEGIN_RELEASE, RA2_BCT_FREE_DATA, RA2_BCT_END_RELEASE, RA2_BCT_BASE_DESTRUCTOR
} Ra2BuildingTailOperation;

typedef struct Ra2BuildingTailServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingTailQuery, uint32_t);
    void (*perform)(void *, Ra2BuildingTailOperation, uint32_t);
} Ra2BuildingTailServices;

/* 先按成员顺序调用当前虚接口，再逆序清理存储；基类析构仍委托原入口。 */
void ra2_cleanup_building_tail(const Ra2BuildingTailServices *services);
