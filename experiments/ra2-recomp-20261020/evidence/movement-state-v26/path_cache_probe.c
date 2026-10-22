#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_cost.h"
#include "ground_path_cache.h"
#include "native_probe_host.h"
static uint32_t bits(float f){uint32_t b;memcpy(&b,&f,4);return b;}
static float from_bits(uint32_t b){float f;memcpy(&f,&b,4);return f;}
static float original_step(double traversal,float weight,float bias,uint16_t control)
{
    float context[2]={0,weight};uint32_t result;uint16_t saved;
    *(float *)0x7CF0DC=bias;
    __asm {
        fnstcw saved
        fldcw control
        push esi
        lea esi,context
        fld traversal
        sub esp,64
        mov dword ptr [esp+20],0
        mov eax,42786Ch
        call eax
        mov eax,[esp+48]
        add esp,64
        pop esi
        mov result,eax
        fldcw saved
    }
    return from_bits(result);
}
#pragma warning(push)
#pragma warning(disable:4731) /* EBP 仅在映射原版片段期间置零，push/pop 成对恢复；禁止内联。 */
static __declspec(noinline) int original_cache(float cached,float parent,double epsilon,uint16_t control)
{
    float node[2]={0,parent};uint32_t status;uint16_t saved;
    memcpy((void *)0x79C4D0,&epsilon,8);
    __asm {
        fnstcw saved
        fldcw control
        lea edx,node
        lea eax,cached
        push ebp
        xor ebp,ebp
        mov ecx,4277C6h
        call ecx
        pop ebp
        mov status,eax
        fldcw saved
    }
    if(status&0x400)return 2;
    return status&0x100?-1:status&0x4000?0:1;
}
#pragma warning(pop)
static float original_priority(double distance,float accumulated,uint16_t control)
{
    float result;uint16_t saved;
    __asm {
        fnstcw saved
        fldcw control
        fld distance
        fadd accumulated
        fstp result
        fldcw saved
    }
    return result;
}
int main(int argc,char **argv)
{
    if(argc!=2)return 2;hold_image();map_original_image(argv[1]);
    const unsigned char step_start[]={0xD8,0x4E,0x04,0x8B,0x44,0x24,0x18};
    const unsigned char cache_start[]={0xD9,0x42,0x04,0xDC,0x05,0xD0,0xC4,0x79,0};
    if(memcmp((void *)0x42786C,step_start,sizeof(step_start)) || memcmp((void *)0x4277C6,cache_start,sizeof(cache_start)))return 2;
    *(unsigned char *)0x42787E=0xC3;*(unsigned char *)0x4277D6=0xC3;
    const uint16_t pc[]={0x7F,0x27F,0x37F};unsigned count=0;uint32_t random=12345;
    const double epsilons[]={0,0.004,0.000001,0.25};
    for(unsigned n=0;n<65536;++n)for(unsigned p=0;p<3;++p)for(unsigned rc=0;rc<4;++rc)
    {
        random=random*1664525u+1013904223u;uint16_t cw=(uint16_t)(pc[p]|(rc<<10));
        float a=from_bits(0x3E800000u+random%0x06000000u),weight=from_bits(0x3F000000u+(random>>9)%0x01000000u);
        float bias=from_bits(0x38800000u+(random>>2)%0x03000000u);double traversal=(double)a;
        float expected=original_step(traversal,weight,bias,cw),actual=ra2_ground_score_path_step(traversal,weight,bias,cw);
        if(bits(expected)!=bits(actual)){printf("step mismatch %u cw=%x\n",n,cw);return 1;}
        float cached=n%3==0?a:n%3==1?from_bits(bits(a)+1):from_bits(bits(a)-1);double epsilon=epsilons[n%4];
        int e=original_cache(cached,a,epsilon,cw),v=ra2_ground_path_cache_compare(cached,a,epsilon,cw);
        if(e!=v){printf("cache mismatch %u cw=%x expected=%d actual=%d\n",n,cw,e,v);return 1;}
        expected=original_priority(traversal,bias,cw);actual=ra2_ground_path_priority(traversal,bias,cw);
        if(bits(expected)!=bits(actual)){printf("priority mismatch %u cw=%x\n",n,cw);return 1;}
        ++count;
    }
    printf("{\"passed\":true,\"step_cases\":%u,\"cache_cases\":%u,\"priority_cases\":%u,\"mapped_original_step_and_cache\":true,\"priority_original_instruction_sequence\":true}\n",count,count,count);return 0;
}
