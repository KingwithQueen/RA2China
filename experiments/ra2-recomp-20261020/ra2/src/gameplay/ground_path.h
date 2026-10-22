#pragma once
#include <stdint.h>

typedef struct Ra2PathSample
{
    int32_t x;
    int32_t y;
    int32_t direction;
} Ra2PathSample;

typedef struct Ra2PathCursor
{
    int32_t sample_index;
    int32_t remaining_progress;
} Ra2PathCursor;

typedef enum Ra2PathSampleOutcome
{
    RA2_PATH_SAMPLE_CONTINUES,
    RA2_PATH_SAMPLE_REACHES_END
} Ra2PathSampleOutcome;

/* 原版以 (0,0) 标记采样表尾部，但第 0 个采样允许位于原点；每次消耗一段的 7 个进度单位。 */
Ra2PathSampleOutcome ra2_ground_consume_path_sample(Ra2PathCursor *cursor, Ra2PathSample sample);
int32_t ra2_ground_next_sample_index(int32_t current_index);
