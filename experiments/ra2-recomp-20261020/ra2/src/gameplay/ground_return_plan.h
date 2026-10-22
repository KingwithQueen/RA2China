#pragma once
#include <stdint.h>
typedef enum Ra2GroundFrameKind { RA2_FRAME_ADVANCE,RA2_FRAME_PREPARE,RA2_FRAME_PASSAGE } Ra2GroundFrameKind;
typedef struct Ra2GroundReturnPlan { uint32_t locals,arguments,total; } Ra2GroundReturnPlan;
/* 共享返回只描述帧布局，不混入移动、通行或目标清理行为。 */
Ra2GroundReturnPlan ra2_ground_return_plan(Ra2GroundFrameKind kind);
