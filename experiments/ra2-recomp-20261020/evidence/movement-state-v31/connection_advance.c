extern void __cdecl ra2_layer_from_context(void *opaque);
#include "ground_template_entry.h"
#include "ground_template_transition.h"
#include <string.h>
#include "ground_advance.h"

static Ra2AdvanceCell cell_of(Ra2WorldPoint position)
{
    /* 原版先向零取整，再保留低 16 位，负坐标不能改成向下取整。 */
    uint32_t packed = ra2_ground_sample_cell(position.x,position.y);
    uint16_t x = (uint16_t)packed, y = (uint16_t)(packed >> 16);
    Ra2AdvanceCell cell;
    memcpy(&cell.x, &x, sizeof(x)); memcpy(&cell.y, &y, sizeof(y));
    return cell;
}

typedef struct AdvanceLayerContext
{
    const Ra2AdvanceServices *services;
    uint32_t cells[2];
} AdvanceLayerContext;

static int32_t layer_level(void *opaque, unsigned next)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    if(!next)ra2_layer_from_context(services->context);
    return services->query(services->context, RA2_ADVANCE_CELL_LEVEL, context->cells[next]);
}

static uint32_t layer_flags(void *opaque, unsigned next)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    return services->query(services->context, RA2_ADVANCE_CELL_HAS_BRIDGE, context->cells[next]) ? 0x100u : 0;
}

static void layer_set(void *opaque, unsigned upper)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    services->act(services->context, RA2_ADVANCE_SET_BRIDGE_LAYER, 0, (int32_t)upper);
}

int ra2_ground_advance_sample(const Ra2AdvanceServices *s)
{
    void *c = s->context;
    if (s->query(c, RA2_ADVANCE_NEEDS_POSITION_MARK, 0))
    {
        s->act(c, RA2_ADVANCE_MARK_POSITION, 0, 0);
        s->act(c, RA2_ADVANCE_CLEAR_SAMPLE_FLAGS, 0, 0);
    }
    int32_t index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    Ra2AdvanceCell previous;
    if (!index) previous = s->current_cell(c);
    else
    {
        Ra2PathSample prior_sample = s->sample(c, index - 1, 1);
        previous = cell_of(s->transform_sample(c, &prior_sample, 1));
    }
    index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    Ra2PathSample sample = s->sample(c, index, 0);
    Ra2WorldPoint position = s->transform_sample(c, &sample, 0);
    position.z = 0;
    Ra2WorldPoint raw_position = s->raw_position(c);
    Ra2TemplateCells cells = ra2_ground_template_cells(ra2_ground_sample_adjusted(position.x),
        ra2_ground_sample_adjusted(position.y), raw_position.x, raw_position.y);
    Ra2AdvanceCell next = cell_of(position);
    int crosses_cell = !cells.same_cell;
    if (crosses_cell)
    {
        s->act(c, RA2_ADVANCE_LEAVE_CELL, 0, 0);
        s->place(c, position, 1);
        uint32_t previous_cell = s->find_cell(c, previous);
        uint32_t next_cell = s->find_cell(c, next);
        AdvanceLayerContext layer_context = {s, {previous_cell, next_cell}};
        Ra2TemplateLayerServices layer_services = {&layer_context, layer_level, layer_flags, layer_set};
        ra2_ground_template_layer(&layer_services);

        if (s->query(c, RA2_ADVANCE_IS_TRAIN, 0) && !s->query(c, RA2_ADVANCE_TRAIN_FLAG_5B8, 0))
        {
            int upper_layer = 1;
            if (!s->query(c, RA2_ADVANCE_BRIDGE_LAYER, 0))
            {
                Ra2WorldPoint raw = s->raw_position(c);
                upper_layer = raw.z >= s->query(c, RA2_ADVANCE_GROUND_HEIGHT, 0);
            }
            /* 重新查格子：放置与伤害回调可改变世界，不能缓存对象链代替查询。 */
            uint32_t cell = s->find_cell(c, next);
            uint32_t object = (uint32_t)s->query(c, upper_layer ? RA2_ADVANCE_OBJECT_HEAD_UPPER : RA2_ADVANCE_OBJECT_HEAD_LOWER, cell);
            while (object)
            {
                uint32_t following = (uint32_t)s->query(c, RA2_ADVANCE_OBJECT_NEXT, object);
                if (!s->query(c, RA2_ADVANCE_OBJECT_CRUSHABLE, object))
                    s->act(c, RA2_ADVANCE_TRAIN_DAMAGE, object, 0);
                /* 下一对象必须在伤害前保存，伤害可把当前对象从格子链中移除。 */
                object = following;
            }
        }
        if (!s->query(c, RA2_ADVANCE_OWNER_ALIVE, 0)) return 0;
        s->act(c, RA2_ADVANCE_ENTER_CELL, 0, 1);
        int32_t overlay = s->query(c, RA2_ADVANCE_OVERLAY_INDEX, next_cell);
        if (overlay != -1 && s->query(c, RA2_ADVANCE_CRUSHING_ENABLED, 0)
            && (s->query(c, RA2_ADVANCE_IS_CRUSHER, 0) || s->query(c, RA2_ADVANCE_CRUSHER_ABILITY, 0))
            && !s->query(c, RA2_ADVANCE_OVERLAY_LAND_TYPE, (uint32_t)overlay))
        {
            s->act(c, RA2_ADVANCE_MARK_CRUSHING, 0, 1);
            if (s->query(c, RA2_ADVANCE_CRUSH_SLOWDOWN, 0))
                s->act(c, RA2_ADVANCE_APPLY_CRUSH_SLOWDOWN, 0, 0);
        }
    }
    else s->place(c, position, 0);
    if (!s->query(c, RA2_ADVANCE_OWNER_ALIVE, 0)) return 0;
    s->act(c, RA2_ADVANCE_REFRESH_PLACEMENT, 0, 0);
    s->act(c, RA2_ADVANCE_SET_FACING, 0, sample.direction);
    index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    if (index && index == s->query(c, RA2_ADVANCE_TRANSITION_SAMPLE, 0))
        s->act(c, RA2_ADVANCE_MARK_POSITION, 0, 1);
    return 1;
}
