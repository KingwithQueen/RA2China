#include "ground_template_entry.h"
uint32_t ra2_ground_sample_adjusted(int32_t value)
{ return (uint32_t)value+(value<0?255u:0u); }
uint32_t ra2_ground_sample_cell(int32_t x,int32_t y)
{ return (uint32_t)(uint16_t)(x/256)|((uint32_t)(uint16_t)(y/256)<<16); }
int32_t ra2_ground_prepare_template_passage(const Ra2TemplatePassageServices *s)
{
    void *c=s->context;uintptr_t cell=s->next_cell(c);
    s->mark(c,0);
    int32_t classification=s->classify(c,cell);
    s->mark(c,1);
    return classification;
}
