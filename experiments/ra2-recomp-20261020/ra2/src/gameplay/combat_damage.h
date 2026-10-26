#pragma once
#include <stdint.h>

typedef struct Ra2CombatDamageInput {
    int32_t damage, distance;
    unsigned disabled, warhead_present;
    float cell_spread, percent_at_max, units_per_cell;
    double armor_multiplier;
    int32_t maximum_damage;
    uint16_t arithmetic_control, conversion_control;
} Ra2CombatDamageInput;

typedef struct Ra2CombatDamageResult {
    int32_t damage, spread_distance, before_armor;
    float initial_damage, edge_damage;
    uint32_t conversion_high;
    uint16_t final_control;
    unsigned positive_path, distance_interpolated;
} Ra2CombatDamageResult;

/* 有限规则值及有界整数换算；先距离衰减、再装甲系数、最后上限。
   负值治疗仅在距离小于8时通过。__ftol切换的控制字会影响后续计算。 */
Ra2CombatDamageResult ra2_combat_adjust_damage(const Ra2CombatDamageInput *input);
