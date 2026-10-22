#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_continuation.h"
#include "ground_continuation_bridge.h"
#include "state_trace.h"

typedef struct ContinuationContext
{
    uint32_t drive,frame,selected_header;
    Ra2ContinuationState state;
} ContinuationContext;
static uint32_t owner(ContinuationContext *c) { return MEM32(c->drive+0xC); }
static Ra2WorldPoint point(uint32_t address)
{ Ra2WorldPoint value;memcpy(&value,(const void *)(uintptr_t)ADDR(address),sizeof(value));return value; }
static void put_point(uint32_t address,Ra2WorldPoint value)
{ memcpy((void *)(uintptr_t)ADDR(address),&value,sizeof(value)); }
static void read_state(ContinuationContext *c)
{
    c->state.segment_end=point(c->drive+0x40); c->state.candidate=point(c->frame+0x18);
    c->state.selector=(int32_t)MEM32(c->drive+0x58); c->state.sample_index=(int32_t)MEM32(c->drive+0x5C);
    c->state.alternate_template=MEM8(c->drive+0x60); c->state.driving=MEM8(c->drive+0x63);
    c->state.orientation_mismatch=MEM8(c->frame+0x13);
}
static void write_state(ContinuationContext *c)
{
    put_point(c->drive+0x40,c->state.segment_end);put_point(c->frame+0x18,c->state.candidate);
    MEM32(c->drive+0x58)=(uint32_t)c->state.selector;MEM32(c->drive+0x5C)=(uint32_t)c->state.sample_index;
    MEM8(c->drive+0x60)=(uint8_t)c->state.alternate_template;MEM8(c->drive+0x63)=(uint8_t)c->state.driving;
    MEM8(c->frame+0x13)=(uint8_t)c->state.orientation_mismatch;
}
static uint32_t call(ContinuationContext *c,uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;write_state(c);
    for(unsigned i=count;i;--i) { g_esp-=4;MEM32(g_esp)=args[i-1]; }
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if(!fn) fn=recomp_lookup(address);
    if(!fn) fn=recomp_lookup_import(address);
    if(!fn) { fprintf(stderr,"[continuation-bridge-error] unresolved %08X\n",address);abort(); }
    fn();if(g_esp!=stack) { fprintf(stderr,"[continuation-bridge-error] unbalanced %08X\n",address);abort(); }
    g_cur_func=caller;uint32_t result=g_eax;read_state(c);return result;
}
static uint32_t owner_call(ContinuationContext *c,uint32_t slot,const uint32_t *args,unsigned count)
{ uint32_t unit=owner(c);return call(c,MEM32(MEM32(unit)+slot),unit,args,count); }
static uint32_t candidate_cell(ContinuationContext *c)
{ uint32_t arg=c->frame+0x18;return call(c,0x548000,0x8324E0,&arg,1); }
static int32_t query(void *opaque,Ra2ContinuationQuery which)
{
    ContinuationContext *c=opaque;uint32_t unit=owner(c);
    switch(which) {
        case RA2_CONTINUATION_TRANSITION_INDEX: return (int32_t)MEM32(0x7A00A4+MEM32(c->frame+0x58));
        case RA2_CONTINUATION_TEMPLATE_HEADING:
        {
            unsigned heading=MEM8(MEM32(c->frame+0xA8)+4);
            MEM16(c->frame+0x6C)=(uint16_t)(heading<<8);return (int32_t)heading;
        }
        case RA2_CONTINUATION_OWNER_KIND: return (int32_t)owner_call(c,0x2C,NULL,0);
        case RA2_CONTINUATION_TYPE_FLAG_BA4: return MEM8(MEM32(unit+0x5AC)+0xBA4);
        case RA2_CONTINUATION_OWNER_ALIVE: return MEM8(unit+0x7D);
        case RA2_CONTINUATION_OWNER_FLAG_76: return MEM8(unit+0x76);
        case RA2_CONTINUATION_OWNER_FLAG_7A: return MEM8(unit+0x7A);
        case RA2_CONTINUATION_CELL_HAS_BRIDGE: return (MEM32(candidate_cell(c)+0x140)&0x100)!=0;
        case RA2_CONTINUATION_CELL_LEVEL: return (int8_t)MEM8(candidate_cell(c)+0x11B);
        case RA2_CONTINUATION_HEIGHT_PER_LEVEL: return (int32_t)MEM32(0x8529D0);
        default: abort();
    }
}
static Ra2ContinuationTemplate find_template(void *opaque,int32_t selector)
{
    ContinuationContext *c=opaque;
    c->selected_header=0x7A0180+(uint32_t)selector*12;
    MEM32(c->frame+0x40)=(uint32_t)selector;
    int32_t kind=(int8_t)MEM8(c->selected_header);
    Ra2ContinuationTemplate result={selector,kind,kind ? (int32_t)MEM32(0x7A00A8+(uint32_t)kind*16) : 0};
    return result;
}
static Ra2WorldPoint offset(void *opaque,int32_t direction)
{
    (void)opaque;uint32_t address=0x851AC0+((uint32_t)direction&7u)*8;
    Ra2WorldPoint result={(int32_t)MEM32(address),(int32_t)MEM32(address+4),0};return result;
}
static uint64_t save_speed(void *opaque)
{
    ContinuationContext *c=opaque;uint64_t value;
    memcpy(&value,(const void *)(uintptr_t)ADDR(owner(c)+0x468),8);
    memcpy((void *)(uintptr_t)ADDR(c->frame+0x74),&value,8);return value;
}
static int32_t passage(void *opaque,Ra2WorldPoint candidate,int32_t direction)
{
    ContinuationContext *c=opaque;(void)candidate;
    uint32_t unit=owner(c),method=MEM32(MEM32(unit)+0x194);
    Ra2WorldPoint value=c->state.candidate;
    uint32_t packed=(uint16_t)(value.x/256)|((uint32_t)(uint16_t)(value.y/256)<<16);
    MEM32(c->frame+0x94)=packed;MEM32(c->frame+0x34)=packed;
    uint32_t level=call(c,0x5D47D0,unit,NULL,0),arg=c->frame+0x34;
    uint32_t cell=call(c,0x548070,0x8324E0,&arg,1);
    uint32_t args[]={cell,(uint32_t)direction,level,0,1};
    return (int32_t)call(c,method,owner(c),args,5);
}
static void classified(void *opaque,int32_t result)
{ ContinuationContext *c=opaque;write_state(c);if((uint32_t)result<=6) ra2_state_movement_audit(21,c->drive,0,(uint32_t)result); }
static void commit(void *opaque,Ra2ContinuationTemplate selected)
{
    ContinuationContext *c=opaque;
    MEM32(c->frame+0xA8)=c->selected_header;
    MEM32(c->frame+0x58)=(uint32_t)selected.sample_kind*16;
    MEM32(c->frame+0x38)=MEM32(0x7A00A0+(uint32_t)selected.sample_kind*16);
}
static void refresh(void *opaque)
{ ContinuationContext *c=opaque;uint32_t arg=2;owner_call(c,0x174,&arg,1); }
static int accepts(void *opaque)
{
    ContinuationContext *c=opaque;uint32_t unit=owner(c);
    uint32_t cell=candidate_cell(c);return (call(c,0x476CC0,cell,&unit,1)&255u)!=0;
}
static void start_segment(void *opaque)
{ ContinuationContext *c=opaque;uint32_t args[]={c->frame+0x18,1};call(c,0x4A0BC0,c->drive,args,2); }
static void restore_speed(void *opaque,uint64_t value)
{ ContinuationContext *c=opaque;uint32_t args[2];memcpy(args,&value,8);owner_call(c,0x4C8,args,2); }
static void shift(void *opaque)
{
    ContinuationContext *c=opaque;uint32_t unit=owner(c);
    for(unsigned i=0;i<23;++i) MEM32(unit+0x4D0+i*4)=MEM32(unit+0x4D4+i*4);
    MEM32(owner(c)+0x52C)=UINT32_MAX;
}
static void reveal(void *opaque)
{ ContinuationContext *c=opaque;call(c,0x478740,candidate_cell(c),NULL,0); }
static void gate(void *opaque)
{
    ContinuationContext *c=opaque;Ra2WorldPoint p=c->state.candidate;
    uint32_t packed=(uint16_t)(p.x/256)|((uint32_t)(uint16_t)(p.y/256)<<16);
    MEM32(c->frame+0x9C)=packed;MEM32(c->frame+0x40)=packed;
    uint32_t args[]={owner(c),c->frame+0x40};call(c,0x55ACD0,0x8324E0,args,2);
}
static Ra2WorldPoint raw_position(void *opaque)
{
    ContinuationContext *c=opaque;Ra2WorldPoint raw=point(owner(c)+0x88);
    MEM32(c->frame+0x5C)=(uint32_t)raw.x;MEM32(c->frame+0x60)=(uint32_t)raw.y;return raw;
}
static void notify(void *opaque,int bridge_layer)
{
    ContinuationContext *c=opaque;MEM8(c->frame+0x14)=(uint8_t)bridge_layer;
    uint32_t arg=c->drive+0x40,cell=call(c,0x548000,0x8324E0,&arg,1);
    uint32_t args[]={0x852998,1,1,MEM32(c->frame+0x14)};
    call(c,0x476920,cell,args,4);
}
uint32_t ra2_ground_continue_turn_bridge(void)
{
    ContinuationContext c={g_ebp,g_esp,0,{0}};read_state(&c);
    int32_t direction=(int32_t)MEM32(c.frame+0x44);
    Ra2ContinuationServices services={&c,query,find_template,offset,save_speed,passage,classified,commit,
        refresh,accepts,start_segment,restore_speed,shift,reveal,gate,raw_position,notify};
    g_esp=c.frame-0x100;
    int proceed=ra2_ground_continue_turn(&c.state,point(0x852998),direction,&services);
    write_state(&c);g_esp=c.frame;g_ebp=c.drive;
    return proceed ? 0x4A1F8D : 0x4A263A;
}
