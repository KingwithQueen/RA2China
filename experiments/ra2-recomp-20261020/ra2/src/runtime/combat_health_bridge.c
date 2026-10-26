#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_health.h"
#include "combat_health_bridge.h"

typedef struct HealthContext {
    uint32_t owner,damage,frame,distance;
    Ra2CombatHealthState state;
} HealthContext;
static uint32_t engine_call(HealthContext *c,uint32_t target,uint32_t ecx,
    const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    MEM32(c->owner+0x6C)=(uint32_t)c->state.health;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=ecx;
    recomp_func_t fn=recomp_lookup_manual(target);
    if(!fn)fn=recomp_lookup(target);
    if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[combat-health] unresolved %08X\n",target);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[combat-health] unbalanced %08X\n",target);abort();}
    g_cur_func=caller;c->state.health=(int32_t)MEM32(c->owner+0x6C);return g_eax;
}
static int32_t health_query(void *opaque,Ra2CombatHealthQuery which)
{
    HealthContext *c=opaque;
    if(which==RA2_HEALTH_DAMAGE)return (int32_t)MEM32(c->damage);
    if(which==RA2_HEALTH_ARMOR)c->distance=MEM32(c->frame+0x2C);
    uint32_t type=engine_call(c,MEM32(MEM32(c->owner)+0x84),c->owner,NULL,0);
    if(which==RA2_HEALTH_TYPE_IMMUNE)return MEM8(type+0x203)!=0;
    if(which==RA2_HEALTH_MAXIMUM){int32_t value=(int32_t)MEM32(type+0xA0);MEM32(c->frame+0x38)=(uint32_t)value;g_edi=(uint32_t)value;return value;}
    return (int32_t)MEM32(type+0x9C);
}
static void store_damage(void *opaque,int32_t damage)
{HealthContext *c=opaque;MEM32(c->damage)=(uint32_t)damage;}
static int32_t adjust_damage(void *opaque,int32_t armor)
{
    HealthContext *c=opaque;uint32_t args[]={(uint32_t)armor,c->distance};
    g_edx=MEM32(c->frame+0x30);
    return (int32_t)engine_call(c,0x47E1C0,MEM32(c->damage),args,2);
}
static void refresh_health(void *opaque)
{
    HealthContext *c=opaque;uint32_t reason=7;
    engine_call(c,MEM32(MEM32(c->owner)+0x13C),c->owner,&reason,1);
}
static double critical_ratio(void *opaque)
{
    (void)opaque;double value;memcpy(&value,(void *)(uintptr_t)ADDR(MEM32(0x839848)+0x1370),sizeof(value));return value;
}
static uint16_t operation_control(void *opaque){(void)opaque;return g_fpu_cw;}
uint32_t ra2_combat_health_bridge(void)
{
    uint32_t entry=g_esp,owner=g_ecx,frame=entry-0x24;
    MEM32(frame)=g_edi;MEM32(frame+4)=g_esi;MEM32(frame+8)=g_ebp;MEM32(frame+12)=g_ebx;
    MEM32(frame+0x10)=0;MEM32(frame+0x14)=MEM32(owner+0x6C);
    HealthContext c={owner,MEM32(entry+4),frame,0,{(int32_t)MEM32(owner+0x6C)}};
    unsigned ignore=MEM8(entry+20);
    g_esi=owner;g_ebp=c.damage;g_ebx=(g_ebx&0xFFFFFF00u)|ignore;g_esp=frame-0x100;
    Ra2CombatHealthServices services={&c,health_query,store_damage,adjust_damage,refresh_health,critical_ratio,operation_control};
    Ra2CombatHealthStep step=ra2_combat_receive_health(&c.state,ignore,&services);
    MEM32(owner+0x6C)=(uint32_t)c.state.health;
    if(step.outcome==RA2_HEALTH_CONTINUE_DAMAGE) {
        MEM32(frame+0x10)=(uint32_t)step.damage_state;
        MEM32(frame+0x14)=(uint32_t)step.original_health;
        if(step.critical_comparison_ran)MEM32(frame+0x38)=(uint32_t)step.comparison_health;
        g_esi=owner;g_ebp=c.damage;g_edi=3;g_edx=MEM32(c.damage);g_eax=(uint32_t)c.state.health;
        g_ebx=(MEM32(frame+12)&0xFFFFFF00u)|ignore;
        /* ECX是下一段会保留的易失中间量；保留原先比较路径的值。 */
        g_ecx=step.critical_comparison_ran?(uint32_t)step.comparison_health:(uint32_t)step.effective_damage;
        g_flag_k=FK_TEST;g_flag_a=g_eax;g_flag_b=g_eax;g_flag_cf=0;g_esp=frame;
        return 0x5D3E68;
    }
    g_eax=0;g_edi=MEM32(frame);g_esi=MEM32(frame+4);g_ebp=MEM32(frame+8);g_ebx=MEM32(frame+12);
    g_flag_k=FK_ADD;g_flag_a=frame+16;g_flag_b=0x14;g_flag_cf=frame+36<frame+16;
    g_esp=entry+28;return 0;
}
