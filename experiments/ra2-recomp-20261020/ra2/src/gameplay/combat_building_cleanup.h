#pragma once
#include <stdint.h>

typedef enum Ra2BuildingCleanupQuery {
    RA2_BC_DELETE_FLAG, RA2_BC_HAS_MEMBER, RA2_BC_FIND_BUILDING, RA2_BC_HAS_SLOT
} Ra2BuildingCleanupQuery;
typedef enum Ra2BuildingCleanupOperation {
    RA2_BC_CLEANUP_BODY, RA2_BC_FREE_OBJECT,
    RA2_BC_RESET_TABLES, RA2_BC_CLEAR_CONTAINER_A, RA2_BC_CLEAR_CONTAINER_B,
    RA2_BC_RELEASE_CONTAINER_A, RA2_BC_RELEASE_CONTAINER_B,
    RA2_BC_CANCEL_MEMBER, RA2_BC_DELETE_MEMBER, RA2_BC_CLEAR_MEMBER,
    RA2_BC_DETACH_REFERENCES, RA2_BC_BUILDING_CLEANUP, RA2_BC_REMOVE_BUILDING,
    RA2_BC_RESET_MODE, RA2_BC_RELEASE_TYPE, RA2_BC_BEGIN_SLOTS,
    RA2_BC_UNINIT_SLOT, RA2_BC_CLEAR_SLOT, RA2_BC_NEXT_SLOT
} Ra2BuildingCleanupOperation;
typedef struct Ra2BuildingCleanupServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingCleanupQuery, uint32_t);
    void (*perform)(void *, Ra2BuildingCleanupOperation, uint32_t);
} Ra2BuildingCleanupServices;

/* 完整清理仍经原入口；返回后才决定是否释放，不再次注销或入队。 */
void ra2_delete_building(const Ra2BuildingCleanupServices *services);
/* 只接管建筑清理前段的直接接口；归属规则及容器/基类析构继续委托。 */
void ra2_cleanup_building_prefix(const Ra2BuildingCleanupServices *services);
