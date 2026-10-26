#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_crew.h"
#include "combat_crew_bridge.h"

typedef struct CrewContext {uint32_t owner,house,rules;} CrewContext;
static uint32_t call(uint32_t target,uint32_t self,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=self;
    recomp_func_t fn=recomp_lookup_manual(target);if(!fn)fn=recomp_lookup(target);if(!fn)fn=recomp_lookup_import(target);
    if(!fn){fprintf(stderr,"[crew] unresolved %08X\n",target);abort();}
    fn();if(g_esp!=stack){fputs("[crew] stack imbalance\n",stderr);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t vcall(CrewContext *c,unsigned slot)
{return call(MEM32(MEM32(c->owner)+slot),c->owner,NULL,0);}
static uint32_t random_range(uint32_t upper)
{uint32_t args[]={0,upper};return call(0x6388A0,MEM32(0xA3D290)+0x218,args,2);}
uint32_t ra2_crew_chance_bridge(void)
{
    uint32_t draw=random_range(0x7FFFFFFE);MEM32(g_esp+0x4C)=draw;
    double unit,chance;memcpy(&unit,(void *)(uintptr_t)ADDR(0x79C280),sizeof(unit));
    memcpy(&chance,(void *)(uintptr_t)ADDR(MEM32(0x839848)+0x4E0),sizeof(chance));
    return ra2_crew_roll_succeeds((int32_t)draw,unit,chance,g_fpu_cw)?0x6FCF67:0x6FD0B8;
}
static uint32_t query(void *opaque,Ra2CrewQuery q)
{
    CrewContext *c=opaque;
    switch(q){
        case RA2_CQ_CREWED:return MEM8(vcall(c,0x80)+0xAD9)!=0;
        case RA2_CQ_HOUSE_KIND:c->house=MEM32(c->owner+0x1B4);c->rules=MEM32(0x839848);return MEM32(c->house+0x130);
        case RA2_CQ_ALLIED:return MEM32(c->rules+0xC50);
        case RA2_CQ_SOVIET:return MEM32(c->rules+0xC54);
        case RA2_CQ_TECHNICIAN:return MEM32(c->rules+0xC44);
        case RA2_CQ_COUNTRY_VALID:return MEM32(MEM32(c->house+0x34)+0xBC)!=UINT32_MAX;
        case RA2_CQ_TECHNICIAN_GATE:return vcall(c,0x28C);
        case RA2_CQ_RANDOM_100:return random_range(99);
        case RA2_CQ_CURRENT_TECHNICIAN:return MEM32(MEM32(0x839848)+0xC44);
    }
    abort();
}
static void perform(void *opaque,Ra2CrewOperation op,uint32_t value)
{
    (void)opaque;
    if(op==RA2_CO_SAVE_SELECTION_REGISTER){g_esp-=4;MEM32(g_esp)=g_esi;}
    else g_esi=value;
}
uint32_t ra2_crew_type_bridge(void)
{
    CrewContext c={g_edi,0,0};Ra2CrewServices s={&c,query,perform};Ra2CrewSelection result=ra2_select_crew_type(&s);
    if(!result.eligible)return 0x6D30C5;
    g_esi=result.type;return 0x6D3149;
}
