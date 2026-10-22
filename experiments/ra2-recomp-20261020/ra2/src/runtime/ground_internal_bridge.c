#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_sampling_shared.h"
#include "ground_prepare_internal.h"
#include "ground_dispatch_bridge.h"
#include "ground_completion_bridge.h"
#include "ground_internal_bridge.h"

typedef struct InternalContext { uint32_t frame, drive, table, anchor; } InternalContext;
static Ra2WorldPoint point(uint32_t a)
{ Ra2WorldPoint p; memcpy(&p, (void *)(uintptr_t)ADDR(a), sizeof(p)); return p; }
static void select_table(void *opaque, int32_t table)
{ InternalContext *c = opaque; c->table = MEM32(0x7A00A0 + (uint32_t)table * 16); }
static Ra2PathSample sample_at(void *opaque, int32_t index)
{ InternalContext *c = opaque; Ra2PathSample p; memcpy(&p, (void *)(uintptr_t)ADDR(c->table + (uint32_t)index * 12), sizeof(p)); return p; }
uint32_t ra2_ground_sampling_shared_bridge(unsigned entry)
{
    InternalContext c = { g_esp, g_ebp, 0, g_ecx };
    Ra2SamplingServices s = { &c, NULL, select_table, sample_at };
    Ra2SamplingChoice choice = {0}; Ra2SamplingPhase phase;
    if (entry == 0)
    {
        if ((int32_t)g_edx <= 7) return 0x4A1FA1;
        uint32_t selected = 0x7A0180 + MEM32(c.drive + 0x58) * 12;
        Ra2SamplingTemplate t = { (int8_t)MEM8(selected), (int8_t)MEM8(selected + 1), MEM8(selected + 4) };
        phase = ra2_ground_choose_shared_full((int32_t)g_edx, (int32_t)g_eax, (int32_t)g_edi,
            t, MEM8(c.drive + 0x60), &choice, &s);
        g_esi = selected; MEM32(c.frame + 0xA8) = selected;
        MEM32(c.frame + 0x58) = (uint32_t)choice.table * 16; MEM32(c.frame + 0x38) = c.table;
        if (phase == RA2_SAMPLING_INVALID_DIRECTION) return 0x4A22F9;
        MEM8(c.frame + 0x13) = (uint8_t)choice.turning;
        if (g_eax != g_edi && g_eax != 8) MEM16(c.frame + 0x14) = (uint16_t)((uint32_t)t.facing << 8);
        return 0x4A166A;
    }
    int32_t index = (int32_t)MEM32(c.drive + 0x5C);
    phase = ra2_ground_choose_selected_remainder((int8_t)MEM8(g_eax), index, (int32_t)g_edi, &choice, &s);
    MEM32(c.frame + 0x8C) = (uint32_t)choice.sample.x; MEM32(c.frame + 0x90) = (uint32_t)choice.sample.y;
    g_eax = (uint32_t)choice.sample.y; g_edx = (uint32_t)index; g_esi = (uint32_t)choice.sample.x;
    if (phase == RA2_SAMPLING_DONE) return 0x4A263A;
    uint32_t start = MEM32(c.drive + 0xC) + 0x88; Ra2WorldPoint p = point(start);
    memcpy((void *)(uintptr_t)ADDR(c.frame + 0x80), &p, sizeof(p));
    MEM32(c.frame + 0x34) = (uint32_t)choice.sample.direction;
    g_eax = start; g_esi = (uint32_t)p.x; g_ebx = (uint32_t)p.y; g_edx = (uint32_t)p.z;
    return 0x4A237D;
}
static uint32_t rebuild(void *opaque, uint32_t cell, unsigned attempts)
{
    InternalContext *c = opaque; uint32_t stack = g_esp, caller = g_cur_func;
    g_esp -= 4; MEM32(g_esp) = attempts; g_esp -= 4; MEM32(g_esp) = 0;
    g_esp -= 4; MEM32(g_esp) = cell; g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = c->anchor;
    recomp_func_t fn = recomp_lookup_manual(0x4C3000); if (!fn) fn = recomp_lookup(0x4C3000);
    if (!fn) { fprintf(stderr, "[ground-internal] unresolved rebuild\n"); abort(); }
    fn(); if (g_esp != stack) { fprintf(stderr, "[ground-internal] rebuild stack\n"); abort(); }
    g_cur_func = caller; return g_eax;
}
static void clear_segment(void *opaque, int32_t first)
{
    InternalContext *c = opaque; MEM32(c->drive + 0x40) = (uint32_t)first;
    MEM32(c->drive + 0x44) = MEM32(0x85299C); MEM32(c->drive + 0x48) = MEM32(0x8529A0);
}
void ra2_ground_prepare_internal_bridge(unsigned entry)
{
    InternalContext c = { g_esp, g_ebp, 0, g_ecx };
    Ra2PrepareInternalServices s = { &c, rebuild, clear_segment };
    if (entry == 2)
    {
        ra2_ground_prepare_clear_internal((int32_t)g_eax, &s);
        g_eax = MEM32(0x8529A0); g_edx = MEM32(0x85299C);
        ra2_ground_prepare_finish_bridge(7); return;
    }
    unsigned retry = entry == 0 ? 0 : g_ebx & 255u;
    Ra2WorldPoint destination = point(c.drive + 0x34);
    uint32_t packed = ra2_ground_prepare_destination_cell(destination);
    MEM32(c.frame + 0x68) = packed; g_esi = c.drive + 0x34;
    g_esp = c.frame - 0x100;
    g_eax = ra2_ground_prepare_rebuild_internal(destination, retry, &s);
    g_esp = c.frame; g_ebp = c.drive; g_esi = c.drive + 0x34;
    ra2_ground_prepare_exit_bridge(0);
}
