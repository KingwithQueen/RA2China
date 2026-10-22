#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_landing.h"
#include "ground_failure.h"
#include "ground_slope.h"
#include "ground_remainder_bridge.h"

typedef struct RemainderContext
{
    uint32_t frame, drive, connection, saved_point, anchor, input_ax;
    int32_t result;
    unsigned entry;
} RemainderContext;
static Ra2WorldPoint point(uint32_t a)
{ Ra2WorldPoint p; memcpy(&p, (void *)(uintptr_t)ADDR(a), sizeof(p)); return p; }
static void store(uint32_t a, Ra2WorldPoint p)
{ memcpy((void *)(uintptr_t)ADDR(a), &p, sizeof(p)); }
static uint32_t owner(RemainderContext *c) { return MEM32(c->drive + 0xC); }
static uint32_t call(uint32_t address, uint32_t object, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = object;
    recomp_func_t fn = recomp_lookup_manual(address);
    if (!fn) fn = recomp_lookup(address);
    if (!fn) fn = recomp_lookup_import(address);
    if (!fn) { fprintf(stderr, "[ground-remainder] unresolved %08X\n", address); abort(); }
    fn();
    if (g_esp != stack) { fprintf(stderr, "[ground-remainder] stack %08X\n", address); abort(); }
    g_cur_func = caller; return g_eax;
}
static uint32_t method(uint32_t object, uint32_t slot, const uint32_t *args, unsigned count)
{ return call(MEM32(MEM32(object) + slot), object, args, count); }
static void return_frame(uint32_t f, uint32_t result, int prepare)
{
    g_eax = result; g_edi = MEM32(f); g_esi = MEM32(f + 4); g_ebp = MEM32(f + 8); g_ebx = MEM32(f + 12);
    g_flag_k = FK_ADD; g_flag_a = f + 16; g_flag_b = prepare ? 0x4C : 0xE4;
    g_flag_cf = f + (prepare ? 0x5C : 0xF4) < f + 16; g_esp = f + (prepare ? 0x6C : 0xFC);
}
static int valid(Ra2WorldPoint a, Ra2WorldPoint b)
{ return a.x != b.x || a.y != b.y || a.z != b.z; }
static void clear_at(RemainderContext *c, uint32_t a, int force)
{
    Ra2WorldPoint invalid = point(0x852998);
    if (force || valid(point(a), invalid)) { store(a, invalid); MEM8(c->drive + 0x63) = 0; }
}
static int32_t selector(void *opaque)
{ RemainderContext *c = opaque; return (int32_t)MEM32(c->drive + 0x58); }
static void leave(void *opaque)
{ RemainderContext *c = opaque; uint32_t zero = 0; method(owner(c), 0x11C, &zero, 1); }
static void clear_landing_segment(void *opaque)
{ RemainderContext *c = opaque; clear_at(c, c->drive + 0x40, 0); }
static int32_t connection_index(void *opaque)
{ RemainderContext *c = opaque; return (int16_t)MEM16(method(owner(c), 0x1A4, NULL, 0) + 0x116); }
static int connection_exists(void *opaque, int32_t index)
{
    RemainderContext *c = opaque;
    if (index < 0 || index >= (int32_t)MEM32(0x8661D8)) return 0;
    c->connection = MEM32(MEM32(0x8661CC) + (uint32_t)index * 4); return 1;
}
static Ra2WorldPoint center(uint32_t packed)
{ return (Ra2WorldPoint){ (int32_t)(int16_t)(uint16_t)packed * 256 + 128, (int32_t)(int16_t)(uint16_t)(packed >> 16) * 256 + 128, 0 }; }
static void start_connection(void *opaque, int32_t index)
{
    RemainderContext *c = opaque; store(c->drive + 0x40, center(MEM32(c->connection + 0x28)));
    uint32_t u = owner(c);
    for (unsigned i = 0; i < 23; ++i) MEM32(u + 0x4D0 + i * 4) = MEM32(u + 0x4D4 + i * 4);
    MEM32(owner(c) + 0x52C) = UINT32_MAX; MEM8(owner(c) + 0x574) = (uint8_t)index; MEM8(owner(c) + 0x575) = 0;
}
static void approach(void *opaque)
{
    RemainderContext *c = opaque; uint32_t direction = MEM32(c->connection + 0x30) & 7, packed = MEM32(c->connection + 0x24), a = c->frame - 0x40;
    MEM16(a) = (uint16_t)((uint16_t)packed + MEM16(0x851A70 + direction * 4));
    MEM16(a + 2) = (uint16_t)((uint16_t)(packed >> 16) + MEM16(0x851A72 + direction * 4));
    uint32_t cell = call(0x548070, 0x8324E0, &a, 1), output = c->frame - 0x60;
    Ra2WorldPoint p = point(call(0x475D60, cell, &output, 1)); store(owner(c) + 0x45C, p);
}
static int32_t floor_at(RemainderContext *c, Ra2WorldPoint p)
{ uint32_t a = c->frame - 0x40; store(a, p); return (int32_t)call(0x55A280, 0x8324E0, &a, 1); }
static int32_t current_height(void *opaque)
{ RemainderContext *c = opaque; return floor_at(c, point(owner(c) + 0x88)); }
static int32_t target_height(void *opaque, int32_t *duration)
{ RemainderContext *c = opaque; Ra2WorldPoint p = center(MEM32(c->connection + 0x28)); *duration = (int32_t)MEM32(c->connection + 0x1C0); return floor_at(c, p); }
static void finish_connection(void *opaque, int32_t height)
{ RemainderContext *c = opaque; MEM32(owner(c) + 0x464) = (uint32_t)height; MEM8(c->drive + 0x63) = 1; MEM32(c->drive + 0x58) = UINT32_MAX; c->result = height; }
static void reject_connection(void *opaque)
{ RemainderContext *c = opaque; MEM32(owner(c) + 0x4D0) = UINT32_MAX; MEM32(c->drive + 0x58) = UINT32_MAX; store(c->drive + 0x40, point(0x852998)); c->result = (int32_t)MEM32(0x852998); }

uint32_t ra2_ground_landing_bridge(unsigned entry)
{
    RemainderContext c = {0}; c.frame = g_esp; c.drive = g_ebp; c.input_ax = g_eax; c.result = (int32_t)g_eax;
    if (entry == 0)
    {
        Ra2LandingServices s = { &c, selector, leave, clear_landing_segment, connection_index, connection_exists,
            start_connection, approach, current_height, target_height, finish_connection, reject_connection };
        uint32_t progress = g_edx; g_esp = c.frame - 0x100;
        if (ra2_ground_land_connection(&s))
        { g_esi = MEM32(c.drive + 0x58); g_edi = UINT32_MAX; g_esp = c.frame; g_ebp = c.drive; g_eax = c.input_ax; g_edx = progress; return 0x4A15F0; }
    }
    else if (entry == 1)
        ra2_ground_reject_direction((int32_t *)(uintptr_t)ADDR(g_ecx + 0x4D0), (int32_t)g_edi);
    return_frame(c.frame, (uint32_t)c.result & 0xFFFFFF00u, 0); return 0;
}

static void clear_failure_segment(void *opaque, int saved)
{ RemainderContext *c = opaque; clear_at(c, saved ? c->saved_point : c->drive + 0x40, c->entry >= 5); }
static void clear_path(void *opaque, int32_t value)
{ RemainderContext *c = opaque; MEM32(owner(c) + 0x4D0) = (uint32_t)value; }
static void start_retry(void *opaque)
{ RemainderContext *c = opaque; uint32_t u = owner(c); MEM32(u + 0x530) = MEM32(0xA40D2C); MEM32(u + 0x534) = MEM32(c->frame + 0x54); MEM32(u + 0x538) = 0; }
static uint32_t prepare_again(void *opaque)
{ RemainderContext *c = opaque; uint32_t args[] = { MEM32(c->frame + 0x60), 0, 0 }; return call(0x4A2670, c->drive, args, 3); }
static uint32_t stop(void *opaque)
{
    RemainderContext *c = opaque; uint32_t args[] = {0,1};
    if (c->entry == 4) return method(c->anchor, 0x410, args, 2) & 0xFFFFFF00u;
    uint32_t u = owner(c); int target = MEM32(u + 0x488) != 0;
    if (target) call(0x4CD9B0, u, NULL, 0);
    uint32_t result = method(owner(c), target ? 0x414 : 0x410, args, 2);
    return target ? result : result & 0xFFFFFF00u;
}
static uint32_t pending(void *opaque)
{ RemainderContext *c = opaque; MEM8(owner(c) + 0x57A) = 0; MEM32(c->drive + 0x58) = UINT32_MAX; return (c->input_ax & 0xFFFFFF00u) | 1; }
void ra2_ground_failure_bridge(unsigned entry)
{
    RemainderContext c = {0}; c.frame = g_esp; c.drive = g_ebp; c.saved_point = g_ebx; c.anchor = g_ecx; c.input_ax = g_eax; c.entry = entry;
    Ra2PrepareFailureServices s = { &c, clear_failure_segment, clear_path, start_retry, prepare_again, stop, pending };
    int retry = MEM8(c.frame + 0x64) != 0; int32_t classification = (int32_t)MEM32(c.frame + 0x18), rejected = (int32_t)g_esi;
    g_esp = c.frame - 0x100;
    uint32_t result = ra2_ground_finish_failure((Ra2PrepareFailureEntry)entry, retry, classification, rejected, &s);
    return_frame(c.frame, result, 1);
}

void ra2_ground_slope_bridge(void)
{
    uint32_t f = g_esp, u = g_ecx; Ra2SlopeCache cache = {0};
    cache.initialized = MEM8(0x850BB8); memcpy(&cache.level_height, (void *)(uintptr_t)ADDR(0x850BA8), 8);
    memcpy(&cache.world_scale, (void *)(uintptr_t)ADDR(0x850BD0), 8); memcpy(cache.planes, (void *)(uintptr_t)ADDR(0x7D27E8), sizeof(cache.planes));
    uint16_t initial = g_fpu_cw, conversion = MEM16(0x7D8964); int32_t height = (int32_t)MEM32(0x850C40);
    ra2_ground_initialize_slopes(&cache, height, initial);
    MEM8(0x850BB8) = cache.initialized; memcpy((void *)(uintptr_t)ADDR(0x850BA8), &cache.level_height, 8);
    memcpy((void *)(uintptr_t)ADDR(0x850BD0), &cache.world_scale, 8); memcpy((void *)(uintptr_t)ADDR(0x7D27E8), cache.planes, sizeof(cache.planes));
    uint32_t a = MEM32(f + 4); Ra2WorldPoint p = { (int32_t)MEM32(a), (int32_t)MEM32(a + 4), 0 };
    g_eax = (uint32_t)ra2_ground_slope_height(&cache, height, (int8_t)MEM8(u + 0x11B), MEM8(u + 0x11C), p, initial, conversion);
    g_fpu_cw = conversion; g_esp = f + 8;
}
