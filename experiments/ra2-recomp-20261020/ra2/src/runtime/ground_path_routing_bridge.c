#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_region_search.h"
#include "ground_path_optimize.h"
#include "ground_path_routing_bridge.h"
typedef struct RoutingContext {uint32_t search,owner;} RoutingContext;
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[path-routing] missing %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[path-routing] stack mismatch %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static double factor(void *opaque)
{
    RoutingContext *c=opaque;call(0x4CAFB0,c->owner,NULL,0);
    int top=g_fp_top;double value=fp_pop_impl(g_st,&top);g_fp_top=top;return value;
}
static uint32_t house(void *opaque){RoutingContext *c=opaque;return MEM32(c->owner+0x1B4);}
static int32_t region_at(void *opaque,const Ra2PathPoint *point,unsigned layer)
{
    (void)opaque;uint32_t arg=(uint32_t)(uintptr_t)point;
    uint32_t index=call(0x54FAB0,0x8324E0,&arg,1);
    return (int16_t)MEM16(MEM32(0x83254C)+index*10+layer*2);
}
static Ra2RegionView region(void *opaque,unsigned layer,uint32_t id)
{
    (void)opaque;uint32_t p=MEM32(0x83256C+layer*24)+id*36;
    return (Ra2RegionView){(Ra2RegionEdge *)(uintptr_t)MEM32(p+4),(int32_t)MEM32(p+0x10),MEM16(p+0x18),MEM32(p+0x1C)};
}
static int32_t penalty(void *opaque,uint32_t owner_house,unsigned layer,uint32_t from,uint32_t to)
{(void)opaque;uint32_t args[]={owner_house,layer,from,to};return (int32_t)call(0x567D20,0x8324E0,args,4);}
static Ra2BlockedRegionEdges blocked_edges(void *opaque,unsigned layer)
{RoutingContext *c=opaque;uint32_t p=c->search+layer*24;return (Ra2BlockedRegionEdges){(uint32_t *)(uintptr_t)MEM32(p+0x78),(int32_t)MEM32(p+0x84)};}
void ra2_region_search_bridge(void)
{
    uint32_t stack=g_esp,b=g_ebx,p=g_ebp,i=g_esi,d=g_edi;
    RoutingContext c={g_ecx,MEM32(stack+16)};Ra2RegionSearch s={0};
    s.generation=(uint32_t *)(uintptr_t)(c.search+0x28);s.nodes=(Ra2RegionRouteNode *)(uintptr_t)MEM32(c.search+0x64);
    s.heap=(Ra2RegionHeap *)(uintptr_t)MEM32(c.search+0x68);s.terrain_allowed=(int32_t *)(uintptr_t)(0x7E00C4+MEM32(stack+12)*32);
    s.terrain_cost=(float *)0x79C4A4;s.numeric_control=&g_fpu_cw;s.integer_conversion_control=(uint16_t)MEM32(0x7D8964);
    for(unsigned layer=0;layer<3;++layer)s.layers[layer]=(Ra2RegionLayer){
        (uint32_t *)(uintptr_t)MEM32(c.search+0x40+layer*4),(uint32_t *)(uintptr_t)MEM32(c.search+0x4C+layer*4),
        (float *)(uintptr_t)MEM32(c.search+0x58+layer*4),(uint16_t *)(uintptr_t)(c.search+0xBC+layer*1000),(uint32_t *)(uintptr_t)(c.search+0xC74+layer*4)};
    Ra2RegionSearchServices v={&c,factor,house,region_at,region,penalty,blocked_edges};
    g_esp=stack-0x100;int success=ra2_region_search(&s,&v,(Ra2PathPoint *)(uintptr_t)MEM32(stack+4),(Ra2PathPoint *)(uintptr_t)MEM32(stack+8),c.owner!=0);
    g_eax=(uint32_t)success;g_esp=stack+20;g_ebx=b;g_ebp=p;g_esi=i;g_edi=d;
}
static Ra2PathPoint connection_exit(void *opaque,const Ra2PathPoint *point)
{
    (void)opaque;uint32_t arg=(uint32_t)(uintptr_t)point;
    uint32_t cell=call(0x548070,0x8324E0,&arg,1);int32_t id=(int16_t)MEM16(cell+0x116);
    Ra2PathPoint result={0,0};
    if(id!=-1)memcpy(&result,(void *)(uintptr_t)(MEM32(MEM32(0x8661CC)+(uint32_t)id*4)+0x28),4);
    return result;
}
static int32_t shorten_turn(void *opaque,int32_t *directions,int32_t *levels,int32_t first_count,int32_t second_count,Ra2PathPoint *anchor)
{
    RoutingContext *c=opaque;uint32_t args[]={c->owner,(uint32_t)(uintptr_t)directions,(uint32_t)(uintptr_t)levels,
        (uint32_t)first_count,(uint32_t)second_count,(uint32_t)(uintptr_t)anchor};
    return (int32_t)call(0x428CF0,c->search,args,6);
}
static void find_anchor(void *opaque,int32_t *directions,int32_t end,int32_t start,int32_t *index,Ra2PathPoint *anchor)
{
    RoutingContext *c=opaque;uint32_t args[]={(uint32_t)(uintptr_t)directions,(uint32_t)end,(uint32_t)start,
        (uint32_t)(uintptr_t)index,(uint32_t)(uintptr_t)anchor};call(0x429570,c->search,args,5);
}
static void rewrite_segment(void *opaque,int32_t *directions,int32_t count,Ra2PathPoint *anchor,Ra2PathPoint *delta,int32_t level,int final_segment)
{
    RoutingContext *c=opaque;uint32_t args[]={(uint32_t)(uintptr_t)directions,(uint32_t)count,(uint32_t)(uintptr_t)anchor,
        (uint32_t)(uintptr_t)delta,c->owner,(uint32_t)level,(uint32_t)final_segment};call(0x4296F0,c->search,args,7);
}
static void optimize(void (*function)(Ra2RebuiltPath *,const Ra2PathOptimizationServices *))
{
    uint32_t stack=g_esp,b=g_ebx,p=g_ebp,i=g_esi,d=g_edi;
    RoutingContext c={g_ecx,MEM32(stack+8)};
    Ra2PathOptimizationServices v={&c,(Ra2PathPoint *)0x851A70,connection_exit,shorten_turn,find_anchor,rewrite_segment};
    g_esp=stack-0x100;function((Ra2RebuiltPath *)(uintptr_t)MEM32(stack+4),&v);
    g_esp=stack+12;g_ebx=b;g_ebp=p;g_esi=i;g_edi=d;
}
void ra2_path_smooth_bridge(void){optimize(ra2_path_smooth);}
void ra2_path_postprocess_bridge(void){optimize(ra2_path_postprocess);}
