#pragma once
#include <stdint.h>

typedef struct Ra2CombatHealthState { int32_t health; } Ra2CombatHealthState;
typedef enum Ra2CombatHealthQuery {
    RA2_HEALTH_DAMAGE, RA2_HEALTH_TYPE_IMMUNE, RA2_HEALTH_MAXIMUM,
    RA2_HEALTH_ARMOR
} Ra2CombatHealthQuery;
typedef struct Ra2CombatHealthServices {
    void *context;
    int32_t (*query)(void *context,Ra2CombatHealthQuery which);
    void (*store_damage)(void *context,int32_t damage);
    int32_t (*adjust_damage)(void *context,int32_t armor);
    void (*refresh_health)(void *context);
    double (*critical_ratio)(void *context);
    uint16_t (*operation_control)(void *context);
} Ra2CombatHealthServices;
typedef enum Ra2CombatHealthOutcome {
    RA2_HEALTH_RETURN_UNAFFECTED, RA2_HEALTH_CONTINUE_DAMAGE
} Ra2CombatHealthOutcome;
typedef struct Ra2CombatHealthStep {
    Ra2CombatHealthOutcome outcome;
    int32_t original_health, maximum_health, damage_state;
    int32_t comparison_health, effective_damage;
    unsigned maximum_queried, critical_comparison_ran;
} Ra2CombatHealthStep;
/* 伤害换算仍交给弹头/装甲服务；只负责受理、治疗封顶、致命钳制及状态分级。
   合法规则使用有限比例。服务回调可以改写生命与伤害，查询顺序不能合并。 */
Ra2CombatHealthStep ra2_combat_receive_health(Ra2CombatHealthState *state,
    unsigned ignore_defenses,const Ra2CombatHealthServices *services);
