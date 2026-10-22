#include "ground_template_next.h"
uint32_t ra2_ground_template_cell(int32_t x,int32_t y)
{
    /* 原版有符号除256向零取整，再分别截为16位。 */
    return (uint32_t)(uint16_t)(x/256)|((uint32_t)(uint16_t)(y/256)<<16);
}
int ra2_ground_prepare_next_template(const Ra2TemplateNextServices *s)
{
    if (!(s->can_advance(s->context)&255u)) return 0;
    return (s->cell_accepts(s->context)&255u)!=0;
}
uintptr_t ra2_ground_advance_template_sample(const Ra2TemplateSampleServices *s)
{
    int32_t heading=s->sample_heading(s->context);
    s->store_heading(s->context,heading);
    return s->transform(s->context);
}
