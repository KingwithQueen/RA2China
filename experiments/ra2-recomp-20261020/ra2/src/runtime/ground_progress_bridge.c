#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_tube_progress.h"
#include "ground_internal_next.h"
#include "ground_passage_finish.h"
#include "ground_progress_bridge.h"

typedef struct ProgressContext { uint32_t frame, unit, approach, drive, offset; int32_t direction; } ProgressContext;
static Ra2WorldPoint point(uint32_t address)
{ Ra2WorldPoint value; memcpy(&value,(void *)(uintptr_t)ADDR(address),12); return value; }
static void store(uint32_t address,Ra2WorldPoint value)
{ memcpy((void *)(uintptr_t)ADDR(address),&value,12); }
static double number(uint32_t address)
{ double value; memcpy(&value,(void *)(uintptr_t)ADDR(address),8); return value; }
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[movement-progress] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[movement-progress] stack %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t method(uint32_t unit,uint32_t slot,const uint32_t *args,unsigned count)
{ return call(MEM32(MEM32(unit)+slot),unit,args,count); }
static Ra2WorldPoint approach(void *opaque)
{ ProgressContext *c=opaque;return point(c->approach); }
static void construct_at(uint32_t output,Ra2WorldPoint value,uint32_t destination)
{
    uint32_t args[]={(uint32_t)value.x,(uint32_t)value.y,(uint32_t)value.z};
    uint32_t result=call(0x41B630,output,args,3);store(destination,point(result));
}
static void construct_tube_probe(void *opaque,Ra2WorldPoint value)
{ ProgressContext *c=opaque;construct_at(c->frame+0x74,value,c->frame+0x50); }
static uintptr_t tube_center(ProgressContext *c,uint32_t p,uint32_t output)
{
    (void)c;
    uint32_t cell=call(0x548000,0x8324E0,&p,1);
    return call(0x475D60,cell,&output,1);
}
static uintptr_t approach_center(void *opaque)
{ ProgressContext *c=opaque;return tube_center(c,c->approach,c->frame+0x40); }
static uintptr_t probe_center(void *opaque)
{ ProgressContext *c=opaque;return tube_center(c,c->frame+0x50,c->frame+0x30); }
static Ra2WorldPoint read_center(void *opaque,uintptr_t address)
{ (void)opaque;return point((uint32_t)address); }
static void store_approach(void *opaque,Ra2WorldPoint value)
{ ProgressContext *c=opaque;store(c->approach,value); }
static void increase_height(void *opaque,int32_t increment)
{ ProgressContext *c=opaque;MEM32(c->unit+0x464)+=(uint32_t)increment; }
static uint32_t heading(void *opaque)
{
    ProgressContext *c=opaque;uint32_t p=c->frame+0x74;
    uint32_t position=method(c->unit,0x48,&p,1),args[]={position,c->approach};
    return MEM32(call(0x423EF0,c->frame+0x30,args,2));
}
static void finish_aligned(uint32_t frame,uint32_t result)
{
    uint32_t bp=MEM32(frame+8);g_eax=result;g_edi=MEM32(frame);g_esi=MEM32(frame+4);
    g_ebx=MEM32(frame+12);g_ebp=MEM32(bp);g_esp=bp+8;
}
uint32_t ra2_ground_tube_progress_bridge(unsigned entry)
{
    ProgressContext c={0};c.frame=g_esp;c.unit=g_esi;c.approach=g_edi;
    if(entry==0){
        uint32_t offset=0x851AC0+(g_ebx&7u)*8;
        Ra2WorldPoint delta={(int32_t)MEM32(offset),(int32_t)MEM32(offset+4),0};
        Ra2TubeApproachServices s={&c,approach,construct_tube_probe,approach_center,probe_center,read_center,store_approach,increase_height,heading};
        g_esp=c.frame-0x100;uint32_t result=ra2_ground_tube_construct_approach(delta,(int32_t)MEM32(c.frame+0x24),&s);
        g_esp=c.frame;g_eax=result;g_esi=c.unit;g_edi=c.approach;g_ebp=c.approach;return 0x6FAC70;
    }
    uint32_t source=c.frame+(entry==1?0x50:0x5C),destination=c.frame+(entry==1?0x5C:0x50);
    uint32_t direction=entry==1?g_ebx:g_ebp;
    int32_t base=(int32_t)MEM32(source+8);
    Ra2WorldPoint output=entry==1?(Ra2WorldPoint){(int32_t)g_edx,(int32_t)g_eax,(int32_t)g_ecx}:
        (Ra2WorldPoint){(int32_t)g_eax,(int32_t)g_ecx,(int32_t)g_edx};store(destination,output);
    double distance=entry==1?(double)(int32_t)MEM32(c.frame+0x30):number(c.frame+0x28);
    double length=number((direction&1u)?0x7A3A20:0x79A700);
    output.z=ra2_ground_tube_progress_height(distance,length,(int32_t)MEM32(c.frame+0x24),base,g_fpu_cw,MEM16(0x7D8964));
    MEM32(destination+8)=(uint32_t)output.z;g_fpu_cw=MEM16(0x7D8964);
    g_esp=c.frame-0x100;uint32_t result=method(c.unit,0x19C,&destination,1);finish_aligned(c.frame,result);return 0;
}

static uint32_t owner(ProgressContext *c){return MEM32(c->drive+0xC);}
static void reset_budget(void *opaque){ProgressContext *c=opaque;MEM32(owner(c)+0x53C)=10;}
static int32_t path_direction(void *opaque)
{ ProgressContext *c=opaque;c->unit=owner(c);c->direction=(int32_t)MEM32(c->unit+0x4D0);c->offset=0x851AC0+((uint32_t)c->direction&7u)*8;return c->direction; }
static Ra2WorldPoint position(void *opaque){ProgressContext *c=opaque;return point(owner(c)+0x88);}
static Ra2WorldPoint offset(void *opaque)
{ ProgressContext *c=opaque;return (Ra2WorldPoint){(int32_t)MEM32(c->offset),(int32_t)MEM32(c->offset+4),0}; }
static void construct_target(void *opaque,Ra2WorldPoint value)
{ ProgressContext *c=opaque;construct_at(c->frame+0x44,value,c->frame+0x38); }
static void store_probe(void *opaque,Ra2WorldPoint value)
{ ProgressContext *c=opaque;store(c->frame+0x2C,value); }
static void construct_prepare_probe(void *opaque,Ra2WorldPoint value)
{ ProgressContext *c=opaque;construct_at(c->frame+0x44,value,c->frame+0x2C); }
static uintptr_t prepare_cell(void *opaque)
{ ProgressContext *c=opaque;uint32_t p=c->frame+0x2C;c->approach=call(0x548000,0x8324E0,&p,1);return c->approach; }
static int32_t level(void *opaque,uintptr_t cell){(void)opaque;return (int8_t)MEM8((uint32_t)cell+0x11B);}
static unsigned upper(void *opaque){ProgressContext *c=opaque;return MEM8(owner(c)+0x79);}
static uint32_t flags(void *opaque,uintptr_t cell){(void)opaque;return MEM32((uint32_t)cell+0x140);}
static void transition(void *opaque){ProgressContext *c=opaque;MEM8(owner(c)+0x57B)=1;}
uint32_t ra2_ground_internal_next_bridge(unsigned entry)
{
    ProgressContext c={0};c.frame=g_esp;c.drive=g_ebp;
    if(entry==0){
        uint32_t index=MEM32(c.drive+0x5C),table=MEM32(c.frame+0x38),a=table+index*12;
        int32_t x=(int32_t)MEM32(a),y=(int32_t)MEM32(a+4);
        uint32_t remaining=MEM32(c.frame+0x3C)-7u;MEM32(c.frame+0x3C)=remaining;
        MEM32(c.frame+0x8C)=(uint32_t)x;MEM32(c.frame+0x90)=(uint32_t)y;
        g_eax=index;g_esi=table;g_ebx=remaining;g_edx=(uint32_t)x;g_ecx=(uint32_t)y;
        return ra2_ground_full_sample_exhausted((int32_t)index,x,y)?0x4A1FDC:0x4A16A6;
    }
    Ra2PrepareApproachServices s={&c,reset_budget,path_direction,position,offset,construct_target,store_probe,prepare_cell,level,upper,construct_prepare_probe,flags,transition};
    int32_t effective_level=(int32_t)g_edi;g_esp=c.frame-0x100;
    int connection=ra2_ground_prepare_approach(&effective_level,&s);g_esp=c.frame;g_ebp=c.drive;g_ebx=(uint32_t)c.direction;
    if(connection){g_eax=c.unit;g_ecx=c.unit;return 0x4A3A44;}
    g_esi=c.offset;g_edi=(uint32_t)effective_level;g_eax=MEM8(owner(&c)+0x79);g_ecx=owner(&c);g_edx=((MEM32(c.approach+0x140)>>8)&1u)^g_eax;return 0x4A33C3;
}

static int finish_query(void *opaque,Ra2PassageFinishQuery which)
{
    ProgressContext *c=opaque;uint32_t zero=0,target,weapon;
    switch(which){
        case RA2_FINISH_CRUSH_TARGET_PRESENT:return call(0x473E30,c->approach,&zero,1)!=0;
        case RA2_FINISH_CRUSH_TARGET_CRUSHABLE:target=call(0x473E30,c->approach,&zero,1);return MEM8(MEM32(target+0x5AC)+0x1FD)!=0;
        case RA2_FINISH_ALLIED_OWNER:target=MEM32(c->frame+0x18);return (call(0x4E5500,MEM32(c->unit+0x1B4),&target,1)&255u)!=0;
        case RA2_FINISH_CRUSHER:return MEM8(MEM32(c->unit+0x5AC)+0xAF3)!=0;
        case RA2_FINISH_CRUSH_ABILITY:target=17;return (call(0x6D7910,c->unit,&target,1)&255u)!=0;
        case RA2_FINISH_TRAIN:return MEM8(MEM32(c->unit+0x5AC)+0xAA0)!=0;
        case RA2_FINISH_FIRST_WEAPON_PRESENT:return MEM32(method(c->unit,0x39C,&zero,1))!=0;
        case RA2_FINISH_SECOND_WEAPON_CAN_CLEAR:weapon=MEM32(method(c->unit,0x39C,&zero,1));return MEM8(MEM32(weapon+0xA0)+0x275)!=0;
        default:abort();
    }
}
void ra2_ground_passage_finish_bridge(void)
{
    ProgressContext c={0};c.frame=g_esp;c.unit=g_ebp;c.approach=g_ebx;
    Ra2PassageFinishState state={(int32_t)g_edi,MEM8(c.frame+0x88),MEM8(c.frame+0x12),MEM8(c.frame+0x13),(int32_t)MEM32(c.frame+0x18)};
    Ra2PassageFinishServices services={&c,finish_query};g_esp=c.frame-0x100;
    uint32_t result=(uint32_t)ra2_ground_finish_passage(state,&services);
    g_eax=result;g_edi=MEM32(c.frame);g_esi=MEM32(c.frame+4);g_ebp=MEM32(c.frame+8);g_ebx=MEM32(c.frame+12);g_esp=c.frame+0x90;
}
