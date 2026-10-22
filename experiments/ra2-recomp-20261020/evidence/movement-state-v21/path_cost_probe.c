#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_cost.h"
#include "native_probe_host.h"

static uint32_t bits(float value) { uint32_t result;memcpy(&result,&value,4);return result; }
static float value(uint32_t raw) { float result;memcpy(&result,&raw,4);return result; }

static float original_accumulate(float previous,float step,uint16_t control)
{
    uint32_t parent[4]={0,bits(previous),0,0},node[4]={0};uint16_t saved;
    __asm {
        fnstcw saved
        fldcw control
        push ebx
        push esi
        lea ebx,parent
        lea esi,node
        sub esp,32
        mov eax,dword ptr step
        mov [esp+28],eax
        mov eax,427E09h
        call eax
        add esp,32
        pop esi
        pop ebx
        fldcw saved
    }
    return value(node[1]);
}

int main(int argc,char **argv)
{
    if(argc!=2) return 2;hold_image();map_original_image(argv[1]);
    const unsigned char original[]={0xD9,0x44,0x24,0x20,0xD8,0x43,0x04,0xD9,0x5E,0x04};
    if(memcmp((void *)0x427E09,original,sizeof(original)))return 2;
    /* 仅测试进程映射中的原版十字节算术片段，结束处置 ret；磁盘原版不变。 */
    *(unsigned char *)0x427E13=0xC3;
    const uint16_t pc[]={0x7F,0x27F,0x37F};
    const uint32_t edges[]={0,0x3F800000,0x3F80C49B,0x3F80C49C,0x3F80A3D7,0x3F801062,0x3F7FFFFF,0x3F800001,0x447A0000,0x40A00000,0x3727C5AC,0x3B83126F};
    uint32_t random=12345;unsigned count=0;
    for(unsigned n=0;n<65536;++n)
    {
        random=random*1664525u+1013904223u;
        /* 覆盖 0..32768 的有限正常寻路代价、相邻 float 和小步长。 */
        float prior=n<4096?value(edges[n%12]):value(0x3A800000u+(random%0x0C000000u));
        float step=value(edges[(n/12)%12]);
        for(unsigned precision=0;precision<3;++precision)for(unsigned round=0;round<4;++round)
        {
            uint16_t control=(uint16_t)(pc[precision]|(round<<10));
            float expected=original_accumulate(prior,step,control);
            float actual=ra2_ground_accumulate_path_cost(prior,step,control);++count;
            if(bits(actual)!=bits(expected))
            {printf("mismatch n=%u cw=%x prior=%x step=%x actual=%x expected=%x\n",n,control,bits(prior),bits(step),bits(actual),bits(expected));return 1;}
        }
    }
    puts("{\"passed\":true,\"cases\":786432,\"precision_modes\":3,\"rounding_modes\":4,\"original_fragment\":\"427E09..427E13\",\"finite_nonnegative_costs_only\":true}");
    return count==786432?0:2;
}
