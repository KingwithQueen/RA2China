#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_effects.h"
#include "combat_effects_bridge.h"
typedef struct EffectsContext {uint32_t owner,frame,crew,projectile,weapon,damage,selected,preset;} EffectsContext;
static uint32_t call(uint32_t target,uint32_t self,const uint32_t *args,unsigned count,unsigned cdecl_call)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=self;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[combat-effects] unresolved %08X\n",target);abort();}
    fn();if(cdecl_call)g_esp+=count*4;
    if(g_esp!=stack){fprintf(stderr,"[combat-effects] stack imbalance %08X\n",target);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t vcall(uint32_t self,unsigned slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(self)+slot),self,args,count,0);}
static uint32_t type(EffectsContext *c){return MEM32(c->owner+0x5AC);}
static void position(uint32_t out,uint32_t owner)
{for(unsigned i=0;i<3;++i)MEM32(out+i*4)=MEM32(owner+0x88+i*4);}
static uint32_t allocate(uint32_t size){return call(0x782017,0,&size,1,1);}
static int32_t query(void *opaque,Ra2EffectsQuery q)
{
    EffectsContext *c=opaque;uint32_t value;
    switch(q) {
        case RA2_EF_PRESET_CREW:c->preset=MEM32(c->owner+0x290);return (int32_t)c->preset;
        case RA2_EF_NO_CREW:return MEM8(c->frame+0x50)!=0;
        case RA2_EF_CREWED:return MEM8(type(c)+0xAD9)!=0;
        case RA2_EF_PASSENGER_CAPACITY:return MEM32(type(c)+0x52C)!=0;
        case RA2_EF_CREW_TYPE:c->selected=g_edi=vcall(c->owner,0x2E0,NULL,0);return c->selected!=0;
        case RA2_EF_CREATE_CREW:
            value=allocate(0x5D8);if(!value)return 0;
            {uint32_t chosen=c->preset!=UINT32_MAX?MEM32(MEM32(0xA40354)+MEM32(c->owner+0x290)*4):c->selected;
            uint32_t args[]={chosen,MEM32(c->owner+0x1B4)};c->crew=g_edi=call(0x4FF640,value,args,2,0);return c->crew!=0;}
        case RA2_EF_PLACE_CREW:{uint32_t args[]={c->frame+0x20,0};return (vcall(c->crew,0xD4,args,2)&255)!=0;}
        case RA2_EF_HOUSE_CONTROLLED:return (call(0x4F52F0,MEM32(c->owner+0x1B4),NULL,0,0)&255)!=0;
        case RA2_EF_SELECTED:return MEM8(c->frame+0x13)!=0;
        case RA2_EF_HAS_TAG:return MEM32(c->owner+0x34)!=0;
        case RA2_EF_TAG_ALLOWED:return (call(0x6B41F0,MEM32(c->owner+0x34),NULL,0,0)&255)!=0;
        case RA2_EF_EXPLOSION_COUNT:return (int32_t)MEM32(type(c)+0x654);
        case RA2_EF_RANDOM:return (int32_t)call(0x638840,MEM32(0xA3D290)+0x218,NULL,0,0);
        case RA2_EF_EXPLODES:return MEM8(type(c)+0xAE2)!=0;
        case RA2_EF_EFFECT_GATE:{uint32_t arg=10;return (call(0x6D7910,c->owner,&arg,1,0)&255)!=0;}
        case RA2_EF_OVERRIDE_EFFECT:return MEM32(type(c)+0x5AC)==UINT32_MAX || (int32_t)MEM32(c->owner+0x254)>0;
        case RA2_EF_DESTROY_ANIM_COUNT:return (int32_t)MEM32(type(c)+0x670);
        case RA2_EF_BUILD_DEATH_PROJECTILE:{
            uint32_t args[]={c->owner,c->damage,MEM32(c->weapon+0xAC),0,(g_eax&0xFFFFFF00)|MEM8(c->weapon+0x10B)};
            g_edx=c->owner;c->projectile=g_ebx=call(0x463990,MEM32(c->weapon+0xA0),args,5,0);return c->projectile!=0;}
    }
    abort();
}
static void emit(EffectsContext *c,unsigned secondary)
{
    uint32_t anim=allocate(0x1A8);if(!anim)return;
    if(secondary)g_esi=c->owner+0x88;
    uint32_t out=c->frame+0xC;position(out,c->owner);
    uint32_t args[]={c->selected,out,0,1,0x600,0};call(0x420110,anim,args,6,0);
}
static void perform(void *opaque,Ra2EffectsOperation op,uint32_t value)
{
    EffectsContext *c=opaque;
    switch(op) {
        case RA2_EF_RESET_CREW_SENTINEL:g_ebp=UINT32_MAX;break;
        case RA2_EF_INIT_CREW:MEM8(c->crew+0x79)=MEM8(c->owner+0x79);position(c->frame+0x20,c->owner);break;
        case RA2_EF_CREW_NOTICE:{
            int32_t strength=(int32_t)MEM32(MEM32(c->crew+0x5A8)+0xA0);uint32_t upper=(uint32_t)(strength/2);
            uint32_t range[]={5,upper};MEM32(c->crew+0x6C)=call(0x6388A0,MEM32(0xA3D290)+0x218,range,2,0);
            uint32_t args[]={0xAD04C0,1,0};vcall(c->crew,0x15C,args,3);break;}
        case RA2_EF_CREW_MISSION:{uint32_t args[]={value,0};vcall(c->crew,0x1D0,args,2);break;}
        case RA2_EF_SELECT_CREW:vcall(c->crew,0x140,NULL,0);break;
        case RA2_EF_INHERIT_TAG:{uint32_t tag=MEM32(c->owner+0x34);call(0x5D4430,c->crew,&tag,1,0);break;}
        case RA2_EF_DELETE_CREW:vcall(c->crew,0x20,&value,1);break;
        case RA2_EF_PICK_EXPLOSION:c->selected=g_edi=MEM32(MEM32(type(c)+0x648)+value*4);break;
        case RA2_EF_PICK_LAST_EXPLOSION:c->selected=g_edi=MEM32(MEM32(type(c)+0x648)+MEM32(type(c)+0x654)*4-4);break;
        case RA2_EF_EMIT_EXPLOSION:emit(c,0);break;
        case RA2_EF_PICK_DESTROY_ANIM:c->selected=g_edi=MEM32(MEM32(type(c)+0x664)+value*4);break;
        case RA2_EF_EMIT_DESTROY_ANIM:emit(c,1);break;
        case RA2_EF_PREPARE_DEATH_PROJECTILE:
            g_esp-=4;MEM32(g_esp)=g_ebx;c->damage=g_ebp+=MEM32(c->frame+0x1C);break;
        case RA2_EF_BIND_DEATH_WEAPON:call(0x463BA0,c->projectile,&c->weapon,1,0);break;
        case RA2_EF_LIMBO_PROJECTILE:vcall(c->projectile,0xD0,NULL,0);break;
        case RA2_EF_DETONATE_PROJECTILE:{uint32_t out=c->frame+0xC;uint32_t pos=vcall(c->owner,0x48,&out,1);call(0x462110,c->projectile,&pos,1,0);break;}
        /* 引爆回调返回的 ECX 是原调用约定的一部分；此处不能擅自重写为投射物。 */
        case RA2_EF_DELETE_PROJECTILE:call(MEM32(MEM32(c->projectile)+8),g_ecx,&c->projectile,1,0);break;
    }
}
static Ra2EffectsServices services(EffectsContext *c){Ra2EffectsServices s={c,query,perform};return s;}
uint32_t ra2_crew_eligibility_bridge(void)
{EffectsContext c={g_esi,g_esp,0,0,0,0,0,0};Ra2EffectsServices s=services(&c);Ra2CrewRoute r=ra2_crew_eligibility(&s);return r==RA2_CREW_SKIP?0x6FD0B8:r==RA2_CREW_CHANCE?0x6FCF2B:0x6FCF6F;}
void ra2_create_death_crew_bridge(void)
{EffectsContext c={g_esi,g_esp,0,0,0,0,0,0};Ra2EffectsServices s=services(&c);ra2_create_death_crew(&s);}
uint32_t ra2_death_explosion_bridge(void)
{EffectsContext c={g_esi,g_esp,0,0,0,0,0,0};Ra2EffectsServices s=services(&c);return ra2_choose_death_explosion(&s)?0x6FD466:0x6FD51F;}
void ra2_destroy_animation_bridge(void)
{EffectsContext c={g_esi,g_esp,0,0,0,0,0,0};Ra2EffectsServices s=services(&c);ra2_emit_destroy_animation(&s);}
void ra2_death_weapon_dispatch_bridge(void)
{EffectsContext c={g_esi,g_esp,0,0,g_edi,g_ebp,0,0};Ra2EffectsServices s=services(&c);ra2_dispatch_death_weapon(&s);}
