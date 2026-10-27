#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_death_delay.h"
#include "combat_building_death_delay_bridge.h"

typedef struct DelayContext { uint32_t building, frame; } DelayContext;

static uint32_t call(uint32_t target, uint32_t self)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building death delay] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack) { fputs("[building death delay] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static int32_t query(void *opaque, Ra2BuildingDeathDelayQuery q)
{
    DelayContext *c = opaque;
    switch (q) {
        case RA2_BDD_MISSION:
            g_edx = MEM32(c->building);
            return (int32_t)call(MEM32(g_edx + 0x16C), c->building);
        case RA2_BDD_EXPLODES:
            g_eax = MEM32(c->building + 0x418);
            g_ecx = (g_ecx & 0xFFFFFF00u) | MEM8(g_eax + 0xAE2);
            return g_ecx & 255;
        case RA2_BDD_TIMER_PENDING: {
            g_ecx = MEM32(c->building + 0x420);
            g_eax = MEM32(c->building + 0x428);
            uint32_t now = g_ecx == UINT32_MAX ? 0 : MEM32(0xA40D2C);
            Ra2BuildingDeathTimer timer = ra2_building_death_timer(g_ecx, g_eax, now);
            g_eax = timer.value;
            if (timer.running) g_edx = timer.elapsed;
            return (int32_t)timer.pending;
        }
    }
    abort();
}

static void perform(void *opaque, Ra2BuildingDeathDelayOperation op, uint32_t value)
{
    DelayContext *c = opaque;
    switch (op) {
        case RA2_BDD_START_TIMER:
            g_eax = MEM32(0xA40D2C); g_edx = c->building + 0x420; g_ecx = value;
            MEM32(g_edx) = g_eax; g_eax = MEM32(c->frame + 0x44);
            MEM32(g_edx + 4) = g_eax; MEM32(g_edx + 8) = value;
            break;
        case RA2_BDD_CLEAR_MISSION_TIMER:
            g_eax = MEM32(0xA40D2C); g_edx = c->building + 0xE4;
            MEM32(c->building + 0xF0) = g_ebx;
            MEM32(g_edx) = g_eax; g_eax = MEM32(c->frame + 0x44);
            MEM32(g_edx + 4) = g_eax; MEM32(g_edx + 8) = g_ecx;
            break;
        case RA2_BDD_UNINIT:
            g_edx = MEM32(c->building);
            call(MEM32(g_edx + 0xF0), c->building);
            break;
        case RA2_BDD_POST_UNINIT:
            call(0x43EBA0, c->building);
            break;
    }
}

void ra2_building_death_delay_bridge(void)
{
    DelayContext c = {g_esi, g_esp};
    Ra2BuildingDeathDelayServices s = {&c, query, perform};
    ra2_initialize_building_death_delay(&s);
}

int ra2_building_death_handoff_bridge(void)
{
    DelayContext c = {g_esi, g_esp};
    Ra2BuildingDeathDelayServices s = {&c, query, perform};
    return ra2_handoff_building_death(&s);
}
