#include "ground_path_rebuild.h"
#include "x87_arithmetic.h"
void ra2_path_rebuild(const Ra2SearchNode *end, int32_t *directions, int32_t *surface_levels,
    const int32_t direction_table[9], Ra2PathPointReader read_point, void *context, Ra2RebuiltPath *out)
{
    out->score = ra2_real_truncate_i32(ra2_real_from_f32(end->priority));
    out->length = end->path_length;
    out->directions = directions;
    out->surface_levels = surface_levels;
    out->reserved = 0;
    out->scratch = (Ra2PathPoint){0, 0};
    const Ra2PathLink *child = end->path_link;
    const Ra2PathLink *parent = child->parent;
    for (int32_t slot = end->path_length - 2; slot >= 0; --slot) {
        surface_levels[slot] = parent->surface_level;
        Ra2PathPoint from = read_point(context, parent->cell_reference);
        Ra2PathPoint to = read_point(context, child->cell_reference);
        int32_t dx = (int32_t)from.x - to.x, dy = (int32_t)from.y - to.y;
        directions[slot] = dx >= -1 && dx <= 1 && dy >= -1 && dy <= 1
            ? direction_table[dy * 3 + dx + 4] : 8;
        child = child->parent;
        parent = parent->parent;
    }
    directions[end->path_length - 1] = -1;
    out->start = read_point(context, child->cell_reference);
    if (!out->score) out->score = 1;
}
