#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_path_search.h"
#include "ground_path_search_bridge.h"
typedef struct SearchContext {uint32_t frame,owner,search,target;} SearchContext;
static uint32_t engine_call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if(!fn)fn=recomp_lookup(address);
    if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[path-search-bridge] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[path-search-bridge] unbalanced %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static void sync_frame(SearchContext *c,const Ra2PathSearch *s)
{
    uint32_t f=c->frame;
    MEM32(f+0x14)=(uint32_t)(uintptr_t)s->current;MEM32(f+0x18)=s->direction;
    MEM32(f+0x1C)=(uint32_t)(uintptr_t)s->pending;
    MEM32(f+0x20)=(uint32_t)s->current_cell;MEM32(f+0x24)=(uint32_t)s->candidate_cell;
    MEM32(f+0x28)=s->expanded;MEM32(f+0x2C)=s->candidate_grid_index*4;
    MEM32(f+0x30)=s->candidate_cell?MEM32((uint32_t)s->candidate_cell)+0x24:0;
    memcpy((void *)(uintptr_t)(f+0x34),&s->step_cost,4);MEM32(f+0x3C)=s->current_grid_index;
    MEM32(f+0x4C)=(uint32_t)s->candidate_region;MEM8(f+0x60)=(uint8_t)s->lower_surface;
}
static uintptr_t neighbor(void *opaque,uintptr_t current,unsigned direction)
{
    (void)opaque;uint32_t reference=(uint32_t)current;
    if(direction!=8)return reference+MEM32(0x79C484+direction*4)*4;
    int32_t connection=(int16_t)MEM16(MEM32(reference)+0x116);
    if(connection==-1)return 0x84E808;
    uint32_t object=MEM32(MEM32(0x8661CC)+(uint32_t)connection*4);
    int32_t x=(int16_t)MEM16(object+0x28),y=(int16_t)MEM16(object+0x2A);
    return MEM32(0x832618)+((uint32_t)y*512+(uint32_t)x)*4;
}
static int cell(void *opaque,uintptr_t reference,Ra2PathCell *result)
{
    (void)opaque;uint32_t address=MEM32((uint32_t)reference);if(!address)return 0;
    memcpy(&result->point,(const void *)(uintptr_t)(address+0x24),4);
    result->ground_level=(int8_t)MEM8(address+0x11B);
    result->has_bridge=(MEM32(address+0x140)&0x100u)!=0;result->has_region_connection=MEM8(address+0x122);
    return 1;
}
static int32_t neighbor_offset(void *opaque,unsigned direction)
{(void)opaque;return (int32_t)MEM32(0x84C838+direction*4);}
static int32_t region(void *opaque,const Ra2PathSearch *s)
{
    SearchContext *c=opaque;sync_frame(c,s);
    uint32_t point=MEM32((uint32_t)s->candidate_cell)+0x24;
    uint32_t index=engine_call(0x54FAB0,0x8324E0,&point,1);
    return (int16_t)MEM16(MEM32(0x83254C)+index*10);
}
static int32_t passage(void *opaque,const Ra2PathSearch *s)
{
    SearchContext *c=opaque;sync_frame(c,s);
    uint32_t args[]={MEM32((uint32_t)s->candidate_cell),s->direction,(uint32_t)*s->current_level,
        MEM32((uint32_t)s->current_cell),*s->movement_mode};
    return (int32_t)engine_call(MEM32(MEM32(c->owner)+0x194),c->owner,args,5);
}
static double traversal(void *opaque,const Ra2PathSearch *s,int32_t pass)
{
    SearchContext *c=opaque;sync_frame(c,s);
    uint32_t args[]={(uint32_t)s->current_cell,(uint32_t)s->candidate_cell,!s->lower_surface,(uint32_t)pass,c->owner};
    engine_call(0x427110,c->search,args,5);
    int top=g_fp_top;double cost=fp_pop_impl(g_st,&top);g_fp_top=top;return cost;
}
static Ra2SearchNode *create_node(void *opaque,const Ra2PathSearch *s)
{
    SearchContext *c=opaque;sync_frame(c,s);uint32_t cost;memcpy(&cost,&s->step_cost,4);
    uint32_t args[]={(uint32_t)(uintptr_t)s->current,(uint32_t)s->candidate_cell,c->target,cost};
    return (Ra2SearchNode *)(uintptr_t)engine_call(0x427D40,c->search,args,4);
}
int ra2_path_region_allows_bridge(void)
{
    return ra2_path_region_allows(MEM32(MEM32(g_esp+0x40)+g_ecx*4),MEM32(g_esi+0x28),
        MEM8(g_esp+0x60),MEM8(g_ebx+0x122),MEM8(g_esp+0x74));
}
void ra2_path_search_neighbors_bridge(void)
{
    SearchContext c={g_esp,MEM32(g_esp+0x68),g_esi,MEM32(g_esp+0x64)};
    Ra2PathSearch s={0};uint32_t context=c.search,f=c.frame;
    s.current=(Ra2SearchNode *)(uintptr_t)MEM32(f+0x14);s.expanded=MEM32(f+0x28);
    s.expansion_limit=(int32_t)MEM32(f+0x70);s.destination=MEM32(f+0x38);
    s.ignore_soft_obstacles=MEM8(f+0x12);s.continue_at_blocked_goal=MEM8(f+0x13);s.restrict_to_connected_regions=MEM8(f+0x74);
    s.current_level=(int32_t *)(uintptr_t)(context+0x30);s.destination_level=(int32_t *)(uintptr_t)(context+0x34);
    s.search_weight=(float *)(uintptr_t)(context+4);s.movement_mode=(uint8_t *)(uintptr_t)(context+8);
    s.region_cursor=(uint32_t *)(uintptr_t)(context+0x6C);s.last_region_point=(uint32_t *)(uintptr_t)(context+0x70);
    s.region_route=(uint16_t *)(uintptr_t)(context+0xBE);s.connected_regions=(uint32_t *)(uintptr_t)MEM32(f+0x40);
    s.cache.lower.stamps=(uint32_t *)(uintptr_t)MEM32(context+0x18);s.cache.lower.costs=(float *)(uintptr_t)MEM32(context+0x24);
    s.cache.upper.stamps=(uint32_t *)(uintptr_t)MEM32(context+0x1C);s.cache.upper.costs=(float *)(uintptr_t)MEM32(context+0x20);
    s.cache.generation=(uint32_t *)(uintptr_t)(context+0x28);s.open=(Ra2PathHeap *)(uintptr_t)MEM32(context+0x14);
    s.grid_width=MEM32(0x84E804);memcpy(&s.cache_epsilon,(const void *)0x79C4D0,8);
    s.direction_bias=(float *)0x7CF0DC;s.numeric_control=g_fpu_cw;
    Ra2PathSearchServices v={&c,neighbor,cell,neighbor_offset,region,passage,traversal,create_node};
    /* 引擎服务仍使用原来的调用约定；独立调用栈避免覆盖被接管的局部帧。 */
    g_esp=f-0x100;ra2_path_search_neighbors(&s,&v);sync_frame(&c,&s);
    g_esp=f;g_esi=context;
}
