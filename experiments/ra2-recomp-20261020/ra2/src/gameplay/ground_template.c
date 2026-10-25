#include <stdint.h>
#include <string.h>
#include "ground_template.h"
#include "ground_segment_admission.h"
#include "ground_template_table.h"

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
    return ra2_ground_template_table(direction, next_direction, crushing, services);
}

Ra2TemplateSelection ra2_ground_template_table(int32_t direction, int32_t next_direction,
    unsigned crushing, const Ra2TemplateServices *services)
{
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

static int32_t consume_direction_queue(Ra2SegmentCommitState *state,int skip_shift,
    int32_t terminal_direction)
{
    if(!skip_shift) {
        for(unsigned i=0;i<23;++i)state->directions[i]=state->directions[i+1];
        terminal_direction=-1;
    }
    /* 保留队列的入口仍写指定尾槽；普通弹出只移动23槽，再补-1。 */
    state->directions[23]=terminal_direction;
    return terminal_direction;
}

static void prepare_segment_publication(Ra2SegmentCommitState *state,Ra2WorldPoint invalid,
    Ra2WorldPoint candidate)
{
    state->target_cell_x=(int16_t)(candidate.x/256);
    state->target_cell_y=(int16_t)(candidate.y/256);
    state->sound_pending=0;
    state->sample_index=0;
    /* 已经无效的旧段不附带改写driving；保留原状态与放行服务的交接。 */
    if(!same_position(state->movement.segment_end,invalid)) {
        state->movement.segment_end=invalid;
        state->movement.driving=0;
    }
}

static void reject_queued_segment(Ra2SegmentCommitState *state,int32_t terminal,
    const Ra2SegmentCommitServices *services)
{
    state->selector=terminal;
    state->directions[0]=terminal;
    services->set_speed_zero(services->context);
}

void ra2_ground_commit_segment(Ra2SegmentCommitState *state,Ra2WorldPoint invalid_position,
    Ra2WorldPoint candidate,int skip_shift,int32_t terminal_direction,const Ra2SegmentCommitServices *services)
{
    terminal_direction=consume_direction_queue(state,skip_shift,terminal_direction);
    prepare_segment_publication(state,invalid_position,candidate);
    const Ra2SegmentAdmissionServices admission={services->context,services->cell_accepts_owner,
        services->owner_flag_76,services->start_segment,services->owner_alive};
    if(ra2_ground_admit_segment(&state->movement.segment_end,&state->movement.driving,
        invalid_position,candidate,&admission)==RA2_SEGMENT_STARTED)return;
    reject_queued_segment(state,terminal_direction,services);
}
