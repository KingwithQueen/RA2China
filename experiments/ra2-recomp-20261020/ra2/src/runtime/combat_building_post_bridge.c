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
        case RA2_BP_FOUNDATION_END:
            return MEM16(g_ebp) == 0x7FFF && MEM16(g_ebp + 2) == 0x7FFF;
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
        case RA2_BP_RUBBLE_FOUNDATION: {
            uint32_t zero = 0;
            g_edx = MEM32(c->building);
            call(MEM32(g_edx + 0x100), c->building, &zero, 1); break;
        }
        case RA2_BP_RUBBLE_POSITION: {
            uint32_t out = c->frame + 0x30;
            g_ecx = out; g_ebp = g_eax; g_eax = MEM32(c->building);
            uint32_t position = call(MEM32(g_eax + 0xA8), c->building, &out, 1);
            g_ecx = position;
            int32_t x = (int32_t)MEM32(position);
            g_edx = x < 0 ? 255u : 0u; g_eax = (uint32_t)(x / 256);
            MEM16(c->frame + 0x14) = (uint16_t)g_eax;
            int32_t y = (int32_t)MEM32(position + 4);
            g_edx = y < 0 ? 255u : 0u; g_eax = (uint32_t)(y / 256);
            MEM16(c->frame + 0x16) = (uint16_t)g_eax;
            g_edx = MEM32(c->frame + 0x14); MEM32(c->frame + 0x10) = g_edx; break;
        }
        case RA2_BP_RUBBLE_CELL: {
            g_eax = g_ebp; g_ebp += 4;
            g_ecx = (g_ecx & 0xFFFF0000u) | MEM16(g_eax);
            g_edx = (g_edx & 0xFFFF0000u) | MEM16(g_eax + 2);
            g_ecx = (g_ecx & 0xFFFF0000u) | (uint16_t)(g_ecx + MEM16(c->frame + 0x10));
            g_edx = (g_edx & 0xFFFF0000u) | (uint16_t)(g_edx + MEM16(c->frame + 0x12));
            MEM16(c->frame + 0x14) = (uint16_t)g_ecx;
            g_ecx = c->frame + 0x18; MEM16(c->frame + 0x16) = (uint16_t)g_edx;
            g_eax = MEM32(c->frame + 0x14); MEM32(c->frame + 0x18) = g_eax;
            uint32_t cell = g_ecx; call(0x548070, 0x8324E0, &cell, 1);
            g_esi = g_eax; break;
        }
        case RA2_BP_CLEAR_CELL: call(0x47C080, g_esi, NULL, 0); break;
        case RA2_BP_PUBLISH_RUBBLE_CELL:
            g_ecx = g_esi; MEM32(g_esi + 0x44) = 239; MEM32(g_esi + 0x40) = 0; break;
        case RA2_BP_RECALCULATE_CELL: {
            uint32_t arg = (uint32_t)value; call(0x472540, g_esi, &arg, 1); break;
        }
        case RA2_BP_REFRESH_MAP_CELL:
            g_edi = g_esi + 0x24; call(0x54FB20, 0x8324E0, &g_edi, 1); break;
        case RA2_BP_REFRESH_PASSABILITY: call(0x566340, 0x8324E0, &g_edi, 1); break;
        case RA2_BP_FINISH_CELL:
            call(0x6D7C80, g_esi, NULL, 0); RECOMP_BACKEDGE(); break;
        case RA2_BP_RUBBLE_ANCHOR: {
            g_edx = c->frame + 0x10; uint32_t cell = g_edx;
            call(0x548070, 0x8324E0, &cell, 1);
            g_ecx = c->frame + 0x30; g_edi = g_eax;
            g_eax = MEM32(c->building + 0x418); MEM32(g_edi + 0x40) = g_eax; break;
        }
        case RA2_BP_FIRST_RECTANGLE: {
            uint32_t out = c->frame + 0x30; call(0x475100, g_edi, &out, 1); break;
        }
        case RA2_BP_SECOND_RECTANGLE: {
            g_edx = c->frame + 0x40; uint32_t out = g_edx;
            g_esi = g_eax; call(0x474EB0, g_edi, &out, 1); break;
        }
        case RA2_BP_PREPARE_INVALIDATION: {
            g_esi = MEM32(0x839630); g_ebp = MEM32(0x839634);
            /* 原构造函数RET12；先压入的零旗标留给后续按值矩形调用。 */
            g_esp -= 4; MEM32(g_esp) = 0;
            g_ecx -= g_esi; uint32_t height = g_eax;
            g_eax = c->frame + 0x20; g_edx -= g_ebp;
            MEM32(c->frame + 0x20) = g_ecx; MEM32(c->frame + 0x24) = g_edx;
            uint32_t args[] = {g_eax, g_edi, height}; call(0x453E40, c->frame + 0x40, args, 3); break;
        }
        case RA2_BP_INVALIDATE_RECTANGLE: {
            uint32_t rectangle = g_eax;
            g_edx = MEM32(rectangle); g_esp -= 16; g_ecx = g_esp;
            MEM32(g_ecx) = g_edx; g_edx = MEM32(rectangle + 4);
            MEM32(g_ecx + 4) = g_edx; g_edx = MEM32(rectangle + 8);
            g_eax = MEM32(rectangle + 12); MEM32(g_ecx + 8) = g_edx; MEM32(g_ecx + 12) = g_eax;
            /* 此处20字节参数已在guest栈；不再额外压入矩形或零旗标。 */
            uint32_t caller = g_cur_func;
            g_ecx = MEM32(0x83996C); g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
            recomp_func_t fn = recomp_lookup_manual(0x6A3020);
            if (!fn) fn = recomp_lookup(0x6A3020);
            if (!fn) fn = recomp_lookup_import(0x6A3020);
            if (!fn) { fputs("[building post] missing rectangle invalidation\n", stderr); abort(); }
            fn();
            if (g_esp != c->frame) { fputs("[building post] rectangle stack imbalance\n", stderr); abort(); }
            g_cur_func = caller; break;
        }
        case RA2_BP_FIND_CURRENT_ANCHOR: {
            g_ecx = c->frame + 0x10; uint32_t cell = g_ecx;
            call(0x548070, 0x8324E0, &cell, 1); break;
        }
        case RA2_BP_INVALIDATE_ANCHOR: {
            uint32_t cell = g_eax; call(0x6AADD0, MEM32(0x83996C), &cell, 1); break;
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

void ra2_building_rubble_cells_bridge(void)
{
    PostContext c = {g_ebx, 0, 0, g_esp};
    Ra2BuildingPostServices s = {&c, query, perform};
    ra2_rewrite_building_rubble(&s);
}

void ra2_building_rubble_invalidate_bridge(void)
{
    PostContext c = {g_ebx, 0, 0, g_esp};
    Ra2BuildingPostServices s = {&c, query, perform};
    ra2_invalidate_building_rubble(&s);
}
