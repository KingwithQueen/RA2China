#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "combat_health_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static unsigned char actor[0x700],type_data[0x300],warhead[0x200],rules[0x1500],private_stack[8192];
static uint32_t table[0x140/4],entry_stack,frame,host_stack,number,type_calls,count,records[16][6];
static uint32_t native_resume,native_eax,native_cx,native_dx,native_bx,native_si,native_di,native_bp,native_sp,native_flags;
static uint16_t native_control,initial_control;
static int32_t damage,effective;
#define PTR(p) ((uint32_t)(uintptr_t)(p))
static void set_control(uint16_t control_value)
{
    __asm {fldcw control_value}
    g_fpu_cw=control_value;
}
static void record(unsigned op,uint32_t a,uint32_t b,uint32_t c,uint32_t d)
{
    if(count>=16)exit(3);
    uint32_t *r=records[count++];r[0]=op;r[1]=a;r[2]=b;r[3]=c;r[4]=d;r[5]=MEM32(PTR(actor)+0x6C);
}
static uint32_t get_type(void)
{
    ++type_calls;record(1,type_calls,0,0,0);
    if(number%13==0)MEM32(PTR(actor)+0x6C)+=3;
    if(number%17==0)damage^=1;
    if(number%11==0 && type_calls==2)MEM32(PTR(type_data)+0xA0)+=17;
    if(number%19==0 && type_calls==3)MEM32(frame+0x2C)+=7;
    if(number%23==0 && type_calls==2)set_control((uint16_t)(0x37F|((number%4)<<10)));
    return PTR(type_data);
}
static int32_t adjusted(uint32_t value,uint32_t wh,uint32_t armor,uint32_t distance)
{
    record(2,value,wh,armor,distance);
    if(number%29==0){MEM32(PTR(actor)+0x6C)+=5;MEM8(PTR(actor)+0x7D)=0;}
    if(number%31==0)set_control((uint16_t)(0x27F|((number%4)<<10)));
    return effective;
}
static void refreshed(uint32_t reason)
{
    record(3,reason,0,0,0);
    if(reason!=7)exit(3);
    if(number%37==0)MEM32(PTR(actor)+0x6C)+=2;
}
static uint32_t __fastcall native_type(void *self,void *ignored)
{(void)ignored;if(PTR(self)!=PTR(actor))exit(3);return get_type();}
static int32_t __fastcall native_adjust(uint32_t value,uint32_t wh,uint32_t armor,uint32_t distance)
{return adjusted(value,wh,armor,distance);}
static void __fastcall native_refresh(void *self,void *ignored,uint32_t reason)
{(void)ignored;if(PTR(self)!=PTR(actor))exit(3);refreshed(reason);}
static void translated_type(void){g_eax=get_type();g_esp+=4;}
static void translated_adjust(void){g_eax=(uint32_t)adjusted(g_ecx,g_edx,MEM32(g_esp+4),MEM32(g_esp+8));g_esp+=12;}
static void translated_refresh(void){refreshed(MEM32(g_esp+4));g_esp+=8;}
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if(address==PTR(native_type))return translated_type;
    if(address==PTR(native_refresh))return translated_refresh;
    if(address==0x47E1C0)return translated_adjust;
    return NULL;
}
recomp_func_t recomp_lookup(uint32_t address){(void)address;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t address){(void)address;return NULL;}
static __declspec(naked) void capture(void)
{
    __asm {
        mov native_eax,eax
        mov native_cx,ecx
        mov native_dx,edx
        mov native_bx,ebx
        mov native_si,esi
        mov native_di,edi
        mov native_bp,ebp
        mov native_sp,esp
        mov esp,host_stack
        pushfd
        pop native_flags
        fnstcw native_control
        popad
        popfd
        ret
    }
}
static __declspec(naked) void boundary(void)
{
    __asm {
        mov native_resume,5D3E68h
        jmp capture
    }
}
static __declspec(naked) void original(void)
{
    __asm {
        pushfd
        pushad
        mov host_stack,esp
        mov esp,entry_stack
        mov ecx,offset actor
        mov ebx,13579BDFh
        mov esi,2468ACE0h
        mov edi,11223344h
        mov ebp,55667788h
        mov eax,5D3D20h
        jmp eax
    }
}
static void patch(uint32_t at,uint32_t target)
{MEM8(at)=0xE9;MEM32(at+1)=target-at-5;}
static void setup(unsigned n)
{
    number=n;type_calls=count=0;memset(records,0,sizeof(records));native_resume=0;
    memset(actor,0,sizeof(actor));memset(type_data,0,sizeof(type_data));memset(private_stack,0xA5,sizeof(private_stack));
    entry_stack=PTR(private_stack)+4096;frame=entry_stack-0x24;
    MEM32(PTR(actor))=PTR(table);MEM32(PTR(actor)+0x6C)=n%9==0?0:n%9==1?UINT32_MAX:1+(n*37)%1100;MEM8(PTR(actor)+0x7D)=1;
    MEM32(PTR(type_data)+0xA0)=1+(n*13)%1000;MEM32(PTR(type_data)+0x9C)=n%11;MEM8(PTR(type_data)+0x203)=(uint8_t)(n%7==0);
    damage=n%7==0?0:n%7==1?-(int32_t)(1+n%700):(int32_t)(1+n%1300);
    if(n%4093==0)damage=INT32_MIN;
    effective=n%5==0?0:n%5==1?-(int32_t)(1+n%1100):(int32_t)(1+n%1400);
    const double ratios[]={0.0,0.25,0.5,1.0,0.3333333333333333,0.49999999999999994,0.5000000000000001,-0.25,2.0};
    double ratio=ratios[(n/7)%9];memcpy(rules+0x1370,&ratio,8);MEM32(0x839848)=PTR(rules);
    MEM32(entry_stack)=PTR(capture);MEM32(entry_stack+4)=PTR(&damage);MEM32(entry_stack+8)=n%513;MEM32(entry_stack+12)=PTR(warhead);MEM32(entry_stack+16)=0;MEM32(entry_stack+20)=n%4==0?0:n%4==1?1:n%4==2?0:0x80;MEM32(entry_stack+24)=0;
    const uint16_t precision[]={0,0x200,0x300};initial_control=(uint16_t)(0x7F|precision[(n/1024)%3]|(((n/3072)%4)<<10));set_control(initial_control);
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    table[0x84/4]=PTR(native_type);table[0x13C/4]=PTR(native_refresh);
    patch(0x47E1C0,PTR(native_adjust));patch(0x5D3E68,PTR(boundary));FlushInstructionCache(GetCurrentProcess(),NULL,0);
    unsigned early=0,applied=0,states[4]={0},healed=0;const unsigned offsets[]={0,4,8,12,0x10,0x14,0x28,0x2C,0x30,0x34,0x38,0x3C};
    for(unsigned n=0;n<131072;++n) {
        setup(n);original();
        unsigned char expected_actor[sizeof(actor)],expected_type[sizeof(type_data)];memcpy(expected_actor,actor,sizeof(actor));memcpy(expected_type,type_data,sizeof(type_data));
        int32_t expected_damage=damage;uint32_t expected_ops[16][6],expected_locals[12];memcpy(expected_ops,records,sizeof(records));unsigned expected_count=count;
        for(unsigned k=0;k<12;++k)expected_locals[k]=MEM32(frame+offsets[k]);
        uint32_t expected_resume=native_resume;
        setup(n);g_eax=0;g_ecx=PTR(actor);g_edx=0;g_esp=entry_stack;g_ebx=0x13579BDF;g_esi=0x2468ACE0;g_edi=0x11223344;g_ebp=0x55667788;g_cur_func=0x5D3D20;
        uint32_t resume=ra2_combat_health_bridge();uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,1);
        int locals_bad=0;for(unsigned k=0;k<12;++k)if(expected_locals[k]!=MEM32(frame+offsets[k]))locals_bad=1;
        int state_bad=memcmp(actor,expected_actor,sizeof(actor)) || memcmp(type_data,expected_type,sizeof(type_data)) || damage!=expected_damage;
        int abi_bad=g_eax!=native_eax || g_esp!=native_sp || g_ebx!=native_bx || g_esi!=native_si || g_edi!=native_di || g_ebp!=native_bp || (flags&0x8D5)!=(native_flags&0x8D5);
        if(resume && (g_ecx!=native_cx || g_edx!=native_dx))abi_bad=1;
        if(state_bad || locals_bad || abi_bad || resume!=expected_resume || g_fpu_cw!=native_control || count!=expected_count || memcmp(records,expected_ops,sizeof(records))) {
            printf("health mismatch n=%u state=%d locals=%d abi=%d resume=%x/%x calls=%u/%u cw=%x/%x eax=%x/%x ecx=%x/%x edx=%x/%x\n",n,state_bad,locals_bad,abi_bad,resume,expected_resume,count,expected_count,g_fpu_cw,native_control,g_eax,native_eax,g_ecx,native_cx,g_edx,native_dx);
            for(unsigned k=0;k<12;++k)if(expected_locals[k]!=MEM32(frame+offsets[k]))printf(" local %x=%x/%x\n",offsets[k],MEM32(frame+offsets[k]),expected_locals[k]);
            return 1;
        }
        if(resume){++applied;++states[MEM32(frame+0x10)];}else ++early;
        for(unsigned k=0;k<count;++k)if(records[k][0]==3)++healed;
    }
    printf("{\"passed\":true,\"health_cases\":131072,\"early_returns\":%u,\"damage_continuations\":%u,\"damage_states\":[%u,%u,%u,%u],\"healing_refreshes\":%u,\"state_callback_order_abi_cw_verified\":true,\"armor_calculation_mocked\":true,\"death_tail_not_replaced\":true}\n",early,applied,states[0],states[1],states[2],states[3],healed);
    return 0;
}
