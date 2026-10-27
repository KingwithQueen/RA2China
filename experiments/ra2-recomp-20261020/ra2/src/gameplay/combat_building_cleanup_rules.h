#pragma once
#include <stdint.h>

typedef enum Ra2BuildingCleanupRuleQuery {
    RA2_BCR_ACTIVE, RA2_BCR_CLOAK_TYPE, RA2_BCR_CLOAK_GENERATOR,
    RA2_BCR_SUPER_INDEX, RA2_BCR_AUX_BUILDING, RA2_BCR_OWNER_AUX_COUNT,
    RA2_BCR_CURRENT_SUPER, RA2_BCR_HEALTH_CHANGED,
    RA2_BCR_CURRENT_TYPE, RA2_BCR_OWNER
} Ra2BuildingCleanupRuleQuery;

typedef enum Ra2BuildingCleanupRuleOperation {
    RA2_BCR_DISABLE_CLOAK, RA2_BCR_REFRESH_SUPERS, RA2_BCR_MARK_OWNER,
    RA2_BCR_REMOVE_OWNER_BUILDING, RA2_BCR_CLEANUP_BUILDING
} Ra2BuildingCleanupRuleOperation;

typedef struct Ra2BuildingCleanupRuleServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingCleanupRuleQuery, uint32_t);
    void (*perform)(void *, Ra2BuildingCleanupRuleOperation, uint32_t);
} Ra2BuildingCleanupRuleServices;

/* 各段保留实时查询接缝；超武、归属容器与隐形传播内部仍委托已有实现。 */
void ra2_cleanup_building_cloak_rules(const Ra2BuildingCleanupRuleServices *services);
void ra2_cleanup_building_super_rules(const Ra2BuildingCleanupRuleServices *services);
void ra2_cleanup_building_owner_rules(const Ra2BuildingCleanupRuleServices *services);
void ra2_cleanup_building_rules(const Ra2BuildingCleanupRuleServices *services);
