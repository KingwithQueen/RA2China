#include <intrin.h>
extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);
extern void __cdecl ra2_overlap_route(unsigned site,unsigned entry);
extern void __cdecl ra2_chain_observe(unsigned unit,unsigned cell,unsigned frame);
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_template_transition.h"
#include "ground_object_chain.h"
#include "ground_joint_bridge.h"
#include "ground_overlap_bridge.h"

typedef struct TransitionContext
{
    uint32_t frame, drive, cell;
    unsigned classification_reads;
} TransitionContext;

static uint32_t type_of(uint32_t unit)
{
    uint32_t address = MEM32(MEM32(unit) + 0x80);
    uint32_t stack = g_esp, caller = g_cur_func;
    g_esp -= 4;
    MEM32(g_esp) = RECOMP_RETADDR;
    g_ecx = unit;
    recomp_func_t function = recomp_lookup_manual(address);
    if (!function) function = recomp_lookup(address);
    if (!function) function = recomp_lookup_import(address);
    if (!function) { fprintf(stderr, "[template-transition] unresolved %08X\n", address); abort(); }
    function();
    if (g_esp != stack) { fprintf(stderr, "[template-transition] stack %08X\n", address); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static int32_t classification(void *opaque)
{
    TransitionContext *context = opaque;
    uint32_t value = MEM32(context->frame + 0x18);
    if (context->classification_reads++) g_eax = value;
    return (int32_t)value;
}

static unsigned type_flag(void *opaque, unsigned crush_flag)
{
    TransitionContext *context = opaque;
    uint32_t type = type_of(MEM32(context->drive + 0xC));
    uint32_t value = MEM8(type + (crush_flag ? 0xAF3 : 0xAA0));
    g_ecx = (g_ecx & UINT32_C(0xFFFFFF00)) | value;
    return value;
}

static int32_t overlay(void *opaque)
{
    TransitionContext *context = opaque;
    g_eax = MEM32(context->cell + 0x44);
    return (int32_t)g_eax;
}

static void clear_classification(void *opaque)
{
    TransitionContext *context = opaque;
    MEM32(context->frame + 0x18) = 0;
}

uint32_t ra2_ground_template_transition_bridge(unsigned entry)
{
    uint32_t frame = g_esp;
    ra2_internal_observe(g_ebp,0,entry?17:16,0,0); ra2_overlap_route(entry?17:16,(unsigned)(uintptr_t)_ReturnAddress());
    if (entry == 0)
    {
        uint32_t unit = g_ecx;
        int32_t x = (int32_t)MEM32(unit + 0x88), y = (int32_t)MEM32(unit + 0x8C);
        Ra2TemplateCells cells = ra2_ground_template_cells(g_esi, g_eax, x, y);
        MEM32(frame + 0xEC) = (uint32_t)y;
        MEM32(frame + 0xF0) = MEM32(unit + 0x90);
        MEM32(frame + 0xA4) = cells.packed_target;
        MEM32(frame + 0x68) = cells.packed_target;
        g_esi = (uint32_t)cells.target_x;
        g_ebx = (uint32_t)cells.target_y;
        g_edi = (uint32_t)cells.current_x;
        g_eax = (uint32_t)cells.current_y;
        g_edx = cells.packed_target;
        unsigned compare_y = (uint16_t)cells.target_x == (uint16_t)cells.current_x;
        g_flag_k = FK_NARROW(FK_CMP, 16);
        g_flag_a = (uint32_t)(uint16_t)(compare_y ? cells.target_y : cells.target_x) << 16;
        g_flag_b = (uint32_t)(uint16_t)(compare_y ? cells.current_y : cells.current_x) << 16;
        g_flag_cf = g_flag_a < g_flag_b;
        return cells.same_cell ? 0x4A1AB0 : 0x4A186C;
    }

    TransitionContext context = {frame, g_ebp, g_esi, 0};
    Ra2TemplateGateServices services = {&context, classification, type_flag, overlay, clear_classification};
    uint32_t drive = g_ebp, cell = g_esi, direction = g_ebx, level = g_edi;
    g_esp = frame - 0x100;
    ra2_ground_template_gate(&services);
    g_esp = frame;
    g_ebp = drive; g_esi = cell; g_ebx = direction; g_edi = level;
    return 0x4A3550;
}

uint32_t ra2_ground_object_chain_bridge(unsigned entry)
{
    uint32_t frame = g_esp;
    if(entry)ra2_internal_observe(0,g_ebp,19,0,0);else ra2_chain_observe(g_ebp,g_ebx,frame); ra2_overlap_route(entry?19:18,(unsigned)(uintptr_t)_ReturnAddress());
    Ra2ObjectChain state = {g_esi, g_ebx, (int32_t)g_edi, MEM8(frame + 0x88)};
    if (!entry)
    {
        unsigned alternate = MEM8(frame + 0x11);
        ra2_ground_object_chain_begin(&state, alternate, MEM32(g_ebx + 0xE4), MEM32(g_ebx + 0xE8));
        MEM8(frame + 0x88) = (uint8_t)state.pending_contact;
        g_eax = (g_eax & UINT32_C(0xFFFFFF00)) | alternate;
    }
    else
    {
        ra2_ground_object_chain_next(&state, MEM32(g_esi + 0x30), MEM32(frame + 0x7C), (int32_t)MEM32(frame + 0x8C));
    }
    g_esi = (uint32_t)state.object; g_ebx = (uint32_t)state.cell; g_edi = (uint32_t)state.classification;
    g_flag_k = FK_TEST; g_flag_a = g_esi; g_flag_b = g_esi; g_flag_cf = 0;
    return state.object ? 0x70346B : 0x703905;
}

void ra2_ground_passage_return_bridge(unsigned entry)
{
    uint32_t result = entry == 0 ? 0 : entry == 1 ? 7 : entry == 2 ? 5 : entry == 3 ? 2 : g_edi;
    ra2_ground_return_frame(g_esp, RA2_FRAME_PASSAGE, result);
}

typedef struct LayerContext
{
    uint32_t drive, previous, next;
} LayerContext;

static int32_t layer_level(void *opaque, unsigned next)
{
    LayerContext *context = opaque;
    int32_t level = (int8_t)MEM8((next ? context->next : context->previous) + 0x11B);
    if (!next) g_eax = (uint32_t)level;
    else
    {
        g_ecx = (uint32_t)level;
        g_flag_k = FK_CMP;
        g_flag_a = (uint32_t)level;
        g_flag_b = g_eax - 4u;
        g_flag_cf = g_flag_a < g_flag_b;
        g_eax = 0x100u;
    }
    return level;
}

static uint32_t layer_flags(void *opaque, unsigned next)
{
    LayerContext *context = opaque;
    uint32_t flags = MEM32((next ? context->next : context->previous) + 0x140);
    g_flag_k = FK_TEST;
    g_flag_a = flags;
    g_flag_b = 0x100u;
    g_flag_cf = 0;
    return flags;
}

static void layer_set(void *opaque, unsigned upper)
{
    LayerContext *context = opaque;
    uint32_t unit = MEM32(context->drive + 0xC);
    MEM8(unit + 0x79) = (uint8_t)upper;
    if (upper) g_edx = unit;
    else g_eax = unit;
}

uint32_t ra2_ground_template_layer_bridge(void)
{
    LayerContext context = {g_ebp, g_esi, g_ebx};
    Ra2TemplateLayerServices services = {&context, layer_level, layer_flags, layer_set};
    MEM32(g_esp + 0x40) = context.next;
    ra2_ground_template_layer(&services);
    return 0x4A18EF;
}

/* 4A3FE3 internal continuation: neighbor crushing was already resolved. */
#include "ground_template_table.h"
static uint8_t table_byte(void *opaque, int32_t selector, Ra2TemplateByte field)
{
    (void)opaque;
    return MEM8(0x7A0180u+(uint32_t)selector*12u+(field==RA2_TEMPLATE_FLAGS?8u:0u));
}
uint32_t ra2_ground_template_table_bridge(void)
{
    uint32_t selector=g_esi+g_ebx*8u;
    unsigned fallback=!table_byte(NULL,(int32_t)selector,RA2_TEMPLATE_ENTRY_TAG);
    Ra2TemplateServices services={NULL,NULL,table_byte};
    Ra2TemplateSelection result=ra2_ground_template_table((int32_t)g_ebx,(int32_t)g_esi,
        MEM8(g_ebp+0x64),&services);
    MEM8(g_ebp+0x60)=0;
    MEM32(g_ebp+0x58)=(uint32_t)result.selector;
    g_ecx=selector*3u;
    if(fallback)g_edx=g_ebx*9u;
    g_eax=(uint32_t)result.selector*3u;
    g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=(uint32_t)result.flags<<24;
    g_flag_b=8u<<24;g_flag_cf=0;
    return result.flags&8u?0x4A4015:0x4A45B7;
}

#include "ground_sampling_shared.h"
uint32_t ra2_ground_template_index_bridge(void)
{
    uint32_t scaled=g_eax*3u, table=0x7A0180u+scaled*4u;
    unsigned alternate=MEM8(g_ebp+0x60);
    Ra2SamplingTemplate selected={(int8_t)MEM8(table),(int8_t)MEM8(table+1),0};
    g_eax=(uint32_t)ra2_ground_template_index(selected,alternate);
    g_ecx=(scaled&UINT32_C(0xFFFFFF00))|alternate;
    g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=alternate<<24;g_flag_b=alternate<<24;g_flag_cf=0;
    return 0x4A2311;
}

uint32_t ra2_ground_sample_anchor_bridge(void)
{
    uint32_t position=MEM32(g_ebp+0xC)+0x88u;
    /* Keep each load adjacent to its store: the sample can alias the saved anchor. */
    MEM32(g_esp+0x80)=MEM32(position);
    MEM32(g_esp+0x84)=MEM32(position+4);
    MEM32(g_esp+0x88)=MEM32(position+8);
    g_ecx=MEM32(g_ecx+8);
    MEM32(g_esp+0x34)=g_ecx;
    g_eax=position;
    g_esi=MEM32(position);g_ebx=MEM32(position+4);g_edx=MEM32(position+8);
    g_flag_k=FK_ADD;g_flag_a=position-0x88u;g_flag_b=0x88u;
    g_flag_cf=position<position-0x88u;
    return 0x4A237D;
}
