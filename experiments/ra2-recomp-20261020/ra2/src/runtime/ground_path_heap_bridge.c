#include <stddef.h>
#include "recomp_types.h"
#include "ground_path_heap.h"
#include "ground_path_heap_bridge.h"
_Static_assert(sizeof(Ra2SearchNode)==16,"original x86 node layout");
_Static_assert(sizeof(Ra2PathHeap)==20 && offsetof(Ra2PathHeap,items)==8,"original x86 heap layout");

void ra2_path_heap_offer_bridge(void)
{
    Ra2PathHeap *heap=(Ra2PathHeap *)(uintptr_t)MEM32(g_esi+0x14);
    Ra2SearchNode *pending=(Ra2SearchNode *)(uintptr_t)MEM32(g_esp+0x1C);
    Ra2SearchNode *candidate=(Ra2SearchNode *)(uintptr_t)g_ebx;
    MEM32(g_esp+0x24)=g_ebx;
    MEM32(g_esp+0x1C)=(uint32_t)(uintptr_t)ra2_path_heap_offer(heap,pending,candidate);
}

void ra2_path_heap_take_bridge(void)
{
    Ra2PathHeap *heap=(Ra2PathHeap *)(uintptr_t)MEM32(g_esi+0x14);
    Ra2SearchNode *pending=(Ra2SearchNode *)(uintptr_t)MEM32(g_esp+0x1C);
    MEM32(g_esp+0x14)=(uint32_t)(uintptr_t)ra2_path_heap_take(heap,pending);
}

void ra2_path_heap_offer_tail_bridge(void)
{
    ra2_path_heap_finish_offer((Ra2PathHeap *)(uintptr_t)g_edi,
        (Ra2SearchNode *)(uintptr_t)MEM32(g_esp+0x1C),g_ecx);
    MEM32(g_esp+0x1C)=g_ebx;
}

void ra2_path_heap_take_tail_bridge(unsigned replacing_root)
{
    uint32_t heap=replacing_root?g_edx:g_ecx;
    uint32_t child=replacing_root?g_ecx:g_edx;
    ra2_path_heap_swap_and_sift((Ra2PathHeap *)(uintptr_t)heap,g_ebx,child);
    MEM32(g_esp+0x14)=MEM32(g_esp+0x4C);
}
