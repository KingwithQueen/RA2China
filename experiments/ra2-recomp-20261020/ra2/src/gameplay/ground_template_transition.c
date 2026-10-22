#include <string.h>
#include "ground_template_entry.h"
#include "ground_template_transition.h"

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

void ra2_ground_template_gate(const Ra2TemplateGateServices *services)
{
    void *context = services->context;
    if (services->classification(context) < 7 && services->type_flag(context, 0))
    {
        services->clear_classification(context);
        return;
    }

    int32_t classification = services->classification(context);
    if ((classification == 5 || classification == 4)
        && services->type_flag(context, 1) && services->overlay(context) == 0)
    {
        services->clear_classification(context);
    }
}

void ra2_ground_template_layer(const Ra2TemplateLayerServices *services)
{
    void *context = services->context;
    int32_t previous_level = services->level(context, 0);
    int32_t next_level = services->level(context, 1);
    if ((uint32_t)next_level == (uint32_t)previous_level - 4u
        && (services->flags(context, 1) & 0x100u))
    {
        services->set_layer(context, 1);
    }
    if (!(services->flags(context, 1) & 0x100u)
        && (services->flags(context, 0) & 0x100u))
    {
        services->set_layer(context, 0);
    }
}
