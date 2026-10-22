#include <stdint.h>
#include <string.h>
#include "recomp_types.h"
#include "walk_movement.h"
#include "walk_movement_bridge.h"

static double read_double(uint32_t address)
{double result;memcpy(&result,(const void *)(uintptr_t)ADDR(address),8);return result;}

void ra2_walk_axis_bridge(unsigned subtract_step)
{
    uint32_t stack=g_esp;
    /* 71F3F2 的 Y 分支仍留有 8 字节参数；71F40C 的 X 分支先消费两次数学调用的 16 字节参数。 */
    double speed=read_double(stack+(subtract_step?0x24:0x2C));
    int32_t origin=subtract_step?(int32_t)read_double(stack+0x1C):(int32_t)MEM32(stack+0x4C);
    uint16_t conversion=(uint16_t)MEM32(0x7D8964),arithmetic=g_fpu_cw;
    int32_t result=ra2_walk_advance_axis(origin,g_st[0],speed,subtract_step,arithmetic,conversion);
    fp_pop_impl(g_st,&g_fp_top);
    if(!subtract_step)g_esp+=16;
    /* 复现原版 __ftol 的寄存器、控制字、栈内结果与最后 add esp,12 的标志。 */
    MEM16(g_esp-16)=arithmetic;
    if(arithmetic!=conversion)MEM32(g_esp-16)=conversion;
    MEM32(g_esp-12)=(uint32_t)result;
    MEM32(g_esp-8)=result<0?UINT32_MAX:0;
    g_eax=(uint32_t)result;g_edx=result<0?UINT32_MAX:0;g_fpu_cw=conversion;
    g_flag_k=FK_ADD;g_flag_a=g_esp-16;g_flag_b=12;g_flag_cf=(g_esp-4)<(g_esp-16);
}
