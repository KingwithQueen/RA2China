#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_shake.h"
#include "combat_building_shake_bridge.h"

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building shake] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack) { fputs("[building shake] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static int32_t cost(void *context)
{
    uint32_t building = *(uint32_t *)context;
    uint32_t type = MEM32(building + 0x418), owner = MEM32(building + 0x1B4);
    return (int32_t)call(MEM32(MEM32(type) + 0x84), type, &owner, 1);
}

static int32_t divisor(void *context)
{
    (void)context;
    g_ecx = MEM32(0x839848);
    return (int32_t)MEM32(g_ecx + 0x4E8);
}

static void publish(void *context, Ra2ShakeAmplitude amplitude)
{
    (void)context;
    g_eax = (uint32_t)amplitude.quotient;
    g_edx = (uint32_t)amplitude.remainder;
}

static void dispatch(void *context, int32_t amplitude)
{
    (void)context;
    call(0x482E00, (uint32_t)amplitude, NULL, 0);
}

void ra2_building_shake_bridge(void)
{
    uint32_t building = g_esi;
    Ra2BuildingShakeServices s = {&building, (int32_t)g_ebx, cost, divisor, publish, dispatch};
    ra2_schedule_building_shake(&s);
}

void ra2_screen_shake_bridge(void)
{
    ra2_legacy_screen_shake((int32_t)g_ecx);
    g_esp += 4;
}
