#ifndef RA2_CAMPAIGN_H
#define RA2_CAMPAIGN_H
#include "battle.h"
#define RA_CAMPAIGN_TRIGGERS 256u
#define RA_CAMPAIGN_ACTIONS 24u
#define RA_CAMPAIGN_EVENTS 8u
#define RA_CAMPAIGN_CELLS 2048u
#define RA_CAMPAIGN_TEAMS 128u
#define RA_CAMPAIGN_MEMBERS 32u
#define RA_CAMPAIGN_SCRIPT 32u

typedef struct
{
    uint32_t kind;
    int32_t argument;
} ra_campaign_event;
typedef struct
{
    uint32_t kind, waypoint;
    int32_t argument;
    char reference[96];
} ra_campaign_action;
typedef struct
{
    char id[32], name[96];
    uint32_t house, linked, persistence, event_count, action_count;
    bool disabled;
    ra_campaign_event events[RA_CAMPAIGN_EVENTS];
    ra_campaign_action actions[RA_CAMPAIGN_ACTIONS];
} ra_campaign_trigger;
typedef struct
{
    char id[32];
    uint32_t house, tag, waypoint, member_count, script_count;
    uint32_t types[RA_CAMPAIGN_MEMBERS], numbers[RA_CAMPAIGN_MEMBERS];
    ra_campaign_event script[RA_CAMPAIGN_SCRIPT];
} ra_campaign_team;
typedef struct
{
    uint32_t enabled, started, fired, actor;
} ra_campaign_trigger_state;
typedef struct
{
    uint32_t active, definition, cursor, started, count, waiting, shots_start, repeat_until_success;
    uint32_t members[RA_CAMPAIGN_MEMBERS];
} ra_campaign_team_state;
typedef struct
{
    ra_campaign_trigger_state triggers[RA_CAMPAIGN_TRIGGERS];
    ra_campaign_team_state teams[RA_CAMPAIGN_TEAMS];
    uint32_t local[256], global[256], allies[RA_BATTLE_TEAMS], previous_health[RA_BATTLE_UNITS];
    uint32_t outcome, input_locked, message_serial, message_tick, fired, rejected_actions, rejected_teams, script_gaps;
    uint32_t timer_end, timer_remaining, timer_running, camera_waypoint, camera_serial;
    uint32_t pending_recruit[RA_CAMPAIGN_TEAMS], production[RA_BATTLE_TEAMS], ai_enabled[RA_BATTLE_TEAMS];
    char message[96];
} ra_campaign_state;
typedef struct ra_battle_campaign
{
    ra_campaign_trigger triggers[RA_CAMPAIGN_TRIGGERS];
    ra_campaign_team teams[RA_CAMPAIGN_TEAMS];
    uint32_t trigger_count, team_count, cell_count, house_count, house_arguments[RA_BATTLE_TEAMS];
    char houses[RA_BATTLE_TEAMS][64], countries[RA_BATTLE_TEAMS][64];
    uint32_t cells[RA_CAMPAIGN_CELLS], cell_triggers[RA_CAMPAIGN_CELLS], waypoints[1024];
    uint32_t incomplete_units[RA_BATTLE_TEAMS], incomplete_buildings[RA_BATTLE_TEAMS];
    uint32_t unsupported_events[128], unsupported_actions[160], unsupported_scripts[128];
    ra_campaign_state state, initial;
} ra_battle_campaign;
/* 导入只读地图的触发定义；首个固定步封存初态。未实现条件始终不成立。 */
bool ra_campaign_open(ra_battle *battle, const ra_ini *map, const char *const *houses, const char *const *countries, uint32_t count, ra_error *error);
uint32_t ra_campaign_tag(const ra_battle *battle, const ra_ini *map, const char *tag);
uint32_t ra_campaign_house(const ra_battle *battle, const char *name);
bool ra_campaign_event_supported(uint32_t kind);
bool ra_campaign_action_supported(uint32_t kind);
#endif
