"""Two reversible service phases; preserve original callback and chain-read ordering."""
from run_batch_v60 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
if sys.argv[1]=='completion':
 p=R/'ra2/src/gameplay/ground_path_completion.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_path_completion.h"
#include <stddef.h>

static int can_publish_path(const Ra2PathCompletion *completion)
{
    /* 原版只排除恰好达到上限的情况；先检查两项上限，再读节点长度。 */
    if(completion->preparation!=RA2_PREPARE_READY || completion->expanded==10000u
        || !completion->current || completion->expanded==(uint32_t)completion->expansion_limit)return 0;
    return completion->current->path_length>=2;
}

static Ra2RebuiltPath *rebuild_and_finalize(const Ra2PathCompletion *completion,
    const Ra2PathCompletionServices *services)
{
    Ra2RebuiltPath *path=services->rebuild(services->context,completion->current);
    /* 三项服务的顺序及空返回值传递保持；回调可以更新共享障碍模式。 */
    services->smooth(services->context,path);
    services->postprocess(services->context,path);
    return path;
}

Ra2RebuiltPath *ra2_path_complete(const Ra2PathCompletion *completion,const Ra2PathCompletionServices *services)
{
    if(completion->preparation==RA2_PREPARE_INVALID_CELL || completion->preparation==RA2_PREPARE_ALREADY_THERE)return NULL;
    Ra2RebuiltPath *path=can_publish_path(completion)?rebuild_and_finalize(completion,services):NULL;
    /* 读取回调之后的共享标志，不提前缓存；早退入口仍不恢复临时障碍。 */
    if(*completion->obstacle_mode)services->restore_obstacles(services->context);
    return path;
}
''',encoding='utf-8',newline='\n')
elif sys.argv[1]=='rebuild':
 p=R/'ra2/src/gameplay/ground_path_rebuild.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_path_rebuild.h"
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
''',encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
