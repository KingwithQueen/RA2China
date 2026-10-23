extern unsigned ra2_ground_allied_relation_bridge(void);
extern unsigned ra2_ground_moving_tail_bridge(void);
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_allied_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))


enum Op { MISSION,KIND,TURNING,MOVING,ALLY,FACING,LOCATION,WANTS,OP_COUNT };
void ra2_state_movement_audit(unsigned a,uint32_t b,uint32_t c,uint32_t d) {(void)a;(void)b;(void)c;(void)d;}
static const unsigned argc_op[]={0,0,0,1,1,1,1,1};
static unsigned char unit[0x700],object_data[0x700],house[0x200],cell[0x200],locomotor[32],stack_data[8192];
static uint32_t owner_vt[0x500/4],object_vt[0x500/4],loco_vt[0xC0/4];
static uint32_t fixture,number,frame,stub_base,cleanup_bytes,records[32][8],count,entry_object,entry_address;
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control,native_esi,native_edi;
static unsigned outcomes[5],mission_reads,tail,relation;
static uint32_t initial_bx;
static uint32_t op(unsigned id,uint32_t object,const uint32_t *args) {
    if(count==32) exit(2); uint32_t *r=records[count++];r[0]=id;r[1]=object;
    switch(id) {
        case MISSION: { const uint32_t values[]={7,11,2,5};return values[(fixture>>(mission_reads++ ? 2 : 0))&3]; }
        case KIND: return fixture&16 ? 15 : fixture&32 ? 1 : 6;
        case TURNING: return (fixture>>6)&1;
        case MOVING: r[2]=args[0];return (fixture>>7)&1;
        case ALLY: r[2]=args[0];return (fixture>>8)&1;
        case FACING:
            MEM32(args[0])=(fixture>>(object==P(unit)+0x2E0 ? 9 : 17))&0xFFFF; return args[0];
        case LOCATION:
            for(unsigned i=0;i<3;++i) MEM32(args[0]+4*i)=MEM32(object+0x88+4*i)+i*3;
            return args[0];
        case WANTS: if(tail && number%3==0){MEM32(frame+0x8C)=number%9-3;MEM32(frame+0x14)=P(unit)+4;}r[2]=args[0];return (fixture>>25)&1;
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
L(l_mission,MISSION) L(l_kind,KIND) L(l_turning,TURNING) L(l_moving,MOVING) L(l_ally,ALLY) L(l_facing,FACING) L(l_location,LOCATION) L(l_wants,WANTS)
static recomp_func_t lifted[]={l_mission,l_kind,l_turning,l_moving,l_ally,l_facing,l_location,l_wants};
/* 用映射原版的实际数学服务验证调用者，避免拿宿主 sqrt/atan2 充当原版近似表。 */
static void l_angle(void) {
    uint16_t saved; __asm fnstcw saved
    __asm fldcw g_fpu_cw
    double result=((double(__cdecl *)(double,double))(uintptr_t)0x4BA600)(*(double *)(uintptr_t)(g_esp+4),*(double *)(uintptr_t)(g_esp+12));
    __asm fnstcw g_fpu_cw
    __asm fldcw saved
    fp_push_impl(g_st,&g_fp_top,result); g_esp+=4;
}
static void l_sqrt(void) {
    uint16_t saved; __asm fnstcw saved
    __asm fldcw g_fpu_cw
    double result=((double(__cdecl *)(double))(uintptr_t)0x4BA410)(*(double *)(uintptr_t)(g_esp+4));
    __asm fnstcw g_fpu_cw
    __asm fldcw saved
    fp_push_impl(g_st,&g_fp_top,result); g_esp+=4;
}
static void l_convert(void) {
    double value=fp_pop_impl(g_st,&g_fp_top); uint16_t saved;
    __asm {
        fnstcw saved
        fldcw g_fpu_cw
        fld value
        mov eax,77F110h
        call eax
        mov g_eax,eax
        mov g_edx,edx
        fnstcw g_fpu_cw
        fldcw saved
    }
    g_esp+=4;
}
recomp_func_t recomp_lookup_manual(uint32_t a) {
    if(a>=stub_base&&a<stub_base+OP_COUNT*16) return lifted[(a-stub_base)/16];
    if(a==0x4B8C90) return l_turning;if(a==0x4E5580) return l_ally;if(a==0x4B8BE0) return l_facing;
    if(a==0x4BA600) return l_angle;if(a==0x4BA410) return l_sqrt;if(a==0x77F110) return l_convert;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
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
        mov ebx,initial_bx
        mov edi,dword ptr [esp+8Ch]
        jmp entry_address
    }
}


static void initialize(unsigned n) {
    number=n;fixture=n*1664525u+1013904223u;fixture^=fixture<<13;fixture^=fixture>>17;fixture^=fixture<<5;
    memset(unit,0,sizeof(unit));memset(object_data,0,sizeof(object_data));memset(stack_data,0xA5,sizeof(stack_data));memset(records,0,sizeof(records));
    count=mission_reads=native_resume=0;frame=P(stack_data+4096);entry_object=P(object_data);entry_address=0x703693;
    F(unit,0)=P(owner_vt);F(object_data,0)=P(object_vt);F(locomotor,0)=P(loco_vt);
    F(unit,0x494)=fixture&(1u<<26) ? P(object_data) : 0;F(unit,0x1B0)=fixture&(1u<<27) ? P(object_data) : 0;
    F(unit,0x1B4)=P(house);F(object_data,0x564)=P(locomotor);
    F(object_data,0x494)=fixture&(1u<<28) ? P(unit) : 0;
    object_data[0x14]=(fixture>>27)&4;object_data[0x5A0]=(fixture>>30)&1;
    for(unsigned i=0;i<3;++i) {
        F(unit,0x88+i*4)=20000+i*64;
        const int32_t edge[]={0,1,255,256,510,511,512,513,1024,-511,-512,-256};
        F(object_data,0x88+i*4)=F(unit,0x88+i*4)+(uint32_t)(i<2 ? edge[(n>>(i*4))%12] : (int32_t)(n%3)*64);
    }
    MEM32(frame+0x14)=P(unit);MEM32(frame+0x7C)=P(cell);MEM32(frame+0x8C)=n%8;
    initial_bx=P(cell);if(relation){entry_address=0x70372C;initial_bx=(P(cell)&0xFFFFFF00u)|(n&1);MEM32(frame+0x20)=P(object_data);}
    if(tail){entry_address=0x703895;MEM32(frame+0x20)=P(object_data);}
    MEM32(0x7D8964)=n&1 ? 0xF7F : 0x37F;
}
int main(int argc,char **argv) {
    if(argc<2||argc>3) return 2;relation=argc==3&&!strcmp(argv[2],"relation");tail=argc==3&&!relation;hold_image();map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);if(!stubs) return 2;stub_base=P(stubs);
    for(unsigned i=0;i<OP_COUNT;++i) { unsigned char *s=stubs+i*16;s[0]=0x68;memcpy(s+1,&i,4);s[5]=0xE9;uint32_t rel=P(native_stub)-P(s+10);memcpy(s+6,&rel,4); }
    patch(0x4B8C90,stub_base+TURNING*16);patch(0x4E5580,stub_base+ALLY*16);patch(0x4B8BE0,stub_base+FACING*16);
    owner_vt[0x16C/4]=stub_base+MISSION*16;owner_vt[0x48/4]=stub_base+LOCATION*16;
    object_vt[0x2C/4]=stub_base+KIND*16;object_vt[0x48/4]=stub_base+LOCATION*16;
    loco_vt[0x10/4]=stub_base+MOVING*16;loco_vt[0xA4/4]=stub_base+WANTS*16;
    const uint32_t boundaries[]={0x7031B1,0x703B5A,0x70397C,0x70394F,0x7038EF};
    for(unsigned i=0;i<5;++i) {
        unsigned char *s=stubs+(OP_COUNT+i)*16;s[0]=0xC7;s[1]=5;uint32_t dest=P(&native_resume);memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4);s[10]=0xE9;uint32_t rel=P(trap)-P(s+15);memcpy(s+11,&rel,4);patch(boundaries[i],P(s));
    }
    FlushInstructionCache(GetCurrentProcess(),NULL,0);
    for(unsigned n=0;n<65536;++n) {
        initialize(n);run_original();
        uint32_t expected_records[32][8],expected_count=count,expected_resume=native_resume;memcpy(expected_records,records,sizeof(records));
        const uint32_t locals[]={0x14,0x20,0x28,0x34,0x38,0x3C,0x40,0x44,0x60,0x64,0x68,0x6C,0x70,0x74,0x7C,0x8C};uint32_t expected_locals[16];
        for(unsigned i=0;i<16;++i) expected_locals[i]=MEM32(frame+locals[i]);
        initialize(n);g_esp=frame;g_ebp=P(unit);g_ebx=initial_bx;g_esi=entry_object;g_edi=MEM32(frame+0x8C);g_fpu_cw=0x37F;g_fp_top=0;memset(g_st,0,sizeof(g_st));
        uint32_t resume=relation?ra2_ground_allied_relation_bridge():tail?ra2_ground_moving_tail_bridge():ra2_ground_allied_bridge();
        int local_diff=0;for(unsigned i=0;i<16;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) local_diff=1;
        if((tail && (g_ebp!=native_ebp||g_esi!=native_esi||g_edi!=native_edi)) || resume!=expected_resume || g_esp!=native_esp || local_diff || count!=expected_count || memcmp(records,expected_records,sizeof(records)) || g_fpu_cw!=(uint16_t)native_control) {
            printf("allied mismatch case=%u fixture=%08x resume=%x/%x calls=%u/%u locals=%d cw=%x/%x\n",number,fixture,resume,expected_resume,count,expected_count,local_diff,g_fpu_cw,native_control);
            for(unsigned i=0;i<16;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) printf("local %x=%x/%x\n",locals[i],MEM32(frame+locals[i]),expected_locals[i]);
            for(unsigned i=0;i<count||i<expected_count;++i) if(memcmp(records[i],expected_records[i],32)) {printf("call %u\n",i);for(unsigned j=0;j<8;++j)printf(" %u:%x/%x",j,records[i][j],expected_records[i][j]);puts("");}
            return 1;
        }
        for(unsigned i=0;i<5;++i) if(resume==boundaries[i]) ++outcomes[i];
    }
    printf("{\"passed\":true,\"allied_cases\":65536,\"moving_tail_cases\":%u,\"outcomes\":[%u,%u,%u,%u,%u],\"native_math_services\":true,\"calls_live_state_control_verified\":true}\n",tail?65536u:0u,outcomes[0],outcomes[1],outcomes[2],outcomes[3],outcomes[4]);return 0;
}
