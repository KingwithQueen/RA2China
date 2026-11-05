#ifndef RA2_COMBAT_MANAGER_RESULT_BRANCH_BRIDGE_H
#define RA2_COMBAT_MANAGER_RESULT_BRANCH_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerResultBranchFlags { uint32_t kind, left, right, carry; } Ra2ManagerResultBranchFlags;

int ra2_manager_result_branch_bridge(Ra2ManagerResultBranchFlags *flags);

#endif
