#include <stdint.h>
#include <string.h>
#include "recomp_types.h"
#include "unit_movement.h"
#include "movement_bridge.h"
#include "state_trace.h"

/* 原始地址/寄存器约定只保留在此适配层；gameplay/unit_movement.c 不依赖游戏内存布局。 */
static Ra2WorldPoint read_point(uint32_t address)
{
    Ra2WorldPoint point;
    memcpy(&point, (const void *)(uintptr_t)ADDR(address), sizeof(point));
    return point;
}

uint32_t ra2_movement_progress_bits(int32_t progress, uint16_t control)
{
    float fraction = ra2_ground_progress_fraction(progress, &ra2_original_ground_path_sampling, control);
    uint32_t bits;
    memcpy(&bits, &fraction, sizeof(bits));
    return bits;
}

void ra2_movement_interpolate_bridge(void)
{
    uint32_t stack = g_esp, output = g_ecx, source = g_edx;
    uint32_t target = MEM32(stack + 4);
    float fraction;
    memcpy(&fraction, (const void *)(uintptr_t)ADDR(stack + 8), sizeof(fraction));
    uint16_t conversion_control = MEM16(0x7D8964);
    ra2_state_math(stack, g_ebp, output, source);
    Ra2WorldPoint result = ra2_ground_interpolate_position(read_point(source), read_point(target), fraction,
        g_fpu_cw, conversion_control);
    memcpy((void *)(uintptr_t)ADDR(output), &result, sizeof(result));
    g_eax = output;
    g_ecx = output;
    g_edx = (uint32_t)result.y;
    g_fpu_cw = conversion_control;
    /* 原版末尾 add esp, 12 的返回标志；ret 8 同时弹出返回地址及两个实参。 */
    g_flag_k = FK_ADD;
    g_flag_a = stack - 12;
    g_flag_b = 12;
    g_flag_cf = stack < stack - 12;
    g_esp = stack + 12;
}

void ra2_movement_transform_bridge(void)
{
    uint32_t stack = g_esp, drive = g_ecx;
    uint32_t output = MEM32(stack + 4), sample = MEM32(stack + 8), direction_address = MEM32(stack + 12);
    uint32_t selector = MEM32(drive + 0x58), direction = MEM32(direction_address);
    uint32_t flags = MEM32(0x7A0188 + selector * 12);
    Ra2WorldPoint local = { (int32_t)MEM32(sample), (int32_t)MEM32(sample + 4), 0 };
    Ra2WorldPoint origin = { (int32_t)MEM32(drive + 0x40), (int32_t)MEM32(drive + 0x44), 0 };
    Ra2WorldPoint result = ra2_ground_transform_path_sample(local, origin, flags, &direction);
    MEM32(direction_address) = direction;
    MEM32(output) = (uint32_t)result.x;
    MEM32(output + 4) = (uint32_t)result.y;
    /* 原版只处理平面坐标；输出的 Z 字段和四个被调用方保存寄存器保持原值。 */
    g_eax = output;
    g_ecx = (uint32_t)result.y;
    g_edx = (uint32_t)result.x;
    g_flag_k = FK_ADD;
    g_flag_a = (uint32_t)origin.y;
    g_flag_b = (uint32_t)result.y - (uint32_t)origin.y;
    g_flag_cf = (uint32_t)result.y < (uint32_t)origin.y;
    g_esp = stack + 16;
}
