#include "combat_building_post.h"
#define Q(q) s->query(s->context, RA2_BP_##q)
#define DO(op, value) s->perform(s->context, RA2_BP_##op, value)

int ra2_prepare_building_rubble(const Ra2BuildingPostServices *s)
{
    if (!Q(LEAVE_RUBBLE) || !Q(IMAGE_OUT_PRESENT)) return 0;
    if (!Q(LOAD_IMAGE)) return 0;
    int32_t half = Q(IMAGE_FRAME_COUNT) / 2;
    DO(PUBLISH_HALF_FRAMES, half);
    if (half <= 3) return 0;
    DO(PUBLISH_RUBBLE_LEVEL, 3);
    return 1;
}

int16_t ra2_building_post_cell(int32_t coordinate)
{
    return (int16_t)(uint16_t)(coordinate / 256);
}

void ra2_schedule_building_crate(const Ra2BuildingPostServices *s)
{
    if (!Q(CRATE_BENEATH)) return;
    DO(CRATE_POSITION, 0);
    /* CrateBeneathIsMoney在坐标回调后从当前类型读取。 */
    DO(PLACE_CRATE, Q(CRATE_MONEY) ? 0 : 20);
}

void ra2_rewrite_building_rubble(const Ra2BuildingPostServices *s)
{
    DO(RUBBLE_FOUNDATION, 0);
    DO(RUBBLE_POSITION, 0);
    /* 保留实时基础格列表：回调可以改变尚未读取的偏移或哨兵。 */
    while (!Q(FOUNDATION_END)) {
        DO(RUBBLE_CELL, 0);
        DO(CLEAR_CELL, 0);
        DO(PUBLISH_RUBBLE_CELL, 0);
        DO(RECALCULATE_CELL, -1);
        DO(REFRESH_MAP_CELL, 0);
        DO(REFRESH_PASSABILITY, 0);
        DO(FINISH_CELL, 0);
    }
    /* 锚格查找返回后才读取建筑当前类型，两个矩形接口维持原次序。 */
    DO(RUBBLE_ANCHOR, 0);
    DO(FIRST_RECTANGLE, 0);
    DO(SECOND_RECTANGLE, 0);
}

void ra2_invalidate_building_rubble(const Ra2BuildingPostServices *s)
{
    DO(PREPARE_INVALIDATION, 0);
    DO(INVALIDATE_RECTANGLE, 0);
    DO(FIND_CURRENT_ANCHOR, 0);
    DO(INVALIDATE_ANCHOR, 0);
}
