#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_cell_services.h"
#include "ground_services_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
static uint32_t slots[262144],map_data[0x140/4],saved_stack,native_stack;
static uint32_t native_result,native_bx,native_si,native_di,native_bp;
static uint32_t native_cx,native_dx,native_flags,adapter_stack[8];
static unsigned char cell_data[0x150];
static Ra2ServiceCell input;
static unsigned adjust;
static __declspec(naked) void original(void)
{
    __asm {
        pushfd
        pushad
        mov saved_stack,esp
        mov ecx,offset map_data
        mov ebx,12345678h
        mov esi,23456789h
        mov edi,3456789Ah
        mov ebp,456789ABh
        push adjust
        push offset input
        mov eax,55A660h
        call eax
        mov native_result,eax
        mov native_cx,ecx
        mov native_dx,edx
        pushfd
        pop native_flags
        mov native_stack,esp
        mov native_bx,ebx
        mov native_si,esi
        mov native_di,edi
        mov native_bp,ebp
        mov esp,saved_stack
        popad
        popfd
        ret
    }
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    *(uint32_t *)0x832618=(uint32_t)(uintptr_t)slots;
    unsigned accepted=0,rejected=0,sloped=0,missing=0;
    for(unsigned n=0;n<131072;++n) {
        int32_t width=(int32_t[]){55,64,128,511}[n/32768];
        Ra2MapArea area={width,(int32_t)(n%7),(int32_t)(n%11),width-4,(int32_t)(40+n%127)};
        map_data[0xF0/4]=(uint32_t)area.width;map_data[0xF8/4]=(uint32_t)area.local_x;
        map_data[0xFC/4]=(uint32_t)area.local_y;map_data[0x100/4]=(uint32_t)area.local_width;map_data[0x104/4]=(uint32_t)area.local_height;
        input=(Ra2ServiceCell){(int16_t)((int)(n%401)-80),(int16_t)((int)((n*31)%401)-80)};
        /* 包含实际地图四个拒绝目标及严格边界两侧，避免只得到远离地图的负例。 */
        if(n<16) {
            area=(Ra2MapArea){55,2,5,51,89};map_data[0xF0/4]=55;map_data[0xF8/4]=2;map_data[0xFC/4]=5;map_data[0x100/4]=51;map_data[0x104/4]=89;
            const Ra2ServiceCell real_targets[]={{63,114},{63,116},{64,116},{65,116},
                {66,110},{67,112},{67,116},{68,118}};
            input=n<8 ? real_targets[n]:(Ra2ServiceCell){(int16_t)(63+n%5),(int16_t)(112+n%6)};
        }
        adjust=n%3 ? 1:0;
        int32_t slot=(int32_t)input.y*512+input.x;
        int present=slot>=0 && slot<262144 && n%5;
        if(slot>=0 && slot<262144)slots[slot]=present?(uint32_t)(uintptr_t)cell_data:0;
        int8_t level=n<16?4:(int8_t)(n>>7),fallback_level=n<16?4:(int8_t)(n>>9);uint8_t slope=n<16?0:(uint8_t)(n&4);
        cell_data[0x11B]=(uint8_t)level;cell_data[0x11C]=slope;
        *(uint8_t *)(0xA6F9F8+0x11B)=(uint8_t)fallback_level;*(uint8_t *)(0xA6F9F8+0x11C)=slope;
        *(uint32_t *)0xA6FA1C=0x12345678;
        uint16_t before,after;__asm fnstcw before
        original();__asm fnstcw after
        int actual=ra2_cell_usable_area(&area,input,adjust?(present?level:fallback_level):0,adjust?slope:0);
        if(n<8 && actual!=(n>=4))return 1;
        uint32_t expected_fallback=*(uint32_t *)0xA6FA1C;
        *(uint32_t *)0xA6FA1C=0x12345678;
        g_eax=0;g_ecx=(uint32_t)(uintptr_t)map_data;g_edx=0;
        g_ebx=0x12345678;g_esi=0x23456789;g_edi=0x3456789A;g_ebp=0x456789AB;
        g_esp=(uint32_t)(uintptr_t)adapter_stack;adapter_stack[1]=(uint32_t)(uintptr_t)&input;adapter_stack[2]=adjust;
        ra2_cell_map_area_bridge();
        uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,1);
        if(actual!=(int)(native_result&255u) || native_stack!=saved_stack || before!=after
            || native_bx!=0x12345678 || native_si!=0x23456789 || native_di!=0x3456789A || native_bp!=0x456789AB
            || g_eax!=native_result || g_ecx!=native_cx || g_edx!=native_dx
            || g_esp!=(uint32_t)(uintptr_t)adapter_stack+12 || (flags&0x8D5)!=(native_flags&0x8D5)
            || g_ebx!=native_bx || g_esi!=native_si || g_edi!=native_di || g_ebp!=native_bp
            || *(uint32_t *)0xA6FA1C!=expected_fallback) {
            printf("map area mismatch %u value=%d/%u\n",n,actual,native_result&255u);return 1;
        }
        if(adjust && !present) {
            if(memcmp((void *)0xA6FA1C,&input,sizeof(input)))return 1;
            ++missing;
        }
        if(actual)++accepted;else ++rejected;
        if(adjust && slope)++sloped;
        if(slot>=0 && slot<262144)slots[slot]=0;
    }
    printf("{\"passed\":true,\"map_area_cases\":131072,\"accepted\":%u,\"rejected\":%u,\"sloped\":%u,\"missing_cell_cases\":%u,\"pure_rule_and_adapter_registers_flags_stack_fallback_verified\":true,\"original_cw_verified\":true}\n",accepted,rejected,sloped,missing);
    return 0;
}
