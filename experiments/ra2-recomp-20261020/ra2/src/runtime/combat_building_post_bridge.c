#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_post.h"
#include "combat_building_post_bridge.h"

typedef struct PostContext { uint32_t building, type, image, frame; } PostContext;

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building post] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack) { fputs("[building post] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static int32_t query(void *opaque, Ra2BuildingPostQuery q)
{
    PostContext *c = opaque;
    switch (q) {
        case RA2_BP_LEAVE_RUBBLE:
            g_eax = (g_eax & 0xFFFFFF00u) | MEM8(c->type + 0x13E9); return g_eax & 255;
        case RA2_BP_IMAGE_OUT_PRESENT:
            g_esi = MEM32(c->frame + 8); return g_esi != 0;
        case RA2_BP_LOAD_IMAGE:
            g_eax = MEM32(c->type);
            c->image = call(MEM32(g_eax + 0x9C), c->type, NULL, 0);
            MEM32(g_esi) = c->image; return c->image != 0;
        case RA2_BP_IMAGE_FRAME_COUNT:
            g_eax = (uint32_t)(int32_t)(int16_t)MEM16(c->image + 6);
            g_edx = (int32_t)g_eax < 0 ? UINT32_MAX : 0;
            return (int32_t)g_eax;
        case RA2_BP_CRATE_BENEATH:
            g_edx = MEM32(c->building + 0x418);
            g_eax = (g_eax & 0xFFFFFF00u) | MEM8(g_edx + 0x13E8); return g_eax & 255;
        case RA2_BP_CRATE_MONEY:
            g_eax = (g_eax & 0xFFFFFF00u) | MEM8(g_edx + 0x13EA); return g_eax & 255;
    }
    abort();
}

static void perform(void *opaque, Ra2BuildingPostOperation op, int32_t value)
{
    PostContext *c = opaque;
    switch (op) {
        case RA2_BP_PUBLISH_HALF_FRAMES: g_eax = (uint32_t)value; break;
        case RA2_BP_PUBLISH_RUBBLE_LEVEL:
            /* 第二输出地址由图像回调返回后重新读取，第一地址已在ESI捕获。 */
            g_ecx = MEM32(c->frame + 12); MEM32(g_ecx) = (uint32_t)value; break;
        case RA2_BP_CRATE_POSITION: {
            uint32_t out = c->frame + 0x30;
            g_eax = MEM32(c->building);
            uint32_t position = call(MEM32(g_eax + 0xA8), c->building, &out, 1);
            g_ecx = position;
            int32_t x = (int32_t)MEM32(position), y = (int32_t)MEM32(position + 4);
            MEM16(c->frame + 0x10) = (uint16_t)ra2_building_post_cell(x);
            g_edx = MEM32(c->building + 0x418);
            g_eax = (uint32_t)(y / 256);
            MEM16(c->frame + 0x12) = (uint16_t)g_eax;
            break;
        }
        case RA2_BP_PLACE_CRATE: {
            uint32_t cell = MEM32(c->frame + 0x10);
            if (!value) g_eax = cell; else g_ecx = cell;
            uint32_t args[] = {cell, (uint32_t)value}; call(0x54E580, 0x8324E0, args, 2); break;
        }
    }
}

void ra2_building_rubble_gate_bridge(void)
{
    uint32_t saved = g_esi;
    g_esp -= 4; MEM32(g_esp) = saved;
    PostContext c = {0, g_ecx, 0, g_esp};
    Ra2BuildingPostServices s = {&c, query, perform};
    unsigned result = (unsigned)ra2_prepare_building_rubble(&s);
    g_eax = (g_eax & 0xFFFFFF00u) | result;
    g_esi = MEM32(g_esp); g_esp += 16;
}

void ra2_building_post_crate_bridge(void)
{
    PostContext c = {g_ebx, 0, 0, g_esp};
    Ra2BuildingPostServices s = {&c, query, perform};
    ra2_schedule_building_crate(&s);
}
