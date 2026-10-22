#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_interpolation.h"
#include "ground_prepare_shared.h"
#include "ground_cell_services.h"
#include "ground_prepare_bridge.h"
#include "ground_services_bridge.h"
#include "movement_bridge.h"

typedef struct InterpolationContext { uint32_t drive, frame; } InterpolationContext;
static Ra2WorldPoint point(uint32_t a)
{ Ra2WorldPoint p; memcpy(&p, (void *)(uintptr_t)ADDR(a), sizeof(p)); return p; }
static void store(uint32_t a, Ra2WorldPoint p)
{ memcpy((void *)(uintptr_t)ADDR(a), &p, sizeof(p)); }
static uint32_t call(uint32_t address, uint32_t object, const uint32_t *args, unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[ground-services] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[ground-services] stack %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t owner(InterpolationContext *c){return MEM32(c->drive+0xC);}
static void owner_call(InterpolationContext *c,uint32_t slot,uint32_t arg)
{uint32_t u=owner(c);call(MEM32(MEM32(u)+slot),u,&arg,1);}
static Ra2WorldPoint transform(void *opaque)
{
    InterpolationContext *c=opaque;uint32_t args[]={c->frame+0xAC,c->frame+0x8C,c->frame+0x34};
    return point(call(0x4A4740,c->drive,args,3));
}
static Ra2WorldPoint position(void *opaque){return point(owner(opaque)+0x88);}
static uintptr_t cell_at(void *opaque,Ra2WorldPoint p)
{
    InterpolationContext *c=opaque;uint32_t arg=c->frame-0x40;store(arg,p);
    return call(0x548000,0x8324E0,&arg,1);
}
static Ra2WorldPoint blend(void *opaque,Ra2WorldPoint delta)
{
    InterpolationContext *c=opaque;uint32_t f=c->frame;
    store(f+0xC4,delta);store(f+0xB8,(Ra2WorldPoint){0,0,0});
    uint32_t args[]={f+0xC4,ra2_movement_progress_bits((int32_t)MEM32(c->drive+0x4C),g_fpu_cw)};
    g_edx=f+0xB8;
    return point(call(0x7220C0,f+0x5C,args,2));
}
static void leave(void *c){owner_call(c,0x11C,0);}
static void place(void *opaque,Ra2WorldPoint p)
{InterpolationContext *c=opaque;store(c->frame+0x18,p);owner_call(c,0x19C,c->frame+0x18);}
static Ra2InterpolationSurface surface(void *c,uintptr_t cell)
{(void)c;return (Ra2InterpolationSurface){(int8_t)MEM8((uint32_t)cell+0x11B),(MEM32((uint32_t)cell+0x140)&0x100)!=0};}
static void set_bridge(void *c,unsigned value){MEM8(owner(c)+0x79)=(uint8_t)value;}
static void enter(void *c){owner_call(c,0x11C,1);}
static uint8_t flag(void *c){return MEM8(owner(c)+0x74);}
static void set_flag(void *c,uint8_t value){MEM8(owner(c)+0x74)=value;}
void ra2_ground_interpolation_bridge(void)
{
    InterpolationContext c={g_ebp,g_esp};uint32_t f=c.frame;
    Ra2WorldPoint start=point(f+0x80);int32_t x=(int32_t)g_esi,y=(int32_t)g_ebx;
    Ra2InterpolationServices s={&c,transform,position,cell_at,blend,leave,place,surface,set_bridge,enter,flag,set_flag};
    g_esp=f-0x100;
    ra2_ground_interpolate_advance(start,x,y,(int32_t)MEM32(c.drive+0x4C),&s);
    g_edi=MEM32(f);g_esi=MEM32(f+4);g_ebp=MEM32(f+8);g_ebx=MEM32(f+12);
    g_eax&=0xFFFFFF00u;g_esp=f+0xFC;
    g_flag_k=FK_ADD;g_flag_a=f+16;g_flag_b=0xE4;g_flag_cf=f+0xF4<f+16;
}
static void reset_budget(void *c,int32_t value){(void)c;MEM32(MEM32(g_ebp+0xC)+0x53C)=(uint32_t)value;}
static int32_t path_head(void *c){(void)c;return (int32_t)MEM32(MEM32(g_ebp+0xC)+0x4D0);}
static uint32_t segment(void *c,int32_t head){(void)c;g_ebx=(uint32_t)head;return ra2_ground_prepare_segment_bridge();}
uint32_t ra2_ground_prepare_shared_bridge(int rebuilt)
{
    Ra2PrepareSharedServices s={NULL,reset_budget,path_head,segment};
    return ra2_ground_prepare_shared(rebuilt,(int32_t)g_ebx,&s);
}
void ra2_cell_service_bridge(unsigned entry)
{
    uint32_t stack=g_esp,input=MEM32(stack+4),map=entry==3?0x8324E0:g_ecx;
    Ra2CellGrid grid={(const uint32_t *)(uintptr_t)ADDR(MEM32(map+0x138)),(int32_t)MEM32(map+0x13C),0xA6F9F8,
        (Ra2ServiceCell *)(uintptr_t)ADDR(0xA6FA1C)};
    Ra2ServiceCell p;memcpy(&p,(void *)(uintptr_t)ADDR(input),4);
    if(entry==0)g_eax=(uint32_t)ra2_cell_at_world(&grid,point(input));
    else if(entry==1||entry==3)
    {
        uint32_t cell=(uint32_t)ra2_cell_at_point(&grid,p);g_eax=cell;
        if(entry==3)
        {
            memcpy(&p,(void *)(uintptr_t)ADDR(cell+0x24),4);
            uint32_t house=MEM32(stack+8);
            g_eax=MEM32(house+0x58DC+(uint32_t)ra2_cell_threat_index(p)*4);
        }
    }
    else g_eax=((uint32_t)(int32_t)p.x&0xFFFFFF00u)|(uint32_t)ra2_cell_slot_present(grid.cells,p);
    g_esp=stack+(entry==3?12:8);
}
