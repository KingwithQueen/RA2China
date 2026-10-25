#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_heap.h"
#include "native_probe_host.h"
static uint32_t host_stack,guest_stack,entry,registers[5];
static __declspec(naked) void original_fragment(void)
{
    __asm {
        pushad
        mov host_stack,esp
        mov esi,registers[0]
        mov ebx,registers[4]
        mov ecx,registers[8]
        mov edx,registers[12]
        mov edi,registers[16]
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
static Ra2SearchNode nodes[130];
static Ra2SearchNode *original_items[128],*c_items[128];
static uint32_t frame[64],context[64];
static Ra2PathHeap original_heap,c_heap;
static uint32_t random_value=12345;
static uint32_t random_u32(void){random_value=random_value*1664525u+1013904223u;return random_value;}
static void setup(uint32_t n)
{
    for(unsigned i=0;i<130;++i)nodes[i].priority=(float)(i/3);
    for(unsigned i=0;i<128;++i)original_items[i]=c_items[i]=&nodes[i];
    uint32_t count=random_u32()%64;
    original_heap.count=c_heap.count=count;
    original_heap.capacity=c_heap.capacity=n%4?128:count+1;
    original_heap.items=original_items;c_heap.items=c_items;
    original_heap.highest_node_address=c_heap.highest_node_address=0;
    original_heap.lowest_node_address=c_heap.lowest_node_address=UINT32_MAX;
    memset(frame,0xA5,sizeof(frame));memset(context,0,sizeof(context));
    context[0x14/4]=(uint32_t)(uintptr_t)&original_heap;
    guest_stack=(uint32_t)(uintptr_t)frame;
    registers[0]=(uint32_t)(uintptr_t)context;
    nodes[128].priority=(float)(int32_t)(random_u32()%80)-10.0f;
    nodes[129].priority=n%5?((float)(random_u32()%40)):nodes[128].priority;
}
static int equal(uint32_t n,const char *operation)
{
    if(original_heap.count!=c_heap.count || original_heap.capacity!=c_heap.capacity
       || original_heap.highest_node_address!=c_heap.highest_node_address
       || original_heap.lowest_node_address!=c_heap.lowest_node_address
       || memcmp(original_items,c_items,sizeof(c_items))) {
        printf("heap mismatch %s case=%u count=%u/%u\n",operation,n,original_heap.count,c_heap.count);return 0;
    }
    return 1;
}
int main(int argc,char **argv)
{
    if(argc!=3)return 2;int improved=atoi(argv[2]);hold_image();map_original_image(argv[1]);
    const unsigned char start[]={0x8B,0x44,0x24,0x1C,0x85,0xC0};
    if(memcmp((void *)0x427914,start,sizeof(start)))return 2;
    *(unsigned char *)0x427A02=0xC3;*(unsigned char *)0x427C96=0xC3;*(unsigned char *)0x427CA6=0xC3;
    unsigned offers=0,takes=0,tails=0,changes=0,sample_count=0;
    struct {uint32_t n,count,capacity;float old_score,new_score;} samples[8];
    for(uint32_t n=0;n<65536;++n) {
        setup(n);
        Ra2SearchNode *best=n%7?&nodes[129]:NULL;
        frame[0x1C/4]=(uint32_t)(uintptr_t)best;
        registers[1]=(uint32_t)(uintptr_t)&nodes[128];entry=0x427914;original_fragment();
        Ra2SearchNode *actual=ra2_path_heap_offer(&c_heap,best,&nodes[128]);
        if(frame[0x1C/4]!=(uint32_t)(uintptr_t)actual){
            if(!improved || !best || c_heap.count+1u<c_heap.capacity || frame[0x1C/4]!=(uint32_t)(uintptr_t)&nodes[128] || actual!=best || !(best->priority<nodes[128].priority)){puts("unexpected offer difference");return 1;}
            if(sample_count<8){samples[sample_count].n=n;samples[sample_count].count=c_heap.count;samples[sample_count].capacity=c_heap.capacity;samples[sample_count].old_score=nodes[128].priority;samples[sample_count].new_score=best->priority;++sample_count;}
            ++changes;
        }
        if(!equal(n,"offer"))return 1;
        ++offers;
        setup(n);best=n%3?&nodes[128]:NULL;
        frame[0x1C/4]=(uint32_t)(uintptr_t)best;entry=0x427A90;original_fragment();
        actual=ra2_path_heap_take(&c_heap,best);
        if(frame[0x14/4]!=(uint32_t)(uintptr_t)actual){printf("take return mismatch case=%u expected=%x actual=%p best=%p\n",n,frame[0x14/4],(void *)actual,(void *)best);return 1;}
        if(!equal(n,"take"))return 1;
        ++takes;
        if(original_heap.count>=3)for(unsigned branch=0;branch<2;++branch) {
            setup(n);original_heap.count=c_heap.count=63;
            registers[1]=1;registers[2]=branch?2:(uint32_t)(uintptr_t)&original_heap;
            registers[3]=branch?(uint32_t)(uintptr_t)&original_heap:2;
            frame[0x4C/4]=(uint32_t)(uintptr_t)&nodes[129];entry=branch?0x427B1F:0x427C22;original_fragment();
            ra2_path_heap_swap_and_sift(&c_heap,1,2);
            if(frame[0x14/4]!=(uint32_t)(uintptr_t)&nodes[129] || !equal(n,"shared-tail"))return 1;
            ++tails;
        }
    }
    if(improved && !changes)return 1;
    printf("{\"passed\":true,\"offer_cases\":%u,\"take_cases\":%u,\"tail_cases\":%u,\"intentional_capacity_changes\":%u,\"unexpected_differences\":0,\"mapped_original_fragments\":true,\"finite_scores\":true,\"samples\":[",offers,takes,tails,changes);
    for(unsigned i=0;i<sample_count;++i)printf("%s{\"case\":%u,\"count\":%u,\"capacity\":%u,\"original_selected_priority\":%g,\"new_selected_priority\":%g}",i?",":"",samples[i].n,samples[i].count,samples[i].capacity,(double)samples[i].old_score,(double)samples[i].new_score);
    puts("]}");return 0;
}
