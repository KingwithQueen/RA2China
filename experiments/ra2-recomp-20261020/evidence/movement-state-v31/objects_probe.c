#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_objects_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))

enum Op { LOCATION,ACCEPT,KIND,FITS,BUILDING,CELL,TECHNO,ABILITY,TYPE,ALLY,WEAPON,SELECT_WEAPON,OP_COUNT };
static const unsigned argc_op[]={1,1,0,1,0,1,0,1,0,1,1,1};
static unsigned char unit[0x700],object_data[0x700],related[0x700],link_data[0x40],owner_type[0x1400],object_type[0x1400],house[0x200],techno[0x200],weapon[0x100],warhead[0x200],stack_data[8192],cell[0x200],neighbor[0x200];
static uint32_t owner_vt[0x500/4],object_vt[0x200/4],holders[2],fixture,number,frame,stub_base,cleanup_bytes,records[32][8],count,phase,entry_object,entry_address,weapon_reads;
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control,native_esi,native_edi;
static unsigned outcomes[7],kind_reads;
static uint32_t op(unsigned id,uint32_t object,const uint32_t *args) {
    if(count==32) exit(2);uint32_t *r=records[count++];r[0]=id;r[1]=object;
    switch(id) {
        case LOCATION: MEM32(args[0])=object==P(related) ? 0x00100020 : fixture&8 ? 0x00100020 : 0x00100021;return args[0];
        case ACCEPT: r[2]=args[0];return (fixture>>4)&1;
        case KIND: { const uint32_t kinds[]={1,6,36,15};return kinds[((fixture>>5)+(phase==4 ? kind_reads++ : 0))&3]; }
        case FITS: r[2]=args[0];return (fixture>>7)&1;
        case BUILDING: return fixture&(1u<<8) ? entry_object : P(related);
        case CELL: r[2]=MEM32(args[0]);return P(neighbor);
        case TECHNO: return fixture&(1u<<9) ? P(techno) : 0;
        case ABILITY: r[2]=args[0];return (fixture>>10)&1;
        case TYPE: return P(object_type);
        case ALLY: r[2]=args[0];return (fixture>>11)&1;
        case WEAPON:
            r[2]=args[0];return P(&holders[weapon_reads++ ? 1 : 0]);
        case SELECT_WEAPON: r[2]=args[0];return 2;
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
L(l_loc,LOCATION) L(l_accept,ACCEPT) L(l_kind,KIND) L(l_fits,FITS) L(l_building,BUILDING) L(l_cell,CELL)
L(l_techno,TECHNO) L(l_ability,ABILITY) L(l_type,TYPE) L(l_ally,ALLY) L(l_weapon,WEAPON) L(l_select,SELECT_WEAPON)
static recomp_func_t lifted[]={l_loc,l_accept,l_kind,l_fits,l_building,l_cell,l_techno,l_ability,l_type,l_ally,l_weapon,l_select};
static const uint32_t targets[]={0x636E30,0x453AF0,0x4717B0,0x548070,0x40DBD0,0x6D7910,0x4E5580};
static const unsigned ids[]={ACCEPT,FITS,BUILDING,CELL,TECHNO,ABILITY,ALLY};
recomp_func_t recomp_lookup_manual(uint32_t a) {
    if(a>=stub_base&&a<stub_base+OP_COUNT*16) return lifted[(a-stub_base)/16];
    for(unsigned i=0;i<7;++i) if(a==targets[i]) return lifted[ids[i]];return NULL;
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
        lea ebx,cell
        mov edi,dword ptr [esp+8Ch]
        lea eax,object_type
        jmp entry_address
    }
}

static void initialize(unsigned n) {
    number=n;fixture=n*1664525u+1013904223u;fixture^=fixture<<13;fixture^=fixture>>17;fixture^=fixture<<5;
    memset(unit,0,sizeof(unit));memset(object_data,0,sizeof(object_data));memset(related,0,sizeof(related));memset(link_data,0,sizeof(link_data));
    memset(owner_type,0,sizeof(owner_type));memset(object_type,0,sizeof(object_type));memset(house,0,sizeof(house));
    memset(techno,0,sizeof(techno));memset(weapon,0,sizeof(weapon));memset(warhead,0,sizeof(warhead));
    memset(cell,0,sizeof(cell));memset(neighbor,0,sizeof(neighbor));memset(stack_data,0xA5,sizeof(stack_data));memset(records,0,sizeof(records));
    count=weapon_reads=native_resume=kind_reads=0;frame=P(stack_data+4096);entry_object=phase==0&&n%17==0 ? P(unit) : P(object_data);
    F(unit,0)=P(owner_vt);F(object_data,0)=P(object_vt);F(related,0)=P(object_vt);
    F(unit,0x5AC)=P(owner_type);F(object_data,0x5AC)=P(object_type);F(object_data,0x418)=P(object_type);
    F(unit,0x588)=fixture&1 ? P(link_data) : 0;F(link_data,0x28)=fixture&2 ? P(related) : 0;
    F(object_data,0x30)=fixture&4 ? P(related) : 0;object_data[0x14]=(uint8_t)((fixture>>3)&255);
    owner_type[0xBB0]=(fixture>>12)&1;object_type[0xBB0]=(fixture>>13)&1;
    object_type[0x1349]=(fixture>>14)&1;object_type[0x1385]=(fixture>>15)&1;
    object_type[0x1359]=(fixture>>16)&1;object_type[0x135A]=(fixture>>17)&1;object_type[0x1214]=(fixture>>18)&1;
    object_type[0x1350]=(fixture>>19)&1;object_type[0x1FD]=(fixture>>20)&1;
    owner_type[0xAF3]=(fixture>>21)&1;owner_type[0xAA0]=(fixture>>22)&1;
    F(object_data,0x1B4)=P(house);F(unit,0x1B4)=P(house);house[0x142]=(fixture>>23)&1;
    const uint32_t missions[]={8,12,0,5};F(object_data,0x4EC)=missions[(fixture>>24)&3];
    F(techno,0x1B8)=fixture&(1u<<26) ? 2 : 0;
    holders[0]=fixture&(1u<<27) ? P(weapon) : 0;holders[1]=fixture&(1u<<28) ? P(weapon) : 0;
    F(weapon,0xAC)=fixture&(1u<<29) ? P(warhead) : 0;warhead[0x146]=(fixture>>30)&1;
    MEM32(frame+0x14)=P(unit);MEM32(frame+0x7C)=P(cell);MEM32(frame+0x80)=n&1 ? UINT32_MAX : 0;
    MEM32(frame+0x8C)=n%8;MEM32(frame+0x88)=0xAABBCC00|((fixture>>31)&1);
    MEM16(cell+0x24)=(uint16_t)n;MEM16(cell+0x26)=(uint16_t)(n^0xFFFF);MEM32(0x851A78)=0x0001FFFF;
    const uint32_t entries[]={0x70346B,0x7035AC,0x70397C,0x70394F,0x7034BF,0x7035DF,0x703A12};entry_address=entries[phase];
}
int main(int argc,char **argv) {
    if(argc!=3) return 2;phase=(unsigned)atoi(argv[2]);if(phase>6) return 2;hold_image();map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);if(!stubs) return 2;stub_base=P(stubs);
    for(unsigned i=0;i<OP_COUNT;++i) { unsigned char *s=stubs+i*16;s[0]=0x68;memcpy(s+1,&i,4);s[5]=0xE9;uint32_t rel=P(native_stub)-P(s+10);memcpy(s+6,&rel,4); }
    for(unsigned i=0;i<7;++i) patch(targets[i],stub_base+ids[i]*16);
    owner_vt[0x39C/4]=stub_base+WEAPON*16;owner_vt[0x2B8/4]=stub_base+SELECT_WEAPON*16;
    object_vt[0x1A0/4]=stub_base+LOCATION*16;object_vt[0x2C/4]=stub_base+KIND*16;object_vt[0x84/4]=stub_base+TYPE*16;
    const uint32_t boundaries[]={0x7031B1,0x703A95,0x703B5A,0x703536,0x7038FD,0x703693,0x7038EF};
    for(unsigned i=0;i<7;++i) {
        unsigned char *s=stubs+(OP_COUNT+i)*16;s[0]=0xC7;s[1]=5;uint32_t dest=P(&native_resume);memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4);s[10]=0xE9;uint32_t rel=P(trap)-P(s+15);memcpy(s+11,&rel,4);patch(boundaries[i],P(s));
    }
    FlushInstructionCache(GetCurrentProcess(),NULL,0);
    for(unsigned n=0;n<65536;++n) {
        initialize(n);run_original();
        uint32_t expected_records[32][8],expected_count=count,expected_resume=native_resume;memcpy(expected_records,records,sizeof(records));
        const uint32_t locals[]={0x10,0x14,0x18,0x1C,0x20,0x2C,0x30,0x7C,0x80,0x88,0x8C};uint32_t expected_locals[11];
        for(unsigned i=0;i<11;++i) expected_locals[i]=MEM32(frame+locals[i]);
        initialize(n);g_esp=frame;g_ebp=P(unit);g_ebx=P(cell);g_esi=entry_object;g_edi=MEM32(frame+0x8C);g_fpu_cw=0x37F;
        uint32_t resume=ra2_ground_object_branch_bridge(phase);
        int local_diff=0;for(unsigned i=0;i<11;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) local_diff=1;
        int live_esi=resume==0x703536||resume==0x7038FD||resume==0x703693||resume==0x7038EF;
        if(resume!=expected_resume || g_esp!=native_esp || g_ebp!=native_ebp || (live_esi&&g_esi!=native_esi)
            || local_diff || count!=expected_count || memcmp(records,expected_records,sizeof(records))) {
            printf("object mismatch phase=%u case=%u fixture=%08x resume=%x/%x calls=%u/%u locals=%d esi=%x/%x\n",phase,number,fixture,resume,expected_resume,count,expected_count,local_diff,g_esi,native_esi);
            for(unsigned i=0;i<11;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) printf("local %x=%x/%x\n",locals[i],MEM32(frame+locals[i]),expected_locals[i]);
            for(unsigned i=0;i<count||i<expected_count;++i) if(memcmp(records[i],expected_records[i],32)) { printf("call %u\n",i);for(unsigned j=0;j<8;++j) printf(" %u:%x/%x",j,records[i][j],expected_records[i][j]);puts(""); }
            return 1;
        }
        for(unsigned i=0;i<7;++i) if(resume==boundaries[i]) ++outcomes[i];
    }
    printf("{\"passed\":true,\"phase\":%u,\"object_cases\":65536,\"outcomes\":[%u,%u,%u,%u,%u,%u,%u],\"calls_live_state_verified\":true}\n",phase,outcomes[0],outcomes[1],outcomes[2],outcomes[3],outcomes[4],outcomes[5],outcomes[6]);return 0;
}

void ra2_state_movement_audit(uint32_t a,uint32_t b,uint32_t c,uint32_t d) { (void)a;(void)b;(void)c;(void)d; }
