#ifndef RA2_GROUND_PATH_COMPLETION_H
#define RA2_GROUND_PATH_COMPLETION_H
#include "ground_path_prepare.h"
#include "ground_path_rebuild.h"
typedef struct Ra2PathCompletion {
    Ra2PathPreparationResult preparation;
    Ra2SearchNode *current;
    uint32_t expanded;
    int32_t expansion_limit;
    const int32_t *obstacle_mode;
} Ra2PathCompletion;
typedef struct Ra2PathCompletionServices {
    void *context;
    Ra2RebuiltPath *(*rebuild)(void *context,Ra2SearchNode *end);
    void (*smooth)(void *context,Ra2RebuiltPath *path);
    void (*postprocess)(void *context,Ra2RebuiltPath *path);
    void (*restore_obstacles)(void *context);
} Ra2PathCompletionServices;
/* 格子无效或已在目标处直接返回；空根/搜索失败恢复临时障碍模式。
 * 成功依次重建、平滑、后处理，再按回调之后的共享障碍标志恢复。 */
Ra2RebuiltPath *ra2_path_complete(const Ra2PathCompletion *completion,const Ra2PathCompletionServices *services);
#endif
