#include <string.h>
#include "ground_path_prepare.h"

static void exclude_cell(Ra2PathPreparation *p, const Ra2PathCell *cell, int32_t threshold)
{
    uint32_t index = (uint32_t)(int32_t)cell->point.y * p->grid_width + (uint32_t)(int32_t)cell->point.x;
    ra2_path_cache_publish(&p->cache, index, *p->start_level <= threshold, 0.0f);
}

static void resolve_bridge_levels(Ra2PathPreparation *p,
    const Ra2PathPreparationServices *v, Ra2PathCell *start, Ra2PathCell *target)
{
    /* 保留校验时的格数据；后续重复读取的返回值原来就不作分支判断。 */
    int32_t kind = v->owner_kind(v->context);
    v->cell(v->context, p->target_reference, target);
    *p->target_level = target->ground_level + (kind != 2 && target->has_bridge ? 4 : 0);
    kind = v->owner_kind(v->context);
    v->cell(v->context, p->start_reference, start);
    *p->start_level = start->ground_level + (kind != 2 && v->owner_on_bridge(v->context) ? 4 : 0);

    Ra2PathOwnerType type = v->owner_type(v->context);
    v->cell(v->context, p->start_reference, start);
    if (type.facing_seed_exclusions && start->has_bridge) {
        int32_t height = v->owner_height(v->context);
        int32_t difference = height - *p->start_level;
        if (difference > 2 || difference < -2) *p->start_level += 4;
    }
}

static void create_root_state(Ra2PathPreparation *p, const Ra2PathPreparationServices *v)
{
    /* 第二次类型查询与区域快照必须先于根节点服务；同格判断仍在创建根之后。 */
    Ra2PathOwnerType type = v->owner_type(v->context);
    *p->movement_zone = type.movement_zone;
    *p->region_cursor = 0;
    memcpy(p->last_region_point, p->start, sizeof(*p->start));
    p->saved_connected_regions = *p->connected_regions;
    p->root = v->create_root(v->context, p->start_reference, p->target);

}

static void seed_start_exclusions(Ra2PathPreparation *p,
    const Ra2PathPreparationServices *v, Ra2PathCell *start)
{
    /* 根节点回调之后才读取障碍模式、类型和朝向；每次仍读取实时context。 */
    if (*p->obstacle_mode) v->toggle_obstacles(v->context);
    v->cell(v->context, p->start_reference, start);
    exclude_cell(p, start, start->ground_level);

    Ra2PathOwnerType type = v->owner_type(v->context);
    p->ignore_soft_obstacles = type.facing_seed_exclusions != 0;
    if (p->ignore_soft_obstacles) {
        /* 原版查询九次朝向，第九次只查询而不排除邻格。角度差3..5
         * 是面向背后的三个方向，差值不先做环绕归一化。 */
        for (unsigned direction = 0; direction <= 8; ++direction) {
            int32_t difference = (int32_t)v->facing(v->context) - (int32_t)direction;
            if (direction == 8 || (difference >= -2 && difference <= 2)
                || difference >= 6 || difference <= -6) continue;
            Ra2PathCell adjacent;
            v->cell(v->context, v->adjacent(v->context, p->start_reference, direction), &adjacent);
            exclude_cell(p, &adjacent, adjacent.ground_level + 1);
        }
    }
}

Ra2PathPreparationResult ra2_path_prepare(Ra2PathPreparation *p, const Ra2PathPreparationServices *v)
{
    Ra2PathCell start, target;
    p->start_reference = v->reference(v->context, p->start);
    p->target_reference = v->reference(v->context, p->target);
    if (!v->cell(v->context, p->start_reference, &start)
        || !v->cell(v->context, p->target_reference, &target))
        return RA2_PREPARE_INVALID_CELL;

    resolve_bridge_levels(p, v, &start, &target);
    create_root_state(p, v);

    if (p->start->x == p->target->x && p->start->y == p->target->y
        && *p->start_level == *p->target_level) return RA2_PREPARE_ALREADY_THERE;
    seed_start_exclusions(p, v, &start);
    int32_t kind = v->owner_kind(v->context);
    p->continue_at_blocked_goal = kind == 1 && v->unit_blocked_goal_flag(v->context);
    if (p->expansion_limit < 0) p->expansion_limit = 0xFFF7;
    return p->root ? RA2_PREPARE_READY : RA2_PREPARE_EMPTY_ROOT;
}
