#pragma once
#include <stdint.h>

typedef struct Ra2TemplateCells
{
    int32_t target_x, target_y;
    int32_t current_x, current_y;
    uint32_t packed_target;
    unsigned same_cell;
} Ra2TemplateCells;

/* Advance 已修正过目标坐标；这里按有符号右移取格子，保留极值回绕。 */
Ra2TemplateCells ra2_ground_template_cells(uint32_t adjusted_x, uint32_t adjusted_y,
                                         int32_t current_x, int32_t current_y);

typedef struct Ra2TemplateGateServices
{
    void *context;
    int32_t (*classification)(void *);
    unsigned (*type_flag)(void *, unsigned crush_flag);
    int32_t (*overlay)(void *);
    void (*clear_classification)(void *);
} Ra2TemplateGateServices;

/* 可忽略障碍的单位允许直接前进；碾压类只在没有地表覆盖物时放行。
   类型回调可能改写共享分类，第二个判断必须重新读取。 */
void ra2_ground_template_gate(const Ra2TemplateGateServices *services);
