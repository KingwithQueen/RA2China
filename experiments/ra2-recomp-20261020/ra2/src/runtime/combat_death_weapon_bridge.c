#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_death_weapon.h"
#include "combat_death_weapon_bridge.h"

typedef struct DeathWeaponContext {uint32_t owner;} DeathWeaponContext;
static uint32_t vcall(DeathWeaponContext *c,unsigned slot)
{
    uint32_t stack=g_esp,caller=g_cur_func,target=MEM32(MEM32(c->owner)+slot);
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=c->owner;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[death-weapon] unresolved %08X\n",target);abort();}
    fn();if(g_esp!=stack){fputs("[death-weapon] stack imbalance\n",stderr);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t query(void *opaque,Ra2DeathWeaponQuery q)
{
    DeathWeaponContext *c=opaque;uint32_t slot;
    switch(q){
        case RA2_DW_EXPLICIT_WEAPON:return MEM32(vcall(c,0x80)+0xAE4);
        case RA2_DW_SLOT_HAS_WEAPON:slot=vcall(c,0x398);return slot && MEM32(slot);
        case RA2_DW_SLOT_WEAPON:return MEM32(vcall(c,0x398));
        case RA2_DW_DEFAULT_WEAPON:return MEM32(MEM32(0x839848)+0xC9C);
    }
    abort();
}
static int32_t damage(void *opaque,uint32_t weapon,unsigned fallback)
{
    DeathWeaponContext *c=opaque;g_edi=weapon;uint32_t type=vcall(c,0x80);double multiplier;
    int32_t base;
    if(fallback){base=(int32_t)MEM32(type+0xA0);memcpy(&multiplier,(void *)(uintptr_t)ADDR(0x79A728),sizeof(multiplier));}
    else {float value;memcpy(&value,(void *)(uintptr_t)ADDR(type+0xAE8),sizeof(value));multiplier=value;base=(int32_t)MEM32(weapon+0xA4);}
    int32_t result=ra2_death_weapon_damage(base,multiplier,g_fpu_cw,MEM16(0x7D8964));
    g_fpu_cw=MEM16(0x7D8964);return result;
}
void ra2_death_weapon_selection_bridge(void)
{
    DeathWeaponContext c={g_esi};Ra2DeathWeaponServices s={&c,query,damage};
    Ra2DeathWeaponSelection result=ra2_select_death_weapon(&s);g_edi=result.weapon;g_eax=(uint32_t)result.damage;
}
