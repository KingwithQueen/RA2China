#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_continuation_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))

enum Op { HEIGHT,CELL,LAND,PASSAGE,KIND,REFRESH,ACCEPT,START,SPEED,REVEAL,GATE,NOTIFY,OP_COUNT };
static const unsigned argc_op[]={0,1,1,5,0,1,1,2,2,0,2,4};
static unsigned char drive[128],unit[0x700],type[0x1000],cell[0x200],stack_data[8192],header[12];
static uint32_t vtable[0x500/4],samples[8][3],fixture,number,frame,stub_base,cleanup_bytes,records[64][16],count;
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control;
static unsigned outcomes[2],passages[8],shift_cases;
static uint32_t op(unsigned id,uint32_t object,const uint32_t *args) {
    if(count==64) exit(2);
    uint32_t *r=records[count++];r[0]=id;r[1]=object;r[12]=F(drive,0x40);r[13]=F(drive,0x58);r[14]=F(drive,0x5C);r[15]=drive[0x63];
    switch(id) {
        case HEIGHT: return 4;
        case CELL: r[2]=MEM32(args[0]);return P(cell);
        case LAND: memcpy(r+2,(void *)(uintptr_t)args[0],12);return P(cell);
        case PASSAGE: memcpy(r+2,args,20);++passages[(fixture>>4)&7];return (fixture>>4)&7;
        case KIND: return fixture&(1u<<8) ? 1 : 6;
        case REFRESH:
            r[2]=args[0];unit[0x7D]=(fixture&(1u<<9)) ? 0 : 1;
            unit[0x76]=(fixture>>10)&1;unit[0x7A]=(fixture>>11)&1;
            if(fixture&(1u<<12)) memcpy(drive+0x40,(void *)0x852998,12);
            return 0;
        case ACCEPT:
            r[2]=args[0];if(fixture&(1u<<13)) unit[0x7D]=0;
            if(fixture&(1u<<14)) unit[0x76]=1;
            return (fixture>>15)&1;
        case START:
            memcpy(r+2,(void *)(uintptr_t)args[0],12);r[5]=args[1];
            drive[0x61]=1;F(unit,0x4D0)=99;return 1;
        case SPEED: memcpy(r+2,args,8);memcpy(unit+0x468,args,8);return 0;
        case REVEAL: unit[0x57B]=1;return 0;
        case GATE: r[2]=args[0];r[3]=MEM32(args[1]);return 0;
        case NOTIFY: memcpy(r+2,args,16);return 0;
        default: exit(2);
    }
}
static uint32_t native_operation(unsigned id,uint32_t object,const uint32_t *args)
{ cleanup_bytes=argc_op[id]*4; return op(id,object,args); }
static __declspec(naked) void native_stub(void)
{
    __asm {
        pushad
        mov ebp,esp
        lea eax,[ebp+40]
        push eax
        push dword ptr [ebp+24]
        push dword ptr [ebp+32]
        call native_operation
        add esp,12
        mov dword ptr [ebp+28],eax
        mov esp,ebp
        popad
        add esp,4
        pop edx
        add esp,cleanup_bytes
        jmp edx
    }
}

#define L(name,id) static void name(void) { g_eax=op(id,g_ecx,(const uint32_t *)(uintptr_t)(g_esp+4));g_esp+=4+argc_op[id]*4; }
L(l_height,HEIGHT) L(l_cell,CELL) L(l_land,LAND) L(l_passage,PASSAGE) L(l_kind,KIND) L(l_refresh,REFRESH)
L(l_accept,ACCEPT) L(l_start,START) L(l_speed,SPEED) L(l_reveal,REVEAL) L(l_gate,GATE) L(l_notify,NOTIFY)
static recomp_func_t lifted[]={l_height,l_cell,l_land,l_passage,l_kind,l_refresh,l_accept,l_start,l_speed,l_reveal,l_gate,l_notify};
static const uint32_t targets[]={0x5D47D0,0x548070,0x548000,0x4A0BC0,0x478740,0x55ACD0,0x476920};
static const unsigned ids[]={HEIGHT,CELL,LAND,START,REVEAL,GATE,NOTIFY};
recomp_func_t recomp_lookup_manual(uint32_t a) {
    if(a>=stub_base&&a<stub_base+OP_COUNT*16) return lifted[(a-stub_base)/16];
    for(unsigned i=0;i<7;++i) if(a==targets[i]) return lifted[ids[i]];
    if(a==0x476CC0) return l_accept;
    return NULL;
}
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
static void patch(uint32_t a,uint32_t b) { MEM8(a)=0xE9; MEM32(a+1)=b-a-5; }
static __declspec(naked) void trap(void)
{
    __asm {
        mov native_esp,esp
        mov native_ebp,ebp
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
        lea ebp,drive
        lea esi,samples
        mov ecx,4A1B60h
        jmp ecx
    }
}

static void initialize(unsigned n) {
    number=n;fixture=n*1664525u+1013904223u;fixture^=fixture<<13;fixture^=fixture>>17;fixture^=fixture<<5;
    memset(drive,0,sizeof(drive));memset(unit,0,sizeof(unit));memset(type,0,sizeof(type));memset(cell,0,sizeof(cell));
    memset(stack_data,0xA5,sizeof(stack_data));memset(records,0,sizeof(records));count=native_resume=0;
    frame=P(stack_data+4096);F(drive,0xC)=P(unit);F(unit,0)=P(vtable);F(unit,0x5AC)=P(type);unit[0x7D]=1;
    const int32_t positions[][3]={{17280,29312,416},{-257,255,-416},{INT32_MAX,INT32_MIN,0},{0,0,0}};
    memcpy(drive+0x40,positions[(fixture>>16)&3],12);
    if(fixture&(1u<<18)) memcpy(drive+0x40,(void *)0x852998,12);
    memcpy(unit+0x88,positions[(fixture>>19)&3],12);
    uint64_t speed=0x3FECCCCCCCCCCCCDull+(uint64_t)n;memcpy(unit+0x468,&speed,8);
    F(drive,0x58)=5;F(drive,0x5C)=n%5;drive[0x60]=1;drive[0x63]=(fixture>>21)&1;
    MEM32(frame+0x38)=P(samples);MEM32(frame+0x58)=0;MEM32(frame+0xA8)=P(header);
    MEM8(frame+0x13)=(n%7!=0);MEM32(frame+0x14)=0xAABBCCDD;MEM32(frame+0x3C)=11;
    const int32_t directions[]={-1,0,1,2,3,4,5,6,7,8};MEM32(frame+0x44)=(uint32_t)directions[n%10];
    header[4]=(uint8_t)(fixture>>24);MEM32(0x7A00A4)=n%11==0 ? 33 : F(drive,0x5C);
    int kind=n%13==0 ? 0 : 2;
    for(unsigned i=0;i<64;++i) MEM8(0x7A0180+i*12)=(uint8_t)kind;
    MEM32(0x7A00A8+32)=n%17==0 ? 0 : 3;MEM32(0x7A00A0+32)=P(samples);
    for(unsigned i=0;i<8;++i) { MEM32(0x851AC0+i*8)=fixture&1 ? 0 : 256;MEM32(0x851AC4+i*8)=fixture&2 ? 0 : (uint32_t)-256; }
    type[0xBA4]=(fixture>>22)&1;F(cell,0x140)=fixture&4 ? 0x100 : 0;cell[0x11B]=(uint8_t)((fixture>>24)&7);
    MEM32(0x8529D0)=104;
    for(unsigned i=0;i<24;++i) F(unit,0x4D0+i*4)=i+100;
}
int main(int argc,char **argv) {
    if(argc!=2) return 2;hold_image();map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);if(!stubs) return 2;stub_base=P(stubs);
    for(unsigned i=0;i<OP_COUNT;++i) { unsigned char *s=stubs+i*16;s[0]=0x68;memcpy(s+1,&i,4);s[5]=0xE9;uint32_t rel=P(native_stub)-P(s+10);memcpy(s+6,&rel,4); }
    for(unsigned i=0;i<7;++i) patch(targets[i],stub_base+ids[i]*16);
    vtable[0x194/4]=stub_base+PASSAGE*16;vtable[0x2C/4]=stub_base+KIND*16;
    vtable[0x174/4]=stub_base+REFRESH*16;vtable[0x4C8/4]=stub_base+SPEED*16;
    const uint32_t boundaries[]={0x4A1F8D,0x4A263A};
    for(unsigned i=0;i<2;++i) {
        unsigned char *s=stubs+(OP_COUNT+i)*16;s[0]=0xC7;s[1]=5;uint32_t dest=P(&native_resume);memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4);s[10]=0xE9;uint32_t rel=P(trap)-P(s+15);memcpy(s+11,&rel,4);patch(boundaries[i],P(s));
    }
    patch(0x476CC0,stub_base+ACCEPT*16);FlushInstructionCache(GetCurrentProcess(),NULL,0);
    for(unsigned n=0;n<65536;++n) {
        initialize(n);run_original();
        unsigned char expected_drive[sizeof(drive)],expected_unit[sizeof(unit)];uint32_t expected_records[64][16],expected_count=count,expected_resume=native_resume;
        memcpy(expected_drive,drive,sizeof(drive));memcpy(expected_unit,unit,sizeof(unit));memcpy(expected_records,records,sizeof(records));
        const uint32_t locals[]={0x10,0x14,0x18,0x1C,0x20,0x38,0x3C,0x40,0x58,0xA8};uint32_t expected_locals[10];
        for(unsigned i=0;i<10;++i) expected_locals[i]=MEM32(frame+locals[i]);
        initialize(n);g_esp=frame;g_ebp=P(drive);g_fpu_cw=0x37F;
        uint32_t resume=ra2_ground_continue_turn_bridge();
        int local_diff=0;for(unsigned i=0;i<10;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) local_diff=1;
        if(resume!=expected_resume || g_esp!=native_esp || g_ebp!=native_ebp || g_fpu_cw!=(uint16_t)native_control || local_diff
            || memcmp(drive,expected_drive,sizeof(drive)) || memcmp(unit,expected_unit,sizeof(unit)) || count!=expected_count || memcmp(records,expected_records,sizeof(records))) {
            printf("continuation mismatch case=%u fixture=%08x resume=%x/%x calls=%u/%u locals=%d\n",number,fixture,resume,expected_resume,count,expected_count,local_diff);
            for(unsigned i=0;i<10;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) printf("local %x=%x/%x\n",locals[i],MEM32(frame+locals[i]),expected_locals[i]);
            for(unsigned i=0;i<count||i<expected_count;++i) if(memcmp(records[i],expected_records[i],64)) { printf("call %u\n",i);for(unsigned j=0;j<16;++j) printf(" %u:%x/%x",j,records[i][j],expected_records[i][j]);puts(""); }
            for(unsigned i=0;i<sizeof(drive);++i) if(drive[i]!=expected_drive[i]) printf("drive %x=%x/%x\n",i,drive[i],expected_drive[i]);
            for(unsigned i=0;i<sizeof(unit);++i) if(unit[i]!=expected_unit[i]) printf("unit %x=%x/%x\n",i,unit[i],expected_unit[i]);
            return 1;
        }
        ++outcomes[resume==boundaries[1]];if(F(unit,0x52C)==UINT32_MAX) ++shift_cases;
    }
    for(unsigned i=0;i<8;++i) if(!passages[i]) return 1;
    if(!outcomes[1]||!shift_cases) return 1;
    printf("{\"passed\":true,\"continuation_cases\":65536,\"continue\":%u,\"abort\":%u,\"shift\":%u,\"all_eight_passages\":true,\"calls_state_live_locals_verified\":true}\n",outcomes[0],outcomes[1],shift_cases);return 0;
}

void ra2_state_movement_audit(uint32_t a,uint32_t b,uint32_t c,uint32_t d) { (void)a;(void)b;(void)c;(void)d; }
