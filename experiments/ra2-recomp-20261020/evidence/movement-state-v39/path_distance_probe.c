#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_distance.h"
#include "native_probe_host.h"
static uint32_t host_stack,guest_stack,entry;
static uint32_t stack_memory[128],references[1];
static unsigned char cell[0x148];
static Ra2PathPoint target;
static double original_argument;
static __declspec(naked) void original_fragment(void)
{
    __asm {
        pushad
        mov host_stack,esp
        mov esp,guest_stack
        lea eax,returned
        mov [esp],eax
        mov eax,entry
        jmp eax
    returned:
        mov esp,host_stack
        popad
        ret
    }
}
static __declspec(naked) void capture_argument(void)
{
    __asm {
        fld qword ptr [esp]
        fstp original_argument
        add esp,8
        ret
    }
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    uint32_t *frame=stack_memory+32;guest_stack=(uint32_t)(uintptr_t)frame;
    unsigned char patch[5]={0xE9};int32_t jump=(int32_t)((uintptr_t)capture_argument-0x427E75);
    memcpy(patch+1,&jump,4);memcpy((void *)0x427E70,patch,5);*(unsigned char *)0x4278C7=0xC3;
    references[0]=(uint32_t)(uintptr_t)cell;uint32_t random=12345;unsigned cases=0;
    for(unsigned n=0;n<131072;++n) {
        Ra2PathPoint from;
        random=random*1664525u+1013904223u;memcpy(&from,&random,4);
        random=random*1664525u+1013904223u;memcpy(&target,&random,4);
        memcpy(cell+0x24,&from,4);frame[0x18/4]=(uint32_t)(uintptr_t)references;frame[0x1C/4]=(uint32_t)(uintptr_t)&target;
        entry=0x427E2A;original_fragment();double actual=(double)ra2_path_squared_distance(from,target);
        if(memcmp(&actual,&original_argument,8) || frame[0x18/4]!=(uint32_t)(int32_t)actual)return 1;
        frame[0x20/4]=(uint32_t)(uintptr_t)references;frame[0x30/4]=(uint32_t)(uintptr_t)&target;
        entry=0x427880;original_fragment();float distance=ra2_path_connection_distance(from,target);
        if(memcmp(&distance,&frame[0x34/4],4))return 1;
        ++cases;
    }
    printf("{\"passed\":true,\"distance_cases\":%u,\"connection_cases\":%u}\n",cases,cases);return 0;
}
