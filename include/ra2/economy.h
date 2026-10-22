#ifndef RA2_ECONOMY_H
#define RA2_ECONOMY_H
#include "battle.h"
#define RA_ECON_QUEUE_LIMIT 16u
#define RA_ECON_CATEGORIES 5u
/* 建筑、车辆、步兵、机场飞机和海军分别保存生产队列。 */
typedef struct
{
    uint32_t cost, ticks, adjacent, factory, storage, free_type;
    int32_t tech;
    bool enabled, harvester, refinery, chrono, airport_bound;
    char prerequisite[192], owners[192], forbidden[192], docks[96];
} ra_econ_type;
typedef struct
{
    uint32_t types[RA_ECON_QUEUE_LIMIT], count, progress, paid, paused, producer;
} ra_econ_queue;
typedef struct
{
    char country[32];
    uint64_t credits, spent, earned;
    uint32_t tech, produced, built;
    ra_econ_queue queues[RA_ECON_CATEGORIES];
} ra_econ_house;
typedef struct
{
    uint32_t active, ore, gems, destination, refinery, delay;
} ra_econ_miner;
typedef struct
{
    ra_econ_house houses[RA_BATTLE_TEAMS];
    ra_econ_miner miners[RA_BATTLE_UNITS];
    uint32_t free_pending[RA_BATTLE_UNITS], dock_owner[RA_BATTLE_UNITS];
} ra_econ_state;
typedef struct ra_battle_economy
{
    ra_econ_type types[RA_BATTLE_TYPES];
    ra_econ_state state, initial;
    uint8_t *ore, *initial_ore;
    uint32_t build_rate, low_min, low_max, low_penalty, ore_value, gem_value, harvest_ticks, unload_ticks;
    char generic[6][256];
} ra_battle_economy;
/* 配置只允许初始阶段写入；后续资金、队列、放置和矿车任务均由有序命令改变。 */
bool ra_economy_open(ra_battle *battle, const ra_ini *rules, ra_error *error);
bool ra_economy_house(ra_battle *battle, uint32_t team, const char *country, uint32_t credits, uint32_t tech, ra_error *error);
bool ra_economy_ore(ra_battle *battle, uint32_t cell, uint32_t kind, uint32_t amount, ra_error *error);
uint32_t ra_economy_category(const ra_battle *battle, uint32_t type);
uint32_t ra_economy_type(const ra_battle *battle, const char *id);
bool ra_economy_owner_allowed(const ra_battle *battle, uint32_t team, uint32_t type);
bool ra_economy_available(const ra_battle *battle, uint32_t team, uint32_t type);
bool ra_economy_placeable(const ra_battle *battle, uint32_t team, uint32_t type, uint32_t cell);
bool ra_economy_command(ra_battle *battle, uint32_t tick, uint32_t actor, ra_battle_order kind, uint32_t target, ra_error *error);
/* 放置命令 target = cell * RA_BATTLE_TYPES + type；不会把界面选择写入模拟。 */
#endif
