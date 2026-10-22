#pragma once
#include <stdint.h>

typedef struct Ra2OverlayBarrier
{
    unsigned present;
    unsigned is_crate;
    unsigned is_wall;
    unsigned is_crushable;
    unsigned actor_is_crusher;
    int32_t armor;
} Ra2OverlayBarrier;

typedef enum Ra2BarrierQuery
{
    RA2_BARRIER_HOUSE_CRATE_PERMISSION,
    RA2_BARRIER_GLOBAL_CRATE_MODE,
    RA2_BARRIER_CRUSHER_ABILITY,
    RA2_BARRIER_WALL_OWNER_ALLIED,
    RA2_BARRIER_ACTOR_CAN_ATTACK,
    /* 返回位 0/1 分别表示原版弹头 +0x144/+0x146，尚未映射 INI 名称。 */
    RA2_BARRIER_WEAPON_WALL_FLAGS,
    RA2_BARRIER_GATE_PASSABLE,
    RA2_BARRIER_GATE_OWNER_ALLIED
} Ra2BarrierQuery;

typedef int (*Ra2BarrierQueryFunction)(void *context, Ra2BarrierQuery query);

typedef enum Ra2BarrierOutcome
{
    RA2_BARRIER_CONTINUE,
    RA2_BARRIER_BLOCKED,
    RA2_BARRIER_NOT_GATE,
    RA2_BARRIER_SKIP_OBJECT
} Ra2BarrierOutcome;

typedef struct Ra2BarrierResult
{
    Ra2BarrierOutcome outcome;
    int32_t passage;
} Ra2BarrierResult;

/* 不把已有等级 7 与“此分支立即返回 7”混为一谈：继续扫描仍可能产生查询或状态变化。 */
Ra2BarrierResult ra2_ground_check_overlay(Ra2OverlayBarrier overlay, int32_t previous_result,
    void *context, Ra2BarrierQueryFunction query);
Ra2BarrierResult ra2_ground_check_gate(unsigned is_gate, int32_t previous_result,
    void *context, Ra2BarrierQueryFunction query);
