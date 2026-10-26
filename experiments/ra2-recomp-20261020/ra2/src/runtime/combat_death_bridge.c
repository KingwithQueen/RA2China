#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_death.h"
#include "combat_death_bridge.h"
#include "x87_arithmetic.h"
typedef struct DeathContext {uint32_t owner,frame,attacker;unsigned ignore;} DeathContext;
static uint32_t call(uint32_t target,uint32_t self,const uint32_t *args,unsigned count,unsigned caller_cleanup)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=self;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[combat-death] unresolved %08X\n",target);abort();}
    fn();if(caller_cleanup)g_esp+=count*4;
    if(g_esp!=stack){fprintf(stderr,"[combat-death] stack imbalance %08X\n",target);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t virtual_call(DeathContext *c,unsigned slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(c->owner)+slot),c->owner,args,count,0);}
static int32_t query(void *opaque,Ra2CombatDeathQuery q)
{
    DeathContext *c=opaque;uint32_t type;
    switch(q) {
        case RA2_DEATH_HEALTH:return (int32_t)MEM32(c->owner+0x6C);
        case RA2_DEATH_ACTIVE:return MEM8(c->owner+0x7D)!=0;
        case RA2_DEATH_CLASS:return (int32_t)virtual_call(c,0x2C,NULL,0);
        case RA2_DEATH_IGNORE_DEFENSES:return (int32_t)c->ignore;
        case RA2_DEATH_SPECIAL_KIND:return MEM8(MEM32(c->owner+0x5A8)+0xC00)!=0;
        case RA2_DEATH_SPECIAL_POSTURE:return MEM8(c->owner+0x5C3)!=0;
        case RA2_DEATH_SPECIAL_HEALTH: {
            double fraction;memcpy(&fraction,(void *)(uintptr_t)ADDR(0x7A7670),8);
            Ra2LegacyReal value=ra2_real_multiply(ra2_real_from_i32((int32_t)MEM32(MEM32(c->owner+0x5A8)+0xA0)),ra2_real_from_f64(fraction),g_fpu_cw);
            g_fpu_cw=MEM16(0x7D8964);return ra2_real_round_i32(value,g_fpu_cw);
        }
        case RA2_DEATH_STATE:return (int32_t)MEM32(c->frame+0x10);
        case RA2_DEATH_CAPTURE_HEALTH:g_ebp=MEM32(c->owner+0x6C);return (int32_t)g_ebp;
        case RA2_DEATH_CAPTURE_ATTACKER:c->attacker=MEM32(c->frame+0x34);g_ebx=c->attacker;return c->attacker!=0;
        case RA2_DEATH_HAS_TRIGGER:return MEM32(c->owner+0x34)!=0;
        case RA2_DEATH_OLD_HEALTH:return (int32_t)MEM32(c->frame+0x14);
        case RA2_DEATH_TYPE_PRESENT:return virtual_call(c,0x84,NULL,0)!=0;
        case RA2_DEATH_TYPE_STRENGTH:type=virtual_call(c,0x84,NULL,0);return (int32_t)MEM32(type+0xA0);
        case RA2_DEATH_NOTIFY_ENABLED:return MEM8(c->owner+0x77)!=0;
    }
    abort();
}
static void perform(void *opaque,Ra2CombatDeathOperation op,int32_t value,unsigned with_attacker)
{
    DeathContext *c=opaque;
    switch(op) {
        case RA2_DEATH_SPECIAL_EFFECT: {
            uint32_t size=0x1A8,anim=call(0x782017,0,&size,1,1);
            if(anim) {
                for(unsigned i=0;i<3;++i)MEM32(c->frame+0x18+i*4)=MEM32(c->owner+0x88+i*4);
                uint32_t args[]={MEM32(MEM32(0x839848)+0xA4),c->frame+0x18,0,1,0x600,0};
                call(0x420110,anim,args,6,0);
            }
            break;
        }
        case RA2_DEATH_SET_HEALTH:MEM32(c->owner+0x6C)=(uint32_t)value;break;
        case RA2_DEATH_SET_POSTURE:MEM8(c->owner+0x5C3)=(uint8_t)value;break;
        case RA2_DEATH_SPECIAL_ACTION: {uint32_t args[]={6,1,0};virtual_call(c,0x4DC,args,3);break;}
        case RA2_DEATH_SET_STATE:MEM32(c->frame+0x10)=(uint32_t)value;break;
        case RA2_DEATH_TRIGGER: {uint32_t args[]={(uint32_t)value,c->owner,MEM32(0xA72EE0),0,with_attacker?c->attacker:0};call(0x6B3DF0,MEM32(c->owner+0x34),args,5,0);break;}
        case RA2_DEATH_FINAL_PHASE:g_edi=4;break;
        case RA2_DEATH_ATTACKER_NOTICE:virtual_call(c,0xDC,&c->attacker,1);break;
        case RA2_DEATH_REMOVE: {uint32_t arg=1;virtual_call(c,0xD8,&arg,1);break;}
        case RA2_DEATH_DAMAGE_NOTICE: {uint32_t arg=2;virtual_call(c,0x11C,&arg,1);break;}
    }
}
void ra2_combat_death_bridge(void)
{
    uint32_t frame=g_esp;DeathContext c={g_esi,frame,0,g_ebx&0xFF};
    Ra2CombatDeathServices s={&c,query,perform};int32_t result=ra2_combat_finish_damage(&s);
    g_eax=(uint32_t)result;g_edi=MEM32(frame);g_esi=MEM32(frame+4);g_ebp=MEM32(frame+8);g_ebx=MEM32(frame+12);
    g_esp=frame+64;g_flag_k=FK_ADD;g_flag_a=frame+16;g_flag_b=20;g_flag_cf=frame+36<frame+16;
}
