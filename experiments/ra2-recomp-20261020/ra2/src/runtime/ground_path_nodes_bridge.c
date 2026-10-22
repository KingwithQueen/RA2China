#include <stddef.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_path_nodes.h"
#include "ground_path_nodes_bridge.h"
_Static_assert(sizeof(Ra2PathLink)==12 && offsetof(Ra2PathLink,parent)==8,"original x86 link layout");

static Ra2PathNodeStorage storage_view(uint32_t context)
{
    uint32_t nodes=MEM32(context+0x10),links=MEM32(context+0x0C);
    Ra2PathNodeStorage view={(Ra2SearchNode *)(uintptr_t)nodes,(uint32_t *)(uintptr_t)(nodes+0x100000),
        (Ra2PathLink *)(uintptr_t)links,(uint32_t *)(uintptr_t)(links+0x180000)};
    return view;
}
static Ra2PathNodeCache cache_view(uint32_t context)
{
    Ra2PathNodeCache cache={
        {(uint32_t *)(uintptr_t)MEM32(context+0x18),(float *)(uintptr_t)MEM32(context+0x24)},
        {(uint32_t *)(uintptr_t)MEM32(context+0x1C),(float *)(uintptr_t)MEM32(context+0x20)},
        (uint32_t *)(uintptr_t)(context+0x28)};
    return cache;
}

void ra2_path_node_create_bridge(void)
{
    uint32_t stack=g_esp,context=g_ecx,cell_reference=MEM32(stack+8);
    Ra2PathNodeInput input={0};
    input.parent=(Ra2SearchNode *)(uintptr_t)MEM32(stack+4);
    input.cell_reference=(void *)(uintptr_t)cell_reference;
    input.root_surface_level=(int32_t)MEM32(context+0x30);
    memcpy(&input.step_cost,(const void *)(uintptr_t)(stack+16),4);
    if(input.parent) {
        uint32_t cell=MEM32(cell_reference);
        Ra2PathLink *parent=(Ra2PathLink *)input.parent->path_link;
        uint32_t parent_cell=MEM32((uint32_t)(uintptr_t)parent->cell_reference);
        input.cell_level=(int8_t)MEM8(cell+0x11B);
        input.parent_cell_level=(int8_t)MEM8(parent_cell+0x11B);
        input.cell_has_bridge=(MEM32(cell+0x140)&0x100u)!=0;
        input.parent_cell_has_bridge=(MEM32(parent_cell+0x140)&0x100u)!=0;
    }
    Ra2PathNodeStorage storage=storage_view(context);
    Ra2SearchNode *node=ra2_path_node_create(&storage,&input,g_fpu_cw);
    /* 原版构造函数余下的距离近似与尾部仍按旧调用约定运行，保存其四个被调用者寄存器。 */
    MEM32(stack-4)=g_ebx;MEM32(stack-8)=g_ebp;MEM32(stack-12)=g_esi;MEM32(stack-16)=g_edi;
    g_esp=stack-16;
    g_ebx=(uint32_t)(uintptr_t)input.parent;
    g_esi=(uint32_t)(uintptr_t)node;
    g_edi=(uint32_t)(uintptr_t)node->path_link;
}

uint32_t ra2_path_cache_stamp_bridge(uint32_t context,unsigned lower,uint32_t byte_offset)
{
    Ra2PathNodeCache cache=cache_view(context);
    return ra2_path_cache_read_stamp(&cache,byte_offset/4,lower);
}
float ra2_path_cache_cost_bridge(uint32_t context,unsigned lower,uint32_t byte_offset)
{
    Ra2PathNodeCache cache=cache_view(context);
    return ra2_path_cache_read_cost(&cache,byte_offset/4,lower);
}
void ra2_path_cache_publish_bridge(unsigned cost_only)
{
    Ra2PathNodeCache cache=cache_view(g_esi);
    unsigned lower=MEM8(g_esp+0x60)!=0;
    uint32_t cell=(cost_only?g_eax:MEM32(g_esp+0x2C))/4;
    Ra2SearchNode *node=(Ra2SearchNode *)(uintptr_t)MEM32(g_esp+0x24);
    if(cost_only)ra2_path_cache_write_cost(&cache,cell,lower,node->accumulated_cost);
    else ra2_path_cache_publish(&cache,cell,lower,node->accumulated_cost);
}
void ra2_path_search_reset_bridge(void)
{
    uint32_t context=g_ecx,stack=g_esp;
    Ra2PathNodeStorage storage=storage_view(context);
    Ra2PathNodeCache cache=cache_view(context);
    Ra2PathRegionCache regions[3];
    for(unsigned group=0;group<3;++group) {
        regions[group].count=MEM32(0x832550+group*4);
        for(unsigned side=0;side<3;++side)regions[group].stamps[side]=(uint32_t *)(uintptr_t)MEM32(context+0x40+side*12+group*4);
    }
    uint32_t width=MEM32(0x84E804);
    ra2_path_search_reset(&storage,(Ra2PathHeap *)(uintptr_t)MEM32(context+0x14),
        (Ra2PathHeap *)(uintptr_t)MEM32(context+0x68),&cache,width*width,regions);
    g_eax=*cache.generation;
    g_edx=0;
    g_flag_k=FK_ADD;g_flag_a=stack-8;g_flag_b=8;g_flag_cf=stack<8;
    g_esp=stack+4;
}
