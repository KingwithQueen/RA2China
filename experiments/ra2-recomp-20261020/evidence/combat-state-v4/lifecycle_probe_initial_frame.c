#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "combat_lifecycle_bridge.h"
#include "native_probe_host.h"
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
#define PTR(p) ((uint32_t)(uintptr_t)(p))
static unsigned char actors[10][0x700],type_data[0xC20],private_stack[8192],attachment[8],team[8],timer[8],attacker[8];
static uint32_t table[0x500/4],vector_table[8],queue[64],frame,host_stack,entry,number,phase,calls,records[128][8],route;
static uint32_t n_ax,n_cx,n_bx,n_si,n_di,n_bp,n_sp,n_flags,n_route,in_ax,in_bx,in_bp;
static unsigned ready_calls,find_calls,destroyed,grown;
static void flags(uint32_t v){g_flag_k=FK_CMP;g_flag_a=v;g_flag_b=0;g_flag_cf=0;}
static uint32_t invoke(unsigned op,uint32_t self,uint32_t args,uint32_t edx)
{
    if(calls>=128)exit(3);uint32_t *rec=records[calls++];rec[0]=op;rec[1]=op==16?0:self;
    unsigned sizes[]={0,1,0,0,2,0,1,0,3,0,0,0,2,0,1,1,1,1,1,1};
    for(unsigned i=0;i<sizes[op] && i<3;++i)rec[2+i]=MEM32(args+i*4);
    rec[5]=MEM32(0xAC0CE8);rec[6]=MEM8(PTR(actors)+0x7D);rec[7]=MEM32(PTR(actors)+0x6C);
    uint32_t result=0xBB000000|op;
    switch(op) {
        case 1:if(number%19==0){MEM32(PTR(actors)+0x230)=0;MEM32(PTR(actors)+0x4C4)=0;}break;
        case 7:if(number%7==0)MEM32(PTR(actors)+0x4C4)=0;break;
        case 8:if(MEM32(args)!=PTR(actors) || MEM32(args+4)!=UINT32_MAX || MEM32(args+8))exit(3);break;
        case 10:if((edx&255)!=1)exit(3);break;
        case 11:if(number%13==0)MEM32(0xAC0CE8)=0;break;
        case 12:
            ++grown;if(MEM32(args+4) || self!=0xAC0CD8)exit(3);
            result=number%5?0x12340001:0x12340000;
            if(result&255){MEM32(0xAC0CE0)=MEM32(args);if(number%17==0)MEM32(0xAC0CE8)=1;}
            break;
        case 13:++ready_calls;result=MEM32(self+0x100);break;
        case 14:{
            ++find_calls;uint32_t value=MEM32(MEM32(args));rec[2]=value;result=UINT32_MAX;
            for(uint32_t i=0;i<MEM32(0xAC0CE8);++i)if(queue[i]==value){result=i;break;}
            if(number%23==0 && find_calls==1)result=MEM32(0xAC0CE8)+3;
            break;
        }
        case 15:result=MEM32(MEM32(args)+0x104);break;
        case 16:result=MEM32(args);break;
        case 17:{uint32_t obj=MEM32(args),kind=MEM32(obj+0x108);const uint32_t names[]={0x7CF6A8,0x7F6D68,0x7DAEC0,0x7CE5E0};result=kind<4 && self==names[kind];break;}
        case 18:
            ++destroyed;if(MEM32(args)!=1)exit(3);MEM32(self+0x10C)+=1;
            if(number%11==0 && destroyed==1){queue[MEM32(0xAC0CE8)++]=PTR(actors[9]);}
            break;
        case 19:if(MEM32(args))exit(3);result=number%3==0?0x100:0x101;break;
    }
    return result;
}
static __declspec(naked) void native_credit(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 1
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_credit(void){g_eax=invoke(1,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_occupation(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 2
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_occupation(void){g_eax=invoke(2,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_stop(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 3
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_stop(void){g_eax=invoke(3,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_mission(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 4
    call invoke
    add esp,16
    cmp eax,0
    ret 8
} }
static void c_mission(void){g_eax=invoke(4,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=12;}
static __declspec(naked) void native_commit(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 5
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_commit(void){g_eax=invoke(5,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_notify(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 6
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_notify(void){g_eax=invoke(6,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_attached(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 7
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_attached(void){g_eax=invoke(7,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_team(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 8
    call invoke
    add esp,16
    cmp eax,0
    ret 12
} }
static void c_team(void){g_eax=invoke(8,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=16;}
static __declspec(naked) void native_timer(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 9
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_timer(void){g_eax=invoke(9,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_detach(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 10
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_detach(void){g_eax=invoke(10,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_limbo(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 11
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_limbo(void){g_eax=invoke(11,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_grow(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 12
    call invoke
    add esp,16
    cmp eax,0
    ret 8
} }
static void c_grow(void){g_eax=invoke(12,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=12;}
static __declspec(naked) void native_ready(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 13
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_ready(void){g_eax=invoke(13,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_find(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 14
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_find(void){g_eax=invoke(14,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_isobject(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 15
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_isobject(void){g_eax=invoke(15,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_typeid(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 16
    call invoke
    add esp,16
    cmp eax,0
    ret 0
} }
static void c_typeid(void){g_eax=invoke(16,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=4;}
static __declspec(naked) void native_equals(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 17
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_equals(void){g_eax=invoke(17,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_destroy(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 18
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_destroy(void){g_eax=invoke(18,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}
static __declspec(naked) void native_sink(void) { __asm {
    mov eax,esp
    add eax,4
    push edx
    push eax
    push ecx
    push 19
    call invoke
    add esp,16
    cmp eax,0
    ret 4
} }
static void c_sink(void){g_eax=invoke(19,g_ecx,g_esp+4,g_edx);flags(g_eax);g_esp+=8;}

recomp_func_t recomp_lookup_manual(uint32_t target)
{
    if(target==0x5D4E90)return ra2_object_uninit_bridge;
    if(target==0x4CCE40)return ra2_foot_uninit_bridge;
    if(target==PTR(native_credit))return c_credit;
    if(target==PTR(native_occupation))return c_occupation;
    if(target==PTR(native_stop))return c_stop;
    if(target==PTR(native_mission))return c_mission;
    if(target==PTR(native_commit))return c_commit;
    if(target==PTR(native_notify))return c_notify;
    if(target==PTR(native_attached))return c_attached;
    if(target==PTR(native_team))return c_team;
    if(target==PTR(native_timer))return c_timer;
    if(target==PTR(native_detach))return c_detach;
    if(target==PTR(native_limbo))return c_limbo;
    if(target==PTR(native_grow))return c_grow;
    if(target==PTR(native_ready))return c_ready;
    if(target==PTR(native_find))return c_find;
    if(target==PTR(native_isobject))return c_isobject;
    if(target==PTR(native_typeid))return c_typeid;
    if(target==PTR(native_equals))return c_equals;
    if(target==PTR(native_destroy))return c_destroy;
    if(target==PTR(native_sink))return c_sink;
    if(target==0x4681E0)return c_attached;
    if(target==0x6B8FB0)return c_team;
    if(target==0x435FB0)return c_timer;
    if(target==0x6ECB90)return c_detach;
    if(target==0x6D3040)return c_notify;
    if(target==0x783C05)return c_typeid;
    if(target==0x781CD1)return c_equals;
    return NULL;
}
recomp_func_t recomp_lookup(uint32_t target){(void)target;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t target){(void)target;return NULL;}
static __declspec(naked) void capture(void)
{
    __asm {
        mov n_ax,eax
        mov n_cx,ecx
        mov n_bx,ebx
        mov n_si,esi
        mov n_di,edi
        mov n_bp,ebp
        mov n_sp,esp
        mov eax,route
        mov n_route,eax
        mov esp,host_stack
        pushfd
        pop n_flags
        popad
        popfd
        ret
    }
}
static __declspec(naked) void unit_effects(void){__asm {mov route,6FCADAh} __asm {jmp capture}}
static __declspec(naked) void unit_delay(void){__asm {mov route,6FCD44h} __asm {jmp capture}}
static __declspec(naked) void unit_live(void){__asm {mov route,6FD1DBh} __asm {jmp capture}}
static __declspec(naked) void inf_effects(void){__asm {mov route,4FFC4Dh} __asm {jmp capture}}
static __declspec(naked) void inf_live(void){__asm {mov route,500193h} __asm {jmp capture}}

static __declspec(naked) void original(void)
{
    __asm {
        pushfd
        pushad
        mov host_stack,esp
        mov esp,frame
        mov esi,offset actors
        mov ecx,offset actors
        mov eax,in_ax
        mov ebx,in_bx
        mov ebp,in_bp
        mov edi,offset attacker
        mov edx,12345678h
        cmp phase,4
        jb run_fragment
        mov esi,13572468h
run_fragment:
        jmp dword ptr [entry]
    }
}
static void patch(uint32_t at,uint32_t target){MEM8(at)=0xE9;MEM32(at+1)=target-at-5;}
static void setup(unsigned n,unsigned kind)
{
    number=n;phase=kind;calls=ready_calls=find_calls=destroyed=grown=route=0;
    memset(records,0,sizeof(records));memset(actors,0,sizeof(actors));memset(type_data,0,sizeof(type_data));memset(queue,0,sizeof(queue));memset(private_stack,0xA5,sizeof(private_stack));
    frame=PTR(private_stack)+4096;in_ax=n%6;in_bx=kind==2?4:0x13579B00|(n&1);in_bp=PTR(attacker);
    for(unsigned i=0;i<10;++i){MEM32(PTR(actors[i]))=PTR(table);MEM32(PTR(actors[i])+0x100)=i==9?0:((n+i)%3==0?0x100:0x101);MEM32(PTR(actors[i])+0x104)=(n+i)%7!=0;MEM32(PTR(actors[i])+0x108)=(n+i)%5;MEM8(PTR(actors[i])+0x7D)=(uint8_t)(n%2);}
    MEM32(PTR(actors)+0x5AC)=PTR(type_data);MEM32(PTR(actors)+0x5A8)=PTR(type_data);MEM32(PTR(actors)+0x6C)=0;
    MEM32(PTR(actors)+0x5C0)=UINT32_MAX;MEM32(PTR(type_data)+0xBB8)=(uint32_t)((int)(n%4)-1);MEM8(PTR(type_data)+0xB45)=(uint8_t)(n%2);MEM8(PTR(actors)+0x325)=(uint8_t)(n%3==0);
    MEM32(PTR(actors)+0x230)=n%2?PTR(attachment):0;MEM32(PTR(actors)+0x4C4)=n%3?PTR(team):0;MEM32(PTR(actors)+0x38)=n%5?PTR(timer):0;
    MEM32(0xAC0CD8)=PTR(vector_table);MEM32(0xAC0CDC)=PTR(queue);MEM32(0xAC0CE0)=(n/7)%3*4;MEM32(0xAC0CE8)=n%9;MEM8(0xAC0CE5)=(uint8_t)(n%2);MEM32(0xAC0CEC)=(uint32_t)((int)((n/9)%6)-1);
    for(unsigned i=0;i<MEM32(0xAC0CE8);++i)queue[i]=PTR(actors[(i+n)%4]);
    if(kind<4){MEM32(frame)=0x11223344;MEM32(frame+4)=0x2468ACE0;MEM32(frame+8)=0x55667788;MEM32(frame+12)=0x13579BDF;MEM32(frame+(kind%2?76:56))=PTR(capture);}
    else MEM32(frame)=PTR(capture);
    g_eax=in_ax;g_ecx=PTR(actors);g_edx=0x12345678;g_ebx=in_bx;g_ebp=in_bp;g_edi=PTR(attacker);g_esi=kind<4?PTR(actors):0x13572468;g_esp=frame;
    g_cur_func=kind==0 || kind==2?0x6FCA30:kind==1 || kind==3?0x4FFB70:kind==4?0x4CCE40:kind==5?0x5D4E90:0x6ECF10;
}
int main(int argc,char **argv)
{
    hold_image();if(argc!=2)return 2;map_original_image(argv[1]);
    table[0x360/4]=PTR(native_credit);
    table[0x48C/4]=PTR(native_occupation);
    table[0x348/4]=PTR(native_stop);
    table[0x1D0/4]=PTR(native_mission);
    table[0x1D4/4]=PTR(native_commit);
    table[0xD0/4]=PTR(native_limbo);
    table[0x44/4]=PTR(native_ready);
    table[0x8/4]=PTR(native_isobject);
    table[0x20/4]=PTR(native_destroy);
    table[0x380/4]=PTR(native_sink);
    table[0xF0/4]=0x4CCE40;vector_table[8/4]=PTR(native_grow);vector_table[0x10/4]=PTR(native_find);
    patch(0x4681E0,PTR(native_attached));
    patch(0x6B8FB0,PTR(native_team));
    patch(0x435FB0,PTR(native_timer));
    patch(0x6ECB90,PTR(native_detach));
    patch(0x6D3040,PTR(native_notify));
    patch(0x783C05,PTR(native_typeid));
    patch(0x781CD1,PTR(native_equals));
    patch(0x6FCADA,PTR(unit_effects));
    patch(0x6FCD44,PTR(unit_delay));
    patch(0x6FD1DB,PTR(unit_live));
    patch(0x4FFC4D,PTR(inf_effects));
    patch(0x500193,PTR(inf_live));
    FlushInstructionCache(GetCurrentProcess(),NULL,0);
    uint32_t totals[7]={0},operations=0,destructors=0,growths=0;
    const uint32_t entries[]={0x6FCA7E,0x4FFBD6,0x6FD17D,0x4FFF61,0x4CCE40,0x5D4E90,0x6ECF10};
    for(unsigned kind=0;kind<1;++kind)for(unsigned n=10;n<32768;n+=12) {
        entry=entries[kind];setup(n,kind);original();
        unsigned char expected[sizeof(actors)];uint32_t expected_queue[64],expected_records[128][8],expected_vector[6];
        memcpy(expected,actors,sizeof(actors));memcpy(expected_queue,queue,sizeof(queue));memcpy(expected_records,records,sizeof(records));memcpy(expected_vector,(void *)0xAC0CD8,sizeof(expected_vector));
        unsigned count=calls,ds=destroyed,gs=grown;uint32_t stored=MEM32(frame+0x40);
        setup(n,kind);uint32_t next=0;
        switch(kind){case 0:next=ra2_unit_death_handoff_bridge();break;case 1:next=ra2_infantry_death_handoff_bridge();break;case 2:ra2_unit_death_finish_bridge();break;case 3:ra2_infantry_death_finish_bridge();break;case 4:ra2_foot_uninit_bridge();break;case 5:ra2_object_uninit_bridge();break;case 6:ra2_object_delete_drain_bridge();break;}
        uint32_t ef=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,1);
        if(next!=n_route || g_esp!=n_sp || g_ebx!=n_bx || g_esi!=n_si || g_edi!=n_di || g_ebp!=n_bp || g_eax!=n_ax || (kind==6 && g_ecx!=n_cx) || (!next && ((ef^n_flags)&0x8D5)) || calls!=count || memcmp(expected,actors,sizeof(actors)) || memcmp(expected_queue,queue,sizeof(queue)) || memcmp(expected_vector,(void *)0xAC0CD8,sizeof(expected_vector)) || memcmp(expected_records,records,sizeof(records)) || (kind==0 && MEM32(frame+0x40)!=stored)) {
            printf("lifecycle mismatch kind=%u n=%u route=%x/%x eax=%x/%x esp=%x/%x flags=%x/%x calls=%u/%u\n",kind,n,next,n_route,g_eax,n_ax,g_esp,n_sp,ef,n_flags,calls,count);
            for(unsigned i=0;i<(calls>count?calls:count);++i)printf("op%u %u/%u self=%x/%x arg=%x/%x count=%u/%u\n",i,records[i][0],expected_records[i][0],records[i][1],expected_records[i][1],records[i][2],expected_records[i][2],records[i][5],expected_records[i][5]);return 1;
        }
        ++totals[kind];operations+=count;destructors+=ds;growths+=gs;
    }
    printf("{\"passed\":true,\"lifecycle_cases\":2730,\"fragments\":1,\"per_fragment\":2730,\"callbacks\":%u,\"destructors\":%u,\"growth_callbacks\":%u,\"actual_original_fragments\":true,\"engine_callbacks_mocked\":true,\"queue_state_order_stack_flags_nonvolatile_verified\":true}\n",operations,destructors,growths);return 0;
}
