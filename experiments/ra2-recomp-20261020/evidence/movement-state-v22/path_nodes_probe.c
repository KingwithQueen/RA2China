#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_nodes.h"
#include "native_probe_host.h"
static uint32_t host_stack,guest_stack,entry,context_address;
static __declspec(naked) void original_fragment(void)
{
    __asm {
        pushad
        mov host_stack,esp
        mov ecx,context_address
        mov esi,ecx
        mov esp,guest_stack
        lea eax,returned
        mov [esp],eax
        mov eax,entry
        jmp eax
    returned:
        mov esp,host_stack
        popad
        ret
    }
}
static uint32_t raw_context[96],stack_memory[128];
static unsigned char cells[2][0x148];
static uint32_t references[2];
static Ra2PathLink parent_link;
static Ra2SearchNode parent_node;
static unsigned char *node_pool,*link_pool;
static Ra2PathNodeStorage storage;
static uint32_t stamps[2][64],region_stamps[3][3][17];
static float costs[2][64];
static Ra2PathNodeCache cache;
static Ra2PathRegionCache regions[3];
static Ra2SearchNode *heap_items[2][33];
static Ra2PathHeap heaps[2];
static uint32_t random_value=12345;
static uint32_t random_u32(void){random_value=random_value*1664525u+1013904223u;return random_value;}
static float from_bits(uint32_t n){float f;memcpy(&f,&n,4);return f;}
static void initialize(void)
{
    node_pool=calloc(1,0x100004);link_pool=calloc(1,0x180004);
    if(!node_pool || !link_pool)exit(2);
    storage.nodes=(Ra2SearchNode *)node_pool;storage.used_nodes=(uint32_t *)(node_pool+0x100000);
    storage.links=(Ra2PathLink *)link_pool;storage.used_links=(uint32_t *)(link_pool+0x180000);
    raw_context[0x10/4]=(uint32_t)(uintptr_t)node_pool;raw_context[0x0C/4]=(uint32_t)(uintptr_t)link_pool;
    raw_context[0x14/4]=(uint32_t)(uintptr_t)&heaps[0];raw_context[0x68/4]=(uint32_t)(uintptr_t)&heaps[1];
    raw_context[0x18/4]=(uint32_t)(uintptr_t)stamps[0];raw_context[0x1C/4]=(uint32_t)(uintptr_t)stamps[1];
    raw_context[0x24/4]=(uint32_t)(uintptr_t)costs[0];raw_context[0x20/4]=(uint32_t)(uintptr_t)costs[1];
    cache.lower.stamps=stamps[0];cache.lower.costs=costs[0];cache.upper.stamps=stamps[1];cache.upper.costs=costs[1];cache.generation=&raw_context[0x28/4];
    for(unsigned g=0;g<3;++g)for(unsigned side=0;side<3;++side) {
        raw_context[0x40/4+side*3+g]=(uint32_t)(uintptr_t)region_stamps[g][side];
        regions[g].stamps[side]=region_stamps[g][side];
    }
    references[0]=(uint32_t)(uintptr_t)cells[0];references[1]=(uint32_t)(uintptr_t)cells[1];
    guest_stack=(uint32_t)(uintptr_t)(stack_memory+32);context_address=(uint32_t)(uintptr_t)raw_context;
}
static int test_nodes(void)
{
    uint32_t *frame=stack_memory+32;const uint16_t pc[]={0x7F,0x27F,0x37F};unsigned cases=0;
    const unsigned char stop[]={0x83,0xC4,0x10,0xC3};memcpy((void *)0x427E2A,stop,sizeof(stop));
    for(unsigned n=0;n<8192;++n)for(unsigned p=0;p<3;++p)for(unsigned rc=0;rc<4;++rc) {
        uint32_t bits=random_u32();uint16_t control=(uint16_t)(pc[p]|(rc<<10)),saved;
        Ra2PathNodeInput input={0};input.parent=n%8?&parent_node:NULL;
        input.cell_reference=references;input.cell_level=(int32_t)(bits%16)-4;input.parent_cell_level=(int32_t)((bits>>4)%16)-4;
        input.root_surface_level=(int32_t)((bits>>8)%16)-4;input.cell_has_bridge=(n>>1)&1;input.parent_cell_has_bridge=(n>>2)&1;
        parent_link.cell_reference=&references[1];parent_link.surface_level=(int32_t)((bits>>12)%24)-4;
        parent_node.path_link=&parent_link;parent_node.accumulated_cost=from_bits(0x3E800000u+bits%0x06000000u);
        parent_node.path_length=n%31?((int32_t)(bits%1000)):-1;
        input.step_cost=from_bits(0x38800000u+(bits>>2)%0x06000000u);
        cells[0][0x11B]=(uint8_t)input.cell_level;cells[1][0x11B]=(uint8_t)input.parent_cell_level;
        *(uint32_t *)(cells[0]+0x140)=input.cell_has_bridge?0x100:0;*(uint32_t *)(cells[1]+0x140)=input.parent_cell_has_bridge?0x100:0;
        raw_context[0x30/4]=(uint32_t)input.root_surface_level;
        uint32_t ni=n%128,li=(n*3)%128;*storage.used_nodes=ni;*storage.used_links=li;
        memset(&storage.nodes[ni],0xA5,16);memset(&storage.links[li],0xA5,12);
        frame[1]=(uint32_t)(uintptr_t)input.parent;frame[2]=(uint32_t)(uintptr_t)input.cell_reference;
        memcpy(&frame[4],&input.step_cost,4);entry=0x427D40;
        __asm {
            fnstcw saved
            fldcw control
        }
        original_fragment();
        __asm { fldcw saved }
        Ra2SearchNode expected_node=storage.nodes[ni];Ra2PathLink expected_link=storage.links[li];
        if(*storage.used_nodes!=ni+1 || *storage.used_links!=li+1)return 1;
        *storage.used_nodes=ni;*storage.used_links=li;memset(&storage.nodes[ni],0xA5,16);memset(&storage.links[li],0xA5,12);
        Ra2SearchNode *actual=ra2_path_node_create(&storage,&input,control);
        if(actual!=&storage.nodes[ni] || memcmp(actual,&expected_node,16) || memcmp(&storage.links[li],&expected_link,12)) {
            printf("node mismatch n=%u control=%x level=%d/%d cost=%g/%g length=%d/%d\n",n,control,storage.links[li].surface_level,expected_link.surface_level,(double)actual->accumulated_cost,(double)expected_node.accumulated_cost,actual->path_length,expected_node.path_length);return 1;
        }
        ++cases;
    }
    printf("\"node_cases\":%u,",cases);return 0;
}
static int test_publish(void)
{
    uint32_t *frame=stack_memory+32;*(unsigned char *)0x427A36=0xC3;entry=0x427A02;
    for(unsigned n=0;n<65536;++n) {
        uint32_t bits=random_u32(),cell=n%64,lower=n%2;*cache.generation=bits;
        parent_node.accumulated_cost=from_bits(0x3E800000u+bits%0x06000000u);
        memset(stamps,0xA5,sizeof(stamps));memset(costs,0x5A,sizeof(costs));
        frame[0x24/4]=(uint32_t)(uintptr_t)&parent_node;frame[0x2C/4]=cell*4;frame[0x60/4]=lower;
        original_fragment();uint32_t expected_stamps[2][64];float expected_costs[2][64];
        memcpy(expected_stamps,stamps,sizeof(stamps));memcpy(expected_costs,costs,sizeof(costs));
        memset(stamps,0xA5,sizeof(stamps));memset(costs,0x5A,sizeof(costs));ra2_path_cache_publish(&cache,cell,lower,parent_node.accumulated_cost);
        if(memcmp(expected_stamps,stamps,sizeof(stamps)) || memcmp(expected_costs,costs,sizeof(costs))){printf("publish mismatch n=%u\n",n);return 1;}
        if(ra2_path_cache_read_stamp(&cache,cell,lower)!=bits || ra2_path_cache_read_cost(&cache,cell,lower)!=parent_node.accumulated_cost)return 1;
    }
    printf("\"publish_cases\":65536,");return 0;
}
static void reset_setup(unsigned n,uint32_t generation)
{
    *storage.used_nodes=n%128;*storage.used_links=(n*3)%128;*cache.generation=generation;
    memset(stamps,0xA5,sizeof(stamps));memset(costs,0x5A,sizeof(costs));memset(region_stamps,0x3C,sizeof(region_stamps));
    for(unsigned h=0;h<2;++h) {
        heaps[h].count=(n+h)%17;heaps[h].capacity=33;heaps[h].items=heap_items[h];
        heaps[h].highest_node_address=0xFFFF;heaps[h].lowest_node_address=0x1234;
        for(unsigned i=0;i<33;++i)heap_items[h][i]=&parent_node;
    }
    for(unsigned g=0;g<3;++g) {
        regions[g].count=(n+g)%17;*(uint32_t *)(0x832550+g*4)=regions[g].count;
    }
    *(uint32_t *)0x84E804=n%9;
}
static int test_reset(void)
{
    unsigned cases=0;entry=0x427E90;
    for(unsigned n=0;n<4096;++n)for(unsigned mode=0;mode<4;++mode) {
        uint32_t generation=mode==0?UINT32_MAX:mode==1?0:mode==2?UINT32_MAX-1:n;
        reset_setup(n,generation);original_fragment();
        uint32_t expected_generation=*cache.generation,expected_stamps[2][64],expected_regions[3][3][17];Ra2SearchNode *expected_items[2][33];
        memcpy(expected_stamps,stamps,sizeof(stamps));memcpy(expected_regions,region_stamps,sizeof(region_stamps));memcpy(expected_items,heap_items,sizeof(heap_items));
        if(*storage.used_nodes || *storage.used_links || heaps[0].count || heaps[1].count)return 1;
        reset_setup(n,generation);ra2_path_search_reset(&storage,&heaps[0],&heaps[1],&cache,(n%9)*(n%9),regions);
        if(*cache.generation!=expected_generation || memcmp(stamps,expected_stamps,sizeof(stamps)) || memcmp(region_stamps,expected_regions,sizeof(region_stamps)) || memcmp(heap_items,expected_items,sizeof(heap_items)) || *storage.used_nodes || *storage.used_links || heaps[0].count || heaps[1].count) {
            printf("reset mismatch n=%u generation=%x/%x\n",n,*cache.generation,expected_generation);return 1;
        }
        if(heaps[0].highest_node_address!=0xFFFF || heaps[0].lowest_node_address!=0x1234)return 1;
        for(unsigned side=0;side<2;++side)for(unsigned i=0;i<64;++i)if(memcmp(&costs[side][i],"ZZZZ",4))return 1;
        ++cases;
    }
    printf("\"reset_cases\":%u,",cases);return 0;
}
int main(int argc,char **argv)
{
    if(argc!=2)return 2;hold_image();map_original_image(argv[1]);initialize();
    printf("{");if(test_nodes() || test_publish() || test_reset())return 1;
    printf("\"passed\":true,\"mapped_original_fragments\":true,\"generation_wrap_tested\":true}\n");return 0;
}
