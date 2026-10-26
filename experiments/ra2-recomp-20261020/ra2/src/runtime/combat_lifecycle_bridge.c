#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_lifecycle.h"
#include "combat_lifecycle_bridge.h"
typedef struct LifecycleContext {uint32_t owner,frame,attacker,current,capacity;} LifecycleContext;
static void test32(uint32_t v){g_flag_k=FK_TEST;g_flag_a=v;g_flag_b=v;g_flag_cf=0;}
static void test8(uint32_t v){g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=(v&255)<<24;g_flag_b=g_flag_a;g_flag_cf=0;}
static void compare(uint32_t a,uint32_t b){g_flag_k=FK_CMP;g_flag_a=a;g_flag_b=b;g_flag_cf=a<b;}
static uint32_t call(uint32_t target,uint32_t self,const uint32_t *args,unsigned count,unsigned cdecl_call)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=self;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[combat-lifecycle] unresolved %08X\n",target);abort();}
    fn();if(cdecl_call)g_esp+=count*4;
    if(g_esp!=stack){fprintf(stderr,"[combat-lifecycle] stack imbalance %08X\n",target);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t virtual_call(uint32_t owner,unsigned slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(owner)+slot),owner,args,count,0);}
static int32_t query(void *opaque,Ra2LifecycleQuery q,uint32_t index)
{
    LifecycleContext *c=opaque;uint32_t value;
    switch(q) {
        case RA2_LIFE_DEATH_FRAMES:g_eax=MEM32(c->owner+0x5AC);g_ecx=MEM32(g_eax+0xBB8);return (int32_t)g_ecx;
        case RA2_LIFE_DEATH_FRAME_UNSET:return MEM32(c->owner+0x5C0)==UINT32_MAX;
        case RA2_LIFE_SINKABLE:return MEM8(MEM32(c->owner+(g_cur_func==0x6FCA30?0x5AC:0x5A8))+0xB45)!=0;
        case RA2_LIFE_START_SINK:{uint32_t zero=0;return (virtual_call(c->owner,0x380,&zero,1)&255)!=0;}
        case RA2_LIFE_DEATH_DEFERRED:return MEM8(c->owner+0x325)!=0;
        case RA2_LIFE_HAS_ATTACHED:g_ecx=MEM32(c->owner+0x230);test32(g_ecx);return g_ecx!=0;
        case RA2_LIFE_HAS_TEAM:g_ecx=MEM32(c->owner+0x4C4);test32(g_ecx);return g_ecx!=0;
        case RA2_LIFE_HAS_TIMER:g_ecx=MEM32(c->owner+0x38);test32(g_ecx);return g_ecx!=0;
        case RA2_LIFE_QUEUE_ROOM:
            c->capacity=g_eax=MEM32(0xAC0CE0);value=MEM32(0xAC0CE8);compare(value,g_eax);return (int32_t)value<(int32_t)g_eax;
        case RA2_LIFE_QUEUE_CAN_GROW:
            g_ecx=(g_ecx&0xFFFFFF00)|MEM8(0xAC0CE5);test8(g_ecx);
            if(!(g_ecx&255)){test32(g_eax);if(g_eax)return 0;}
            g_ecx=MEM32(0xAC0CEC);test32(g_ecx);return (int32_t)g_ecx>0;
        case RA2_LIFE_QUEUE_GROW:{
            uint32_t args[]={c->capacity+MEM32(0xAC0CEC),0};g_edx=MEM32(0xAC0CD8);
            value=call(MEM32(g_edx+8),0xAC0CD8,args,2,0);test8(value);return (value&255)!=0;
        }
        case RA2_LIFE_QUEUE_NONEMPTY:g_eax=MEM32(0xAC0CE8);test32(g_eax);return (int32_t)g_eax>0;
        case RA2_LIFE_QUEUE_MORE:g_esi=index;compare(index,MEM32(0xAC0CE8));return (int32_t)index<(int32_t)MEM32(0xAC0CE8);
        case RA2_LIFE_READY_TO_DELETE:value=virtual_call(c->current,0x44,NULL,0);test8(value);return (value&255)!=0;
        case RA2_LIFE_FIND_CURRENT:{
            uint32_t arg=c->frame+4;g_edx=MEM32(0xAC0CD8);g_eax=arg;
            return (int32_t)call(MEM32(g_edx+0x10),0xAC0CD8,&arg,1,0);
        }
        case RA2_LIFE_VALID_INDEX:
            compare(index,UINT32_MAX);if(index==UINT32_MAX)return 0;
            g_ecx=MEM32(0xAC0CE8);compare(index,g_ecx);return (int32_t)index<(int32_t)g_ecx;
        case RA2_LIFE_SHIFT_MORE:g_eax=index;g_ecx=MEM32(0xAC0CE8);compare(index,g_ecx);return (int32_t)index<=(int32_t)g_ecx;
        case RA2_LIFE_IS_OBJECT:{
            uint32_t arg=c->current;g_eax=arg;value=call(MEM32(MEM32(arg)+8),MEM32(arg),&arg,1,0);test32(value);return value!=0;
        }
        case RA2_LIFE_KEEP_ACTIVE_TYPE:{
            const uint32_t names[]={0x7CF6A8,0x7F6D68,0x7DAEC0,0x7CE5E0};
            for(unsigned i=0;i<4;++i) {
                uint32_t arg=c->current;value=call(0x783C05,g_ecx,&arg,1,1);
                value=call(0x781CD1,names[i],&value,1,0);test32(value);if(value)return 1;
            }
            return 0;
        }
    }
    abort();
}
static void perform(void *opaque,Ra2LifecycleOperation op,uint32_t index)
{
    LifecycleContext *c=opaque;
    switch(op) {
        case RA2_LIFE_CREDIT_KILL:virtual_call(c->owner,0x360,&c->attacker,1);break;
        case RA2_LIFE_BEGIN_DEATH_FRAME:MEM32(c->owner+0x5C0)=0;break;
        case RA2_LIFE_REVIVE_DELAYED:MEM32(c->owner+0x6C)=1;MEM8(c->owner+0x7D)=1;break;
        case RA2_LIFE_CLEAR_OCCUPATION:virtual_call(c->owner,0x48C,NULL,0);break;
        case RA2_LIFE_STOP_MOTION:virtual_call(c->owner,0x348,NULL,0);break;
        case RA2_LIFE_CLEAR_MISSION:{uint32_t args[]={UINT32_MAX,0};virtual_call(c->owner,0x1D0,args,2);break;}
        case RA2_LIFE_DEATH_MISSION:{uint32_t args[]={5,0};virtual_call(c->owner,0x1D0,args,2);break;}
        case RA2_LIFE_COMMIT_MISSION:virtual_call(c->owner,0x1D4,NULL,0);break;
        case RA2_LIFE_NOTIFY_DEATH:call(0x6D3040,c->owner,&c->attacker,1,0);break;
        case RA2_LIFE_UNINIT:virtual_call(c->owner,0xF0,NULL,0);break;
        case RA2_LIFE_CANCEL_ATTACHED:call(0x4681E0,g_ecx,NULL,0,0);break;
        case RA2_LIFE_LEAVE_TEAM:{uint32_t args[]={c->owner,UINT32_MAX,0};call(0x6B8FB0,g_ecx,args,3,0);break;}
        case RA2_LIFE_OBJECT_UNINIT:call(0x5D4E90,c->owner,NULL,0,0);break;
        case RA2_LIFE_CANCEL_TIMER:call(0x435FB0,g_ecx,NULL,0,0);break;
        case RA2_LIFE_DETACH_REFERENCES:g_edx=(g_edx&0xFFFFFF00)|1;call(0x6ECB90,c->owner,NULL,0,0);break;
        case RA2_LIFE_LIMBO:virtual_call(c->owner,0xD0,NULL,0);break;
        case RA2_LIFE_MARK_INACTIVE:MEM8(c->owner+0x7D)=0;break;
        case RA2_LIFE_APPEND_DELETE:
            g_ecx=MEM32(0xAC0CE8);g_eax=g_ecx;g_flag_k=FK_INC;g_flag_a=g_ecx;g_flag_b=1;++g_ecx;
            MEM32(0xAC0CE8)=g_ecx;g_ecx=MEM32(0xAC0CDC);MEM32(g_ecx+g_eax*4)=c->owner;break;
        case RA2_LIFE_SELECT_CURRENT:
            g_eax=MEM32(0xAC0CDC);g_ecx=MEM32(g_eax+index*4);c->current=g_ecx;MEM32(c->frame+4)=g_ecx;break;
        case RA2_LIFE_DECREMENT_COUNT:
            g_ecx=MEM32(0xAC0CE8)-1;compare(index,g_ecx);MEM32(0xAC0CE8)=g_ecx;break;
        case RA2_LIFE_SHIFT_ITEM:
            g_ecx=MEM32(0xAC0CDC);g_edx=MEM32(g_ecx+index*4);MEM32(g_ecx+index*4-4)=g_edx;break;
        case RA2_LIFE_MARK_CURRENT_ACTIVE:MEM8(c->current+0x7D)=1;break;
        case RA2_LIFE_DELETE_CURRENT:
            g_ecx=c->current;test32(g_ecx);if(g_ecx){uint32_t one=1;virtual_call(c->current,0x20,&one,1);}break;
    }
}
static Ra2LifecycleServices services(LifecycleContext *c)
{Ra2LifecycleServices s={c,query,perform};return s;}
static void damage_return(uint32_t frame,uint32_t locals,uint32_t result)
{
    g_eax=result;g_edi=MEM32(frame);g_esi=MEM32(frame+4);g_ebp=MEM32(frame+8);g_ebx=MEM32(frame+12);
    g_flag_k=FK_ADD;g_flag_a=frame+16;g_flag_b=locals;g_flag_cf=frame+16+locals<frame+16;
    g_esp=frame+16+locals+28;
}
uint32_t ra2_unit_death_handoff_bridge(void)
{
    LifecycleContext c={g_esi,g_esp,g_edi,0,0};Ra2LifecycleServices s=services(&c);
    g_ebx=g_eax;MEM32(c.frame+0x40)=g_eax;
    Ra2DerivedDeathRoute route=ra2_unit_damage_handoff(&s,(int32_t)g_eax);
    if(route==RA2_DEATH_RETURN){damage_return(c.frame,0x28,g_ebx);return 0;}
    return route==RA2_DEATH_LIVE_EFFECTS?0x6FD1DB:route==RA2_DEATH_DELAYED_EFFECTS?0x6FCD44:0x6FCADA;
}
uint32_t ra2_infantry_death_handoff_bridge(void)
{
    LifecycleContext c={g_esi,g_esp,g_ebp,0,0};Ra2LifecycleServices s=services(&c);g_edi=g_eax;
    Ra2DerivedDeathRoute route=ra2_infantry_damage_handoff(&s,(int32_t)g_eax);
    if(route==RA2_DEATH_RETURN){damage_return(c.frame,0x3C,g_edi);return 0;}
    return route==RA2_DEATH_LIVE_EFFECTS?0x500193:0x4FFC4D;
}
void ra2_unit_death_finish_bridge(void)
{
    LifecycleContext c={g_esi,g_esp,0,0,0};Ra2LifecycleServices s=services(&c);uint32_t state=g_ebx;
    ra2_finish_derived_death(&s,1);damage_return(c.frame,0x28,state);
}
void ra2_infantry_death_finish_bridge(void)
{
    LifecycleContext c={g_esi,g_esp,0,0,0};Ra2LifecycleServices s=services(&c);
    ra2_finish_derived_death(&s,0);damage_return(c.frame,0x3C,4);
}
void ra2_foot_uninit_bridge(void)
{
    LifecycleContext c={g_ecx,g_esp,0,0,0};Ra2LifecycleServices s=services(&c);uint32_t saved=g_esi;g_esi=c.owner;
    g_esp-=4;MEM32(g_esp)=saved;ra2_uninit_foot(&s);g_esi=saved;g_esp+=8;
}
void ra2_object_uninit_bridge(void)
{
    LifecycleContext c={g_ecx,g_esp,0,0,0};Ra2LifecycleServices s=services(&c);uint32_t saved=g_esi;g_esi=c.owner;
    g_esp-=4;MEM32(g_esp)=saved;ra2_uninit_object(&s);g_esi=saved;g_esp+=8;
}
void ra2_object_delete_drain_bridge(void)
{
    uint32_t saved=g_esi;g_esp-=8;MEM32(g_esp)=saved;MEM32(g_esp+4)=g_ecx;g_esi=0;
    LifecycleContext c={0,g_esp,0,0,0};Ra2LifecycleServices s=services(&c);ra2_drain_object_deletions(&s);
    g_ecx=MEM32(c.frame+4);g_esi=saved;g_esp=c.frame+12;
}
