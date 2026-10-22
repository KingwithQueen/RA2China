#include <stdint.h>
#include <string.h>
#include "ground_template.h"

static int32_t signed_bits(uint32_t bits)
{
    int32_t result;
    memcpy(&result,&bits,sizeof(result));
    return result;
}

Ra2TemplateSelection ra2_ground_choose_template(int32_t direction, int32_t next_direction,
    int prevent_turn, int crush_current_overlay, int normalize_directions, const Ra2TemplateServices *services)
{
    if (normalize_directions)
    {
        if (next_direction == 8) next_direction = direction;
        if (next_direction == -1 || prevent_turn) next_direction = direction;
    }
    int crush_neighbor = next_direction != -1
        && services->neighbor_overlay_crushable(services->context,next_direction);
    unsigned crushing = crush_neighbor || crush_current_overlay;
    if (crushing) next_direction = direction;
    int32_t selector = signed_bits((uint32_t)next_direction + (uint32_t)direction * 8u);
    if (!services->template_byte(services->context,selector,RA2_TEMPLATE_ENTRY_TAG))
    {
        selector = signed_bits((uint32_t)direction * 9u);
    }
    Ra2TemplateSelection result = { next_direction,selector,crushing,
        services->template_byte(services->context,selector,RA2_TEMPLATE_FLAGS) };
    return result;
}

static int same_position(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return left.x==right.x && left.y==right.y && left.z==right.z;
}

void ra2_ground_commit_segment(Ra2SegmentCommitState *state, Ra2WorldPoint invalid_position,
    Ra2WorldPoint candidate, int skip_shift, int32_t terminal_direction, const Ra2SegmentCommitServices *services)
{
    if (!skip_shift)
    {
        for (unsigned i=0; i<23; ++i) state->directions[i] = state->directions[i+1];
        terminal_direction = -1;
    }
    state->directions[23] = terminal_direction;
    state->target_cell_x = (int16_t)(candidate.x / 256);
    state->target_cell_y = (int16_t)(candidate.y / 256);
    state->sound_pending = 0;
    state->sample_index = 0;
    if (!same_position(state->movement.segment_end,invalid_position))
    {
        state->movement.segment_end = invalid_position;
        state->movement.driving = 0;
    }
    if (!same_position(candidate,invalid_position))
    {
        state->movement.segment_end = candidate;
        state->movement.driving = 1;
        if (services->cell_accepts_owner(services->context,candidate)
            && !services->owner_flag_76(services->context))
        {
            services->start_segment(services->context,candidate);
            return;
        }
        if (services->owner_alive(services->context))
        {
            state->movement.segment_end = invalid_position;
            state->movement.driving = 0;
        }
    }
    state->selector = terminal_direction;
    state->directions[0] = terminal_direction;
    services->set_speed_zero(services->context);
}
