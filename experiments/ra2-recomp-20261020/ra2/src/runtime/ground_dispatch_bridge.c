#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_sampling.h"
#include "ground_prepare_exit.h"
#include "ground_object_services.h"
#include "ground_dispatch_bridge.h"
typedef struct DispatchContext {uint32_t frame,drive,object,cell,destination,table,arg1,arg2;} DispatchContext;
static Ra2WorldPoint point(uint32_t a){Ra2WorldPoint p;memcpy(&p,(void *)(uintptr_t)ADDR(a),12);return p;}
static void store(uint32_t a,Ra2WorldPoint p){memcpy((void *)(uintptr_t)ADDR(a),&p,12);}
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[ground-dispatch] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[ground-dispatch] stack %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t method(uint32_t object,uint32_t slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(object)+slot),object,args,count);}
static uint32_t owner(DispatchContext *c){return MEM32(c->drive+0xC);}
static Ra2SamplingTemplate template_at(void *opaque,int32_t selector)
{
    (void)opaque;uint32_t a=0x7A0180+(uint32_t)selector*12;
    return (Ra2SamplingTemplate){(int8_t)MEM8(a),(int8_t)MEM8(a+1),MEM8(a+4)};
}
static void select_table(void *opaque,int32_t table)
{DispatchContext *c=opaque;c->table=MEM32(0x7A00A0+(uint32_t)table*16);}
static Ra2PathSample sample_at(void *opaque,int32_t index)
{DispatchContext *c=opaque;Ra2PathSample p;memcpy(&p,(void *)(uintptr_t)ADDR(c->table+(uint32_t)index*12),12);return p;}
uint32_t ra2_ground_sampling_bridge(unsigned entry)
{
    DispatchContext c={0};c.drive=g_ebp;c.frame=g_esp;
    int32_t progress=(int32_t)MEM32(c.frame+0x3C),selector=(int32_t)MEM32(c.drive+0x58),index=(int32_t)MEM32(c.drive+0x5C);
    Ra2SamplingServices services={&c,template_at,select_table,sample_at};Ra2SamplingChoice choice={0};Ra2SamplingPhase phase;
    if(entry==1)
    {
        phase=ra2_ground_finish_sample(&index,progress);MEM32(c.drive+0x5C)=(uint32_t)index;
        return phase==RA2_SAMPLING_FULL_STEP?0x4A166A:0x4A1FA1;
    }
    if(entry==0)
    {
        phase=ra2_ground_choose_full_sample((int32_t)g_edx,(int32_t)g_eax,selector,MEM8(c.drive+0x60),&choice,&services);
        g_edi=UINT32_MAX;
        if(phase==RA2_SAMPLING_REMAINDER)return 0x4A1FA1;
        MEM32(c.frame+0xA8)=0x7A0180+(uint32_t)selector*12;g_esi=MEM32(c.frame+0xA8);
        MEM32(c.frame+0x58)=(uint32_t)choice.table*16;MEM32(c.frame+0x38)=c.table;
        if(phase==RA2_SAMPLING_INVALID_DIRECTION)return 0x4A22F9;
        MEM8(c.frame+0x13)=(uint8_t)choice.turning;
        if((int32_t)g_eax!=-1 && g_eax!=8)MEM16(c.frame+0x14)=(uint16_t)((uint32_t)template_at(&c,selector).facing<<8);
        return 0x4A166A;
    }
    MEM32(c.drive+0x4C)=(uint32_t)progress;g_edi=0;
    phase=ra2_ground_choose_remainder(progress,selector,MEM8(c.drive+0x60),index,&choice,&services);
    if(progress>0 && selector>=0)
    {MEM32(c.frame+0x8C)=(uint32_t)choice.sample.x;MEM32(c.frame+0x90)=(uint32_t)choice.sample.y;}
    if(phase==RA2_SAMPLING_DONE)return 0x4A263A;
    Ra2WorldPoint start=point(owner(&c)+0x88);store(c.frame+0x80,start);MEM32(c.frame+0x34)=(uint32_t)choice.sample.direction;
    g_esi=(uint32_t)start.x;g_ebx=(uint32_t)start.y;MEM32(c.frame+0x64)=(uint32_t)start.z;
    return 0x4A237D;
}
static int owner_exists(void *opaque){return owner(opaque)!=0;}
static void aborted(void *opaque){DispatchContext *c=opaque;MEM8(MEM32(c->frame+0x60))=1;}
static int accepted(void *opaque){DispatchContext *c=opaque;return (method(owner(c),0x2AC,&c->destination,1)&255)!=0;}
static void stop(void *opaque){DispatchContext *c=opaque;uint32_t args[]={0,1};method(owner(c),0x410,args,2);}
static int32_t current_frame(void *opaque){(void)opaque;return (int32_t)MEM32(0xA40D2C);}
static int32_t retry_delay(void *opaque)
{
    (void)opaque;double factor;memcpy(&factor,(void *)(uintptr_t)ADDR(MEM32(0x839848)+0x13C8),8);
    int32_t delay=ra2_ground_scale_speed(900,factor,g_fpu_cw);g_fpu_cw=MEM16(0x7D8964);return delay;
}
static void restart(void *opaque,int32_t frame,int32_t delay)
{DispatchContext *c=opaque;uint32_t u=owner(c);MEM32(u+0x530)=(uint32_t)frame;MEM32(u+0x534)=MEM32(c->frame+0x54);MEM32(u+0x538)=(uint32_t)delay;}
void ra2_ground_prepare_exit_bridge(unsigned entry)
{
    DispatchContext c={0};c.drive=g_ebp;c.frame=g_esp;c.destination=g_esi;
    int rebuilt=(g_eax&255)!=0,result=0;g_esp=c.frame-0x100;
    if(entry<2)
    {
        Ra2PrepareExitServices s={&c,owner_exists,aborted,accepted,stop,current_frame,retry_delay,restart};
        result=ra2_ground_prepare_after_rebuild(rebuilt,entry==1,&s);
    }
    else if(entry==2)
    {
        Ra2PreparePendingState pending={MEM8(owner(&c)+0x57A),(int32_t)MEM32(c.drive+0x58)};
        ra2_ground_prepare_clear_pending(&pending);MEM8(owner(&c)+0x57A)=pending.sound_pending;MEM32(c.drive+0x58)=(uint32_t)pending.selector;result=1;
    }
    uint32_t f=c.frame;g_eax=(g_eax&0xFFFFFF00u)|(uint32_t)result;
    g_edi=MEM32(f);g_esi=MEM32(f+4);g_ebp=MEM32(f+8);g_ebx=MEM32(f+12);g_esp=f+0x6C;
    g_flag_k=FK_ADD;g_flag_a=f+16;g_flag_b=0x4C;g_flag_cf=f+0x5C<f+16;
}
static int enabled(void *opaque){(void)opaque;return MEM8(0xA40958)!=0;}
static uintptr_t head(void *opaque,int upper){DispatchContext *c=opaque;return MEM32(c->cell+(upper?0xE8:0xE4));}
static int32_t kind(void *opaque,uintptr_t object){(void)opaque;return (int32_t)method((uint32_t)object,0x2C,NULL,0);}
static uintptr_t next(void *opaque,uintptr_t object){(void)opaque;return MEM32((uint32_t)object+0x30);}
static uintptr_t fallback(void *opaque){DispatchContext *c=opaque;uint32_t args[]={c->arg1,c->arg2,0};return call(0x471660,c->cell,args,3);}
static int32_t cell_level(void *opaque){DispatchContext *c=opaque;uint32_t cell=method(c->object,0x1A4,NULL,0);return (int8_t)MEM8(cell+0x11B);}
static unsigned bridge_layer(void *opaque){DispatchContext *c=opaque;return MEM8(c->object+0x79)!=0;}
static Ra2WorldPoint position(void *opaque){DispatchContext *c=opaque;return point(c->object+0x88);}
static int32_t ground_height(void *opaque,Ra2WorldPoint p){DispatchContext *c=opaque;uint32_t arg=c->frame-0x40;store(arg,p);return (int32_t)call(0x55A280,0x8324E0,&arg,1);}
static int32_t bridge_height(void *opaque){(void)opaque;return (int32_t)MEM32(0xA72F30);}
void ra2_ground_object_service_bridge(unsigned entry)
{
    DispatchContext c={0};c.frame=g_esp;c.object=c.cell=g_ecx;c.arg1=MEM32(g_esp+4);c.arg2=MEM32(g_esp+8);
    uint32_t ebx=g_ebx,esi=g_esi,edi=g_edi,ebp=g_ebp,result;
    g_esp=c.frame-0x100;
    Ra2ObjectScanServices s={&c,enabled,head,kind,next,fallback};
    Ra2HeightServices h={&c,cell_level,bridge_layer,position,ground_height,bridge_height};
    if(entry==0)result=(uint32_t)ra2_ground_find_kind(0,6,&s);
    else if(entry==1)result=(uint32_t)ra2_ground_find_kind((c.arg1&255)!=0,36,&s);
    else if(entry==2)result=(uint32_t)ra2_ground_find_blocking_object(&s);
    else if(entry==3)result=(uint32_t)ra2_ground_cell_connection((int16_t)MEM16(c.cell+0x116),(int32_t)MEM32(0x8661D8),(const uint32_t *)(uintptr_t)ADDR(MEM32(0x8661CC)));
    else if(entry==4)result=(uint32_t)ra2_ground_surface_level(&h);
    else result=(uint32_t)ra2_ground_height_above_surface(&h);
    g_eax=result;g_ebx=ebx;g_esi=esi;g_edi=edi;g_ebp=ebp;g_esp=c.frame+(entry==1?8:entry==2?12:4);
}
