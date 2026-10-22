"""独立装载原版片段，对照限速和第二方向补建，不替换数值参照。"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v7'
text = (ROOT/'evidence/movement-state-v6/template_probe.c').read_text(encoding='utf-8')
text = text.replace('#include "ground_prepare_bridge.h"', '#include "ground_prepare_bridge.h"\n#include "ground_followup_bridge.h"')
text = text.replace('ZERO_SPEED, OP_COUNT','ZERO_SPEED, TARGET_POSITION, PREPARE_CANDIDATE, OWNER_KIND, SLOW_RATIO, OP_COUNT')
text = text.replace('if (fixture & (1u << 11)) FIELD32(drive, 0xC) = 0;',
    'if ((fixture & (1u << 11)) && !(fixture & (1u << 14))) FIELD32(drive, 0xC) = 0;')
text = text.replace('3,1,1,2,2 };','3,1,1,2,2,1,2,0,0 };')
text = text.replace('uint16_t g_fpu_cw;','uint16_t g_fpu_cw;\ndouble g_st[8]; int g_fp_top;\nstatic double ratio_value;\nstatic unsigned surface_reads;')
text = text.replace('return (fixture & (1u << 16)) ? 104 : 208;',
    'return surface_reads++==0 ? ((fixture>>16)&3)*104 : ((fixture>>18)&3)*104;')
text = text.replace('FIELD32(owner,0x468)=FIELD32(owner,0x46C)=0;', 'memcpy(owner+0x468,arguments,8);')
text = text.replace('        default: exit(2);', '''        case TARGET_POSITION:
            memcpy((void *)(uintptr_t)arguments[0],owner+0x88,12);
            return arguments[0];
        case PREPARE_CANDIDATE:
            record[1]=MEM32(arguments[0]); record[2]=arguments[1];
            if (fixture & 16) FIELD32(owner,0x4D4)=UINT32_MAX;
            return 0;
        case OWNER_KIND: return fixture & 32 ? 1 : 6;
        case SLOW_RATIO: return 0;
        default: exit(2);''')
text = text.replace('    return operation(id, object, arguments);', '''    uint32_t result=operation(id,object,arguments);
    if (id==SLOW_RATIO) { __asm fld ratio_value }
    return result;''')
special = (ROOT/'evidence/movement-state-v6/special_probe.c').read_text(encoding='utf-8')
length = special[special.index('static void l_length(void)'):special.index('LIFTED(l_empty,STOP_EMPTY)')]
text = text.replace('LIFTED(l_length,LENGTH) ', length)
text = text.replace('static recomp_func_t lifted[OP_COUNT]', '''LIFTED(l_target_position,TARGET_POSITION) LIFTED(l_prepare_candidate,PREPARE_CANDIDATE) LIFTED(l_owner_kind,OWNER_KIND)
static void l_ratio(void)
{
    g_eax=operation(SLOW_RATIO,g_ecx,NULL);
    fp_push_impl(g_st,&g_fp_top,ratio_value); g_esp+=4;
}
static recomp_func_t lifted[OP_COUNT]''')
text = text.replace('l_neighbor,l_cell_accept,l_start,l_zero };','l_neighbor,l_cell_accept,l_start,l_zero,l_target_position,l_prepare_candidate,l_owner_kind,l_ratio };')
text = text.replace('        case 0x476AC0:', '        case 0x475D60: return l_target_position;\n        case 0x5D4540: return l_ratio;\n        case 0x476AC0:')
text = text.replace('    patch_jump(0x476AC0,', '''    patch_jump(0x475D60,stub_base+TARGET_POSITION*16);
    patch_jump(0x5D4540,stub_base+SLOW_RATIO*16);
    owner_vtable[0x4B8/4]=stub_base+PREPARE_CANDIDATE*16;
    owner_vtable[0x2C/4]=stub_base+OWNER_KIND*16;
    patch_jump(0x476AC0,''')
text = text.replace('for (unsigned i = 0; i < 6; ++i) patch_jump(addresses[i], stub_base + ids[i] * 16);',
    'for (unsigned i = 0; i < 6; ++i) if (addresses[i]!=0x41B780) patch_jump(addresses[i], stub_base + ids[i] * 16);')
text = text.replace('if (phase > 4)', 'if (phase > 1)')
text = text.replace('boundaries[0]=0x4A4015; boundaries[1]=0x4A45B7;',
    'boundaries[0]=phase==0 ? 0x4A3E35 : 0x4A3F8B; boundaries[1]=0x4A3F9F;')
text = text.replace('unsigned boundary_count=(phase==0 || phase>=3) ? 2 : 0;', 'unsigned boundary_count=phase==0 ? 1 : 2;')
text = text.replace('const uint32_t entries[] = { 0x4A3F8B,0x4A45B7,0x4A45D0,0x4A3F9F,0x4A3FA1 };',
    'const uint32_t entries[] = { 0x4A3C9B,0x4A3E35 };')
text = text.replace('        mov esi, dword ptr [esp + 24h]', '        mov esi, fixture_number\n        and esi, 3')
text = text.replace('    FIELD32(drive,0x58)=5;', '''    surface_reads=0; g_fp_top=0; memset(g_st,0,sizeof(g_st));
    static const float factors[]={0.0f,0.01f,0.1f,0.33333334f,0.7f,1.0f,1.5f,-0.1f};
    float terrain=factors[(number/3)%8];
    for (unsigned i=0;i<36;++i) memcpy((void *)(uintptr_t)(0x850EA0+i*4),&terrain,4);
    FIELD32(type_data,0x5A4)=(number/24)%9;
    static const double slopes[]={0.1,0.3,0.7,1.0,1.1,1.3333333333333333,1.0000000000000002,0.0};
    for(unsigned i=0;i<4;++i) memcpy(rules+0x690+i*8,&slopes[((number/7)+i)%8],8);
    static const double ratios[]={0.0,0.5,0.5000000000000001,1.0};
    ratio_value=ratios[(number/17)%4];
    double limit=0.5; memcpy(rules+0x1368,&limit,8);
    double speed=slopes[(number/19)%8]; memcpy(owner+0x468,&speed,8);
    FIELD32(drive,0x58)=(number&1) ? 64 : 5;''')
# 第二阶段的队列分别覆盖已有、缺失和重建回调更改。
text = text.replace('    owner[0x76]=(uint8_t)((fixture>>12)&1);', '''    owner[0x76]=(uint8_t)((fixture>>12)&1);
    FIELD32(owner,0x4D4)=number&1 ? UINT32_MAX : number&7;
    static const int32_t offsets[]={0,1,511,512,513,6144,100000,INT32_MAX,INT32_MIN};
    FIELD32(drive,0x34)=FIELD32(owner,0x88)+(uint32_t)offsets[(number/8)%9];
    FIELD32(drive,0x38)=FIELD32(owner,0x8C)+(fixture>>20);
    FIELD32(drive,0x3C)=FIELD32(owner,0x90)+(fixture&255);
    if (phase==1) FIELD32(drive,0x58)=5;''')
text = text.replace('            unsigned expected_crush = MEM8(frame_stack + 0x13);',
    '            unsigned expected_crush = MEM8(frame_stack + 0x13);\n            uint64_t expected_factor; memcpy(&expected_factor,(void *)(uintptr_t)(frame_stack+0x18),8);')
start = text.index('            g_ebx=number&7;')
end = text.index('            uint32_t flags = recomp_eflags',start)
text = text[:start]+'''            g_ebx=number&7; g_esi=number&3;
            uint32_t resume;
            if (phase==0) { ra2_ground_speed_prepare_bridge(); resume=0x4A3E35; }
            else resume=ra2_ground_followup_bridge();
'''+text[end:]
text = text.replace('|| g_ebx != native_head || g_esi != native_cell)',
    '|| g_ebx != native_head || (phase==1 && resume!=0x4A3F9F && g_esi!=native_cell))')
text = text.replace('int locals_diff=MEM8(frame_stack+0x13)!=expected_crush || MEM32(frame_stack+0x28)!=expected_level;',
    'uint64_t actual_factor; memcpy(&actual_factor,(void *)(uintptr_t)(frame_stack+0x18),8);\n            int locals_diff=MEM8(frame_stack+0x13)!=expected_crush || MEM32(frame_stack+0x28)!=expected_level || (phase==0 && actual_factor!=expected_factor);')
text = text.replace('template_cases','followup_cases')
text = text.replace('                for (unsigned i = 0; i < operation_count', '''                for(unsigned i=0;i<sizeof(drive);++i) if(drive[i]!=expected_drive[i]) printf("drive %x: %x/%x\\n",i,drive[i],expected_drive[i]);
                for(unsigned i=0;i<sizeof(owner);++i) if(owner[i]!=expected_owner[i]) printf("owner %x: %x/%x\\n",i,owner[i],expected_owner[i]);
                printf("locals=%d factor=%llx/%llx\\n",locals_diff,(unsigned long long)actual_factor,(unsigned long long)expected_factor);
                for (unsigned i = 0; i < operation_count''')
handler = '''static LONG CALLBACK log_probe_exception(EXCEPTION_POINTERS *info)
{
    fprintf(stderr,"native exception code=%08lx ip=%p case=%u fixture=%08x\\n",info->ExceptionRecord->ExceptionCode,info->ExceptionRecord->ExceptionAddress,fixture_number,fixture);
    fflush(stderr); return EXCEPTION_CONTINUE_SEARCH;
}
'''
text = text.replace('int main(int argc, char **argv)',handler+'\nint main(int argc, char **argv)')
text = text.replace('    if (argc != 3)', '    AddVectoredExceptionHandler(1,log_probe_exception);\n    if (argc != 3)')
(STAGE/'followup_probe.c').write_text(text,encoding='utf-8',newline='\n')
shutil.copy2(ROOT/'evidence/movement-state-v6/native_probe_host.h',STAGE/'native_probe_host.h')
script = (ROOT/'build-template-probe-v6.ps1').read_text(encoding='utf-8')
script = script.replace('movement-state-v6','movement-state-v7').replace('template_probe','followup_probe')
script = script.replace(' /Fe:', ' ..\\..\\ra2\\src\\runtime\\ground_followup_bridge.c ..\\..\\ra2\\src\\gameplay\\ground_followup.c ..\\..\\ra2\\src\\gameplay\\ground_turn.c /Fe:')
(ROOT/'build-followup-probe-v7.ps1').write_text(script,encoding='utf-8',newline='\n')
