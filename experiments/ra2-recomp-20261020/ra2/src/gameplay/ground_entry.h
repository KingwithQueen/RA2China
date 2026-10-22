#pragma once
#include <stdint.h>

typedef struct Ra2CellLink
{
    int present;
    int16_t endpoint_x, endpoint_y;
    int32_t direction;
} Ra2CellLink;
typedef struct Ra2EntryState
{
    int32_t direction, reference_level, infantry_owner, passage;
    uint8_t alternate_layer, occupation_flags, vehicle_present;
} Ra2EntryState;
typedef enum Ra2EntryQuery
{
    RA2_ENTRY_HAS_BRIDGE, RA2_ENTRY_CELL_LEVEL,
    RA2_ENTRY_UPPER_FLAGS, RA2_ENTRY_UPPER_INFANTRY_OWNER,
    RA2_ENTRY_GLOBAL_VISIBILITY_OVERRIDE, RA2_ENTRY_CELL_VISIBLE,
    RA2_ENTRY_OWNER_VISIBILITY_EXEMPT, RA2_ENTRY_OWNER_FLAG_32D
} Ra2EntryQuery;
typedef struct Ra2EntryServices
{
    void *context;
    Ra2CellLink (*neighbor_link)(void *context, int32_t direction);
    int32_t (*check_placement)(void *context, Ra2EntryState *state);
    int32_t (*query)(void *context, Ra2EntryQuery query);
    int32_t (*base_passage)(void *context, Ra2EntryState *state);
} Ra2EntryServices;

typedef enum Ra2EntryOutcome { RA2_ENTRY_CONTINUE, RA2_ENTRY_CLEAR, RA2_ENTRY_BLOCKED } Ra2EntryOutcome;
/* 碰撞的前置阶段。方向 8 使用连接端点判定；其他方向还要检查来路连接、
   放置约束、桥面占用层与可见性，再交给基础通行判断。 */
Ra2EntryOutcome ra2_ground_check_entry(Ra2EntryState *state, Ra2CellLink link, const Ra2EntryServices *services);
