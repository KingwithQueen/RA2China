#include "ground_allied.h"

Ra2AlliedOutcome ra2_ground_classify_allied_motion(int32_t *passage,
    const Ra2AlliedServices *s)
{
    void *c = s->context;
    /* 原版会两次询问任务；第一次查询期间可能执行世界回调。 */
    if (s->query(c, RA2_ALLIED_OWNER_MISSION) == 7
        && s->query(c, RA2_ALLIED_IS_OWNER_DESTINATION)
        && s->query(c, RA2_ALLIED_OBJECT_KIND) == 1)
        return RA2_ALLIED_CLEAR;
    if (s->query(c, RA2_ALLIED_OWNER_MISSION) == 11
        && s->query(c, RA2_ALLIED_IS_OWNER_TARGET))
        return RA2_ALLIED_BLOCKED;

    int moving = 0;
    if (s->query(c, RA2_ALLIED_OBJECT_HAS_MOVEMENT))
    {
        s->remember_moving_object(c, 1);
        moving = s->query(c, RA2_ALLIED_OBJECT_HAS_DESTINATION)
            || s->query(c, RA2_ALLIED_OBJECT_IS_TURNING)
            || s->query(c, RA2_ALLIED_OBJECT_IS_MOVING);
    }
    else s->remember_moving_object(c, 0);

    if (!s->query(c, RA2_ALLIED_OBJECT_IS_ALLIED))
        return RA2_ALLIED_CHECK_ENEMY;
    if (!moving) return RA2_ALLIED_CHECK_STATIONARY;

    unsigned owner_heading = s->owner_heading(c);
    unsigned opposite_heading = s->opposite_object_heading(c);
    /* 即使方向不相等也计算相对方向，保留原版数值服务的执行顺序。 */
    unsigned relative_heading = s->relative_heading(c);
    if (owner_heading == opposite_heading && s->distance(c) <= 511
        && relative_heading == owner_heading)
        return RA2_ALLIED_BLOCKED;

    /* 5A0 含义尚未完全确认。15 号对象仍须查询移动器，不能合并分支。 */
    int moving_passage = s->query(c, RA2_ALLIED_OBJECT_FLAG_5A0)
        && s->query(c, RA2_ALLIED_OBJECT_KIND) != 15;
    if (!moving_passage)
        moving_passage = s->query(c, RA2_ALLIED_OBJECT_WANTS_MOVING_PASSAGE);
    if (moving_passage && *passage < RA2_CELL_MOVING_OBSTACLE)
        *passage = RA2_CELL_MOVING_OBSTACLE;
    return RA2_ALLIED_SCANNED;
}
