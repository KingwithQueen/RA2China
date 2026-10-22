#ifndef RA2_GROUND_PATH_PREPARE_H
#define RA2_GROUND_PATH_PREPARE_H
#include "ground_path_search.h"

typedef struct Ra2PathOwnerType {
    unsigned facing_seed_exclusions;
    int32_t movement_zone;
} Ra2PathOwnerType;
typedef struct Ra2PathPreparation {
    const Ra2PathPoint *start, *target;
    uintptr_t start_reference, target_reference;
    Ra2SearchNode *root;
    int32_t expansion_limit;
    unsigned ignore_soft_obstacles, continue_at_blocked_goal;
    int32_t *start_level, *target_level, *movement_zone, *obstacle_mode;
    uint32_t *region_cursor, *last_region_point;
    const uint32_t **connected_regions;
    const uint32_t *saved_connected_regions;
    Ra2PathNodeCache cache;
    uint32_t grid_width;
} Ra2PathPreparation;
typedef struct Ra2PathPreparationServices {
    void *context;
    uintptr_t (*reference)(void *, const Ra2PathPoint *);
    int (*cell)(void *, uintptr_t, Ra2PathCell *);
    int32_t (*owner_kind)(void *);
    Ra2PathOwnerType (*owner_type)(void *);
    unsigned (*owner_on_bridge)(void *);
    int32_t (*owner_height)(void *);
    unsigned (*unit_blocked_goal_flag)(void *);
    Ra2SearchNode *(*create_root)(void *, uintptr_t, const Ra2PathPoint *);
    void (*toggle_obstacles)(void *);
    unsigned (*facing)(void *);
    uintptr_t (*adjacent)(void *, uintptr_t, unsigned);
} Ra2PathPreparationServices;
typedef enum Ra2PathPreparationResult {
    RA2_PREPARE_INVALID_CELL, RA2_PREPARE_ALREADY_THERE,
    RA2_PREPARE_EMPTY_ROOT, RA2_PREPARE_READY
} Ra2PathPreparationResult;
/* 不合并重复的类型/朝向查询：服务调用顺序也是原版行为的一部分。
 * 缓存层选择沿用入口的严格高度比较，不能套用邻格循环的高度差规则。 */
Ra2PathPreparationResult ra2_path_prepare(Ra2PathPreparation *, const Ra2PathPreparationServices *);
#endif
