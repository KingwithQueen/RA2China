#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_path_prepare.h"
#include "ground_region_route.h"
#include "ground_path_rebuild.h"
#include "ground_path_lifecycle_bridge.h"

static uint32_t call_service(uint32_t address, uint32_t object, const uint32_t *args, unsigned count, int cdecl_call)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) {g_esp -= 4; MEM32(g_esp) = args[i - 1];}
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = object;
    recomp_func_t fn = recomp_lookup_manual(address);
    if (!fn) fn = recomp_lookup(address);
    if (!fn) fn = recomp_lookup_import(address);
    if (!fn) {fprintf(stderr, "[path-lifecycle] missing %08X\n", address); abort();}
    fn(); if (cdecl_call) g_esp += count * 4;
    if (g_esp != stack) {fprintf(stderr, "[path-lifecycle] stack mismatch %08X\n", address); abort();}
    g_cur_func = caller; return g_eax;
}
typedef struct PreparationContext {uint32_t search, owner, frame;} PreparationContext;
static uintptr_t reference(void *opaque, const Ra2PathPoint *point)
{(void)opaque; return MEM32(0x832618) + ((uint32_t)(int32_t)point->y * 512 + (uint32_t)(int32_t)point->x) * 4;}
static int cell(void *opaque, uintptr_t ref, Ra2PathCell *out)
{
    (void)opaque; uint32_t p = MEM32((uint32_t)ref); if (!p) return 0;
    memcpy(&out->point, (void *)(uintptr_t)(p + 0x24), 4);
    out->ground_level = (int8_t)MEM8(p + 0x11B); out->has_bridge = (MEM32(p + 0x140) & 0x100u) != 0;
    out->has_region_connection = MEM8(p + 0x122); return 1;
}
static int32_t kind(void *opaque)
{PreparationContext *c = opaque; return (int32_t)call_service(MEM32(MEM32(c->owner) + 0x2C), c->owner, NULL, 0, 0);}
static Ra2PathOwnerType owner_type(void *opaque)
{
    PreparationContext *c = opaque;uint32_t type = call_service(MEM32(MEM32(c->owner) + 0x80), c->owner, NULL, 0, 0);
    return (Ra2PathOwnerType){MEM8(type + 0xAA0), (int32_t)MEM32(type + 0x5A4)};
}
static unsigned on_bridge(void *opaque){PreparationContext *c = opaque;return MEM8(c->owner + 0x79);}
static int32_t height(void *opaque){PreparationContext *c = opaque;return (int32_t)MEM32(c->owner + 0x90) / (int32_t)MEM32(0x84E800);}
static unsigned unit_flag(void *opaque){PreparationContext *c = opaque;return MEM8(MEM32(c->owner + 0x5AC) + 0xBA4);}
static Ra2SearchNode *create_root(void *opaque, uintptr_t start, const Ra2PathPoint *target)
{
    PreparationContext *c = opaque;MEM32(c->frame + 0x40) = MEM32(c->search + 0x40);
    uint32_t args[] = {0, (uint32_t)start, (uint32_t)(uintptr_t)target, 0};
    return (Ra2SearchNode *)(uintptr_t)call_service(0x427D40, c->search, args, 4, 0);
}
static void toggle(void *opaque){PreparationContext *c = opaque;call_service(0x4285D0, c->search, &c->owner, 1, 0);}
static unsigned facing(void *opaque)
{
    PreparationContext *c = opaque;uint32_t result = c->frame + 0x60;
    uint32_t p = call_service(0x4B8BE0, c->owner + 0x2E0, &result, 1, 0);
    return (((MEM32(p) >> 12) + 1) >> 1) & 7;
}
static uintptr_t adjacent(void *opaque, uintptr_t ref, unsigned direction)
{(void)opaque;return ref + MEM32(0x79C484 + direction * 4) * 4;}
int ra2_path_prepare_bridge(void)
{
    uint32_t f = g_esp;PreparationContext c = {g_ecx, MEM32(f + 0x68), f};
    Ra2PathPreparation p = {0};p.start = (Ra2PathPoint *)(uintptr_t)MEM32(f + 0x60);p.target = (Ra2PathPoint *)(uintptr_t)MEM32(f + 0x64);
    p.expansion_limit = (int32_t)MEM32(f + 0x70);
    p.start_level = (int32_t *)(uintptr_t)(c.search + 0x30);p.target_level = (int32_t *)(uintptr_t)(c.search + 0x34);
    p.movement_zone = (int32_t *)(uintptr_t)(c.search + 0x2C);p.obstacle_mode = (int32_t *)(uintptr_t)(c.search + 0x3C);
    p.region_cursor = (uint32_t *)(uintptr_t)(c.search + 0x6C);p.last_region_point = (uint32_t *)(uintptr_t)(c.search + 0x70);
    p.connected_regions = (const uint32_t **)(uintptr_t)(c.search + 0x40);
    p.cache = (Ra2PathNodeCache){{(uint32_t *)(uintptr_t)MEM32(c.search+0x18),(float *)(uintptr_t)MEM32(c.search+0x24)},
        {(uint32_t *)(uintptr_t)MEM32(c.search+0x1C),(float *)(uintptr_t)MEM32(c.search+0x20)},(uint32_t *)(uintptr_t)(c.search+0x28)};
    p.grid_width = MEM32(0x84E804);
    Ra2PathPreparationServices v = {&c, reference, cell, kind, owner_type, on_bridge, height, unit_flag, create_root, toggle, facing, adjacent};
    g_esp = f - 0x100;int result = ra2_path_prepare(&p, &v);g_esp = f;
    MEM32(f+0x28)=0;MEM32(f+0x14)=(uint32_t)(uintptr_t)p.root;MEM32(f+0x38)=(uint32_t)p.target_reference;
    MEM32(f+0x2C)=(uint32_t)p.start_reference;MEM32(f+0x30)=MEM32((uint32_t)p.target_reference);
    MEM32(f+0x40)=(uint32_t)(uintptr_t)p.saved_connected_regions;MEM32(f+0x70)=(uint32_t)p.expansion_limit;
    MEM8(f+0x12)=(uint8_t)p.ignore_soft_obstacles;MEM8(f+0x13)=(uint8_t)p.continue_at_blocked_goal;
    g_esi=c.search;g_ebx=c.owner;return result;
}
void ra2_region_route_publish_bridge(void)
{
    uint32_t f=g_esp, pass=MEM32(f+0x38), context=g_edi;
    ra2_region_route_publish((Ra2RegionRouteNode *)(uintptr_t)MEM32(context+0x64),(Ra2RegionRouteNode *)(uintptr_t)g_eax,
        MEM32(context+0x28),(uint32_t *)(uintptr_t)MEM32(f+0x5C),(uint16_t *)(uintptr_t)(context+0xBC+pass*1000),
        (uint32_t *)(uintptr_t)(context+0xC74+pass*4));
    g_esi=pass; /* 后面的原版 DEC 决定是否开始下一层区域搜索。 */
}
static Ra2PathPoint read_point(void *opaque, void *ref)
{(void)opaque;Ra2PathPoint p;memcpy(&p,(void *)(uintptr_t)(MEM32((uint32_t)(uintptr_t)ref)+0x24),4);return p;}
void ra2_path_rebuild_bridge(void)
{
    uint32_t stack=g_esp;
    if(!(MEM8(0x84E7D4)&1)){
        MEM8(0x84E7D4)|=1;uint32_t callback=0x4284D0;call_service(0x78298A,0,&callback,1,1);
    }
    ra2_path_rebuild((Ra2SearchNode *)(uintptr_t)MEM32(stack+4),(int32_t *)(uintptr_t)MEM32(stack+8),
        (int32_t *)0x84C858,(int32_t *)0x7CF100,read_point,NULL,(Ra2RebuiltPath *)0x84C810);
    g_eax=0x84C810;g_esp=stack+12;
}
