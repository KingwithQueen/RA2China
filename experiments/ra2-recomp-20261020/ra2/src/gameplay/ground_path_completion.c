#include "ground_path_completion.h"
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
