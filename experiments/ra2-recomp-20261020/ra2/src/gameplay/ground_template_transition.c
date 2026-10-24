#include <string.h>
#include "ground_template_entry.h"
#include "ground_template_transition.h"
#include "ground_bridge_plane.h"

static int32_t signed_shift_cell(uint32_t adjusted)
{
    int32_t signed_value;
    memcpy(&signed_value, &adjusted, sizeof(signed_value));
    return signed_value >> 8;
}

Ra2TemplateCells ra2_ground_template_cells(uint32_t adjusted_x, uint32_t adjusted_y,
                                         int32_t current_x, int32_t current_y)
{
    Ra2TemplateCells cells;
    cells.target_x = signed_shift_cell(adjusted_x);
    cells.target_y = signed_shift_cell(adjusted_y);
    cells.current_x = signed_shift_cell(ra2_ground_sample_adjusted(current_x));
    cells.current_y = signed_shift_cell(ra2_ground_sample_adjusted(current_y));
    cells.packed_target = (uint16_t)cells.target_x | ((uint32_t)(uint16_t)cells.target_y << 16);
    cells.same_cell = (uint16_t)cells.target_x == (uint16_t)cells.current_x
                   && (uint16_t)cells.target_y == (uint16_t)cells.current_y;
    return cells;
}

static int clear_type_gate(const Ra2TemplateGateServices *services, void *context)
{
    if (services->classification(context) >= 7) return 0;
    if (!services->type_flag(context, 0)) return 0;
    services->clear_classification(context);
    return 1;
}

static void clear_overlay_gate(const Ra2TemplateGateServices *services, void *context)
{
    /* 第一阶段的类型查询可能改变分类；第二阶段必须重新读取。 */
    int32_t classification = services->classification(context);
    if (classification != 5 && classification != 4) return;
    if (!services->type_flag(context, 1)) return;
    if (services->overlay(context) != 0) return;
    services->clear_classification(context);
}

void ra2_ground_template_gate(const Ra2TemplateGateServices *services)
{
    void *context = services->context;
    if (!clear_type_gate(services, context)) clear_overlay_gate(services, context);
}

void ra2_ground_template_layer(const Ra2TemplateLayerServices *services)
{
    /* set_layer 后重新查询标志的约定由共享边界保持，不能预先缓存下一格标志。 */
    ra2_ground_transition_bridge(services->context,services->level,services->flags,services->set_layer);
}
