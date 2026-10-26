#pragma once
#include <stdint.h>
typedef enum Ra2CombatDeathQuery {
    RA2_DEATH_HEALTH, RA2_DEATH_ACTIVE, RA2_DEATH_CLASS,
    RA2_DEATH_IGNORE_DEFENSES, RA2_DEATH_SPECIAL_KIND, RA2_DEATH_SPECIAL_POSTURE,
    RA2_DEATH_SPECIAL_HEALTH, RA2_DEATH_STATE, RA2_DEATH_CAPTURE_HEALTH,
    RA2_DEATH_CAPTURE_ATTACKER, RA2_DEATH_HAS_TRIGGER, RA2_DEATH_OLD_HEALTH,
    RA2_DEATH_TYPE_PRESENT, RA2_DEATH_TYPE_STRENGTH, RA2_DEATH_NOTIFY_ENABLED
} Ra2CombatDeathQuery;
typedef enum Ra2CombatDeathOperation {
    RA2_DEATH_SPECIAL_EFFECT, RA2_DEATH_SET_HEALTH, RA2_DEATH_SET_POSTURE,
    RA2_DEATH_SPECIAL_ACTION, RA2_DEATH_SET_STATE, RA2_DEATH_TRIGGER,
    RA2_DEATH_FINAL_PHASE, RA2_DEATH_ATTACKER_NOTICE, RA2_DEATH_REMOVE,
    RA2_DEATH_DAMAGE_NOTICE
} Ra2CombatDeathOperation;
typedef struct Ra2CombatDeathServices {
    void *context;
    int32_t (*query)(void *context,Ra2CombatDeathQuery query);
    void (*perform)(void *context,Ra2CombatDeathOperation operation,int32_t value,unsigned with_attacker);
} Ra2CombatDeathServices;
/* 每次外部通知后重新读取对象存活/生命/标签；提前失效返回5，正常收尾返回伤害状态。
   特殊步兵恢复和对象删除仍通过命名服务完成，不能把回调前的对象状态缓存到整段结束。 */
int32_t ra2_combat_finish_damage(const Ra2CombatDeathServices *services);
