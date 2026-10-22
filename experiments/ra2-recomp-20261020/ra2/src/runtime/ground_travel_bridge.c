#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_tube_travel.h"
#include "ground_template_next.h"
#include "ground_passage_neighbor.h"
#include "ground_travel_bridge.h"
typedef struct TravelContext { uint32_t frame,unit,drive,route,approach,last,neighbor; int32_t count; } TravelContext;
static Ra2WorldPoint point(uint32_t a){Ra2WorldPoint p;memcpy(&p,(void *)(uintptr_t)ADDR(a),12);return p;}
static void store(uint32_t a,Ra2WorldPoint p){memcpy((void *)(uintptr_t)ADDR(a),&p,12);}
static double number(uint32_t a){double d;memcpy(&d,(void *)(uintptr_t)ADDR(a),8);return d;}
static void store_number(uint32_t a,double d){memcpy((void *)(uintptr_t)ADDR(a),&d,8);}
static float single(uint32_t a){float f;memcpy(&f,(void *)(uintptr_t)ADDR(a),4);return f;}
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[movement-travel] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[movement-travel] stack %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t method(uint32_t unit,uint32_t slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(unit)+slot),unit,args,count);}
static int32_t distance(void *opaque)
{
    TravelContext *c=opaque;uint32_t p=c->frame+0x74;
    uint32_t current=method(c->unit,0x48,&p,1);c->approach=c->unit+0x45C;
    uint32_t args[]={c->frame+0x5C,c->approach};uint32_t delta=call(0x4348F0,current,args,2);
    int32_t result=(int32_t)call(0x41B780,delta,NULL,0);MEM32(c->frame+0x28)=(uint32_t)result;return result;
}
static void route(void *opaque)
{TravelContext *c=opaque;c->route=MEM32(MEM32(0x8661CC)+(uint32_t)(int32_t)(int8_t)MEM8(c->unit+0x574)*4);}
static uint32_t heading(void *opaque)
{
    TravelContext *c=opaque;uint32_t p=c->frame+0x74;
    uint32_t current=method(c->unit,0x48,&p,1),args[]={current,c->approach};
    uint32_t result=MEM32(call(0x423EF0,c->frame+0x30,args,2));MEM32(c->frame+0x30)=result;return result;
}
static int32_t speed(void *opaque)
{
    TravelContext *c=opaque;int32_t value=(int32_t)MEM32(MEM32(c->unit+0x5AC)+0x5A0);
    int32_t result=ra2_ground_tube_step(value,number(0x79D568),g_fpu_cw,MEM16(0x7D8964));
    g_fpu_cw=MEM16(0x7D8964);MEM32(c->frame+0x18)=(uint32_t)result;return result;
}
static Ra2WorldPoint center(uint32_t packed)
{Ra2WorldPoint p={(int32_t)((uint32_t)(int32_t)(int16_t)packed*256u+128u),(int32_t)((uint32_t)(int32_t)(int16_t)(packed>>16)*256u+128u),0};return p;}
static void endpoints(void *opaque)
{
    TravelContext *c=opaque;store(c->frame+0x50,center(MEM32(c->route+0x28)));
    store(c->frame+0x5C,center(MEM32(c->route+0x24)));c->count=(int32_t)MEM32(c->route+0x1C0);
    MEM32(c->frame+0x24)=(uint32_t)c->count;
}
static int32_t entrance_height(void *opaque)
{TravelContext *c=opaque;uint32_t p=c->frame+0x5C;c->last=call(0x55A280,0x8324E0,&p,1);return (int32_t)c->last;}
static int32_t exit_height(void *opaque)
{TravelContext *c=opaque;uint32_t p=c->frame+0x50;return (int32_t)call(0x55A280,0x8324E0,&p,1);}
static int32_t count(void *opaque){return ((TravelContext *)opaque)->count;}
uint32_t ra2_ground_tube_travel_bridge(unsigned entry)
{
    TravelContext c={0};c.frame=g_esp;c.unit=g_esi;c.route=g_ebp;c.approach=g_edi;
    if(entry==0){
        Ra2TubeEntryServices s={&c,distance,route,heading,speed,endpoints,entrance_height,exit_height,count};
        g_esp=c.frame-0x100;Ra2TubeEntryPreparation out=ra2_ground_tube_prepare_entry(&s);g_esp=c.frame;
        MEM32(c.frame+0x24)=(uint32_t)out.rise;g_eax=(uint32_t)out.rise;g_ecx=(uint32_t)out.step;
        g_ebx=c.last;g_ebp=c.route;g_esi=c.unit;g_edi=c.approach;return 0x6FAB6A;
    }
    int remaining=entry==1;uint32_t direction=remaining?g_ebx:MEM32(c.route+(uint32_t)(int32_t)(int8_t)MEM8(c.unit+0x575)*4+0x30);
    Ra2WorldPoint origin=point(c.unit+0x88);MEM32(c.frame+0x74)=(uint32_t)origin.x;MEM32(c.frame+0x78)=(uint32_t)origin.y;
    int32_t distance_value=(int32_t)MEM32(c.frame+0x18);
    int32_t heading_value=remaining?(int32_t)g_eax:(int32_t)MEM32(c.frame+0x30);
    if(remaining){distance_value=(int32_t)((uint32_t)distance_value-MEM32(c.frame+0x28));MEM32(c.frame+0x30)=(uint32_t)distance_value;}
    Ra2TubeHorizontalInput input={origin,heading_value,distance_value,number(0x79B620),single(0x7D8048),single(0x7D804C),(const float *)(uintptr_t)ADDR(0x801DC4),g_fpu_cw,MEM16(0x7D8964)};
    Ra2TubeHorizontalResult out=ra2_ground_tube_horizontal(input);g_fpu_cw=MEM16(0x7D8964);
    store_number(c.frame+0x40,out.angle);store_number(c.frame+0x18,(double)distance_value);
    if(remaining){store_number(c.frame+0x28,(double)origin.y);MEM32(c.frame+0x28)=(uint32_t)out.point.y;}
    else{store_number(c.frame+0x28,(double)distance_value);store_number(c.frame+0x30,(double)origin.y);MEM32(c.frame+0x30)=(uint32_t)out.point.y;}
    uint32_t args[]={(uint32_t)out.point.x,(uint32_t)out.point.y,(uint32_t)origin.z};uint32_t dest=c.frame+(remaining?0x50:0x5C);
    g_esp=c.frame-0x100;call(0x41B630,dest,args,3);g_esp=c.frame;
    if(remaining){g_edx=MEM32(dest);g_eax=MEM32(dest+4);g_ecx=MEM32(dest+8);g_ebx=direction;g_ebp=MEM32(c.frame+0x44);g_edi=(uint32_t)origin.z;return 0x6FAD1C;}
    g_eax=MEM32(dest);g_ecx=MEM32(dest+4);g_edx=MEM32(dest+8);g_ebx=MEM32(c.frame+0x44);g_ebp=direction;g_edi=(uint32_t)origin.z;return 0x6FAE1D;
}
static uint32_t owner(TravelContext *c){return MEM32(c->drive+0xC);}
static unsigned can_advance(void *opaque){TravelContext *c=opaque;return method(owner(c),0x27C,NULL,0);}
static unsigned accepts(void *opaque)
{
    TravelContext *c=opaque;uint32_t packed=ra2_ground_template_cell((int32_t)MEM32(c->frame+0x38),(int32_t)MEM32(c->frame+0x3C));
    MEM32(c->frame+0x18)=packed;MEM32(c->frame+0x28)=packed;
    uint32_t args[]={owner(c),c->frame+0x28};return call(0x55ACD0,0x8324E0,args,2);
}
static int32_t sample_heading(void *opaque)
{TravelContext *c=opaque;return (int32_t)MEM32(MEM32(c->frame+0x38)+MEM32(c->drive+0x5C)*12+8);}
static void save_heading(void *opaque,int32_t value){TravelContext *c=opaque;MEM32(c->frame+0x30)=(uint32_t)value;}
static uintptr_t transform(void *opaque)
{TravelContext *c=opaque;uint32_t args[]={c->frame+0xAC,c->frame+0x8C,c->frame+0x30};return call(0x4A4740,c->drive,args,3);}
uint32_t ra2_ground_template_next_bridge(unsigned entry)
{
    TravelContext c={0};c.frame=g_esp;c.drive=g_ebp;g_esp=c.frame-0x100;
    if(entry==0){Ra2TemplateSampleServices s={&c,sample_heading,save_heading,transform};uint32_t output=(uint32_t)ra2_ground_advance_template_sample(&s);
        g_ecx=MEM32(output);g_edi=MEM32(output+4);g_eax=output;g_esp=c.frame;return 0x4A17D5;}
    Ra2TemplateNextServices s={&c,can_advance,accepts};int accepted=ra2_ground_prepare_next_template(&s);g_esp=c.frame;
    if(accepted)return 0x4A3433;
    g_eax=(g_eax&0xFFFFFF00u)|1u;g_edi=MEM32(c.frame);g_esi=MEM32(c.frame+4);g_ebp=MEM32(c.frame+8);g_ebx=MEM32(c.frame+12);g_esp=c.frame+0x6C;return 0;
}
static uintptr_t neighbor(void *opaque,unsigned direction)
{TravelContext *c=opaque;c->neighbor=direction;return call(0x476AC0,c->unit,&c->neighbor,1);}
static uintptr_t obstacle(void *opaque,uintptr_t cell)
{(void)opaque;return call(0x47A130,(uint32_t)cell,NULL,0);}
static int32_t orientation(void *opaque,uintptr_t object){(void)opaque;return (int32_t)MEM32((uint32_t)object+0x2C);}
uint32_t ra2_ground_passage_neighbor_bridge(void)
{
    TravelContext c={0};c.frame=g_esp;c.unit=g_ebx;uint32_t incoming_edi=g_edi,incoming_esi=g_esi;
    int32_t direction=(int32_t)MEM32(c.frame+0x80);Ra2NeighborPassageServices s={&c,neighbor,obstacle,orientation};g_esp=c.frame-0x100;
    int blocked=ra2_ground_neighbor_blocks(direction,&s);g_esp=c.frame;
    if(!blocked){g_edi=(uint32_t)direction;g_esi=c.neighbor;return 0x70323E;}
    (void)incoming_edi;(void)incoming_esi;g_eax=7;g_edi=MEM32(c.frame);g_esi=MEM32(c.frame+4);g_ebp=MEM32(c.frame+8);g_ebx=MEM32(c.frame+12);g_esp=c.frame+0x90;return 0;
}
