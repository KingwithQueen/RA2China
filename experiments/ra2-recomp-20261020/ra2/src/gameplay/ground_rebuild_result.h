#pragma once
/* 成功重建时是否复核owner由调用点决定；返回拒绝后是否继续取方向也由调用点决定。 */
typedef enum Ra2RebuildResult { RA2_REBUILD_READY, RA2_REBUILD_NO_OWNER, RA2_REBUILD_REJECTED } Ra2RebuildResult;
typedef struct Ra2RebuildResultServices
{
    void *context;
    int (*owner_exists)(void *);
    void (*write_aborted)(void *);
    int (*destination_accepted)(void *);
    void (*stop_navigation)(void *);
} Ra2RebuildResultServices;
Ra2RebuildResult ra2_ground_check_rebuild_result(int rebuilt, int check_success,
    const Ra2RebuildResultServices *services);
