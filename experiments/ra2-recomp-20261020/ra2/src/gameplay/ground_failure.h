#pragma once
#include <stdint.h>

typedef struct Ra2PrepareFailureServices
{
    void *context;
    void (*clear_segment)(void *context, int through_saved_pointer);
    void (*clear_path)(void *context, int32_t value);
    void (*start_retry)(void *context);
    uint32_t (*prepare_again)(void *context);
    uint32_t (*stop)(void *context);
    uint32_t (*clear_pending)(void *context);
} Ra2PrepareFailureServices;

typedef enum Ra2PrepareFailureEntry
{
    RA2_FAILURE_REVEALED_OBSTACLE,
    RA2_FAILURE_CLASSIFIED_OBSTACLE,
    RA2_FAILURE_CLEAR_DIRECT_SEGMENT,
    RA2_FAILURE_CLEAR_SAVED_SEGMENT,
    RA2_FAILURE_STOP_ONLY,
    RA2_FAILURE_CLEAR_DIRECT_TAIL,
    RA2_FAILURE_CLEAR_SAVED_TAIL
} Ra2PrepareFailureEntry;
/* 保留失败7的立即递归、其他失败的待播清理，以及已有目标的停止语义。 */
uint32_t ra2_ground_finish_failure(Ra2PrepareFailureEntry entry, int may_retry,
    int32_t classification, int32_t rejected_direction, const Ra2PrepareFailureServices *services);
