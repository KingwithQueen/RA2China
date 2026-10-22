#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_collision_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))


static unsigned char unit[0x700],cell[0x200],type[0x700],stack_data[8192];
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control,native_esi,native_edi;
static uint32_t frame,entry_object,entry_address=0x703905;
recomp_func_t recomp_lookup_manual(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
void ra2_state_movement_audit(unsigned a,uint32_t b,uint32_t c,uint32_t d) {(void)a;(void)b;(void)c;(void)d;}
static void patch(uint32_t a,uint32_t b) { MEM8(a)=0xE9; MEM32(a+1)=b-a-5; }
static __declspec(naked) void trap(void)
{
    __asm {
        mov native_esp,esp
        mov native_ebp,ebp
        mov native_esi,esi
        mov native_edi,edi
        fnstcw word ptr native_control
        mov esp,host_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}
static __declspec(naked) void run_original(void)
{
    __asm {
        push ebp
        push ebx
        push esi
        push edi
        mov host_stack,esp
        fninit
        mov esp,frame
        lea ebp,unit
        mov esi,entry_object
        lea ebx,cell
        mov edi,dword ptr [esp+8Ch]
        jmp entry_address
    }
}


int main(int argc,char **argv) {
    if(argc!=2) return 2;hold_image();map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);if(!stubs) return 2;
    const uint32_t boundaries[]={0x703AA9,0x703940};
    for(unsigned i=0;i<2;++i) {
        unsigned char *s=stubs+i*16;s[0]=0xC7;s[1]=5;uint32_t dest=P(&native_resume);memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4);s[10]=0xE9;uint32_t rel=P(trap)-P(s+15);memcpy(s+11,&rel,4);patch(boundaries[i],P(s));
    }
    unsigned blocked=0,upper=0,unordered=0;
    for(unsigned n=0;n<65536;++n) {
        uint32_t edge[]={0,0x80000000,1,0x80000001,0x3F800000,0xBF800000,0x7F800000,0xFF800000,0x7FC00000,0x7F800001};
        uint32_t bits=n%3 ? edge[(n/3)%10] : n*1664525u+1013904223u;
        memset(stack_data,0xA5,sizeof(stack_data));frame=P(stack_data+4096);
        MEM8(frame+0x11)=(uint8_t)((n>>7)&1);MEM32(frame+0x8C)=n%8;MEM32(frame+0x7C)=P(cell);
        F(unit,0x5AC)=P(type);F(type,0x5A4)=n%9;F(cell,0xEC)=(n/9)%10;
        MEM32(0x850EA0+((n/9)%10*9+n%9)*4)=bits;
        run_original();g_esp=frame;g_ebp=P(unit);g_ebx=P(cell);g_edi=n%8;
        int result=ra2_ground_terrain_tail_bridge();
        if((native_resume==0x703940)!=result || g_esp!=native_esp) {printf("tail mismatch %u bits=%x result=%d resume=%x\n",n,bits,result,native_resume);return 1;}
        blocked+=result!=0;upper+=MEM8(frame+0x11)!=0;unordered+=(bits&0x7FFFFFFF)>0x7F800000;
    }
    printf("{\"passed\":true,\"terrain_tail_cases\":65536,\"blocked\":%u,\"upper_layer\":%u,\"unordered_inputs\":%u}\n",blocked,upper,unordered);return 0;
}
