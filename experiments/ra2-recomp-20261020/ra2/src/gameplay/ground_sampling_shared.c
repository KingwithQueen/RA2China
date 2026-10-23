#include "ground_sampling_shared.h"

Ra2SamplingPhase ra2_ground_choose_shared_full(int32_t progress, int32_t direction,
    int32_t direction_sentinel, Ra2SamplingTemplate selected, unsigned alternate,
    Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    if (progress <= 7) return RA2_SAMPLING_REMAINDER;
    choice->table = ra2_ground_template_index(selected, alternate);
    s->select_table(s->context, choice->table);
    if (direction < direction_sentinel || direction > 8) return RA2_SAMPLING_INVALID_DIRECTION;
    choice->turning = 0;
    if (direction != direction_sentinel && direction != 8)
    {
        unsigned facing = ((((unsigned)selected.facing >> 4) + 1u) >> 1) & 7u;
        choice->turning = facing != (unsigned)direction;
    }
    return RA2_SAMPLING_FULL_STEP;
}

Ra2SamplingPhase ra2_ground_choose_selected_remainder(int32_t table, int32_t index,
    int32_t end_sentinel, Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    choice->table = table;
    s->select_table(s->context, table);
    choice->sample = s->sample_at(s->context, index);
    if (choice->sample.x == end_sentinel && choice->sample.y == end_sentinel && index != end_sentinel)
        return RA2_SAMPLING_DONE;
    return RA2_SAMPLING_INTERPOLATE;
}

int32_t ra2_ground_template_index(Ra2SamplingTemplate selected, unsigned alternate)
{ return alternate ? selected.alternate : selected.normal; }
