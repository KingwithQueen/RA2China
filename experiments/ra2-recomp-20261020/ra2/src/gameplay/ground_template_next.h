#pragma once
#include <stdint.h>
typedef struct Ra2TemplateNextServices {
    void *context;
    unsigned (*can_advance)(void *);
    unsigned (*cell_accepts)(void *);
} Ra2TemplateNextServices;
/* 保留两次服务之间的单位重读，先确认单位继续，再检查下一格。 */
int ra2_ground_prepare_next_template(const Ra2TemplateNextServices *services);
uint32_t ra2_ground_template_cell(int32_t x,int32_t y);
typedef struct Ra2TemplateSample { int32_t x,y,heading; } Ra2TemplateSample;
typedef struct Ra2TemplateSampleServices {
    void *context;
    int32_t (*sample_heading)(void *);
    void (*store_heading)(void *,int32_t);
    uintptr_t (*transform)(void *);
} Ra2TemplateSampleServices;
uintptr_t ra2_ground_advance_template_sample(const Ra2TemplateSampleServices *services);
