#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "combat_damage_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static unsigned char wh[0x180],rules[0x1400],session[16],stack_data[8192];
static uint32_t entry,host_stack,number,n_eax,n_ecx,n_edx,n_ebx,n_esi,n_edi,n_ebp,n_esp,n_flags;
static uint16_t n_control;
static int32_t incoming;
#define PTR(p) ((uint32_t)(uintptr_t)(p))
static __declspec(naked) void capture(void)
{
    __asm {
        mov n_eax,eax
        mov n_ecx,ecx
        mov n_edx,edx
        mov n_ebx,ebx
        mov n_esi,esi
        mov n_edi,edi
        mov n_ebp,ebp
        mov n_esp,esp
        mov esp,host_stack
        pushfd
        pop n_flags
        fnstcw n_control
        popad
        popfd
        ret
    }
}
static __declspec(naked) void original(void)
{
    __asm {
        pushfd
        pushad
        mov host_stack,esp
        mov esp,entry
        mov ecx,incoming
        mov edx,offset wh
        cmp number,262144
        jae present
        // 空弹头与禁用/零值也必须覆盖真实原版提前返回。
        mov eax,number
        and eax,31
        jnz present
        xor edx,edx
present:
        mov eax,47E1C0h
        mov ebx,13579BDFh
        mov esi,2468ACE0h
        mov edi,11223344h
        mov ebp,55667788h
        jmp eax
    }
}
static void setup(unsigned n)
{
    number=n;memset(wh,0,sizeof(wh));memset(rules,0,sizeof(rules));memset(session,0,sizeof(session));memset(stack_data,0xA5,sizeof(stack_data));
    entry=PTR(stack_data)+4096;MEM32(entry)=PTR(capture);MEM32(entry+4)=(n/17)%11;
    const int32_t damages[]={0,-1,-50,1,7,65,200,10000,16777217,INT32_MAX,INT32_MIN};incoming=damages[n%11];
    const float spreads[]={0,.0001f,.1f,.3f,.5f,1,1.5f,2,3,5};float spread=spreads[(n/11)%10];memcpy(wh+0x124,&spread,4);
    const float edges[]={0,.25f,.5f,.9f,1,1.25f};float edge=edges[(n/110)%6];memcpy(wh+0x12C,&edge,4);
    const double verses[]={0,.01,.25,.5,.75,1,1.3,1.5,3};
    for(unsigned a=0;a<11;++a){double v=verses[(n/660+a)%9];memcpy(wh+0xA0+a*8,&v,8);}
    const int32_t distances[]={0,1,7,8,25,76,127,128,255,256,257,384,511,512,513,1024,-1};MEM32(entry+8)=(uint32_t)distances[(n/37)%17];
    const int32_t caps[]={0,1,100,10000,INT32_MAX};MEM32(PTR(rules)+0x1330)=(uint32_t)caps[(n/71)%5];
    MEM32(0x839848)=PTR(rules);MEM32(0xA3D290)=PTR(session);session[0]=(uint8_t)(n%23==0?0x20:0);
    const uint16_t precision[]={0,0x200,0x300};uint16_t control=(uint16_t)(0x7F|precision[(n/1024)%3]|(((n/3072)%4)<<10));
    const uint16_t conversions[]={0xE7F,0xF7F,0xC7F,0xE7F,0x27F,0x67F,0xA7F};MEM32(0x7D8964)=conversions[(n/97)%7];
    if(n>=262144) {
        incoming=200;MEM32(entry+4)=3;MEM32(entry+8)=37;session[0]=0;
        float one=1;memcpy(wh+0x124,&one,4);memcpy(wh+0x12C,&one,4);
        double coefficient=n==262144?0.8999999999999999:0.9;memcpy(wh+0xB8,&coefficient,8);
        MEM32(PTR(rules)+0x1330)=10000;control=0xE7F;MEM32(0x7D8964)=control;
    }
    __asm {fldcw control}
    g_fpu_cw=control;
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    unsigned zero=0,healing=0,positive=0,changed_control=0,nonzero=0,neighbors[2]={0};const unsigned offsets[]={0,4,8,12,16,24,28};
    for(unsigned n=0;n<262146;++n) {
        setup(n);original();uint32_t expected[7];for(unsigned k=0;k<7;++k)expected[k]=MEM32(entry-20+offsets[k]);
        setup(n);uint16_t before=g_fpu_cw;
        g_eax=0;g_ecx=(uint32_t)incoming;g_edx=(n%32 || n>=262144)?PTR(wh):0;g_esp=entry;g_ebx=0x13579BDF;g_esi=0x2468ACE0;g_edi=0x11223344;g_ebp=0x55667788;
        ra2_combat_damage_bridge();uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,1);
        int bad=g_eax!=n_eax || g_ecx!=n_ecx || g_edx!=n_edx || g_esp!=n_esp || g_ebx!=n_ebx || g_esi!=n_esi || g_edi!=n_edi || g_ebp!=n_ebp || ((flags^n_flags)&0x8D5) || ((g_fpu_cw^n_control)&0x1F3F);
        for(unsigned k=0;k<7;++k)if(expected[k]!=MEM32(entry-20+offsets[k]))bad=1;
        if(bad) {
            printf("damage mismatch n=%u damage=%d distance=%d eax=%x/%x cx=%x/%x dx=%x/%x cw=%x/%x flags=%x/%x\n",n,incoming,(int32_t)MEM32(entry+8),g_eax,n_eax,g_ecx,n_ecx,g_edx,n_edx,g_fpu_cw,n_control,flags,n_flags);
            for(unsigned k=0;k<7;++k)if(expected[k]!=MEM32(entry-20+offsets[k]))printf(" local %x=%x/%x\n",offsets[k],MEM32(entry-20+offsets[k]),expected[k]);
            return 1;
        }
        if(incoming==0 || session[0] || (n%32==0 && n<262144))++zero;else if(incoming<0)++healing;else ++positive;
        if(n>=262144)neighbors[n-262144]=g_eax;
        if((before^g_fpu_cw)&0x1F3F)++changed_control;
        if(g_eax)++nonzero;
    }
    if(neighbors[0]!=179 || neighbors[1]!=180)return 1;
    printf("{\"passed\":true,\"damage_cases\":262146,\"zero_or_rejected\":%u,\"healing_cases\":%u,\"positive_cases\":%u,\"control_changed\":%u,\"nonzero_results\":%u,\"coefficient_neighbor_cases\":2,\"neighbor_results\":[179,180],\"actual_original_damage_and_ftol\":true,\"armor_slots\":11,\"mocked_damage_math\":false,\"state_abi_flags_and_control_verified\":true}\n",zero,healing,positive,changed_control,nonzero);
    return 0;
}
