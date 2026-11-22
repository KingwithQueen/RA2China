#include "ground_sampling.h"
#include "ground_sampling_shared.h"
Ra2SamplingPhase ra2_ground_choose_full_sample(int32_t progress, int32_t direction,
    int32_t selector, unsigned alternate, Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    if(progress<=RA2_PATH_SAMPLE_PROGRESS_QUANTUM)return RA2_SAMPLING_REMAINDER;
    Ra2SamplingTemplate selected=s->template_at(s->context,selector);
    return ra2_ground_choose_shared_full(progress,direction,-1,selected,alternate,choice,s);
}
Ra2SamplingPhase ra2_ground_finish_sample(int32_t *index, int32_t progress)
{
    *index=ra2_ground_next_sample_index(*index);
    return progress>RA2_PATH_SAMPLE_PROGRESS_QUANTUM?RA2_SAMPLING_FULL_STEP:RA2_SAMPLING_REMAINDER;
}
Ra2SamplingPhase ra2_ground_choose_remainder(int32_t progress, int32_t selector,
    unsigned alternate, int32_t index, Ra2SamplingChoice *choice, const Ra2SamplingServices *s)
{
    if(progress<=0 || selector<=-1)return RA2_SAMPLING_DONE;
    Ra2SamplingTemplate selected=s->template_at(s->context,selector);
    int32_t table=ra2_ground_template_index(selected,alternate);
    return ra2_ground_choose_selected_remainder(table,index,0,choice,s);
}
