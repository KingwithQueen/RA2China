extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);
extern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_tube_state.h"
#include "ground_handoff.h"
#include "ground_surface_class.h"
#include "ground_sampling_shared.h"
#include "ground_tube_state_bridge.h"
typedef struct TubeContext {uint32_t frame,unit,tube,vector,cell,drive,table;} TubeContext;
static Ra2WorldPoint point(uint32_t a){Ra2WorldPoint p;memcpy(&p,(void *)(uintptr_t)ADDR(a),12);return p;}
static void store(uint32_t a,Ra2WorldPoint p){memcpy((void *)(uintptr_t)ADDR(a),&p,12);}
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count,int caller_cleanup)
{
    uint32_t sp=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[tube-state] unresolved %08X\n",address);abort();}fn();
    if(caller_cleanup)g_esp+=count*4;
    if(g_esp!=sp){fprintf(stderr,"[tube-state] stack %08X\n",address);abort();}g_cur_func=caller;return g_eax;
}
static uint32_t method(uint32_t unit,uint32_t slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(unit)+slot),unit,args,count,0);}
static uint32_t tube_of(uint32_t unit)
{return MEM32(MEM32(0x8661CC)+(uint32_t)(int32_t)(int8_t)MEM8(unit+0x574)*4);}
static uintptr_t occupants(void *opaque)
{TubeContext *c=opaque;uint32_t p=c->frame+0x74;store(p,point(c->unit+0x88));c->cell=call(0x548000,0x8324E0,&p,1,0);return MEM32(c->cell+0xE4);}
static void begin(void *opaque)
{TubeContext *c=opaque;ra2_connection_observe(MEM32(c->unit+0x564)-4,3);uint32_t args[]={0,0};call(0x4BFBD0,c->vector,args,2,0);MEM32(c->vector)=0x79DB7C;MEM32(c->vector+0x14)=10;MEM32(c->vector+0x10)=0;}
static void append(void *opaque,uintptr_t object)
{
    TubeContext *c=opaque;uint32_t v=c->vector;int32_t capacity=(int32_t)MEM32(v+8),count=(int32_t)MEM32(v+0x10),grow=(int32_t)MEM32(v+0x14);
    if(count>=capacity)
    {
        if((!MEM8(v+0xD)&&capacity!=0)||grow<=0)return;
        uint32_t args[]={(uint32_t)capacity+(uint32_t)grow,0};if(!(method(v,8,args,2)&255u))return;
    }
    uint32_t index=MEM32(v+0x10);MEM32(v+0x10)=index+1;MEM32(MEM32(v+4)+index*4)=(uint32_t)object;
}
static uintptr_t next(void *opaque,uintptr_t object){(void)opaque;return MEM32((uint32_t)object+0x30);}
static int32_t count(void *opaque){TubeContext *c=opaque;return (int32_t)MEM32(c->vector+0x10);}
static uintptr_t item(void *opaque,int32_t index){TubeContext *c=opaque;return MEM32(MEM32(c->vector+4)+(uint32_t)index*4);}
static int32_t kind(void *opaque,uintptr_t object){(void)opaque;return (int32_t)method((uint32_t)object,0x2C,NULL,0);}
static int moving(void *opaque,uintptr_t object)
{
    (void)opaque;uint32_t locomotor=MEM32((uint32_t)object+0x564);
    if(!locomotor){uint32_t error=0x80004003;call(0x795940,0,&error,1,1);locomotor=MEM32((uint32_t)object+0x564);}
    uint32_t table=MEM32(locomotor);return (call(MEM32(table+0x10),table,&locomotor,1,0)&255u)!=0;
}
static void request_object_clearance(void *opaque,uintptr_t object)
{TubeContext *c=opaque;uint32_t p=c->frame+0x74;store(p,(Ra2WorldPoint){0,0,0});uint32_t args[]={p,1,1};method((uint32_t)object,0x15C,args,3);}
static void speed(void *opaque,int blocked)
{TubeContext *c=opaque;uint32_t args[]={0,blocked?0:0x3FF00000};method(c->unit,0x4C8,args,2);}
static uint32_t end(void *opaque)
{TubeContext *c=opaque;uint32_t v=c->vector,p=MEM32(v+4);MEM32(v)=0x79A91C;if(p&&MEM8(v+0xD))return call(0x781D3B,0,&p,1,1);return p;}
static Ra2WorldPoint center(uint32_t p,int32_t z)
{return (Ra2WorldPoint){(int32_t)(int16_t)(uint16_t)p*256+128,(int32_t)(int16_t)(uint16_t)(p>>16)*256+128,z};}
static void place_exit(void *opaque)
{TubeContext *c=opaque;ra2_connection_observe(MEM32(c->unit+0x564)-4,2);uint32_t p=c->frame+0x74;store(p,center(MEM32(tube_of(c->unit)+0x28),(int32_t)MEM32(c->unit+0x464)));method(c->unit,0x19C,&p,1);}
static void enter(void *opaque)
{TubeContext *c=opaque;uint32_t address=MEM32(MEM32(c->unit)+0x11C),one=1;MEM8(c->unit+0x574)=255;call(address,c->unit,&one,1,0);}
static int goal_is_exit_cell(void *opaque){TubeContext *c=opaque;return MEM32(c->unit+0x494)==c->cell;}
static void request_self_clearance(void *opaque)
{TubeContext *c=opaque;uint32_t p=c->frame+0x5C;store(p,(Ra2WorldPoint){0,0,0});uint32_t args[]={p,1,1};method(c->unit,0x15C,args,3);}
static void mission(void *opaque)
{TubeContext *c=opaque;uint32_t two=2;MEM8(c->unit+0x57B)=1;method(c->unit,0x174,&two,1);}
static uint32_t face(void *opaque)
{
    TubeContext *c=opaque;uint32_t p=c->frame+0x5C;store(p,point(c->unit+0x88));uint32_t cell=call(0x548000,0x8324E0,&p,1,0);
    uint32_t tube=call(0x47A130,cell,NULL,0,0);if(!tube)return 0;
    p=c->frame+0x30;MEM16(p)=(uint16_t)(((MEM32(tube+0x2C)<<13)-0x6001u)&0xFFFFE000u);
    return call(0x4B8B10,c->unit+0x2E0,&p,1,0);
}
static void snap(void *opaque)
{
    TubeContext *c=opaque;uint8_t index=(uint8_t)(MEM8(c->unit+0x575)+1);MEM8(c->unit+0x575)=index;
    c->table=MEM32(c->tube+0x30+(uint32_t)(int32_t)(int8_t)index*4);MEM8(c->frame+0x17)=(uint8_t)(c->table==UINT32_MAX);
    uint32_t p=c->unit+0x45C;method(c->unit,0x19C,&p,1);
}
static int finished(void *opaque){TubeContext *c=opaque;return MEM8(c->frame+0x17)!=0;}
uint32_t ra2_ground_tube_state_bridge(unsigned entry)
{
    TubeContext c={0};c.frame=g_esp;c.unit=g_esi;c.tube=g_ebp;c.vector=c.frame+0x5C;
    if(entry==1)
    {
        g_eax=MEM32(c.frame+0x28);
        if((int32_t)g_eax>(int32_t)g_ecx)return 0x6FAD75;
        Ra2TubeWaypointServices s={&c,snap,finished};g_esp=c.frame-0x100;
        Ra2TubeWaypointResult result=ra2_ground_tube_waypoint((int32_t)g_eax,(int32_t)g_ecx,&s);
        g_esp=c.frame;g_esi=c.unit;g_ebp=c.tube;g_edi=c.unit+0x45C;g_ebx=c.table;g_eax=(g_eax&0xFFFFFF00u)|MEM8(c.frame+0x17);
        return result==RA2_TUBE_EXIT?0x6FAE76:0x6FABAA;
    }
    if(entry==2)
    {
        uint32_t tube=MEM32(g_edx+(uint32_t)(int32_t)(int8_t)MEM8(c.unit+0x574)*4);
        return MEM32(tube+0x30+(uint32_t)(int32_t)(int8_t)MEM8(c.unit+0x575)*4)==UINT32_MAX?0x6FAE76:0x6FAA66;
    }
    Ra2TubeExitServices s={&c,occupants,begin,append,next,count,item,kind,moving,request_object_clearance,speed,end,place_exit,enter,goal_is_exit_cell,request_self_clearance,mission,face};
    g_esp=c.frame-0x100;uint32_t result=ra2_ground_tube_exit(&s),bp=MEM32(c.frame+8);
    g_eax=result;g_edi=MEM32(c.frame);g_esi=MEM32(c.frame+4);g_ebx=MEM32(c.frame+12);g_ebp=MEM32(bp);g_esp=bp+8;return 0;
}
static void select_table(void *opaque,int32_t index){TubeContext *c=opaque;c->table=MEM32(0x7A00A0+(uint32_t)index*16);}
static Ra2PathSample sample(void *opaque,int32_t index){TubeContext *c=opaque;Ra2PathSample p;memcpy(&p,(void *)(uintptr_t)ADDR(c->table+(uint32_t)index*12),12);return p;}
static void retain_loaded_table(void *opaque,int32_t table){(void)opaque;(void)table;}
static Ra2PathSample loaded_sample(void *opaque,int32_t index)
{
    TubeContext *c=opaque;(void)index;Ra2PathSample value;
    memcpy(&value,(void *)(uintptr_t)ADDR(c->table+c->vector*4u),sizeof(value));return value;
}
uint32_t ra2_ground_internal_handoff_bridge(unsigned entry)
{
    TubeContext c={0};c.frame=g_esp;c.drive=g_ebp;c.cell=g_esi;
    if(entry==0)
    {
        uint32_t flags=MEM32(c.cell+0x140);unsigned upper=0;
        if(flags&0x100u){Ra2WorldPoint p=point(MEM32(c.drive+0xC)+0x88);MEM32(c.frame+0x44)=(uint32_t)p.x;MEM32(c.frame+0x48)=(uint32_t)p.y;upper=ra2_ground_prepare_upper_layer(flags,(int8_t)MEM8(c.cell+0x11B),p.z,(int32_t)MEM32(0x8529D0));}
        MEM8(c.frame+0x18)=(uint8_t)upper;uint32_t args[]={0x852998,1,1,MEM32(c.frame+0x18)};
        g_esp=c.frame-0x100;g_eax=call(0x476920,c.cell,args,4,0);g_esp=c.frame;g_ebp=c.drive;g_esi=c.cell;return 0x4A32B4;
    }
    if(entry==2)
    {int32_t index=(int32_t)(g_ecx+1u);MEM32(c.drive+0x5C)=(uint32_t)index;g_ecx=(uint32_t)index;g_eax=MEM32(c.frame+0x3C);return (int32_t)MEM32(c.frame+0x3C)>7?0x4A166A:0x4A1FA1;}
    Ra2SamplingServices services={&c,NULL,select_table,sample};Ra2SamplingChoice choice={0};
    if(entry==4){c.table=g_eax;c.vector=g_ecx;services.select_table=retain_loaded_table;services.sample_at=loaded_sample;}
    int32_t index=entry>=3?(int32_t)g_edx:(int32_t)MEM32(c.drive+0x5C);Ra2SamplingPhase phase=ra2_ground_choose_selected_remainder((int32_t)g_eax,index,(int32_t)g_edi,&choice,&services);
    MEM32(c.frame+0x8C)=(uint32_t)choice.sample.x;MEM32(c.frame+0x90)=(uint32_t)choice.sample.y;
    g_eax=(uint32_t)choice.sample.y;g_esi=(uint32_t)choice.sample.x;g_edx=(uint32_t)index;
    if(phase==RA2_SAMPLING_DONE)return 0x4A263A;
    uint32_t p=MEM32(c.drive+0xC)+0x88;Ra2WorldPoint start=point(p);store(c.frame+0x80,start);MEM32(c.frame+0x34)=(uint32_t)choice.sample.direction;
    g_eax=p;g_esi=(uint32_t)start.x;g_ebx=(uint32_t)start.y;g_edx=(uint32_t)start.z;return 0x4A237D;
}
static int32_t base_height(void *opaque)
{TubeContext *c=opaque;uint32_t p=c->frame+0xC;MEM32(p)=MEM32(p+4)=128;return (int32_t)call(0x4706C0,c->cell,&p,1,0);}
static int scan(void *opaque){(void)opaque;return MEM8(0xA40958)!=0;}
static uintptr_t first(void *opaque){TubeContext *c=opaque;return MEM32(c->cell+0xE4);}
static int32_t support(void *opaque,uintptr_t object)
{TubeContext *c=opaque;uint32_t p=c->frame+0x18,body=MEM32((uint32_t)object+0x418);uint32_t result=method(body,0x7C,&p,1);return (int32_t)MEM32(result+8);}
static int fallback(void *opaque)
{TubeContext *c=opaque;uint32_t p=c->frame+0xC;MEM32(p)=MEM32(p+4)=0;uint32_t args[]={p,0,0};return call(0x471660,c->cell,args,3,0)!=0;}
void ra2_ground_surface_class_bridge(unsigned entry)
{
    TubeContext c={0};uint32_t sp=g_esp,ebx=g_ebx,ebp=g_ebp,esi=g_esi,edi=g_edi;c.frame=sp-0x24;c.cell=g_ecx;g_esp=sp-0x200;
    uint32_t result;
    if(entry==0)result=(uint32_t)ra2_ground_is_tube_entrance((int16_t)MEM16(c.cell+0x116),(int32_t)MEM32(0x8661D8),(int32_t)MEM32(c.cell+0xEC));
    else if(entry==1)result=(uint32_t)ra2_ground_is_tile_family((int32_t)MEM32(c.cell+0x38),(int32_t)MEM32(0xA52580));
    else {Ra2SurfaceSupportServices s={&c,base_height,scan,first,kind,next,support,fallback};result=(uint32_t)ra2_ground_surface_support_height(&s);}
    g_eax=result;g_ebx=ebx;g_ebp=ebp;g_esi=esi;g_edi=edi;g_esp=sp+4;
}
