#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_entry_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))

enum Op { NEIGHBOR,LINK,PLACEMENT,VISIBLE,EXEMPT,BASE,OP_COUNT };
static const unsigned argc_op[]={1,0,5,2,0,5};
static unsigned char unit[0x700],cells[2][0x200],links[2][0x40],stack_data[8192];
static uint32_t vtable[0x400/4],fixture,number,frame,stub_base,cleanup_bytes,records[32][12],count;
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control,native_esi,native_edi,entry_link;
static unsigned outcomes[3],upper_layer_cases,placement_changes;
static uint32_t op(unsigned id,uint32_t object,const uint32_t *args)
{
    if(count==32) exit(2);
    uint32_t *r=records[count++]; r[0]=id; r[1]=object;
    switch(id) {
        case NEIGHBOR: r[2]=args[0]; return P(cells[1]);
        case LINK: return fixture&2 ? P(links[1]) : 0;
        case PLACEMENT:
            r[2]=args[0]; r[3]=args[1]; r[4]=MEM32(args[2]); r[5]=MEM8(args[3]); r[6]=args[4];
            if(fixture&4) { MEM32(args[2])=5; MEM8(args[3])=1; }
            return fixture&8 ? 7 : (fixture>>4)&7;
        case VISIBLE: r[2]=args[0]; r[3]=args[1]; return (fixture>>7)&1;
        case EXEMPT: return (fixture>>8)&1;
        case BASE: memcpy(r+2,args,20); return (fixture>>9)&7;
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

#define L(name,id) static void name(void) { g_eax=op(id,g_ecx,(const uint32_t *)(uintptr_t)(g_esp+4)); g_esp+=4+argc_op[id]*4; }
L(l_neighbor,NEIGHBOR) L(l_link,LINK) L(l_place,PLACEMENT) L(l_visible,VISIBLE) L(l_exempt,EXEMPT) L(l_base,BASE)
static recomp_func_t lifted[]={l_neighbor,l_link,l_place,l_visible,l_exempt,l_base};
static const uint32_t targets[]={0x476AC0,0x47A130,0x55A740,0x4C86E0};
static const unsigned ids[]={NEIGHBOR,LINK,VISIBLE,BASE};
recomp_func_t recomp_lookup_manual(uint32_t a) {
    if(a>=stub_base && a<stub_base+OP_COUNT*16) return lifted[(a-stub_base)/16];
    for(unsigned i=0;i<4;++i) if(a==targets[i]) return lifted[ids[i]];
    return NULL;
}
recomp_func_t recomp_lookup(uint32_t a) { (void)a; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a; return NULL; }
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
        mov esi,entry_link
        lea ebx,cells
        mov ecx,703182h
        jmp ecx
    }
}

static void initialize(unsigned n) {
    number=n; fixture=n*1664525u+1013904223u; fixture^=fixture<<13; fixture^=fixture>>17; fixture^=fixture<<5;
    memset(unit,0,sizeof(unit)); memset(cells,0,sizeof(cells)); memset(links,0,sizeof(links));
    memset(stack_data,0xA5,sizeof(stack_data)); memset(records,0,sizeof(records)); count=native_resume=0;
    frame=P(stack_data+4096); F(unit,0)=P(vtable); entry_link=fixture&1 ? P(links[0]) : 0;
    const int32_t directions[]={-1,0,1,2,3,4,5,6,7,8};
    MEM32(frame+0x80)=(uint32_t)directions[n%10]; MEM32(frame+0x84)=fixture&16 ? 5 : UINT32_MAX;
    MEM32(frame+0x88)=fixture&0x2000 ? 0x100 : 0x101; MEM32(frame+0x8C)=0x12345678;
    MEM8(frame+0x11)=(fixture>>16)&1; MEM8(frame+0x12)=(fixture>>17)&255;
    MEM8(frame+0x13)=(MEM8(frame+0x12)>>5)&1; MEM32(frame+0x18)=0xFFFFFFFF;
    MEM32(0xA40774)=fixture&64;
    unit[0x32D]=(fixture>>12)&1;
    cells[0][0x11B]=1; F(cells[0],0x140)=(fixture>>4)&0x100;
    F(cells[0],0x128)=(fixture>>16)&255; F(cells[0],0x58)=12345;
    F(links[0],0x28)=fixture&0x4000 ? 0x80000000 : 0;
    if(fixture&0x8000) F(links[0],0x28)|=1;
    F(links[0],0x2C)=(n/10)%8; F(links[1],0x2C)=(n/80)%8;
}
int main(int argc,char **argv) {
    if(argc!=2) return 2;
    hold_image(); map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
    if(!stubs) return 2; stub_base=P(stubs);
    for(unsigned i=0;i<OP_COUNT;++i) {
        unsigned char *s=stubs+i*16; s[0]=0x68; memcpy(s+1,&i,4); s[5]=0xE9;
        uint32_t rel=P(native_stub)-P(s+10); memcpy(s+6,&rel,4);
    }
    for(unsigned i=0;i<4;++i) patch(targets[i],stub_base+ids[i]*16);
    vtable[0x198/4]=stub_base+PLACEMENT*16; vtable[0x2F4/4]=stub_base+EXEMPT*16;
    const uint32_t boundaries[]={0x703331,0x7031B1,0x703B5A};
    for(unsigned i=0;i<3;++i) {
        unsigned char *s=stubs+(OP_COUNT+i)*16;
        s[0]=0xC7; s[1]=5; uint32_t dest=P(&native_resume); memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4); s[10]=0xE9;
        uint32_t rel=P(trap)-P(s+15); memcpy(s+11,&rel,4); patch(boundaries[i],P(s));
    }
    /* 原版两个内联阻塞返回也截到共同终点，避免把测试宿主的栈当游戏返回栈。 */
    patch(0x7031E3,0x703B5A); patch(0x70322F,0x703B5A);
    patch(0x703265,0x703B5A); patch(0x7032E9,0x703B5A); patch(0x703327,0x703B5A);
    FlushInstructionCache(GetCurrentProcess(),NULL,0);
    for(unsigned n=0;n<65536;++n) {
        initialize(n); run_original();
        uint32_t expected_records[32][12],expected_count=count,expected_resume=native_resume;
        memcpy(expected_records,records,sizeof(records));
        const uint32_t locals[]={0x10,0x18,0x80,0x84,0x88,0x8C}; uint32_t expected_locals[6];
        for(unsigned i=0;i<6;++i) expected_locals[i]=MEM32(frame+locals[i]);
        initialize(n); g_esp=frame; g_ebp=P(unit); g_ebx=P(cells); g_esi=entry_link; g_fpu_cw=0x37F;
        uint32_t resume=ra2_ground_entry_bridge();
        int local_diff=0; for(unsigned i=0;i<6;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) local_diff=1;
        int abi_diff=resume==0x703331 && (g_esi!=native_esi||g_edi!=native_edi);
        if(resume!=expected_resume || g_esp!=native_esp || g_ebp!=native_ebp || abi_diff || local_diff
            || count!=expected_count || memcmp(records,expected_records,sizeof(records))) {
            printf("entry mismatch case=%u fixture=%08x resume=%x/%x calls=%u/%u locals=%d abi=%d\n",number,fixture,resume,expected_resume,count,expected_count,local_diff,abi_diff);
            for(unsigned i=0;i<6;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) printf("local %x=%x/%x\n",locals[i],MEM32(frame+locals[i]),expected_locals[i]);
            for(unsigned i=0;i<count||i<expected_count;++i) if(memcmp(records[i],expected_records[i],48)) {
                printf("call %u\n",i); for(unsigned j=0;j<12;++j) printf(" %u:%x/%x",j,records[i][j],expected_records[i][j]); puts("");
            }
            return 1;
        }
        ++outcomes[resume==boundaries[0] ? 0 : resume==boundaries[1] ? 1 : 2];
        if(MEM32(frame+0x18)==12345) ++upper_layer_cases;
        if(MEM8(frame+0x11)==1) ++placement_changes;
    }
    if(!outcomes[0]||!outcomes[1]||!outcomes[2]||!upper_layer_cases) return 1;
    printf("{\"passed\":true,\"entry_cases\":65536,\"continue\":%u,\"clear\":%u,\"blocked\":%u,\"upper_layer\":%u,\"placement_changes\":%u,\"calls_live_locals_verified\":true}\n",outcomes[0],outcomes[1],outcomes[2],upper_layer_cases,placement_changes);
    return 0;
}
