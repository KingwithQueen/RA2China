#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_completion.h"
#include "ground_passage.h"
#include "ground_arrival_bridge.h"
#include "ground_completion_bridge.h"

typedef struct CompletionContext
{
    uint32_t frame, drive, anchor, timer, cookie, delay;
    unsigned entry;
} CompletionContext;

static Ra2WorldPoint point(uint32_t a)
{ Ra2WorldPoint p; memcpy(&p, (void *)(uintptr_t)ADDR(a), sizeof(p)); return p; }
static void store(uint32_t a, Ra2WorldPoint p)
{ memcpy((void *)(uintptr_t)ADDR(a), &p, sizeof(p)); }
static uint32_t call(uint32_t address, uint32_t object, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = object;
    recomp_func_t fn = recomp_lookup_manual(address);
    if (!fn) fn = recomp_lookup(address);
    if (!fn) fn = recomp_lookup_import(address);
    if (!fn) { fprintf(stderr, "[ground-completion] unresolved %08X\n", address); abort(); }
    fn();
    if (g_esp != stack) { fprintf(stderr, "[ground-completion] stack %08X\n", address); abort(); }
    g_cur_func = caller;
    return g_eax;
}
static uint32_t owner(CompletionContext *c) { return MEM32(c->drive + 0xC); }
static uint32_t method(uint32_t object, uint32_t slot, const uint32_t *args, unsigned count)
{ return call(MEM32(MEM32(object) + slot), object, args, count); }

uint32_t ra2_ground_arrival_complete_bridge(void)
{
    uint32_t u = MEM32(g_ebp + 0xC);
    Ra2WorldPoint position = point(u + 0x88), end = point(g_ebp + 0x40);
    MEM32(g_esp + 0x64) = (uint32_t)position.z;
    g_eax = (uint32_t)ra2_ground_arrival_adjustment(position, end, g_fpu_cw);
    g_fpu_cw = MEM16(0x7D8964);
    g_ebx = MEM32(g_esp + 0x3C);
    return ra2_ground_finish_segment_bridge();
}

static void clear_segment(void *opaque)
{
    CompletionContext *c = opaque;
    Ra2WorldPoint p = point(c->drive + 0x40), invalid = point(0x852998);
    if (p.x != invalid.x || p.y != invalid.y || p.z != invalid.z)
    { store(c->drive + 0x40, invalid); MEM8(c->drive + 0x63) = 0; }
}
static void clear_driving(void *opaque)
{ CompletionContext *c = opaque; MEM8(c->drive + 0x63) = 0; }
static int has_target(void *opaque)
{ CompletionContext *c = opaque; return MEM32(c->anchor + 0x488) != 0; }
static void cancel_target(void *opaque)
{ CompletionContext *c = opaque; call(0x4CD9B0, c->anchor, NULL, 0); }
static uint32_t stop(void *opaque, int cancelled)
{ CompletionContext *c = opaque; uint32_t args[] = { 0, 1 }; return method(owner(c), cancelled ? 0x414 : 0x410, args, 2); }
static void clear_path(void *opaque)
{ CompletionContext *c = opaque; MEM32((c->entry == 6 ? c->anchor : owner(c)) + 0x4D0) = UINT32_MAX; }
static void start_retry(void *opaque)
{
    CompletionContext *c = opaque; c->timer = owner(c) + 0x530;
    MEM32(c->timer) = MEM32(0xA40D2C); c->cookie = MEM32(c->frame + 0x54); c->delay = 0;
}
static void finish_timer(void *opaque)
{ CompletionContext *c = opaque; MEM32(c->timer + 4) = c->cookie; MEM32(c->timer + 8) = c->delay; }
static uint32_t prepare_again(void *opaque)
{ CompletionContext *c = opaque; uint32_t args[] = { MEM32(c->frame + 0x60), 0, 0 }; return call(0x4A2670, c->drive, args, 3); }

uint32_t ra2_ground_prepare_finish_bridge(unsigned entry)
{
    if (entry == 6 && g_esi != 7) return 0x4A4174;
    CompletionContext c = { g_esp, g_ebp, g_ecx, g_edx, g_eax, g_ecx, entry };
    if (entry == 0 || entry == 2 || entry == 7) c.anchor = owner(&c);
    Ra2PrepareFinishServices s = { &c, clear_segment, clear_driving, has_target, cancel_target,
        stop, clear_path, start_retry, finish_timer, prepare_again };
    g_esp = c.frame - 0x100;
    uint32_t result = ra2_ground_prepare_finish((Ra2PrepareFinishEntry)entry, MEM8(c.frame + 0x64) != 0, &s);
    uint32_t f = c.frame;
    g_eax = result; g_edi = MEM32(f); g_esi = MEM32(f + 4); g_ebp = MEM32(f + 8); g_ebx = MEM32(f + 12);
    g_esp = f + 0x6C; g_flag_k = FK_ADD; g_flag_a = f + 16; g_flag_b = 0x4C; g_flag_cf = f + 0x5C < f + 16;
    return 0;
}

static Ra2PassageCell passage_cell(uint32_t a)
{ return (Ra2PassageCell){ (int8_t)MEM8(a + 0x11B), MEM8(a + 0x11C), MEM32(a + 0x140) }; }
static int has_locomotor(void *opaque)
{ CompletionContext *c = opaque; return MEM32(c->anchor + 0x564) != 0; }
static int32_t locomotor_can_enter(void *opaque)
{
    CompletionContext *c = opaque;
    uint32_t packed = MEM32(MEM32(c->frame + 4) + 0x24), locomotor = MEM32(c->anchor + 0x564);
    uint32_t args[] = { locomotor, packed };
    return (int32_t)call(MEM32(MEM32(locomotor) + 0x1C), MEM32(locomotor), args, 2);
}
static uintptr_t height_cell(void *opaque, Ra2WorldPoint p)
{
    (void)opaque;
    Ra2CellGrid grid = { (const uint32_t *)(uintptr_t)ADDR(MEM32(0x832618)), (int32_t)MEM32(0x83261C),
        0xA6F9F8, (Ra2ServiceCell *)(uintptr_t)ADDR(0xA6FA1C) };
    return ra2_cell_at_world(&grid, p);
}
static int32_t cell_height(void *opaque, uintptr_t cell, Ra2WorldPoint p)
{ CompletionContext *c = opaque; uint32_t a = c->frame - 0x40; store(a, p); return (int32_t)call(0x4706C0, (uint32_t)cell, &a, 1); }

void ra2_ground_passage_bridge(unsigned entry)
{
    CompletionContext c = { 0 }; c.frame = g_esp; c.anchor = g_ecx;
    uint32_t ebx = g_ebx, esi = g_esi, edi = g_edi, ebp = g_ebp, f = c.frame, result;
    g_esp = f - 0x100;
    if (entry == 0)
    {
        Ra2BasePassageServices s = { &c, has_locomotor, locomotor_can_enter };
        result = (uint32_t)ra2_ground_base_can_enter(MEM8(f + 0x14) != 0, &s);
    }
    else if (entry == 1)
    {
        uint32_t to = MEM32(f + 4), from = MEM32(f + 0x14), direction = MEM32(f + 8);
        if (!from)
        {
            uint32_t i = (direction - 4) & 7, a = f - 0x40;
            MEM16(a) = (uint16_t)(MEM16(to + 0x24) + MEM16(0x851A70 + i * 4));
            MEM16(a + 2) = (uint16_t)(MEM16(to + 0x26) + MEM16(0x851A72 + i * 4));
            from = call(0x548070, 0x8324E0, &a, 1);
        }
        Ra2PassageCell t = { 0 }, o = { 0 };
        if (to) t = passage_cell(to);
        if (from) o = passage_cell(from);
        result = (uint32_t)ra2_ground_classify_transition(to ? &t : NULL, from ? &o : NULL, (int32_t)direction,
            (int32_t *)(uintptr_t)ADDR(MEM32(f + 0xC)), (uint8_t *)(uintptr_t)ADDR(MEM32(f + 0x10)));
    }
    else
    {
        Ra2GroundHeightServices s = { &c, height_cell, cell_height };
        result = (uint32_t)ra2_ground_height_at(point(MEM32(f + 4)), &s);
    }
    g_eax = result; g_ebx = ebx; g_esi = esi; g_edi = edi; g_ebp = ebp;
    g_esp = f + (entry == 2 ? 8 : 0x18);
}
