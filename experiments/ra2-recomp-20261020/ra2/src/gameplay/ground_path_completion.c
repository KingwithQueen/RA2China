#include "ground_path_completion.h"
#include <stddef.h>
Ra2RebuiltPath *ra2_path_complete(const Ra2PathCompletion *c,const Ra2PathCompletionServices *v)
{
    if(c->preparation==RA2_PREPARE_INVALID_CELL || c->preparation==RA2_PREPARE_ALREADY_THERE)return NULL;
    Ra2RebuiltPath *path=NULL;
    /* 上限按相等判断，不能改成>=；两项上限检查先于节点长度读取。 */
    if(c->preparation==RA2_PREPARE_READY && c->expanded!=10000u && c->current
        && c->expanded!=(uint32_t)c->expansion_limit && c->current->path_length>=2) {
        path=v->rebuild(v->context,c->current);
        v->smooth(v->context,path);v->postprocess(v->context,path);
    }
    if(*c->obstacle_mode)v->restore_obstacles(v->context);
    return path;
}
