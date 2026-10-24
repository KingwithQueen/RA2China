#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "native_probe_host.h"
static void call_ctor(void *event, uint32_t actor, uint32_t target)
{
    __asm {
        mov ecx, event
        push 0
        push 0
        push 0
        push 0
        push 34h
        push target
        push 8
        push 34h
        push actor
        push 0
        mov eax, 4B6170h
        call eax
    }
}
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image(); map_original_image(argv[1]);
    for (unsigned n=0;n<64;++n)
    {
        unsigned char native[111]={0}, expected[111]={0};
        uint32_t frame=100u+n*101u, actor=1023364u+n, target=1023367u+n;
        *(uint32_t *)0xA40D2C=frame;
        call_ctor(native,actor,target);
        expected[0]=4; memcpy(expected+3,&frame,4);memcpy(expected+7,&actor,4);
        expected[11]=0x34;expected[12]=8;memcpy(expected+0x0E,&target,4);expected[0x12]=0x34;
        if(memcmp(native,expected,111)){printf("capture packet mismatch %u\n",n);return 1;}
    }
    puts("{\"passed\":true,\"native_capture_constructor_cases\":64,\"all_111_bytes_equal\":true}");
    return 0;
}
