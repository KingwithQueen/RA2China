#ifndef RA2_BATTLE_H
#define RA2_BATTLE_H
#include "ra2.h"

#define RA_BATTLE_HZ 15u
#define RA_BATTLE_CELL 65536u
#define RA_BATTLE_UNITS 2048u
#define RA_BATTLE_TYPES 512u
#define RA_BATTLE_TEAMS 32u
#define RA_BATTLE_PATH 4096u
#define RA_BATTLE_COMMANDS 16384u
#define RA_BATTLE_SHOTS 256u
#define RA_BATTLE_WAYPOINTS 32u
#define RA_BATTLE_VERSION 11u
#define RA_BATTLE_REPLAY_MAGIC "RA2RPL13"
#define RA_BATTLE_RESERVED 12u
#define RA_BATTLE_BRIDGES 4096u

typedef enum
{
    RA_ORDER_MOVE,
    RA_ORDER_ATTACK,
    RA_ORDER_STOP,
    RA_ORDER_FORCE_GROUND,
    RA_ORDER_FORCE_UNIT,
    RA_ORDER_ATTACK_MOVE,
    RA_ORDER_GUARD,
    RA_ORDER_SCATTER,
    RA_ORDER_WAYPOINT,
    RA_ORDER_WAYPOINT_APPEND,
    RA_ORDER_WAYPOINT_LOOP,
    RA_EVENT_BRIDGE_HIT,
    RA_EVENT_BRIDGE_DEMOLISH,
    RA_EVENT_BRIDGE_REPAIR,
    RA_ECON_QUEUE,
    RA_ECON_PAUSE,
    RA_ECON_CANCEL,
    RA_ECON_PLACE,
    RA_ECON_HARVEST,
    RA_ECON_RETURN,
    RA_ORDER_DEPLOY,
    RA_ORDER_ENTER,
    RA_EVENT_SELECT,
    RA_ORDER_LOAD,
    RA_ORDER_UNLOAD
} ra_battle_order;
typedef struct
{
    uint32_t initial, target, started, duration;
} ra_battle_turn;
typedef struct
{
    char id[32], projectile[32], warhead[32];
    uint32_t damage, rof, range, speed, gravity, spread, percent_at_max, projectile_rot;
    uint32_t verses[11];
    uint32_t max_damage, percent_bits;
    bool arcing, cliffs, walls, elevation, high, floater;
    bool aa, no_ground, proximity, ranged;
    uint32_t arm;
    bool wall, bridge_forced;
    /* 生成导弹独立保存生命和飞行阶段；最小射程、齐射与再生周期来自规则。 */
    uint32_t minimum, burst, missile, launch_delay, missile_health, altitude, regeneration;
} ra_battle_weapon;

/* 模拟仅使用整数；显示、选择、墙钟时间和工作线程均不拥有游戏状态。 */
typedef struct
{
    uint16_t track;
    uint8_t height, ramp, blocked, land;
} ra_battle_tile;
typedef struct
{
    char id[32], faction[32];
    uint32_t step, rot, strength, armor, uphill, downhill, slowdown, deceleration, acceleration, sight, guard_range;
    int32_t flh[3], threat_coefficients[5], special_threat, turret_offset;
    ra_battle_weapon weapon;
    /* 建筑与车辆共用生命、装甲、目标和弹体；矩形占地由稳定对象编号持有。 */
    uint32_t foundation_width, foundation_height, height;
    int32_t power;
    bool structure;
    /* 对象能力来自规则；转换目标保存类型编号加一，零表示不可展开。 */
    bool infantry, engineer, c4, capturable, bridge_hut, insignificant, instant_weapon, amphibious;
    uint32_t deploy_type, c4_ticks;
    bool naval, flying, passive_acquire, gate, powered;
    uint32_t passengers, size, size_limit, flight_height, ammo;
} ra_battle_type;
/* 未来内容包通过稳定名称注册阵营；保留中国命名空间，但不启用中国内容。 */
typedef struct
{
    const char *id;
    bool enabled;
} ra_battle_faction;
extern const ra_battle_faction ra_battle_factions[3];
/* TMP 的地表编号与规则 LandType 不是同一枚举；未知值返回 255。 */
uint8_t ra_battle_land(uint8_t tmp_land);
typedef struct
{
    uint32_t id, type, cell, next, goal, progress, retry, facing;
    uint32_t path[RA_BATTLE_PATH], path_count, path_cursor;
    int32_t x, y;
    uint32_t team, health, target, order, cooldown, speed_factor, shots, kills, destroyed_tick;
    /* 原版连续系数的二进制位状态；speed_factor 只作为万分比诊断值，不能驱动运动。 */
    uint64_t motion_factor;
    /* 轨迹余量沿用原版七分采样；双格弯道和提前衔接均保留完整确定性状态。 */
    uint32_t track_control, track_index, track_remainder, track_active, track_via;
    uint32_t reserved[RA_BATTLE_RESERVED], reserved_count, curve_joins;
    /* 任务目的地与临时追击目的地分离；巡逻起点使用从一开始的索引，零表示不循环。 */
    uint32_t destination, anchor, fire_cell, waypoints[RA_BATTLE_WAYPOINTS], waypoint_count, waypoint_cursor, waypoint_loop;
    ra_battle_turn body, turret;
    /* 各位是影响候选资格的模拟状态；零值表示普通、可见的地面单位。 */
    uint32_t traits, hidden_from, detected_by;
    /* 坠桥在桥面撤销的同一步摧毁单位；保留出事格和高度，不能被随后修桥复活。 */
    uint32_t subcell, tag, script_team, action_tick, selected_tick, c4_owner;
    /* 乘员保留对象编号和生命，运输中不占地、不索敌、不触发进入格事件。 */
    uint32_t carrier, unloading, unload_tick, ammunition, burst_left, flash_until, spawn_ready, gate_open_until;
    int32_t altitude;
    uint32_t fall_cell, killer;
    int32_t fall_height;
} ra_battle_unit;

enum
{
    RA_UNIT_LIMBO = 1u,
    RA_UNIT_SINKING = 2u,
    RA_UNIT_CLOAKED = 4u,
    RA_UNIT_AIRBORNE = 8u,
    RA_UNIT_UNTARGETABLE = 16u,
    RA_UNIT_IMMUNE = 32u,
    RA_UNIT_SUBMERGED = 64u,
    RA_UNIT_FALLEN = 128u
};
typedef enum
{
    RA_COLLISION_NONE,
    RA_COLLISION_GROUND,
    RA_COLLISION_BRIDGE_UP,
    RA_COLLISION_BRIDGE_DOWN,
    RA_COLLISION_TARGET_CELL,
    RA_COLLISION_OBJECT,
    RA_COLLISION_WALL,
    RA_COLLISION_CLIFF,
    RA_COLLISION_OUTSIDE,
    RA_COLLISION_EXPIRED
} ra_battle_collision;
typedef struct
{
    uint32_t tick, sequence, unit, target, kind;
} ra_battle_command;
typedef struct
{
    uint32_t id, active, owner, target, type, team, age, duration, impact_tick, hit;
    int32_t x, y, z, start_x, start_y, start_z, end_x, end_y, end_z;
    /* 无制导炮弹保留原版二进制速度，位置仍在每步截断至整数 lepton。 */
    uint64_t velocity[3];
    uint32_t collision, retired_tick, fuse_distance;
    uint32_t health, launch_delay, cruise_height;
} ra_battle_shot;
typedef struct
{
    /* kind：0 高架混凝土、1 高架木桥、2 低木桥、3 低混凝土桥；255 帧表示高桥段已经移除。 */
    uint32_t cell, axis, kind, frame, original_frame, changed_tick;
    ra_battle_tile under;
} ra_battle_bridge;
typedef struct
{
    uint32_t width, height, tick, count, initial_count, type_count, command_count, command_cursor, rejected;
    ra_battle_tile *tiles;
    /* 地面节点在前，桥面节点在后；桥下与桥面的占格和路径互不覆盖。 */
    uint8_t *bridges;
    uint32_t *occupied;
    ra_battle_type *types;
    uint32_t allies[RA_BATTLE_TEAMS];
    ra_battle_unit *units, *initial;
    ra_battle_command *commands;
    uint8_t content[20];
    ra_battle_shot *shots;
    uint32_t next_shot, fired, impacts, kills, dropped_shots;
    uint32_t random[250], random_a, random_b;
    ra_battle_bridge *bridge_parts, *initial_parts;
    uint32_t *bridge_at, bridge_count, topology_revision, bridge_hits, bridge_destroyed, bridge_repaired, bridge_falls, bridge_strength;
    ra_battle_tile *initial_tiles;
    uint8_t *initial_bridges;
    bool terrain_sealed;
    struct ra_battle_economy *economy;
    struct ra_battle_campaign *campaign;
    void *search;
} ra_battle;
bool ra_battle_create(ra_battle *battle, uint32_t width, uint32_t height, const ra_battle_tile *tiles, const uint8_t content[20], ra_error *error);
void ra_battle_close(ra_battle *battle);
bool ra_battle_type_add(ra_battle *battle, const char *id, const char *faction, uint32_t step, ra_error *error);
bool ra_battle_spawn(ra_battle *battle, uint32_t type, uint32_t x, uint32_t y, ra_error *error);
bool ra_battle_spawn_team(ra_battle *battle, uint32_t type, uint32_t team, uint32_t x, uint32_t y, ra_error *error);
bool ra_battle_spawn_layer(ra_battle *battle, uint32_t type, uint32_t team, uint32_t x, uint32_t y, uint32_t layer, ra_error *error);
/* axis 为 1（沿 X）、2（沿 Y）；桥面固定高于基底四层，仅在初始化阶段安装。 */
bool ra_battle_bridge_add(ra_battle *battle, uint32_t cell, uint32_t axis, bool intact, ra_error *error);
/* 注册原始桥段；事件是场景/工程师系统的完成通知，不作为免费修桥的玩家快捷键。 */
bool ra_battle_bridge_segment_add(ra_battle *battle, uint32_t cell, uint32_t axis, uint32_t kind, uint32_t frame, ra_error *error);
bool ra_battle_bridge_event_add(ra_battle *battle, uint32_t tick, ra_battle_order kind, uint32_t cell, ra_error *error);
uint32_t ra_battle_cell_y(const ra_battle *battle, uint32_t node);
uint32_t ra_battle_unit_layer(const ra_battle *battle, const ra_battle_unit *unit);
int32_t ra_battle_unit_height(const ra_battle *battle, const ra_battle_unit *unit);
uint32_t ra_battle_unit_ramp(const ra_battle *battle, const ra_battle_unit *unit);
bool ra_battle_targetable(const ra_battle *battle, const ra_battle_unit *unit, const ra_battle_unit *target, bool automatic, bool force);
/* 返回原版行主序 float 位模式；不依赖主机的浮点舍入环境。 */
bool ra_battle_chassis(uint32_t ramp, uint32_t facing, uint32_t matrix[12]);
bool ra_battle_attack_add(ra_battle *battle, uint32_t tick, uint32_t unit, uint32_t target, ra_error *error);
bool ra_battle_stop_add(ra_battle *battle, uint32_t tick, uint32_t unit, ra_error *error);
bool ra_battle_order_add(ra_battle *battle, uint32_t tick, uint32_t unit, ra_battle_order kind, uint32_t target, ra_error *error);
/* 整组路径点先验证再入队；loop_from 为 UINT32_MAX 时不循环，否则是从零开始的路径点索引。 */
bool ra_battle_waypoints_add(ra_battle *battle, uint32_t tick, uint32_t unit, const uint32_t *cells, uint32_t count, uint32_t loop_from, ra_error *error);
uint32_t ra_battle_nearest(const ra_battle *battle, uint32_t unit);
bool ra_battle_type_rules(ra_battle *battle, uint32_t type, const ra_ini *rules, ra_error *error);
bool ra_battle_type_art(ra_battle *battle, uint32_t type, const ra_ini *rules, const ra_ini *art, ra_error *error);
bool ra_battle_structure_rules(ra_battle *battle, uint32_t type, const ra_ini *rules, const ra_ini *local, const ra_ini *art, ra_error *error);
bool ra_battle_spawn_structure(ra_battle *battle, uint32_t type, uint32_t team, uint32_t x, uint32_t y, ra_error *error);
bool ra_battle_allied(const ra_battle *battle, uint32_t first, uint32_t second);
void ra_battle_power(const ra_battle *battle, uint32_t team, uint32_t *output, uint32_t *drain);
uint32_t ra_battle_native_speed(uint32_t speed);
uint32_t ra_battle_turn_value(const ra_battle_turn *turn, uint32_t tick);
void ra_battle_turn_start(ra_battle_turn *turn, uint32_t target, uint32_t rot, uint32_t tick);
uint32_t ra_battle_motion_rate(const ra_battle_type *type, uint32_t terrain, int slope, uint32_t factor);
uint32_t ra_battle_slowdown(const ra_battle_type *type, uint32_t distance, uint32_t factor);
bool ra_battle_command_add(ra_battle *battle, uint32_t tick, uint32_t unit, uint32_t target, ra_error *error);
bool ra_battle_passable(const ra_battle *battle, uint32_t cell);
bool ra_battle_edge(const ra_battle *battle, uint32_t from, uint32_t to, uint32_t unit);
/* 局部坐标为 0..255 lepton，格中心是 128；返回原版地表高度的 lepton 值。 */
int32_t ra_battle_tile_height(const ra_battle_tile *tile, uint32_t local_x, uint32_t local_y);
int32_t ra_battle_ground_height(const ra_battle *battle, int32_t x, int32_t y);
bool ra_battle_slope_edge(const ra_battle_tile *from, const ra_battle_tile *to);
bool ra_battle_route(ra_battle *battle, uint32_t unit, uint32_t target);
void ra_battle_step(ra_battle *battle);
void ra_battle_reset(ra_battle *battle);
void ra_battle_hash(const ra_battle *battle, uint8_t digest[20]);
/* 回放使用显式小端序与完整摘要，不序列化结构体填充或指针。输出内存由调用方 free。 */
bool ra_battle_replay_write(ra_battle *battle, uint8_t **bytes, size_t *size, ra_error *error);
bool ra_battle_replay_read(ra_battle *battle, ra_view bytes, uint32_t *end_tick, uint8_t expected[20], ra_error *error);
/* 墙钟以微秒输入；余量保留，暂停时由宿主清零。不丢弃积压的模拟步。 */
uint32_t ra_battle_clock(uint64_t *phase, uint64_t microseconds);
#endif
