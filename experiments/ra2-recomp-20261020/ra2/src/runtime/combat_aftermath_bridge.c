#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_aftermath.h"
#include "combat_aftermath_bridge.h"
typedef struct AftermathContext {uint32_t owner,frame,source,passenger,passenger_vtable,index,team;} AftermathContext;
static void test32(uint32_t value){g_flag_k=FK_TEST;g_flag_a=value;g_flag_b=value;g_flag_cf=0;}
static uint32_t call(uint32_t target,uint32_t self,const uint32_t *args,unsigned count,unsigned cdecl_call)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=self;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[combat-aftermath] unresolved %08X\n",target);abort();}
    fn();if(cdecl_call)g_esp+=count*4;
    if(g_esp!=stack){fprintf(stderr,"[combat-aftermath] stack imbalance %08X\n",target);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t virtual_call(uint32_t self,unsigned slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(self)+slot),self,args,count,0);}
static void coordinates(uint32_t target,uint32_t source)
{for(unsigned i=0;i<3;++i)MEM32(target+i*4)=MEM32(source+i*4);}
static void effect(AftermathContext *c,uint32_t kind,int custom)
{
    uint32_t size=0x1A8,animation=call(0x782017,0,&size,1,1);
    if(!animation)return;
    uint32_t scratch=c->frame+0x10,type;
    if(!custom)scratch+=(kind-2)*12;
    coordinates(scratch,c->owner+0x88);
    if(custom)type=MEM32(MEM32(MEM32(c->owner+0x5A8)+0xBC4)+kind*4);
    else if(kind==4)type=MEM32(MEM32(0x8661E4)+4);
    else {unsigned offsets[]={0xA4,0xA8,0,0xAC,0xB0};type=MEM32(MEM32(0x839848)+offsets[kind-2]);}
    uint32_t args[]={type,scratch,0,1,0x600,0};call(0x420110,animation,args,6,0);
}
static int32_t query(void *opaque,Ra2AftermathQuery q,uint32_t index)
{
    AftermathContext *c=opaque;uint32_t value;
    switch(q) {
        case RA2_AF_DEATH_MODE:return (int32_t)MEM32(MEM32(c->frame+0x58)+0x120);
        case RA2_AF_CURRENT_SEQUENCE:return (int32_t)MEM32(c->owner+0x5AC);
        case RA2_AF_SOURCE_PRESENT:return c->source!=0;
        case RA2_AF_SOURCE_CLASS:return (int32_t)virtual_call(c->source,0x2C,NULL,0);
        case RA2_AF_SOURCE_MODE_FIVE:return MEM8(MEM32(c->source+0x418)+0x1359)!=0;
        case RA2_AF_CUSTOM_COUNT:return (int32_t)MEM32(MEM32(c->owner+0x5A8)+0xBD0);
        case RA2_AF_CUSTOM_ANIMATION:return MEM32(MEM32(MEM32(c->owner+0x5A8)+0xBC4)+index*4)!=0;
        case RA2_AF_NOT_HUMAN:return MEM8(MEM32(c->owner+0x5A8)+0xC01)!=0;
        case RA2_AF_FORCE_IMMEDIATE:return MEM8(c->frame+0x60)!=0;
        case RA2_AF_CARRIER_SINKABLE:return MEM8(MEM32(c->owner+0x5AC)+0xB45)!=0;
        case RA2_AF_HAS_PASSENGERS:g_eax=MEM32(c->owner+0xFC);test32(g_eax);return g_eax!=0;
        case RA2_AF_POP_PASSENGER:
            c->passenger=call(0x4CCFC0,c->owner,NULL,0,0);g_edi=c->passenger;test32(g_edi);
            if(g_edi){g_ebp=c->owner+0x88;c->passenger_vtable=MEM32(g_edi);g_ebx=c->passenger_vtable;}
            return g_edi!=0;
        case RA2_AF_CAN_ENTER_CELL:{
            coordinates(c->frame+0x20,c->owner+0x88);uint32_t position=c->frame+0x20;
            uint32_t cell=call(0x548000,0x8324E0,&position,1,0);
            uint32_t args[]={cell,UINT32_MAX,UINT32_MAX,0,1};value=call(MEM32(c->passenger_vtable+0x194),c->passenger,args,5,0);
            unsigned allowed=value==0 || value==2;g_ebx=(g_ebx&0xFFFFFF00)|allowed;return (int32_t)allowed;
        }
        case RA2_AF_IGNORE_DEFENSES:return MEM8(c->frame+0x4C)!=0;
        case RA2_AF_CARRIER_FLAG_7C:return MEM8(c->owner+0x7C)!=0;
        case RA2_AF_UNLIMBO_PASSENGER:{
            uint32_t output=c->frame+0x44,angle=call(0x4B8BE0,c->owner+0x2E0,&output,1,0);
            uint32_t direction=(((MEM32(angle)>>7)+1)>>1)&255;
            uint32_t args[]={c->frame+0x14,direction};return (virtual_call(c->passenger,0xD4,args,2)&255)!=0;
        }
        case RA2_AF_HOUSE_CONTROLLED:return (call(0x4F52F0,MEM32(c->owner+0x1B4),NULL,0,0)&255)!=0;
        case RA2_AF_CARRIER_TEAM:c->team=MEM32(c->owner+0x4C4);return c->team!=0;
        case RA2_AF_INHERIT_SELECTION:return MEM8(c->frame+0x13)!=0;
        case RA2_AF_PASSENGER_TEAM:c->team=g_ecx=MEM32(c->passenger+0x4C4);test32(g_ecx);return g_ecx!=0;
        case RA2_AF_POP_RAW_PASSENGER:
            c->passenger=call(0x4689F0,c->owner+0xF8,NULL,0,0);g_esi=c->passenger;test32(g_esi);return g_esi!=0;
    }
    abort();
}
static void perform(void *opaque,Ra2AftermathOperation op,uint32_t value)
{
    AftermathContext *c=opaque;
    switch(op) {
        case RA2_AF_SET_PRESENTATION_INDEX:c->index=g_edi=value;break;
        case RA2_AF_CUSTOM_EFFECT:effect(c,value,1);break;
        case RA2_AF_DEFAULT_EFFECT:effect(c,value,0);break;
        case RA2_AF_DEATH_ACTION:{uint32_t args[]={value,1,0};virtual_call(c->owner,0x4DC,args,3);break;}
        case RA2_AF_CARRIER_NOTICE:{uint32_t zero=0;virtual_call(c->owner,0x11C,&zero,1);break;}
        case RA2_AF_BEGIN_RELEASE:
            MEM32(0xA40774)+=1;MEM8(c->passenger+0x79)=MEM8(c->owner+0x79);break;
        case RA2_AF_RELEASE_POSITION:{
            coordinates(c->frame+0x14,c->owner+0x88);
            uint32_t location=virtual_call(c->owner,0x1A4,NULL,0),output=c->frame+0x2C;
            uint32_t result=virtual_call(location,0x48,&output,1);MEM32(c->frame+0x1C)=MEM32(result+8);break;
        }
        case RA2_AF_PLACED_NOTICE:{uint32_t args[]={0xAD04C0,1,0};virtual_call(c->passenger,0x15C,args,3);break;}
        case RA2_AF_ADD_TO_TEAM:call(0x6B8CC0,c->team,&c->passenger,1,0);break;
        case RA2_AF_GUARD_MISSION:{uint32_t args[]={value,0};virtual_call(c->passenger,0x1D0,args,2);break;}
        case RA2_AF_SELECT_PASSENGER:virtual_call(c->passenger,0x140,NULL,0);break;
        case RA2_AF_KILL_NOTICE:{
            uint32_t source=g_cur_func==0x6FCA30?MEM32(c->frame+0x48):c->source;
            virtual_call(c->passenger,0xDC,&source,1);break;
        }
        case RA2_AF_DELETE_PASSENGER:virtual_call(c->passenger,0x20,&value,1);break;
        case RA2_AF_END_RELEASE:
            g_ebx=MEM32(c->frame+0x40);MEM32(0xA40774)-=1;break;
        case RA2_AF_PEEK_PASSENGER:c->passenger=call(0x468A10,c->owner+0xF8,NULL,0,0);break;
        case RA2_AF_LEAVE_TEAM:{uint32_t args[]={c->passenger,UINT32_MAX,0};call(0x6B8FB0,c->team,args,3,0);break;}
    }
}
static Ra2AftermathServices services(AftermathContext *c)
{Ra2AftermathServices s={c,query,perform};return s;}
uint32_t ra2_infantry_presentation_bridge(void)
{
    AftermathContext c={g_esi,g_esp,g_ebp,0,0,0,0};Ra2AftermathServices s=services(&c);
    return ra2_present_infantry_death(&s)==RA2_PRESENTATION_DEFER?0x500184:0x4FFF61;
}
void ra2_carrier_release_bridge(void)
{
    AftermathContext c={g_esi,g_esp,MEM32(g_esp+0x48),0,0,0,0};Ra2AftermathServices s=services(&c);
    ra2_release_carrier_passengers(&s);
}
void ra2_carrier_destroy_passengers_bridge(void)
{
    uint32_t entry=g_esp,owner=g_ecx,source=MEM32(entry+4),saved=g_ebx;
    g_esp-=4;MEM32(g_esp)=saved;g_ebx=owner;
    int nonempty=MEM32(owner+0xFC)!=0;
    if(nonempty){g_esp-=12;MEM32(g_esp)=g_edi;MEM32(g_esp+4)=g_esi;MEM32(g_esp+8)=g_ebp;g_ebp=source;g_edi=owner+0xF8;}
    AftermathContext c={owner,entry,source,0,0,0,0};Ra2AftermathServices s=services(&c);ra2_destroy_carrier_passengers(&s);
    if(nonempty){g_edi=MEM32(g_esp);g_esi=MEM32(g_esp+4);g_ebp=MEM32(g_esp+8);g_esp+=12;}
    g_ebx=MEM32(g_esp);g_esp=entry+8;
}
