#pragma once
#include <stdint.h>

typedef enum Ra2DeathWeaponQuery {
    RA2_DW_EXPLICIT_WEAPON, RA2_DW_SLOT_HAS_WEAPON, RA2_DW_SLOT_WEAPON, RA2_DW_DEFAULT_WEAPON
} Ra2DeathWeaponQuery;
typedef struct Ra2DeathWeaponServices {
    void *context;
    uint32_t (*query)(void *,Ra2DeathWeaponQuery);
    int32_t (*damage)(void *,uint32_t weapon,unsigned fallback);
} Ra2DeathWeaponServices;
typedef struct Ra2DeathWeaponSelection {uint32_t weapon;int32_t damage;} Ra2DeathWeaponSelection;

Ra2DeathWeaponSelection ra2_select_death_weapon(const Ra2DeathWeaponServices *services);
/* 乘法使用当前精度/舍入，整数转换使用CRT控制字，返回64位转换结果的低32位。 */
int32_t ra2_death_weapon_damage(int32_t base,double multiplier,uint16_t arithmetic_control,uint16_t conversion_control);
