#include <string.h>
#include "ground_passage.h"

static int32_t signed_bits(uint32_t value)
{
    int32_t result;
    memcpy(&result, &value, sizeof(result));
    return result;
}

int32_t ra2_ground_classify_transition(const Ra2PassageCell *to, const Ra2PassageCell *from,
    int32_t direction, int32_t *level, uint8_t *changing_layer)
{
    if (direction == -1)
    {
        if (*level == -1 && (to->flags & 0x100u))
            *level = to->level + 4;
        return 0;
    }
    if (!from || !to) return 0;
    if (*level == -1 && (from->flags & 0x100u))
    {
        *level = from->level + 4;
        if (!(to->flags & 0x200u)) return 7;
    }
    uint32_t bridge = from->flags & 0x100u;
    int32_t difference = signed_bits((uint32_t)(bridge ? from->level : *level) - (uint32_t)to->level);
    uint32_t magnitude = difference < 0 ? 0u - (uint32_t)difference : (uint32_t)difference;
    switch (magnitude)
    {
        case 0:
            if ((to->flags & 0x300u) == 0x300u && bridge) return 0;
            return *level == -1 || *level == to->level ? 0 : 7;
        case 1:
            return (difference > 0 ? to->ramp : from->ramp) ? 0 : 7;
        case 4:
            if (from->level == to->level - 4 && (*level != to->level || !bridge)) return 7;
            if (to->level == from->level - 4)
            {
                if ((to->flags & 0x300u) != 0x300u) return 7;
                *changing_layer = 1;
            }
            return 0;
        default:
            return 7;
    }
}

int32_t ra2_ground_base_can_enter(unsigned check_locomotor, const Ra2BasePassageServices *s)
{
    /* 原版先读locomotor，再检查开关。 */
    int present = s->has_locomotor(s->context);
    return present && check_locomotor ? s->locomotor_can_enter(s->context) : 0;
}

int32_t ra2_ground_height_at(Ra2WorldPoint point, const Ra2GroundHeightServices *s)
{
    uintptr_t cell = s->cell_at_world(s->context, point);
    return s->height_in_cell(s->context, cell, point);
}
