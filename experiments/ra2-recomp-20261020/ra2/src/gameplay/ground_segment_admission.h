#pragma once
#include "ground_prepare.h"

typedef enum Ra2SegmentAdmission
{
    RA2_SEGMENT_NO_CANDIDATE,
    RA2_SEGMENT_STARTED,
    RA2_SEGMENT_REJECTED_ALIVE,
    RA2_SEGMENT_OWNER_REMOVED
} Ra2SegmentAdmission;

typedef struct Ra2SegmentAdmissionServices
{
    void *context;
    int (*accepts_owner)(void *context, Ra2WorldPoint candidate);
    int (*owner_restricted)(void *context);
    void (*start_segment)(void *context, Ra2WorldPoint candidate);
    int (*owner_alive)(void *context);
} Ra2SegmentAdmissionServices;

/* 候选接入的共同服务次序；服务可能改写状态或移除对象。
   调用方保留拒绝后的方向/速度策略，以及候选按值或实时读取的区别。 */
Ra2SegmentAdmission ra2_ground_admit_segment(Ra2WorldPoint *end, unsigned *driving,
    Ra2WorldPoint invalid, Ra2WorldPoint candidate, const Ra2SegmentAdmissionServices *services);
