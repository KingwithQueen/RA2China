#ifndef RA2_BATTLE_INTERNAL_H
#define RA2_BATTLE_INTERNAL_H
#include "ra2/battle.h"
#include "battle_number.h"
#include "ra2/economy.h"
#include "ra2/campaign.h"
bool battle_cell_passable(const ra_battle *battle, uint32_t cell, uint32_t unit);
bool battle_cell_available(const ra_battle *battle, uint32_t cell, uint32_t unit);
bool battle_type_passable(const ra_battle *battle, uint32_t cell, const ra_battle_type *type);
void battle_sea_air_move(ra_battle *battle, ra_battle_unit *unit);
void battle_transport_step(ra_battle *battle);
void battle_gates_step(ra_battle *battle);
bool battle_transport_load(ra_battle *battle, ra_battle_unit *unit, ra_battle_unit *carrier);
bool battle_transport_spawn(ra_battle *battle, uint32_t type, uint32_t team, uint32_t carrier, ra_error *error);
uint32_t battle_transport_count(const ra_battle *battle, uint32_t carrier);
void battle_people_move(ra_battle *battle, ra_battle_unit *unit);
void battle_people_step(ra_battle *battle);
bool battle_people_target(const ra_battle *battle, uint32_t unit, uint32_t kind, uint32_t target);
void battle_people_apply(ra_battle *battle, const ra_battle_command *command);
void battle_campaign_step(ra_battle *battle);
void battle_campaign_seal(ra_battle *battle);
void battle_campaign_reset(ra_battle *battle);
void battle_campaign_close(ra_battle *battle);
void battle_campaign_hash(const ra_battle *battle, bool initial, uint8_t **bytes);
bool battle_spawn_runtime(ra_battle *battle, uint32_t type, uint32_t team, uint32_t cell, ra_error *error);
bool battle_spawn_mobile(ra_battle *battle, uint32_t type, uint32_t team, uint32_t x, uint32_t y, uint32_t layer, bool runtime, ra_error *error);
bool battle_spawn_building(ra_battle *battle, uint32_t type, uint32_t team, uint32_t x, uint32_t y, bool runtime, ra_error *error);
bool battle_economy_target(const ra_battle *battle, uint32_t actor, uint32_t kind, uint32_t target);
void battle_economy_apply(ra_battle *battle, const ra_battle_command *command);
void battle_economy_step(ra_battle *battle);
void battle_economy_seal(ra_battle *battle);
void battle_economy_close(ra_battle *battle);
void battle_economy_hash(const ra_battle *battle, bool initial, uint8_t **bytes);
battle_real battle_legacy_sqrt(battle_real value);
battle_real battle_legacy_trig(battle_real value, bool cosine);
battle_real battle_legacy_acos(battle_real value);
battle_real battle_legacy_atan(battle_real y, battle_real x);
bool battle_arc_angle(uint32_t distance, int32_t height, uint32_t speed, battle_real gravity, bool high, battle_real *angle);
bool battle_arc_direction(uint32_t distance, int32_t height, uint32_t speed, battle_real gravity, bool high, uint32_t *direction);
uint32_t battle_projectile_speed(uint32_t distance, battle_real gravity);
uint32_t battle_native_direction(int32_t dx, int32_t dy);
bool battle_projectile_launch(const ra_battle_weapon *weapon, int32_t dx, int32_t dy, int32_t height, battle_real velocity[3]);
void battle_projectile_step(int32_t position[3], battle_real velocity[3], battle_real gravity);
int32_t battle_guard_range(int32_t guard, int32_t primary, int32_t secondary, int32_t kind, bool special);
void battle_muzzle(const ra_battle_type *type, uint32_t facing, int32_t position[3]);
void battle_chassis_muzzle(const ra_battle_type *type, uint32_t ramp, uint32_t body, uint32_t turret, int32_t position[3]);
bool battle_bridge_edge(const ra_battle *battle, uint32_t from, uint32_t to);
uint32_t battle_surface_collision(int32_t previous_z, int32_t z, int32_t ground, int32_t deck, bool bridge);
bool battle_projectile_snap(const ra_battle *battle, ra_battle_shot *shot);
uint32_t battle_fuse(int32_t dx, int32_t dy, int32_t dz, uint32_t *previous);
uint32_t battle_track_node(const ra_battle *battle, uint32_t physical, uint32_t previous, uint32_t end, uint32_t unit);
uint32_t battle_bridge_test(const ra_battle_tile *from, const ra_battle_tile *to, uint32_t from_flags, uint32_t to_flags, int32_t *level, bool *transition,
                            bool initial);
uint32_t battle_damage(const ra_battle_weapon *weapon, uint32_t armor, uint32_t distance);
int32_t battle_threat_score(const ra_battle *battle, const ra_battle_unit *unit, const ra_battle_unit *target);
typedef struct
{
    uint64_t *cost;
    uint32_t *parent, *heap, *position;
    uint8_t *closed, *canonical;
    uint32_t count;
} battle_search;
void battle_move(ra_battle *battle, ra_battle_unit *unit);
bool battle_track_sample(uint32_t control, uint32_t index, int32_t *x, int32_t *y, uint32_t *direction);
int32_t battle_track_partial(int32_t delta, uint32_t remainder);
void battle_reservations_clear(ra_battle *battle, ra_battle_unit *unit);
battle_real battle_motion_target(const ra_battle_type *type, uint32_t terrain, int slope);
battle_real battle_motion_factor(const ra_battle_type *type, uint32_t distance, battle_real current, battle_real target);
uint32_t battle_motion_rate(const ra_battle_type *type, battle_real factor);
void battle_attack_orders(ra_battle *battle);
void battle_missions(ra_battle *battle);
void battle_command_apply(ra_battle *battle, const ra_battle_command *command);
bool battle_command_target(const ra_battle *battle, uint32_t unit, uint32_t kind, uint32_t target);
bool battle_aim(const ra_battle *battle, const ra_battle_unit *unit, ra_battle_unit *aim);
void battle_combat(ra_battle *battle);
uint32_t battle_direction(int64_t dx, int64_t dy);
uint64_t battle_distance_squared(const ra_battle_unit *a, const ra_battle_unit *b);
uint32_t battle_sqrt(uint64_t value);
void battle_random_reset(ra_battle *battle);
uint32_t battle_random_delay(ra_battle *battle);
uint32_t battle_random_range(ra_battle *battle, uint32_t low, uint32_t high);
void battle_terrain_seal(ra_battle *battle);
void battle_bridge_event(ra_battle *battle, const ra_battle_command *command);
void battle_bridge_impact(ra_battle *battle, const ra_battle_shot *shot);
void battle_kill(ra_battle *battle, ra_battle_unit *unit, uint32_t killer);
uint32_t battle_bridge_frame(uint32_t frame, bool first_side, bool removal);
bool battle_bridge_damage_test(int32_t height, int32_t z, bool low, bool wall, bool demolition, uint32_t damage, uint32_t roll);
bool battle_route_range(ra_battle *battle, uint32_t unit, const ra_battle_unit *enemy, uint32_t range);
void battle_initial_occupancy(const ra_battle *battle, uint32_t *occupied);
void battle_structure_release(ra_battle *battle, const ra_battle_unit *unit);
uint32_t battle_structure_distance(const ra_battle *battle, const ra_battle_unit *unit, int32_t x, int32_t y, int32_t z);
void battle_target_point(const ra_battle *battle, const ra_battle_unit *source, const ra_battle_unit *target, ra_battle_unit *aim);
#endif
