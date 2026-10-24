#include "ground_template_transition.h"
#include "ground_segment.h"

typedef struct SegmentGateContext
{
    Ra2SegmentPreparation *output;
    const Ra2SegmentServices *services;
} SegmentGateContext;
static int32_t gate_classification(void *opaque)
{return ((SegmentGateContext *)opaque)->output->passage;}
static unsigned gate_type(void *opaque,unsigned crusher)
{
    SegmentGateContext *c=opaque;const Ra2SegmentServices *s=c->services;
    return (unsigned)s->query(s->context,crusher?RA2_SEGMENT_ACTOR_IS_CRUSHER:RA2_SEGMENT_ACTOR_IS_TRAIN);
}
static int32_t gate_overlay(void *opaque)
{
    SegmentGateContext *c=opaque;return c->services->query(c->services->context,RA2_SEGMENT_CELL_OVERLAY_INDEX);
}
static void gate_clear(void *opaque)
{((SegmentGateContext *)opaque)->output->passage=0;}

Ra2SegmentPhase ra2_ground_prepare_segment(int32_t path_head, Ra2SegmentPreparation *output, const Ra2SegmentServices *services)
{
    if (path_head == 8)
    {
        return RA2_SEGMENT_EMPTY;
    }
    void *context = services->context;
    unsigned direction = (uint32_t)path_head & 7u;
    output->candidate = services->candidate_point(context, direction);
    Ra2CellSurface current = services->current_surface(context);
    output->reference_level = current.level + (services->query(context, RA2_SEGMENT_OWNER_BRIDGE_FLAG) ? 4 : 0);
    /* 原版在两次地图查询之间重新读位置并构造相邻点；世界服务可能更新对象，不能合并查询。 */
    Ra2WorldPoint next_position = services->candidate_point(context, direction);
    Ra2CellSurface next = services->surface_at(context, next_position);
    if (next.has_bridge != (unsigned)services->query(context, RA2_SEGMENT_OWNER_BRIDGE_FLAG))
    {
        services->mark_bridge_transition(context);
    }
    if (!services->query(context, RA2_SEGMENT_OWNER_PREDICATE_27C))
    {
        return RA2_SEGMENT_WAIT;
    }
    output->cell.x = (int16_t)(output->candidate.x / 256);
    output->cell.y = (int16_t)(output->candidate.y / 256);
    if (!services->request_gate(context, output->cell))
    {
        return RA2_SEGMENT_WAIT;
    }
    uint16_t desired_facing = (uint16_t)((uint32_t)path_head << 13);
    uint16_t current_facing = (uint16_t)services->query(context, RA2_SEGMENT_FACING_RAW);
    /* 原版使用 16 位回绕差；此处只判断差是否为零，不改动转向速率或路径朝向。 */
    if ((uint16_t)(current_facing - desired_facing) != 0)
    {
        services->turn_toward(context, desired_facing);
        return RA2_SEGMENT_WAIT;
    }
    output->passage = services->classify_cell(context, output->cell, path_head, output->reference_level);
    SegmentGateContext gate_context={output,services};
    Ra2TemplateGateServices gate={&gate_context,gate_classification,gate_type,gate_overlay,gate_clear};
    ra2_ground_template_gate(&gate);
    return RA2_SEGMENT_CLASSIFIED;
}
