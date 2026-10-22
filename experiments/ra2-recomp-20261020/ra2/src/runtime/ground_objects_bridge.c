#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_objects.h"
#include "ground_objects_bridge.h"
#include "state_trace.h"

typedef struct ObjectContext { uint32_t frame,owner,cell,object; } ObjectContext;
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i) { g_esp-=4;MEM32(g_esp)=args[i-1]; }
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if(!fn) fn=recomp_lookup(address);
    if(!fn) fn=recomp_lookup_import(address);
    if(!fn) { fprintf(stderr,"[object-bridge-error] unresolved %08X\n",address);abort(); }
    fn();if(g_esp!=stack) { fprintf(stderr,"[object-bridge-error] unbalanced %08X\n",address);abort(); }
    g_cur_func=caller;return g_eax;
}
static uint32_t virtual_call(uint32_t object,uint32_t slot,const uint32_t *args,unsigned count)
{ return call(MEM32(MEM32(object)+slot),object,args,count); }
static uint32_t building_type(ObjectContext *c) { return MEM32(c->object+0x418); }
static int32_t query(void *opaque,Ra2ObjectPassageQuery which)
{
    ObjectContext *c=opaque;uint32_t argument;
    switch(which)
    {
        case RA2_OBJECT_IS_OWNER: return c->owner==c->object;
        case RA2_OBJECT_RELATED_CELL_MATCHES:
        {
            uint32_t link=MEM32(c->owner+0x588);
            if(!link || !MEM32(link+0x28)) return 0;
            argument=c->frame+0x2C;
            uint32_t first=virtual_call(MEM32(link+0x28),0x1A0,&argument,1);
            argument=c->frame+0x30;
            uint32_t second=virtual_call(c->object,0x1A0,&argument,1);
            return MEM16(first)==MEM16(second) && MEM16(first+2)==MEM16(second+2);
        }
        case RA2_OBJECT_OWNER_ACCEPTS_LINK:
            argument=(MEM8(c->object+0x14)&1) ? c->object : 0;
            return (call(0x636E30,c->owner,&argument,1)&255u)!=0;
        case RA2_OBJECT_KIND: return (int32_t)virtual_call(c->object,0x2C,NULL,0);
        case RA2_OBJECT_BUILDING_OCCUPIES_CELL:
            return (call(0x453AF0,c->object,&c->cell,1)&255u)!=0;
        case RA2_OBJECT_OWNER_PAIR_FLAG_BB0: return MEM8(MEM32(c->owner+0x5AC)+0xBB0);
        case RA2_OBJECT_PAIR_FLAG_BB0: return MEM8(MEM32(c->object+0x5AC)+0xBB0);
        /* 尚未确认下列字段的 INI 名称；仅以已验证的通行行为命名核心查询。 */
        case RA2_OBJECT_BUILDING_FOOTPRINT_TEST: return MEM8(building_type(c)+0x1349);
        case RA2_OBJECT_IS_CELL_BUILDING: return call(0x4717B0,c->cell,NULL,0)==c->object;
        case RA2_OBJECT_BUILDING_IGNORED: return MEM8(building_type(c)+0x1385);
        case RA2_OBJECT_BUILDING_MISSION_PASSAGE: return MEM8(building_type(c)+0x1359);
        case RA2_OBJECT_MISSION_STATE: return (int32_t)MEM32(c->object+0x4EC);
        case RA2_OBJECT_BUILDING_HOUSE_PASSAGE: return MEM8(building_type(c)+0x135A);
        case RA2_OBJECT_HOUSE_FLAG_142: return MEM8(MEM32(c->object+0x1B4)+0x142);
        case RA2_OBJECT_BUILDING_NEIGHBOR_ANCHOR: return MEM8(building_type(c)+0x1214);
        case RA2_OBJECT_MATCHES_NEIGHBOR_BUILDING:
        {
            uint32_t packed=(uint16_t)(MEM16(c->cell+0x24)+MEM16(0x851A78))
                |((uint32_t)(uint16_t)(MEM16(c->cell+0x26)+MEM16(0x851A7A))<<16);
            MEM32(c->frame+0x1C)=packed;MEM32(c->frame+0x20)=packed;
            argument=c->frame+0x20;
            uint32_t cell=call(0x548070,0x8324E0,&argument,1);
            return call(0x4717B0,cell,NULL,0)==c->object;
        }
        case RA2_OBJECT_CLOAKED:
        {
            uint32_t techno=call(0x40DBD0,c->object,NULL,0);
            return techno && MEM32(techno+0x1B8)==2;
        }
        case RA2_OBJECT_OWNER_CRUSHER: return MEM8(MEM32(c->owner+0x5AC)+0xAF3);
        case RA2_OBJECT_CRUSHER_ABILITY:
            argument=17;return (call(0x6D7910,c->owner,&argument,1)&255u)!=0;
        case RA2_OBJECT_CRUSHABLE: return MEM8(virtual_call(c->object,0x84,NULL,0)+0x1FD);
        case RA2_OBJECT_ALLIED:
            return (call(0x4E5580,MEM32(c->owner+0x1B4),&c->object,1)&255u)!=0;
        case RA2_OBJECT_HAS_WEAPON_ZERO:
            argument=0;return MEM32(virtual_call(c->owner,0x39C,&argument,1))!=0;
        case RA2_OBJECT_OWNER_IS_TRAIN: return MEM8(MEM32(c->owner+0x5AC)+0xAA0);
        case RA2_OBJECT_TERRAIN_WEAPON_ALLOWED:
        {
            uint32_t index=virtual_call(c->owner,0x2B8,&c->object,1);
            uint32_t weapon=MEM32(virtual_call(c->owner,0x39C,&index,1));
            if(!weapon || !MEM32(weapon+0xAC)) return 0;
            return MEM8(MEM32(weapon+0xAC)+0x146);
        }
        case RA2_OBJECT_BUILDING_FLAG_1350: return MEM8(building_type(c)+0x1350);
        default: abort();
    }
}
uint32_t ra2_ground_object_branch_bridge(unsigned entry)
{
    ObjectContext c={g_esp,g_ebp,MEM32(g_esp+0x7C),g_esi};
    Ra2ObjectPassageServices services={&c,query};
    Ra2ObjectPassageState state={(int32_t)MEM32(c.frame+0x8C),MEM8(c.frame+0x88)};
    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit(24,c.owner,c.cell,c.object);
    g_esp=c.frame-0x100;
    Ra2ObjectPassageOutcome outcome;
    if(entry==0) outcome=ra2_ground_filter_object(&services);
    else if(entry==1) outcome=ra2_ground_filter_building((int32_t)MEM32(c.frame+0x80),&services);
    else if(entry==2) outcome=ra2_ground_classify_enemy(&state,&services);
    else outcome=ra2_ground_classify_stationary_ally(&state,&services);
    MEM32(c.frame+0x8C)=(uint32_t)state.passage;MEM8(c.frame+0x88)=(uint8_t)state.crush_enemy;
    g_esp=c.frame;g_ebp=c.owner;g_ebx=c.cell;g_esi=c.object;g_edi=(uint32_t)state.passage;
    switch(outcome) {
        case RA2_OBJECT_CLEAR: return 0x7031B1;
        case RA2_OBJECT_CLEAR_OCCUPATION: return 0x703A95;
        case RA2_OBJECT_BLOCKED: return 0x703B5A;
        case RA2_OBJECT_CHECK_GATE: return 0x703536;
        case RA2_OBJECT_SKIP: g_esi=MEM32(c.object+0x30);return 0x7038FD;
        case RA2_OBJECT_SCANNED: return 0x7038EF;
        default: return 0x703693;
    }
}
