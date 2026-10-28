#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_techno_cleanup.h"
#include "combat_techno_cleanup_bridge.h"

typedef struct TechnoCleanupContext { uint32_t owner; } TechnoCleanupContext;
static const uint32_t member_offsets[] = {0x408, 0x230, 0x238, 0x208};

static void reset_tables(void *opaque)
{
    TechnoCleanupContext *c = opaque;
    /* 第一个成员先读入 ECX，再切换四张虚表；原函数的保存帧保留在调用处。 */
    g_ecx = MEM32(c->owner + 0x408);
    MEM32(c->owner) = 0x7ACB80; MEM32(c->owner + 4) = 0x7ACB64;
    MEM32(c->owner + 8) = 0x7ACB5C; MEM32(c->owner + 12) = 0x7ACB54;
}

static int32_t has_member(void *opaque, uint32_t member)
{
    TechnoCleanupContext *c = opaque;
    if (member) g_ecx = MEM32(c->owner + member_offsets[member]);
    g_flag_k = FK_CMP; g_flag_a = g_ecx; g_flag_b = g_ebx; g_flag_cf = g_ecx < g_ebx;
    return g_ecx != g_ebx;
}

static void cleanup_member(void *opaque, uint32_t member)
{
    (void)opaque;
    uint32_t stack = g_esp, caller = g_cur_func, target;
    if (!member) target = 0x6130B0;
    else {
        /* 各成员进入时读取当前虚表；不能提前缓存后续成员或其清理目标。 */
        if (member == 2) { g_edx = MEM32(g_ecx); target = MEM32(g_edx + 0x20); }
        else { g_eax = MEM32(g_ecx); target = MEM32(g_eax + 0x20); }
        g_esp -= 4; MEM32(g_esp) = 1;
    }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[techno cleanup] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack) { fputs("[techno cleanup] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
}

static void clear_member(void *opaque, uint32_t member)
{
    TechnoCleanupContext *c = opaque;
    /* 回调换入原槽的指针也只清槽，不追加一次清理。 */
    MEM32(c->owner + member_offsets[member]) = g_ebx;
}

void ra2_techno_cleanup_prefix_bridge(void)
{
    TechnoCleanupContext c = {g_esi};
    Ra2TechnoCleanupServices s = {&c, reset_tables, has_member, cleanup_member, clear_member};
    ra2_cleanup_techno_prefix(&s);
}
