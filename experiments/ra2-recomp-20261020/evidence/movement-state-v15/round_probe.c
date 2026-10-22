#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "x87_arithmetic.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))



static int32_t original_convert(int32_t integer,double coefficient,uint16_t arithmetic,uint16_t conversion,uint16_t *after)
{
    int32_t result;uint16_t saved;
    MEM32(0x7D8964)=conversion;
    __asm {
        fnstcw saved
        fldcw arithmetic
        fild integer
        fmul coefficient
        mov eax,77F110h
        call eax
        mov result,eax
        fnstcw arithmetic
        fldcw saved
    }
    *after=arithmetic;return result;
}
int main(int argc,char **argv)
{
    if(argc!=2) return 2;hold_image();map_original_image(argv[1]);
    const uint16_t pc[]={0x7F,0x27F,0x37F};
    const double coefficients[]={0,0.5,-0.5,1.0,-1.0,0.33333333333333331,1.0000000000000002,0.99999999999999989,1.5,-1.5,127.99999999999999,255.5};
    for(unsigned n=0;n<131072;++n)
    {
        int32_t value=(int32_t)(n%65536)-32768;
        double coefficient=coefficients[(n/13)%12];
        uint16_t arithmetic=(uint16_t)(pc[n%3]|((n/3)%4)<<10);
        uint16_t conversion=(uint16_t)(0x37F|((n/36)%4)<<10),after=0;
        int32_t expected=original_convert(value,coefficient,arithmetic,conversion,&after);
        Ra2LegacyReal real=ra2_real_multiply(ra2_real_from_i32(value),ra2_real_from_f64(coefficient),arithmetic);
        int32_t actual=ra2_real_round_i32(real,conversion);
        if(actual!=expected || after!=conversion) {printf("round mismatch %u value=%d a=%x c=%x actual=%d expected=%d\n",n,value,arithmetic,conversion,actual,expected);return 1;}
    }
    puts("{\"passed\":true,\"round_cases\":131072,\"precision_modes\":3,\"rounding_modes\":4,\"original_ftol\":true}");return 0;
}
