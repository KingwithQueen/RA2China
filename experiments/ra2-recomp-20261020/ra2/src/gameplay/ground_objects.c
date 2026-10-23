#include "ground_objects.h"
#include "ground_enemy_contact.h"
#include "ground_enemy_kind.h"
#include "ground_object_kind.h"
#include "ground_building_flags.h"
#include "ground_collision.h"

Ra2ObjectPassageOutcome ra2_ground_filter_object(const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if(s->query(c,RA2_OBJECT_IS_OWNER)) return RA2_OBJECT_CLEAR_OCCUPATION;
    if(s->query(c,RA2_OBJECT_RELATED_CELL_MATCHES)) return RA2_OBJECT_CLEAR;
    return ra2_ground_filter_object_kind(s);
}

Ra2ObjectPassageOutcome ra2_ground_filter_object_kind(const Ra2ObjectPassageServices *s)
{
    void *c = s->context;
    if(s->query(c,RA2_OBJECT_OWNER_ACCEPTS_LINK) && s->query(c,RA2_OBJECT_KIND)==6
        && !s->query(c,RA2_OBJECT_BUILDING_OCCUPIES_CELL)) return RA2_OBJECT_SKIP;
    if(s->query(c,RA2_OBJECT_OWNER_PAIR_FLAG_BB0) && s->query(c,RA2_OBJECT_KIND)==1
        && s->query(c,RA2_OBJECT_PAIR_FLAG_BB0)) return RA2_OBJECT_CLEAR;
    return s->query(c,RA2_OBJECT_KIND)==6 ? RA2_OBJECT_CHECK_GATE : RA2_OBJECT_GENERAL_COLLISION;
}
Ra2ObjectPassageOutcome ra2_ground_filter_building(int32_t direction,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if(direction!=-1 && s->query(c,RA2_OBJECT_BUILDING_FOOTPRINT_TEST)
        && s->query(c,RA2_OBJECT_IS_CELL_BUILDING) && !s->query(c,RA2_OBJECT_BUILDING_OCCUPIES_CELL))
        return RA2_OBJECT_SKIP;
    return ra2_ground_filter_building_flags(s);
}
Ra2ObjectPassageOutcome ra2_ground_filter_building_flags(const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if(s->query(c,RA2_OBJECT_BUILDING_IGNORED)) return RA2_OBJECT_SKIP;
    if(s->query(c,RA2_OBJECT_BUILDING_MISSION_PASSAGE))
    {
        int32_t mission=s->query(c,RA2_OBJECT_MISSION_STATE);
        if(mission==12 || mission==8) return RA2_OBJECT_SKIP;
    }
    if(s->query(c,RA2_OBJECT_BUILDING_HOUSE_PASSAGE))
        return s->query(c,RA2_OBJECT_HOUSE_FLAG_142) ? RA2_OBJECT_BLOCKED : RA2_OBJECT_SKIP;
    if(s->query(c,RA2_OBJECT_BUILDING_NEIGHBOR_ANCHOR) && !s->query(c,RA2_OBJECT_MATCHES_NEIGHBOR_BUILDING))
        return RA2_OBJECT_SKIP;
    return RA2_OBJECT_GENERAL_COLLISION;
}
static void raise_passage(Ra2ObjectPassageState *state,int32_t minimum)
{ if(state->passage<minimum) state->passage=minimum; }
Ra2ObjectPassageOutcome ra2_ground_classify_enemy(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if(s->query(c,RA2_OBJECT_CLOAKED))
    {
        raise_passage(state,RA2_CELL_CLOAKED_OBSTACLE);return RA2_OBJECT_SCANNED;
    }
    return ra2_ground_classify_enemy_contact(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_contact(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if((s->query(c,RA2_OBJECT_OWNER_CRUSHER) || s->query(c,RA2_OBJECT_CRUSHER_ABILITY))
        && s->query(c,RA2_OBJECT_CRUSHABLE))
    {
        /* 原版在此重新查询阵营关系；不能因为先前按敌方进入就缓存为 false。 */
        if(!s->query(c,RA2_OBJECT_ALLIED)) state->crush_enemy=1;
        return RA2_OBJECT_SCANNED;
    }
    return ra2_ground_classify_enemy_weapon(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_weapon(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    if(!s->query(c,RA2_OBJECT_HAS_WEAPON_ZERO) && !s->query(c,RA2_OBJECT_OWNER_IS_TRAIN))
        return RA2_OBJECT_BLOCKED;
    return ra2_ground_classify_enemy_kind(state,s);
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_kind(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    void *c=s->context;
    int32_t kind=s->query(c,RA2_OBJECT_KIND);
    if(kind==6) return ra2_ground_classify_enemy_building(state,s);
    if(kind==36) return ra2_ground_classify_enemy_terrain(state,s);
    raise_passage(state,RA2_CELL_DESTROYABLE);
    return RA2_OBJECT_SCANNED;
}
Ra2ObjectPassageOutcome ra2_ground_classify_enemy_terrain(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    return ra2_ground_classify_enemy_warhead(state,(unsigned)s->query(s->context,RA2_OBJECT_TERRAIN_WEAPON_ALLOWED));
}
Ra2ObjectPassageOutcome ra2_ground_classify_stationary_ally(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    if(s->query(s->context,RA2_OBJECT_KIND)==6) return RA2_OBJECT_BLOCKED;
    raise_passage(state,RA2_CELL_TEMPORARY_OBSTACLE);return RA2_OBJECT_SCANNED;
}

Ra2ObjectPassageOutcome ra2_ground_classify_enemy_building(Ra2ObjectPassageState *state,const Ra2ObjectPassageServices *s)
{
    if(s->query(s->context,RA2_OBJECT_BUILDING_FLAG_1350)) return RA2_OBJECT_BLOCKED;
    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;
}

Ra2ObjectPassageOutcome ra2_ground_classify_enemy_warhead(Ra2ObjectPassageState *state,unsigned flag)
{
    if(!flag)return RA2_OBJECT_BLOCKED;
    raise_passage(state,RA2_CELL_DESTROYABLE);return RA2_OBJECT_SCANNED;
}
