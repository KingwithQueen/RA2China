#include "ground_transition_rules.h"
#include "ground_passage.h"

int32_t ra2_ground_classify_transition(const Ra2PassageCell *to, const Ra2PassageCell *from,
    int32_t direction, int32_t *level, uint8_t *changing_layer)
{
    if (direction == -1)
    {
        if (*level == -1 && (to->flags & 0x100u))
            *level = ra2_ground_layer_reference(to->level,1);
        return 0;
    }
    if (!from || !to) return 0;
    if (*level == -1 && (from->flags & 0x100u))
    {
        *level = ra2_ground_layer_reference(from->level,1);
        if (!(to->flags & 0x200u)) return 7;
    }
    return ra2_ground_check_height_step(from->level,to->level,*level,from->flags,to->flags,
        from->ramp,to->ramp,changing_layer);
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
