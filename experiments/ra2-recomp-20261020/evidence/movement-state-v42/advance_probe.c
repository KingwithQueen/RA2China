#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_advance_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw; double g_st[8]; int g_fp_top;
#define P(x) ((uint32_t)(uintptr_t)(x))
#define F(x,o) (*(uint32_t *)((x)+(o)))
enum Op { NEEDS_MARK,MARK,CURRENT_CELL,TRANSFORM,PLACE,OCCUPATION,TYPE,HEIGHT,CELL,OBJECT_TYPE,DAMAGE,ABILITY,REFRESH,FACING,OP_COUNT };
static const unsigned argc_op[]={0,1,1,3,1,1,0,1,1,0,6,1,1,1};
static unsigned char drive[128],unit[0x700],type[0x1000],cells[2][0x200],objects[3][0x100],object_types[3][0x200],stack_data[8192],overlay[0x300],rules[0x1000];
static uint32_t vtable[0x500/4],object_vtable[0x200/4],samples[8][3],overlay_table[3];
static uint32_t fixture,number,frame,stub_base,cleanup_bytes,records[64][12],count,cell_reads;
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control;
static unsigned counts[2],damage_cases,same_cell_cases,multi_damage_cases,removed_before_enter_cases;
static uint32_t op(unsigned id,uint32_t object,const uint32_t *args)
{
    if(count==64) exit(2);
    uint32_t *r=records[count++]; r[0]=id; r[1]=object;
    r[9]=unit[0x74]; r[10]=unit[0x79]; r[11]=unit[0x5A0]|unit[0x5A1]<<8;
    switch(id)
    {
        case NEEDS_MARK: return fixture&1;
        case MARK: memcpy(r+2,(void *)(uintptr_t)args[0],12); return 0;
        case CURRENT_CELL:
            MEM16(args[0])=(uint16_t)((int32_t)F(unit,0x88)/256);
            MEM16(args[0]+2)=(uint16_t)((int32_t)F(unit,0x8C)/256);
            return args[0];
        case TRANSFORM:
        {
            r[2]=MEM32(args[1]); r[3]=MEM32(args[1]+4); r[4]=MEM32(args[2]);
            MEM32(args[0])=MEM32(args[1]); MEM32(args[0]+4)=MEM32(args[1]+4);
            MEM32(args[0]+8)=1234;
            MEM32(args[2])=(MEM32(args[2])+((fixture>>1)&7))&255;
            return args[0];
        }
        case PLACE:
            memcpy(r+2,(void *)(uintptr_t)args[0],12);
            memcpy(unit+0x88,(void *)(uintptr_t)args[0],12);
            if(fixture&(1u<<22)) unit[0x7D]=0;
            return 0;
        case OCCUPATION:
            r[2]=args[0];
            if(args[0] && (fixture&(1u<<23))) unit[0x7D]=0;
            return 0;
        case TYPE: return P(type);
        case HEIGHT: memcpy(r+2,(void *)(uintptr_t)args[0],12); return fixture&128 ? 0 : UINT32_MAX-103;
        case CELL:
            r[2]=MEM32(args[0]);
            return P(cells[cell_reads++ ? 1 : 0]);
        case OBJECT_TYPE:
            for(unsigned i=0;i<3;++i) if(object==P(objects[i])) return P(object_types[i]);
            exit(2);
        case DAMAGE:
            r[2]=MEM32(args[0]); memcpy(r+3,args+1,20);
            if(object==P(unit)) { if(fixture&(1u<<24)) unit[0x7D]=0; }
            else { MEM32(object+0x30)=0; } /* 回调移除当前链项，下一项仍需被处理。 */
            return 0;
        case ABILITY: r[2]=args[0]; return (fixture>>18)&1;
        case REFRESH: r[2]=args[0]; return 0;
        case FACING: r[2]=MEM16(args[0]); return 0;
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
L(l_needs,NEEDS_MARK) L(l_mark,MARK) L(l_current,CURRENT_CELL) L(l_transform,TRANSFORM)
L(l_place,PLACE) L(l_occ,OCCUPATION) L(l_type,TYPE) L(l_height,HEIGHT) L(l_cell,CELL)
L(l_objtype,OBJECT_TYPE) L(l_damage,DAMAGE) L(l_ability,ABILITY) L(l_refresh,REFRESH) L(l_facing,FACING)
static recomp_func_t lifted[]={l_needs,l_mark,l_current,l_transform,l_place,l_occ,l_type,l_height,l_cell,l_objtype,l_damage,l_ability,l_refresh,l_facing};
static const uint32_t targets[]={0x4A4740,0x55A280,0x548070,0x6D7910,0x4B8B10};
static const unsigned ids[]={TRANSFORM,HEIGHT,CELL,ABILITY,FACING};
recomp_func_t recomp_lookup_manual(uint32_t a)
{
    if(a>=stub_base && a<stub_base+OP_COUNT*16) return lifted[(a-stub_base)/16];
    for(unsigned i=0;i<5;++i) if(a==targets[i]) return lifted[ids[i]];
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
        mov ecx,4A16A6h
        jmp ecx
    }
}
static void initialize(unsigned n)
{
    number=n; fixture=n*1664525u+1013904223u; fixture^=fixture<<13; fixture^=fixture>>17; fixture^=fixture<<5;
    memset(drive,0,sizeof(drive)); memset(unit,0,sizeof(unit)); memset(stack_data,0xA5,sizeof(stack_data));
    memset(type,0,sizeof(type)); memset(cells,0,sizeof(cells)); memset(objects,0,sizeof(objects));
    memset(object_types,0,sizeof(object_types)); memset(overlay,0,sizeof(overlay)); memset(records,0,sizeof(records));
    count=cell_reads=native_resume=0;
    frame=P(stack_data+4096); F(drive,0xC)=P(unit); F(unit,0)=P(vtable);
    unit[0x74]=(uint8_t)((fixture>>2)&255); unit[0x79]=(fixture>>10)&1; unit[0x7D]=1;
    unit[0x5A0]=3; unit[0x5A1]=4; unit[0x5B8]=(fixture>>11)&1;
    type[0xAA0]=(fixture>>12)&1; type[0xAF3]=(fixture>>13)&1; type[0xAF4]=(fixture>>14)&1;
    drive[0x64]=(fixture>>15)&1;
    F(drive,0x5C)=(fixture>>16)&3;
    const int32_t coords[]={-16777217,-65537,-257,-256,-255,-1,0,1,255,256,257,65537,16777217,INT32_MAX,INT32_MIN};
    int32_t x=coords[n%15],y=coords[(n/15)%15];
    F(unit,0x88)=(uint32_t)x; F(unit,0x8C)=(uint32_t)y; F(unit,0x90)=fixture&128 ? 300 : UINT32_MAX-300;
    for(unsigned i=0;i<8;++i) {
        samples[i][0]=(uint32_t)x+((fixture&2) ? 257u : 0u);
        samples[i][1]=(uint32_t)y+((fixture&4) ? 513u : 0u);
        samples[i][2]=i*31;
    }
    MEM32(frame+0x38)=P(samples); MEM32(frame+0x58)=0;
    MEM32(0x7A00AC)=(fixture>>16)&3;
    MEM32(frame+0x8C)=samples[F(drive,0x5C)][0]; MEM32(frame+0x90)=samples[F(drive,0x5C)][1];
    cells[0][0x11B]=8; cells[1][0x11B]=(fixture&256) ? 4 : 8;
    F(cells[0],0x140)=(fixture&512) ? 256 : 0; F(cells[1],0x140)=(fixture&1024) ? 256 : 0;
    F(cells[1],0x44)=(fixture&(1u<<19)) ? 1 : UINT32_MAX;
    F(overlay,0x264)=(fixture>>20)&1; overlay_table[1]=P(overlay); MEM32(0xA35DEC)=P(overlay_table);
    for(unsigned i=0;i<3;++i) {
        F(objects[i],0)=P(object_vtable); F(objects[i],0x30)=i==2 ? 0 : P(objects[i+1]);
        object_types[i][0x1FD]=(fixture>>(25+i))&1;
    }
    F(cells[1],0xE4)=(fixture&(1u<<28)) ? P(objects[0]) : 0;
    F(cells[1],0xE8)=(fixture&(1u<<29)) ? P(objects[1]) : 0;
    F(rules,0xC74)=0x12345678; MEM32(0x839848)=P(rules); MEM32(0x8529C0)=104;
}
int main(int argc,char **argv)
{
    if(argc!=2) return 2;
    hold_image(); map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
    if(!stubs) return 2;
    stub_base=P(stubs);
    for(unsigned i=0;i<OP_COUNT;++i) {
        unsigned char *s=stubs+i*16; s[0]=0x68; memcpy(s+1,&i,4); s[5]=0xE9;
        uint32_t rel=P(native_stub)-P(s+10); memcpy(s+6,&rel,4);
    }
    for(unsigned i=0;i<5;++i) patch(targets[i],stub_base+ids[i]*16);
    const uint32_t slots[]={0xBC,0xEC,0x1A0,0x19C,0x11C,0x80,0x158,0x1B4};
    const unsigned vi[]={NEEDS_MARK,MARK,CURRENT_CELL,PLACE,OCCUPATION,TYPE,DAMAGE,REFRESH};
    for(unsigned i=0;i<8;++i) vtable[slots[i]/4]=stub_base+vi[i]*16;
    object_vtable[0x84/4]=stub_base+OBJECT_TYPE*16; object_vtable[0x158/4]=stub_base+DAMAGE*16;
    const uint32_t boundaries[]={0x4A1B60,0x4A263A};
    for(unsigned i=0;i<2;++i) {
        unsigned char *s=stubs+(OP_COUNT+i)*16;
        s[0]=0xC7; s[1]=5; uint32_t dest=P(&native_resume); memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4); s[10]=0xE9;
        uint32_t rel=P(trap)-P(s+15); memcpy(s+11,&rel,4); patch(boundaries[i],P(s));
    }
    FlushInstructionCache(GetCurrentProcess(),NULL,0);
    for(unsigned n=0;n<65536;++n) {
        initialize(n); run_original();
        unsigned char expected_unit[sizeof(unit)],expected_drive[sizeof(drive)],expected_objects[sizeof(objects)];
        uint32_t expected_records[64][12],expected_count=count,expected_resume=native_resume;
        memcpy(expected_unit,unit,sizeof(unit)); memcpy(expected_drive,drive,sizeof(drive));
        memcpy(expected_objects,objects,sizeof(objects)); memcpy(expected_records,records,sizeof(records));
        uint32_t expected_locals[8]; const uint32_t locals[]={0x30,0x48,0x4C,0x50,0x58,0x68,0x98,0x3C};
        for(unsigned i=0;i<8;++i) expected_locals[i]=MEM32(frame+locals[i]);
        initialize(n); g_esp=frame; g_ebp=P(drive); g_esi=P(samples); g_fpu_cw=0x37F;
        uint32_t resume=ra2_ground_advance_sample_bridge();
        int local_diff=0; for(unsigned i=0;i<8;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) local_diff=1;
        if(resume!=expected_resume || g_esp!=native_esp || g_ebp!=native_ebp || g_fpu_cw!=(uint16_t)native_control
            || memcmp(expected_unit,unit,sizeof(unit)) || memcmp(expected_drive,drive,sizeof(drive))
            || memcmp(expected_objects,objects,sizeof(objects)) || local_diff
            || count!=expected_count || memcmp(records,expected_records,sizeof(records))) {
            printf("advance mismatch case=%u fixture=%08x resume=%x/%x calls=%u/%u locals=%d\n",number,fixture,resume,expected_resume,count,expected_count,local_diff);
            for(unsigned i=0;i<8;++i) if(expected_locals[i]!=MEM32(frame+locals[i])) printf("local %x=%x/%x\n",locals[i],MEM32(frame+locals[i]),expected_locals[i]);
            for(unsigned i=0;i<count||i<expected_count;++i) if(memcmp(records[i],expected_records[i],48)) {
                printf("call %u\n",i); for(unsigned j=0;j<12;++j) printf(" %u:%x/%x",j,records[i][j],expected_records[i][j]); puts("");
            }
            for(unsigned i=0;i<sizeof(unit);++i) if(unit[i]!=expected_unit[i]) printf("unit %x=%x/%x\n",i,unit[i],expected_unit[i]);
            return 1;
        }
        ++counts[resume==boundaries[1]];
        unsigned damage_in_case=0,entered=0;
        for(unsigned i=0;i<count;++i) {
            if(records[i][0]==DAMAGE) ++damage_in_case;
            if(records[i][0]==OCCUPATION&&records[i][2]) entered=1;
        }
        if(damage_in_case>=4) ++multi_damage_cases;
        if(damage_in_case&&!entered&&(fixture&(1u<<24))) ++removed_before_enter_cases;

        for(unsigned i=0;i<count;++i) { if(records[i][0]==DAMAGE) ++damage_cases; if(records[i][0]==PLACE&&i&&records[i-1][0]!=OCCUPATION) ++same_cell_cases; }
    }
    if(!counts[0]||!counts[1]||!damage_cases||!same_cell_cases||!multi_damage_cases||!removed_before_enter_cases) return 1;
    printf("{\"passed\":true,\"advance_cases\":65536,\"continue_cases\":%u,\"removed_cases\":%u,\"damage_calls\":%u,\"same_cell_calls\":%u,\"multiple_chain_target_cases\":%u,\"removed_before_enter_cases\":%u,\"state_calls_live_locals_verified\":true}\n",counts[0],counts[1],damage_cases,same_cell_cases,multi_damage_cases,removed_before_enter_cases);
    return 0;
}

void ra2_state_movement_audit(uint32_t stage,uint32_t actor,uint32_t cell,uint32_t object)
{ (void)stage; (void)actor; (void)cell; (void)object; }
