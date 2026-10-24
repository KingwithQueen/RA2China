#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "walk_movement.h"
#include "native_probe_host.h"
static int32_t original_axis(int32_t origin,double component,double speed,unsigned subtract_step,uint16_t arithmetic,uint16_t conversion,uint16_t *after)
{
    int32_t result;double base=(double)origin;uint16_t saved,observed;
    *(uint32_t *)0x7D8964=conversion;
    __asm {
        fnstcw saved
        fldcw arithmetic
        fld component
        fmul speed
        cmp subtract_step,0
        je add_axis
        fsubr base
        jmp convert_axis
    add_axis:
        fiadd origin
    convert_axis:
        mov eax,77F110h
        call eax
        mov result,eax
        fnstcw observed
        fldcw saved
    }
    *after=observed;return result;
}
int main(int argc,char **argv)
{
    if(argc!=2)return 2;hold_image();map_original_image(argv[1]);
    const uint16_t precisions[]={0x7F,0x27F,0x37F};
    const double components[]={0,1,-1,0.7071067811865475,-0.7071067811865475,0x1p-52,-0x1p-52,0x1p-60,-0x1p-60,0.9999999999999999,-0.9999999999999999};
    const double speeds[]={0,1,10,18,32,0.5,127.25};unsigned total=0;
    for(unsigned n=0;n<65536;++n)for(unsigned mode=0;mode<2;++mode)for(unsigned pc=0;pc<3;++pc)for(unsigned rc=0;rc<4;++rc)
    {
        int32_t origin=(int32_t)((n*7919u)%262144u)-131072;
        double c=components[n%11],speed=speeds[(n/11)%7];
        uint16_t arithmetic=(uint16_t)(precisions[pc]|(rc<<10)),conversion=(uint16_t)(0x37F|(((n/77)%4)<<10)),after;
        int32_t expected=original_axis(origin,c,speed,mode,arithmetic,conversion,&after);
        int32_t actual=ra2_walk_advance_axis(origin,c,speed,mode,arithmetic,conversion);++total;
        if(actual!=expected || after!=conversion){printf("mismatch %u mode=%u pc=%x rc=%x origin=%d actual=%d expected=%d\n",n,mode,arithmetic,conversion,origin,actual,expected);return 1;}
    }
    printf("{\"passed\":true,\"cases\":%u,\"precision_modes\":3,\"rounding_modes\":4,\"original_ftol\":true,\"scope\":\"finite bounded inputs, original arithmetic instruction sequence\"}\n",total);return 0;
}
