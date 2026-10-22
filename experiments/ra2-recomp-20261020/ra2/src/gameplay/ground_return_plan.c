#include "ground_return_plan.h"
Ra2GroundReturnPlan ra2_ground_return_plan(Ra2GroundFrameKind kind)
{
    static const uint32_t locals[]={0xE4,0x4C,0x68},arguments[]={4,12,20};
    Ra2GroundReturnPlan plan={locals[kind],arguments[kind],16+locals[kind]+4+arguments[kind]};
    return plan;
}
