#include <string.h>
#include "recomp_types.h"
#include "ground_connection_numeric.h"
#include "ground_connection_trig.h"
#include "ground_connection_numeric_bridge.h"

static double number_at(uint32_t address)
{ double value; memcpy(&value, (void *)(uintptr_t)ADDR(address), sizeof(value)); return value; }
void ra2_ground_connection_numeric_bridge(unsigned axis)
{
    uint32_t f = g_esp;
    if (axis == 2 || axis == 7)
    {
        if (axis == 7) MEM32(f + 0x18) = g_ecx;
        double angle = ra2_ground_connection_angle((int32_t)MEM32(f + (axis == 7 ? 0x28 : 0x30)), number_at(0x79B620), g_fpu_cw);
        memcpy((void *)(uintptr_t)ADDR(f + 0x40), &angle, sizeof(angle)); return;
    }
    if (axis == 3 || axis == 4)
    {
        int cosine = axis == 4; float scale;
        memcpy(&scale, (void *)(uintptr_t)ADDR(cosine ? 0x7D804C : 0x7D8048), sizeof(scale));
        float value = ra2_ground_connection_component(number_at(f), scale,
            (const float *)(uintptr_t)ADDR(0x801DC4), cosine, g_fpu_cw);
        fp_push_impl(g_st, &g_fp_top, (double)value); g_fpu_cw = MEM16(0x7D8964); return;
    }
    int x_axis = axis == 1 || axis == 6;
    double component = fp_pop_impl(g_st, &g_fp_top);
    double distance = number_at(f + (axis == 5 ? 0x20 : axis == 6 ? 0x28 : x_axis ? 0x38 : 0x30));
    double origin = x_axis ? (double)(int32_t)MEM32(f + 0x84) : number_at(f + (axis == 5 ? 0x30 : 0x38));
    g_eax = (uint32_t)ra2_ground_connection_axis(origin, distance, component, !x_axis, g_fpu_cw);
    g_fpu_cw = MEM16(0x7D8964);
    if (x_axis)
    {
        g_esp = f + 0x10; g_flag_k = FK_ADD; g_flag_a = f; g_flag_b = 0x10; g_flag_cf = g_esp < f;
    }
}
