#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_entry.h"
#include "ground_entry_bridge.h"

typedef struct EntryContext { uint32_t frame,owner,cell,mode,option; } EntryContext;
static uint32_t engine_call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i) { g_esp-=4; MEM32(g_esp)=args[i-1]; }
    g_esp-=4; MEM32(g_esp)=RECOMP_RETADDR; g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if(!fn) fn=recomp_lookup(address);
    if(!fn) fn=recomp_lookup_import(address);
    if(!fn) { fprintf(stderr,"[entry-bridge-error] unresolved %08X\n",address); abort(); }
    fn();
    if(g_esp!=stack) { fprintf(stderr,"[entry-bridge-error] unbalanced %08X\n",address); abort(); }
    g_cur_func=caller; return g_eax;
}
static Ra2CellLink read_link(uint32_t link)
{
    Ra2CellLink result={0};
    if(link) { result.present=1; result.endpoint_x=(int16_t)MEM16(link+0x28); result.endpoint_y=(int16_t)MEM16(link+0x2A); result.direction=(int32_t)MEM32(link+0x2C); }
    return result;
}
static Ra2CellLink neighbor_link(void *opaque,int32_t direction)
{
    EntryContext *c=opaque; uint32_t arg=(uint32_t)direction;
    uint32_t neighbor=engine_call(0x476AC0,c->cell,&arg,1);
    return read_link(engine_call(0x47A130,neighbor,NULL,0));
}
static void write_state(EntryContext *c,const Ra2EntryState *s)
{
    MEM32(c->frame+0x84)=(uint32_t)s->reference_level;
    MEM8(c->frame+0x11)=s->alternate_layer;
    MEM8(c->frame+0x12)=s->occupation_flags; MEM8(c->frame+0x13)=s->vehicle_present;
    MEM32(c->frame+0x18)=(uint32_t)s->infantry_owner;
}
static int32_t check_placement(void *opaque,Ra2EntryState *s)
{
    EntryContext *c=opaque; write_state(c,s);
    uint32_t args[]={c->cell,(uint32_t)s->direction,c->frame+0x84,c->frame+0x11,c->mode};
    int32_t result=(int32_t)engine_call(MEM32(MEM32(c->owner)+0x198),c->owner,args,5);
    s->reference_level=(int32_t)MEM32(c->frame+0x84); s->alternate_layer=MEM8(c->frame+0x11);
    return result;
}
static int32_t query(void *opaque,Ra2EntryQuery which)
{
    EntryContext *c=opaque;
    switch(which)
    {
        case RA2_ENTRY_HAS_BRIDGE: return (MEM32(c->cell+0x140)&0x100)!=0;
        case RA2_ENTRY_CELL_LEVEL: return (int8_t)MEM8(c->cell+0x11B);
        case RA2_ENTRY_UPPER_FLAGS: return MEM8(c->cell+0x128);
        case RA2_ENTRY_UPPER_INFANTRY_OWNER: return (int32_t)MEM32(c->cell+0x58);
        case RA2_ENTRY_GLOBAL_VISIBILITY_OVERRIDE: return MEM32(0xA40774)!=0;
        case RA2_ENTRY_CELL_VISIBLE:
        {
            uint32_t args[]={c->cell,1}; return (engine_call(0x55A740,0x8324E0,args,2)&255u)!=0;
        }
        case RA2_ENTRY_OWNER_VISIBILITY_EXEMPT: return (engine_call(MEM32(MEM32(c->owner)+0x2F4),c->owner,NULL,0)&255u)!=0;
        case RA2_ENTRY_OWNER_FLAG_32D: return MEM8(c->owner+0x32D);
        default: abort();
    }
}
static int32_t base_passage(void *opaque,Ra2EntryState *s)
{
    EntryContext *c=opaque; write_state(c,s);
    uint32_t args[]={c->cell,(uint32_t)s->direction,(uint32_t)s->reference_level,c->mode,c->option};
    int32_t result=(int32_t)engine_call(0x4C86E0,c->owner,args,5);
    MEM32(c->frame+0x8C)=(uint32_t)result;
    return result;
}
uint32_t ra2_ground_entry_bridge(void)
{
    EntryContext c={g_esp,g_ebp,g_ebx,MEM32(g_esp+0x88),MEM32(g_esp+0x8C)};
    Ra2EntryState state={(int32_t)MEM32(c.frame+0x80),(int32_t)MEM32(c.frame+0x84),
        (int32_t)MEM32(c.frame+0x18),0,MEM8(c.frame+0x11),MEM8(c.frame+0x12),MEM8(c.frame+0x13)};
    Ra2CellLink link=read_link(g_esi);
    Ra2EntryServices services={&c,neighbor_link,check_placement,query,base_passage};
    g_esp=c.frame-0x100;
    Ra2EntryOutcome outcome=ra2_ground_check_entry(&state,link,&services);
    write_state(&c,&state); g_esp=c.frame; g_ebp=c.owner; g_ebx=c.cell;
    if(outcome==RA2_ENTRY_BLOCKED) return 0x703B5A;
    if(outcome==RA2_ENTRY_CLEAR) return 0x7031B1;
    g_esi=c.mode; g_edi=(uint32_t)state.passage;
    return 0x703331;
}
