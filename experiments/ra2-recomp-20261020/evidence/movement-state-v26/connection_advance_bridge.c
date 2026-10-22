extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);
#include "ground_template_entry.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_advance.h"
#include "ground_advance_bridge.h"
#include "state_trace.h"

typedef struct AdvanceContext
{
    uint32_t drive, frame, train_owner, previous_cell, next_cell;
} AdvanceContext;

static Ra2WorldPoint read_point(uint32_t address)
{
    Ra2WorldPoint result;
    memcpy(&result, (const void *)(uintptr_t)ADDR(address), sizeof(result));
    return result;
}
static void write_point(uint32_t address, Ra2WorldPoint point)
{ memcpy((void *)(uintptr_t)ADDR(address), &point, sizeof(point)); }
static uint32_t owner(AdvanceContext *c) { return MEM32(c->drive + 0xC); }

static uint32_t engine_call(uint32_t address, uint32_t object, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i=count; i; --i) { g_esp-=4; MEM32(g_esp)=args[i-1]; }
    g_esp-=4; MEM32(g_esp)=RECOMP_RETADDR; g_ecx=object;
    recomp_func_t function = recomp_lookup_manual(address);
    if (!function) function = recomp_lookup(address);
    if (!function) function = recomp_lookup_import(address);
    if (!function) { fprintf(stderr,"[advance-bridge-error] unresolved %08X\n",address); abort(); }
    function();
    if (g_esp!=stack) { fprintf(stderr,"[advance-bridge-error] unbalanced %08X\n",address); abort(); }
    g_cur_func=caller;
    return g_eax;
}
static uint32_t object_call(uint32_t object, uint32_t slot, const uint32_t *args, unsigned count)
{ return engine_call(MEM32(MEM32(object)+slot),object,args,count); }
static int32_t signed_bits(uint32_t bits)
{ int32_t result; memcpy(&result,&bits,4); return result; }

static int32_t query(void *opaque, Ra2AdvanceQuery which, uint32_t object)
{
    AdvanceContext *c=opaque;
    uint32_t unit=owner(c);
    switch (which)
    {
        case RA2_ADVANCE_NEEDS_POSITION_MARK: return (object_call(unit,0xBC,NULL,0)&255u)!=0;
        case RA2_ADVANCE_SAMPLE_INDEX: return (int32_t)MEM32(c->drive+0x5C);
        case RA2_ADVANCE_CELL_LEVEL: return (int8_t)MEM8(object+0x11B);
        case RA2_ADVANCE_CELL_HAS_BRIDGE: return (MEM32(object+0x140)&0x100)!=0;
        case RA2_ADVANCE_IS_TRAIN: return MEM8(object_call(unit,0x80,NULL,0)+0xAA0);
        case RA2_ADVANCE_TRAIN_FLAG_5B8: c->train_owner=unit; return MEM8(unit+0x5B8);
        case RA2_ADVANCE_BRIDGE_LAYER: return MEM8(unit+0x79);
        case RA2_ADVANCE_GROUND_HEIGHT:
        {
            uint32_t point=c->frame+0xD0;
            write_point(point,read_point(c->train_owner+0x88));
            uint32_t height=engine_call(0x55A280,0x8324E0,&point,1);
            return signed_bits(height+MEM32(0x8529C0));
        }
        case RA2_ADVANCE_OBJECT_HEAD_LOWER: return (int32_t)MEM32(object+0xE4);
        case RA2_ADVANCE_OBJECT_HEAD_UPPER: return (int32_t)MEM32(object+0xE8);
        case RA2_ADVANCE_OBJECT_NEXT: return (int32_t)MEM32(object+0x30);
        case RA2_ADVANCE_OBJECT_CRUSHABLE: return MEM8(object_call(object,0x84,NULL,0)+0x1FD);
        case RA2_ADVANCE_OWNER_ALIVE: return MEM8(unit+0x7D);
        case RA2_ADVANCE_OVERLAY_INDEX: return (int32_t)MEM32(object+0x44);
        case RA2_ADVANCE_CRUSHING_ENABLED: return MEM8(c->drive+0x64);
        case RA2_ADVANCE_IS_CRUSHER: return MEM8(object_call(unit,0x80,NULL,0)+0xAF3);
        case RA2_ADVANCE_CRUSHER_ABILITY:
        {
            uint32_t ability=17;
            return (engine_call(0x6D7910,unit,&ability,1)&255u)!=0;
        }
        case RA2_ADVANCE_OVERLAY_LAND_TYPE: return (int32_t)MEM32(MEM32(MEM32(0xA35DEC)+object*4)+0x264);
        case RA2_ADVANCE_CRUSH_SLOWDOWN: return MEM8(object_call(unit,0x80,NULL,0)+0xAF4);
        case RA2_ADVANCE_TRANSITION_SAMPLE: return (int32_t)MEM32(0x7A00AC+MEM32(c->frame+0x58));
        default: abort();
    }
}
static void mark_position(AdvanceContext *c, uint32_t local)
{
    uint32_t point=c->frame+local;
    write_point(point,read_point(owner(c)+0x88));
    object_call(owner(c),0xEC,&point,1);
}
static void act(void *opaque, Ra2AdvanceAction which, uint32_t object, int32_t value)
{
    AdvanceContext *c=opaque;
    uint32_t unit=owner(c), argument=(uint32_t)value;
    switch (which)
    {
        case RA2_ADVANCE_MARK_POSITION: mark_position(c,value ? 0xB8 : 0xDC); break;
        case RA2_ADVANCE_CLEAR_SAMPLE_FLAGS: MEM8(owner(c)+0x5A0)=0; MEM8(owner(c)+0x5A1)=0; break;
        case RA2_ADVANCE_LEAVE_CELL:
        case RA2_ADVANCE_ENTER_CELL: object_call(unit,0x11C,&argument,1); break;
        case RA2_ADVANCE_SET_BRIDGE_LAYER: MEM8(unit+0x79)=(uint8_t)value; break;
        case RA2_ADVANCE_TRAIN_DAMAGE:
        {
            uint32_t args[]={c->frame+0x70,0,MEM32(MEM32(0x839848)+0xC74),0,1,1};
            MEM32(c->frame+0x70)=10000;
            object_call(object,0x158,args,6);
            MEM32(c->frame+0x70)=20;
            args[2]=MEM32(MEM32(0x839848)+0xC74); args[5]=0;
            object_call(c->train_owner,0x158,args,6);
            break;
        }
        case RA2_ADVANCE_MARK_CRUSHING: MEM8(unit+0x59F)=1; break;
        case RA2_ADVANCE_APPLY_CRUSH_SLOWDOWN: MEM32(unit+0x28C)=0xBCA3D70A; break;
        case RA2_ADVANCE_REFRESH_PLACEMENT:
        {
            uint8_t flag=MEM8(unit+0x74); MEM8(unit+0x74)=0;
            object_call(owner(c),0x1B4,&argument,1);
            MEM8(owner(c)+0x74)=flag;
            break;
        }
        case RA2_ADVANCE_SET_FACING:
        {
            MEM16(c->frame+0x54)=(uint16_t)((uint32_t)value<<8);
            uint32_t facing=c->frame+0x54;
            engine_call(0x4B8B10,owner(c)+0x2E0,&facing,1);
            break;
        }
        default: abort();
    }
}
static Ra2WorldPoint raw_position(void *opaque)
{ return read_point(owner(opaque)+0x88); }
static Ra2AdvanceCell current_cell(void *opaque)
{
    AdvanceContext *c=opaque;
    uint32_t argument=c->frame+0x24;
    uint32_t result=object_call(owner(c),0x1A0,&argument,1);
    Ra2AdvanceCell cell;
    memcpy(&cell,(const void *)(uintptr_t)ADDR(result),4);
    memcpy((void *)(uintptr_t)ADDR(c->frame+0x98),&cell,4);
    return cell;
}
static Ra2PathSample sample(void *opaque, int32_t index, int previous)
{
    AdvanceContext *c=opaque;
    uint32_t address=MEM32(c->frame+0x38)+(uint32_t)index*12;
    Ra2PathSample result;
    memcpy(&result,(const void *)(uintptr_t)ADDR(address),sizeof(result));
    /* 当前 x/y 在消耗采样时已保存；标记/放置回调后只重新读取方向。 */
    if (!previous) { result.x=(int32_t)MEM32(c->frame+0x8C); result.y=(int32_t)MEM32(c->frame+0x90); }
    return result;
}
static Ra2WorldPoint transform_sample(void *opaque, Ra2PathSample *value, int previous)
{
    AdvanceContext *c=opaque;
    uint32_t input=c->frame+(previous ? 0x80 : 0x8C);
    uint32_t args[]={c->frame+(previous ? 0xC4 : 0xAC),input,c->frame+0x30};
    MEM32(input)=(uint32_t)value->x; MEM32(input+4)=(uint32_t)value->y;
    MEM32(c->frame+0x30)=(uint32_t)value->direction;
    ra2_internal_observe(c->drive,0,previous?11:10,0,0);
    Ra2WorldPoint result=read_point(engine_call(0x4A4740,c->drive,args,3));
    if(!previous)ra2_internal_observe(c->drive,0,12,result.x,result.y);
    value->direction=(int32_t)MEM32(c->frame+0x30);
    uint32_t packed=ra2_ground_sample_cell(result.x,result.y);
    MEM32(c->frame+(previous ? 0x98 : 0x68))=packed;
    return result;
}
static uint32_t find_cell(void *opaque, Ra2AdvanceCell cell)
{
    AdvanceContext *c=opaque;
    uint32_t address=c->frame+(c->previous_cell ? 0x68 : 0x98);
    memcpy((void *)(uintptr_t)ADDR(address),&cell,4);
    uint32_t result=engine_call(0x548070,0x8324E0,&address,1);
    if (!c->previous_cell) c->previous_cell=result;
    else { c->next_cell=result; MEM32(c->frame+0x40)=result; }
    return result;
}
static void place(void *opaque, Ra2WorldPoint point, int crosses_cell)
{
    AdvanceContext *c=opaque;
    uint32_t argument=c->frame+0x48;
    write_point(argument,point);
    uint8_t flag=MEM8(owner(c)+0x74);
    if (!crosses_cell) MEM8(owner(c)+0x74)=0;
    object_call(owner(c),0x19C,&argument,1);
    if (!crosses_cell) MEM8(owner(c)+0x74)=flag;
}
uint32_t ra2_ground_advance_sample_bridge(void)
{
    AdvanceContext context={g_ebp,g_esp,0,0,0};
    ra2_state_movement_audit(20,context.drive,0,MEM32(context.drive+0x5C));
    Ra2AdvanceServices services={&context,query,act,raw_position,current_cell,sample,transform_sample,find_cell,place};
    g_esp=context.frame-0x100;
    int alive=ra2_ground_advance_sample(&services);
    g_ebp=context.drive; g_esp=context.frame;
    return alive ? 0x4A1B60 : 0x4A263A;
}
