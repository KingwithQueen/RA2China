#pragma once
#include <stdint.h>

typedef enum Ra2EffectsQuery {
    RA2_EF_PRESET_CREW, RA2_EF_NO_CREW, RA2_EF_CREWED, RA2_EF_PASSENGER_CAPACITY,
    RA2_EF_CREW_TYPE, RA2_EF_CREATE_CREW, RA2_EF_PLACE_CREW,
    RA2_EF_HOUSE_CONTROLLED, RA2_EF_SELECTED, RA2_EF_HAS_TAG, RA2_EF_TAG_ALLOWED,
    RA2_EF_EXPLOSION_COUNT, RA2_EF_RANDOM, RA2_EF_EXPLODES, RA2_EF_EFFECT_GATE,
    RA2_EF_OVERRIDE_EFFECT, RA2_EF_DESTROY_ANIM_COUNT, RA2_EF_BUILD_DEATH_PROJECTILE
} Ra2EffectsQuery;
typedef enum Ra2EffectsOperation {
    RA2_EF_RESET_CREW_SENTINEL, RA2_EF_INIT_CREW, RA2_EF_CREW_NOTICE,
    RA2_EF_CREW_MISSION, RA2_EF_SELECT_CREW, RA2_EF_INHERIT_TAG, RA2_EF_DELETE_CREW,
    RA2_EF_PICK_EXPLOSION, RA2_EF_PICK_LAST_EXPLOSION, RA2_EF_EMIT_EXPLOSION,
    RA2_EF_PICK_DESTROY_ANIM, RA2_EF_EMIT_DESTROY_ANIM, RA2_EF_PREPARE_DEATH_PROJECTILE,
    RA2_EF_BIND_DEATH_WEAPON, RA2_EF_LIMBO_PROJECTILE, RA2_EF_DETONATE_PROJECTILE,
    RA2_EF_DELETE_PROJECTILE
} Ra2EffectsOperation;
typedef struct Ra2EffectsServices {
    void *context;
    int32_t (*query)(void *context,Ra2EffectsQuery query);
    void (*perform)(void *context,Ra2EffectsOperation operation,uint32_t value);
} Ra2EffectsServices;
typedef enum Ra2CrewRoute {RA2_CREW_SKIP,RA2_CREW_CHANCE,RA2_CREW_CREATE} Ra2CrewRoute;
Ra2CrewRoute ra2_crew_eligibility(const Ra2EffectsServices *services);
void ra2_create_death_crew(const Ra2EffectsServices *services);
unsigned ra2_choose_death_explosion(const Ra2EffectsServices *services);
void ra2_emit_destroy_animation(const Ra2EffectsServices *services);
void ra2_dispatch_death_weapon(const Ra2EffectsServices *services);
