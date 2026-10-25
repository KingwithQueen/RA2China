#include "ground_path_rebuild.h"
#include "x87_arithmetic.h"

static void initialize_result(const Ra2SearchNode *end,int32_t *directions,int32_t *surface_levels,
    Ra2RebuiltPath *out)
{
    out->score=ra2_real_truncate_i32(ra2_real_from_f32(end->priority));
    out->length=end->path_length;
    out->directions=directions;
    out->surface_levels=surface_levels;
    out->reserved=0;
    out->scratch=(Ra2PathPoint){0,0};
}

static int32_t direction_between(Ra2PathPoint from,Ra2PathPoint to,const int32_t direction_table[9])
{
    int32_t dx=(int32_t)from.x-to.x,dy=(int32_t)from.y-to.y;
    return dx>=-1 && dx<=1 && dy>=-1 && dy<=1?direction_table[dy*3+dx+4]:8;
}

static const Ra2PathLink *reconstruct_steps(const Ra2SearchNode *end,int32_t *directions,
    int32_t *surface_levels,const int32_t direction_table[9],Ra2PathPointReader read_point,void *context)
{
    const Ra2PathLink *child=end->path_link;
    const Ra2PathLink *parent=child->parent;
    for(int32_t slot=end->path_length-2;slot>=0;--slot) {
        /* 每步层高来自父链；先读父格，再读子格，读完才推进链。 */
        surface_levels[slot]=parent->surface_level;
        Ra2PathPoint from=read_point(context,parent->cell_reference);
        Ra2PathPoint to=read_point(context,child->cell_reference);
        directions[slot]=direction_between(from,to,direction_table);
        child=child->parent;
        parent=parent->parent;
    }
    return child;
}

void ra2_path_rebuild(const Ra2SearchNode *end,int32_t *directions,int32_t *surface_levels,
    const int32_t direction_table[9],Ra2PathPointReader read_point,void *context,Ra2RebuiltPath *out)
{
    initialize_result(end,directions,surface_levels,out);
    const Ra2PathLink *root=reconstruct_steps(end,directions,surface_levels,direction_table,read_point,context);
    /* 保留终止槽之后的根格读取与末尾零分修正，不复用此前读格结果。 */
    directions[end->path_length-1]=-1;
    out->start=read_point(context,root->cell_reference);
    if(!out->score)out->score=1;
}
