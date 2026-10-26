#include "combat_effects.h"
#define Q(q) s->query(s->context,RA2_EF_##q)
#define DO(op,v) s->perform(s->context,RA2_EF_##op,v)
Ra2CrewRoute ra2_crew_eligibility(const Ra2EffectsServices *s)
{
    DO(RESET_CREW_SENTINEL,0);
    if(Q(PRESET_CREW)!=-1)return RA2_CREW_CREATE;
    if(Q(NO_CREW) || !Q(CREWED) || Q(PASSENGER_CAPACITY))return RA2_CREW_SKIP;
    return RA2_CREW_CHANCE;
}
void ra2_create_death_crew(const Ra2EffectsServices *s)
{
    if(Q(PRESET_CREW)==-1 && !Q(CREW_TYPE))return;
    if(!Q(CREATE_CREW))return;
    DO(INIT_CREW,0);
    if(!Q(PLACE_CREW)){DO(DELETE_CREW,1);return;}
    DO(CREW_NOTICE,0);
    DO(CREW_MISSION,Q(HOUSE_CONTROLLED)?5:15);
    if(Q(SELECTED))DO(SELECT_CREW,0);
    if(Q(HAS_TAG) && Q(TAG_ALLOWED))DO(INHERIT_TAG,0);
}
unsigned ra2_choose_death_explosion(const Ra2EffectsServices *s)
{
    if(Q(EXPLOSION_COUNT)<=0)return 0;
    uint32_t random=(uint32_t)Q(RANDOM);
    /* 随机回调可能替换类型；使用回调后的数组和数量。 */
    DO(PICK_EXPLOSION,random%(uint32_t)Q(EXPLOSION_COUNT));
    if((Q(EXPLODES) || Q(EFFECT_GATE)) && Q(OVERRIDE_EFFECT))DO(PICK_LAST_EXPLOSION,0);
    DO(EMIT_EXPLOSION,0);return 1;
}
void ra2_emit_destroy_animation(const Ra2EffectsServices *s)
{
    if(Q(DESTROY_ANIM_COUNT)<=0)return;
    uint32_t random=(uint32_t)Q(RANDOM);
    DO(PICK_DESTROY_ANIM,random%(uint32_t)Q(DESTROY_ANIM_COUNT));DO(EMIT_DESTROY_ANIM,0);
}
void ra2_dispatch_death_weapon(const Ra2EffectsServices *s)
{
    DO(PREPARE_DEATH_PROJECTILE,0);
    if(!Q(BUILD_DEATH_PROJECTILE))return;
    DO(BIND_DEATH_WEAPON,0);DO(LIMBO_PROJECTILE,0);
    DO(DETONATE_PROJECTILE,0);DO(DELETE_PROJECTILE,0);
}
