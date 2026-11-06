#ifndef RA2_COMBAT_MANAGER_FRONT_RESULT_BRIDGE_H
#define RA2_COMBAT_MANAGER_FRONT_RESULT_BRIDGE_H
#include <stdint.h>

/* 401DB5：保存完整结果位值和局部TEST，绝不写公开helper状态。 */
typedef struct Ra2ManagerFrontResultState {
    uint32_t value, kind, left, right, carry;
} Ra2ManagerFrontResultState;

int ra2_manager_front_result_bridge(uint32_t result, Ra2ManagerFrontResultState *state);
#endif
