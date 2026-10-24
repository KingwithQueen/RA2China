#pragma once

typedef struct Ra2OwnerRefreshServices
{
    void *context;
    void (*refresh)(void *context);
    int (*usable)(void *context);
} Ra2OwnerRefreshServices;

typedef struct Ra2OwnerCompletionServices
{
    Ra2OwnerRefreshServices refresh;
    void (*cancel_target_and_path)(void *context);
    int (*effective_mission)(void *context);
    int (*stop_move_mission)(void *context);
    int (*update_owner)(void *context);
    int (*alive)(void *context);
} Ra2OwnerCompletionServices;

typedef enum Ra2OwnerCompletion
{
    RA2_OWNER_CONTINUE,
    RA2_OWNER_RETURN_FALSE,
    RA2_OWNER_RETURN_TRUE
} Ra2OwnerCompletion;

/* 刷新可能移除或禁用对象。可用性必须在服务之后读取。 */
int ra2_ground_refresh_owner(const Ra2OwnerRefreshServices *services);
/* 到达后的任务停止/更新也可移除对象；保留短路顺序与立即返回策略。 */
Ra2OwnerCompletion ra2_ground_complete_owner(int reached_target,
    const Ra2OwnerCompletionServices *services);
