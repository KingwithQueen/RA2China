#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_crew.h"
#include "combat_building_crew_bridge.h"

typedef struct BuildingCrewContext { uint32_t building; } BuildingCrewContext;

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building crew] unresolved %08X\n", target); abort(); }
    fn();
    if (target == 0x782017) g_esp += 4; /* cdecl operator new。 */
    if (g_esp != stack) { fputs("[building crew] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static uint32_t query(void *opaque, Ra2BuildingCrewQuery q)
{
    BuildingCrewContext *c = opaque;
    switch (q) {
        case RA2_BCQ_SPECIAL_DISABLED: return MEM8(c->building + 0x5B3);
        case RA2_BCQ_RANDOM_100: {
            uint32_t args[] = {0, 99};
            return call(0x6388A0, MEM32(0xA3D290) + 0x218, args, 2);
        }
        case RA2_BCQ_FACTORY_KIND: return MEM32(MEM32(c->building + 0x418) + 0xC44);
        case RA2_BCQ_CURRENT_ENGINEER: return MEM32(MEM32(0x839848) + 0xC48);
        case RA2_BCQ_GENERIC_CREW: return call(0x6D30B0, c->building, NULL, 0);
    }
    abort();
}

uint32_t ra2_building_crew_bridge(void)
{
    BuildingCrewContext c = {g_esi};
    Ra2BuildingCrewServices s = {&c, query};
    return ra2_select_building_crew(&s);
}

static uint32_t select_type(void *opaque)
{
    BuildingCrewContext *c = opaque;
    /* 原疏散段在选员回调前清ESI，在分配/构造回调前发布EBP。 */
    g_esi = 0;
    g_ebp = call(MEM32(MEM32(c->building) + 0x2E0), c->building, NULL, 0);
    return g_ebp;
}

static uint32_t allocate(void *opaque, uint32_t size)
{
    (void)opaque;
    return call(0x782017, g_ecx, &size, 1);
}

static uint32_t construct(void *opaque, uint32_t storage, uint32_t type)
{
    BuildingCrewContext *c = opaque;
    uint32_t args[] = {type, MEM32(c->building + 0x1B4)};
    return call(0x4FF640, storage, args, 2);
}

void ra2_building_evacuation_bridge(void)
{
    BuildingCrewContext c = {g_edi};
    Ra2BuildingEvacuationServices s = {&c, select_type, allocate, construct};
    g_esi = ra2_create_building_evacuee(&s);
}

static uint32_t sale_select_type(void *opaque)
{
    BuildingCrewContext *c = opaque;
    g_edi = call(MEM32(MEM32(c->building) + 0x2E0), c->building, NULL, 0);
    return g_edi;
}

static int is_engineer(void *opaque, uint32_t type)
{
    (void)opaque;
    /* 原接口先读取标志再检查类型；空类型不是此调用段的有效输入。 */
    return MEM8(type + 0xC11) != 0;
}

static int engineer_already_selected(void *opaque)
{ (void)opaque; return MEM8(g_esp + 0x12) != 0; }

static void mark_engineer_selected(void *opaque)
{ (void)opaque; MEM8(g_esp + 0x12) = 1; }

void ra2_building_sale_crew_bridge(void)
{
    BuildingCrewContext c = {g_esi};
    Ra2BuildingCrewRetryServices s = {&c, sale_select_type, is_engineer,
                                    engineer_already_selected, mark_engineer_selected};
    g_edi = ra2_select_building_sale_crew(&s);
}
