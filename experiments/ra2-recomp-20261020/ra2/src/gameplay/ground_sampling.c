#include "ground_sampling.h"
static void choose_table(int32_t selector, unsigned alternate, Ra2SamplingChoice *choice,
    const Ra2SamplingServices *s, Ra2SamplingTemplate *selected)
{
    *selected=s->template_at(s->context,selector);
    choice->table=alternate?selected->alternate:selected->normal;
    s->select_table(s->context,choice->table);
}
Ra2SamplingPhase ra2_ground_choose_full_sample(int32_t progress, int32_t direction,
    int32_t selector, unsigned alternate, Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    if(progress<=7)return RA2_SAMPLING_REMAINDER;
    Ra2SamplingTemplate selected;
    choose_table(selector,alternate,choice,s,&selected);
    if(direction < -1 || direction > 8)return RA2_SAMPLING_INVALID_DIRECTION;
    choice->turning=0;
    if(direction!=-1 && direction!=8)
    {
        unsigned template_direction=(((unsigned)selected.facing>>4)+1u)>>1;
        choice->turning=(template_direction&7u)!=(unsigned)direction;
    }
    return RA2_SAMPLING_FULL_STEP;
}
Ra2SamplingPhase ra2_ground_finish_sample(int32_t *index, int32_t progress)
{
    *index=ra2_ground_next_sample_index(*index);
    return progress>7?RA2_SAMPLING_FULL_STEP:RA2_SAMPLING_REMAINDER;
}
Ra2SamplingPhase ra2_ground_choose_remainder(int32_t progress, int32_t selector,
    unsigned alternate, int32_t index, Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    if(progress<=0 || selector<=-1)return RA2_SAMPLING_DONE;
    Ra2SamplingTemplate selected;
    choose_table(selector,alternate,choice,s,&selected);
    choice->sample=s->sample_at(s->context,index);
    if(!choice->sample.x && !choice->sample.y && index)return RA2_SAMPLING_DONE;
    return RA2_SAMPLING_INTERPOLATE;
}
