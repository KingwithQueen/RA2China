#pragma once
#include <stdint.h>
typedef struct Ra2PassageEntryCell { int32_t level;uint32_t flags,occupancy,owner; } Ra2PassageEntryCell;
typedef struct Ra2PassageEntryServices {
    void *context;
    int32_t (*delegate)(void *);
    int32_t (*level)(void *);
    Ra2PassageEntryCell (*cell)(void *);
    void (*import_upper)(void *,Ra2PassageEntryCell);
    unsigned (*special_mode)(void *);
    unsigned (*visible)(void *);
    unsigned (*ignores_visibility)(void *);
    unsigned (*requires_visibility)(void *);
    int32_t (*foot_classify)(void *);
} Ra2PassageEntryServices;
/* 先保留虚函数的输出，再覆盖匹配桥层的占用信息，最后执行基础通行分类。 */
int32_t ra2_ground_classify_entry(const Ra2PassageEntryServices *services);
