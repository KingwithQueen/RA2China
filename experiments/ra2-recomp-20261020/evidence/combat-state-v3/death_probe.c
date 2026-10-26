#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_death_bridge.h"
#include "native_probe_host.h"
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static unsigned char actor[0x700],type_data[0xC20],rules[0x1400],animation[0x200],private_stack[8192],tag_data[8],attacker[8];
static uint32_t table[0x500/4],frame,host_stack,number,calls,type_calls,records[32][10];
static uint32_t n_eax,n_sp,n_bx,n_si,n_di,n_bp,n_flags;
static uint16_t n_control;
static unsigned emulated;
#define PTR(p) ((uint32_t)(uintptr_t)(p))
static void control(uint16_t value){__asm {fldcw value} g_fpu_cw=value;}
static void record(unsigned op,uint32_t a,uint32_t b,uint32_t c,uint32_t d,uint32_t e)
{
    if(calls>=32)exit(3);uint32_t *r=records[calls++];r[0]=op;r[1]=a;r[2]=b;r[3]=c;r[4]=d;r[5]=e;
    r[6]=MEM32(PTR(actor)+0x6C);r[7]=MEM8(PTR(actor)+0x7D)|(MEM8(PTR(actor)+0x5C3)<<8);r[8]=MEM32(PTR(actor)+0x34);
    uint16_t cw=g_fpu_cw;if(!emulated){__asm fnstcw cw}
    r[9]=cw&0x1F3F;
    if(number%31==0 && calls==2)MEM8(PTR(actor)+0x7D)=0;
    if(number%37==0 && op>=4)MEM32(PTR(actor)+0x6C)=0;
    if(number%41==0 && calls==1)MEM32(PTR(actor)+0x34)=0;
    if(number%43==0 && op==4)MEM32(PTR(type_data)+0xA0)+=3;
    if(number%53==0)MEM32(frame+0x34)=op<4?PTR(attacker):0;
    if(number%59==0 && op>=4)MEM32(PTR(actor)+0x6C)+=7;
    if(number%23==0)control((uint16_t)(0x7F|((number%4)<<10)|0x200));
}
static uint32_t get_class(void){record(1,0,0,0,0,0);return number%3?15:73;}
static uint32_t allocate(uint32_t size){record(2,size,0,0,0,0);return number%13?PTR(animation):0;}
static uint32_t construct(uint32_t self,uint32_t type,uint32_t coords,uint32_t zero,uint32_t one,uint32_t flags,uint32_t last)
{
    if(self!=PTR(animation) || zero || one!=1 || flags!=0x600 || last)exit(3);
    record(3,type,MEM32(coords),MEM32(coords+4),MEM32(coords+8),flags);return self;
}
static uint32_t get_type(void){++type_calls;record(4,type_calls,0,0,0,0);return type_calls==1 && number%17==0?0:PTR(type_data);}
static void action(uint32_t a,uint32_t b,uint32_t c){record(5,a,b,c,0,0);}
static void event(uint32_t tag,uint32_t which,uint32_t object,uint32_t tick,uint32_t zero,uint32_t source)
{if(object!=PTR(actor) || zero)exit(3);record(6,which,source,tick,tag,0);}
static void attacked(uint32_t source){record(7,source,0,0,0,0);}
static void remove_object(uint32_t reason){record(8,reason,0,0,0,0);if(number%3==0)MEM8(PTR(actor)+0x7D)=0;}
static void notify(uint32_t reason){record(9,reason,0,0,0,0);if(number%67==0)MEM8(PTR(actor)+0x7D)=0;}
static uint32_t __fastcall class_native(void *self,void *unused){(void)self;(void)unused;return get_class();}
static uint32_t __cdecl allocate_native(uint32_t size){return allocate(size);}
static uint32_t __fastcall construct_native(void *self,void *unused,uint32_t type,uint32_t coords,uint32_t z,uint32_t one,uint32_t f,uint32_t last){(void)unused;return construct(PTR(self),type,coords,z,one,f,last);}
static uint32_t __fastcall type_native(void *self,void *unused){(void)self;(void)unused;return get_type();}
static void __fastcall action_native(void *self,void *unused,uint32_t a,uint32_t b,uint32_t c){(void)self;(void)unused;action(a,b,c);}
static void __fastcall event_native(void *tag,void *unused,uint32_t which,uint32_t object,uint32_t tick,uint32_t z,uint32_t source){(void)unused;event(PTR(tag),which,object,tick,z,source);}
static void __fastcall attacked_native(void *self,void *unused,uint32_t source){(void)self;(void)unused;attacked(source);}
static void __fastcall remove_native(void *self,void *unused,uint32_t reason){(void)self;(void)unused;remove_object(reason);}
static void __fastcall notify_native(void *self,void *unused,uint32_t reason){(void)self;(void)unused;notify(reason);}
static void class_c(void){g_eax=get_class();g_esp+=4;}
static void allocate_c(void){g_eax=allocate(MEM32(g_esp+4));g_esp+=4;}
static void construct_c(void){g_eax=construct(g_ecx,MEM32(g_esp+4),MEM32(g_esp+8),MEM32(g_esp+12),MEM32(g_esp+16),MEM32(g_esp+20),MEM32(g_esp+24));g_esp+=28;}
static void type_c(void){g_eax=get_type();g_esp+=4;}
static void action_c(void){action(MEM32(g_esp+4),MEM32(g_esp+8),MEM32(g_esp+12));g_esp+=16;}
static void event_c(void){event(g_ecx,MEM32(g_esp+4),MEM32(g_esp+8),MEM32(g_esp+12),MEM32(g_esp+16),MEM32(g_esp+20));g_esp+=24;}
static void attacked_c(void){attacked(MEM32(g_esp+4));g_esp+=8;}
static void remove_c(void){remove_object(MEM32(g_esp+4));g_esp+=8;}
static void notify_c(void){notify(MEM32(g_esp+4));g_esp+=8;}
recomp_func_t recomp_lookup_manual(uint32_t target)
{
    if(target==PTR(class_native))return class_c;if(target==0x782017)return allocate_c;if(target==0x420110)return construct_c;
    if(target==PTR(type_native))return type_c;if(target==PTR(action_native))return action_c;if(target==0x6B3DF0)return event_c;
    if(target==PTR(attacked_native))return attacked_c;if(target==PTR(remove_native))return remove_c;if(target==PTR(notify_native))return notify_c;return NULL;
}
recomp_func_t recomp_lookup(uint32_t target){(void)target;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t target){(void)target;return NULL;}
static __declspec(naked) void capture(void)
{
    __asm {
        mov n_eax,eax
        mov n_sp,esp
        mov n_bx,ebx
        mov n_si,esi
        mov n_di,edi
        mov n_bp,ebp
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
        mov esp,frame
        mov esi,offset actor
        mov ebp,12345678h
        mov ebx,13579B00h
        mov eax,number
        and eax,3
        cmp eax,1
        jne normal
        mov bl,80h
normal:
        mov edi,3
        mov eax,dword ptr [actor+6Ch]
        test eax,eax
        mov ecx,5D3E68h
        jmp ecx
    }
}
static void patch(uint32_t at,uint32_t target){MEM8(at)=0xE9;MEM32(at+1)=target-at-5;}
static void setup(unsigned n)
{
    number=n;calls=type_calls=0;memset(records,0,sizeof(records));memset(actor,0,sizeof(actor));memset(type_data,0,sizeof(type_data));memset(private_stack,0xA5,sizeof(private_stack));
    frame=PTR(private_stack)+4096;MEM32(frame)=0x11223344;MEM32(frame+4)=0x2468ACE0;MEM32(frame+8)=0x55667788;MEM32(frame+12)=0x13579BDF;MEM32(frame+36)=PTR(capture);
    const int32_t hp[]={0,-1,1,25,100,300};MEM32(PTR(actor)+0x6C)=(uint32_t)hp[n%6];MEM32(PTR(actor))=PTR(table);MEM32(PTR(actor)+0x5A8)=PTR(type_data);
    MEM8(PTR(actor)+0x7D)=(uint8_t)(n%11!=0);MEM8(PTR(actor)+0x77)=(uint8_t)(n%7!=0);MEM8(PTR(actor)+0x5C3)=(uint8_t)(n%5==0);MEM8(PTR(type_data)+0xC00)=(uint8_t)(n%4!=0);
    int32_t strength=1+(n*13)%1000;MEM32(PTR(type_data)+0xA0)=(uint32_t)strength;MEM32(frame+0x14)=n%2?(uint32_t)strength:MEM32(PTR(actor)+0x6C);MEM32(frame+0x10)=(n/6)%5;
    MEM32(PTR(actor)+0x34)=n%7?PTR(tag_data):0;MEM32(frame+0x34)=n%3?PTR(attacker):0;
    MEM32(PTR(actor)+0x88)=100;MEM32(PTR(actor)+0x8C)=200;MEM32(PTR(actor)+0x90)=300;MEM32(0x839848)=PTR(rules);MEM32(PTR(rules)+0xA4)=0x11221122;MEM32(0xA72EE0)=1234;
    const uint16_t precision[]={0,0x200,0x300};control((uint16_t)(0x7F|precision[(n/1024)%3]|(((n/3072)%4)<<10)));MEM32(0x7D8964)=n%2?0xE7F:0xA7F;
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    table[0x2C/4]=PTR(class_native);table[0x84/4]=PTR(type_native);table[0x4DC/4]=PTR(action_native);table[0xDC/4]=PTR(attacked_native);table[0xD8/4]=PTR(remove_native);table[0x11C/4]=PTR(notify_native);
    patch(0x782017,PTR(allocate_native));patch(0x420110,PTR(construct_native));patch(0x6B3DF0,PTR(event_native));FlushInstructionCache(GetCurrentProcess(),NULL,0);
    unsigned result_counts[6]={0},special=0,removed=0,events=0;
    for(unsigned n=0;n<131072;++n) {
        setup(n);emulated=0;original();unsigned char expected_actor[sizeof(actor)],expected_type[sizeof(type_data)];memcpy(expected_actor,actor,sizeof(actor));memcpy(expected_type,type_data,sizeof(type_data));
        uint32_t ops[32][10];memcpy(ops,records,sizeof(ops));unsigned count=calls;uint32_t state=MEM32(frame+0x10);
        setup(n);emulated=1;g_esp=frame;g_esi=PTR(actor);g_ebp=0x12345678;g_ebx=0x13579B00|(n%4==1?0x80:0);g_edi=3;g_cur_func=0x5D3D20;
        ra2_combat_death_bridge();uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,1);
        if(g_eax!=n_eax || g_esp!=n_sp || g_ebx!=n_bx || g_esi!=n_si || g_edi!=n_di || g_ebp!=n_bp || ((flags^n_flags)&0x8D5) || ((g_fpu_cw^n_control)&0x1F3F) || calls!=count || memcmp(ops,records,sizeof(ops)) || memcmp(actor,expected_actor,sizeof(actor)) || memcmp(type_data,expected_type,sizeof(type_data)) || MEM32(frame+0x10)!=state) {
            printf("death mismatch n=%u result=%u/%u calls=%u/%u health=%d/%d active=%u/%u state=%u/%u cw=%x/%x\n",n,g_eax,n_eax,calls,count,(int32_t)MEM32(PTR(actor)+0x6C),*(int32_t *)(expected_actor+0x6C),MEM8(PTR(actor)+0x7D),expected_actor[0x7D],MEM32(frame+0x10),state,g_fpu_cw,n_control);
            for(unsigned i=0;i<(calls>count?calls:count);++i)if(memcmp(ops[i],records[i],sizeof(ops[i])))printf(" op%u=%u/%u\n",i,records[i][0],ops[i][0]);return 1;
        }
        if(g_eax>5)return 1;++result_counts[g_eax];for(unsigned i=0;i<calls;++i){if(records[i][0]==5)++special;if(records[i][0]==8)++removed;if(records[i][0]==6)++events;}
    }
    printf("{\"passed\":true,\"death_cases\":131072,\"special_recoveries\":%u,\"remove_callbacks\":%u,\"trigger_notifications\":%u,\"returns\":[%u,%u,%u,%u,%u,%u],\"callback_order_state_stack_flags_cw_verified\":true,\"engine_callbacks_mocked\":true,\"actual_original_tail_and_ftol\":true}\n",special,removed,events,result_counts[0],result_counts[1],result_counts[2],result_counts[3],result_counts[4],result_counts[5]);return 0;
}
