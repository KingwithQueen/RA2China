from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v6'
text = (ROOT/'evidence/movement-state-v5/reaction_probe.c').read_text(encoding='utf-8')
text = text.replace('RECURSE, OP_COUNT','RECURSE, REVEAL, OP_COUNT').replace('2,2,3,3 };','2,2,3,3,0 };')
text = text.replace('        default: exit(2);','        case REVEAL: owner[0x57B] = 1; return 0;\n        default: exit(2);')
text = text.replace('static recomp_func_t lifted[OP_COUNT]', 'LIFTED(l_reveal,REVEAL)\nstatic recomp_func_t lifted[OP_COUNT]')
text = text.replace('l_sound,l_find,l_attack,l_recurse };','l_sound,l_find,l_attack,l_recurse,l_reveal };')
text = text.replace('        case 0x713DB0:', '        case 0x478740: return l_reveal;\n        case 0x713DB0:')
text = text.replace('LIFTED(l_length,LENGTH)', '''static void l_length(void)
{
    uint32_t point = g_ecx, result, target_address = 0x41B780;
    uint16_t host_control, guest_control = g_fpu_cw;
    __asm
    {
        fnstcw host_control
        fldcw guest_control
        mov ecx, point
        call target_address
        mov result, eax
        fnstcw guest_control
        fldcw host_control
    }
    g_eax = result; g_fpu_cw = guest_control; g_esp += 4;
}''')
text = text.replace('for (unsigned i = 0; i < 6; ++i) patch_jump(addresses[i], stub_base + ids[i] * 16);',
    'for (unsigned i = 0; i < 6; ++i) if (addresses[i] != 0x41B780) patch_jump(addresses[i], stub_base + ids[i] * 16);')
text = text.replace('    patch_jump(0x713DB0,', '    patch_jump(0x478740, stub_base + REVEAL * 16);\n    patch_jump(0x713DB0,')
text = text.replace('    unsigned boundary_count = 0;', '    boundaries[0] = 0x4A3600;\n    unsigned boundary_count = 1;')
text = text.replace('if (phase > 3)', 'if (phase > 0)')
text = text.replace('const uint32_t entries[] = { 0x4A3A8E,0x4A3A98,0x4A3ACF,0x4A3BFD };','const uint32_t entries[] = { 0x4A36ED };')
text = text.replace('        mov eax, dword ptr [esp + 18h]\n        jmp entry_address',
    '        mov ecx, dword ptr [esp + 18h]\n        jmp entry_address')
text = text.replace('    FIELD32(drive, 0x58) = 5;', '''    FIELD32(drive, 0x58) = 5;
    MEM32(frame_stack + 0x18) = number % 8;
    static const int32_t offsets[] = { 0,1,255,511,512,513,1000,100000,INT32_MAX,INT32_MIN };
    FIELD32(drive, 0x34) = FIELD32(owner, 0x88) + (uint32_t)offsets[(number / 8) % 10];
    FIELD32(drive, 0x38) = FIELD32(owner, 0x8C) + ((fixture >> 16) & 255);
    FIELD32(drive, 0x3C) = FIELD32(owner, 0x90) + ((fixture >> 23) & 511);''')
text = text.replace('            ra2_ground_reaction_bridge(phase);\n            uint32_t resume = 0;',
    '            g_ecx = MEM32(frame_stack + 0x18);\n            uint32_t resume = ra2_ground_special_obstacle_bridge();')
text = text.replace('|| (phase != 2 && (g_ebx != native_head || g_esi != native_cell || (resume != 0x4A3C9B && g_edi != native_level)))',
    '|| g_esi != native_cell')
text = text.replace('reaction_cases','special_cases')
text = text.replace('expected_resume = native_resume;', 'expected_resume = native_resume == 0x4A3600 ? 0x4A35FE : native_resume;')
(STAGE/'special_probe.c').write_text(text,encoding='utf-8',newline='\n')
shutil.copy2(ROOT/'evidence/movement-state-v5/native_probe_host.h',STAGE/'native_probe_host.h')
script = (ROOT/'build-reaction-probe-v5.ps1').read_text(encoding='utf-8').replace('movement-state-v5','movement-state-v6').replace('reaction_probe','special_probe')
script = script.replace(' /Fe:',' ..\\..\\ra2\\src\\gameplay\\ground_special.c /Fe:')
(ROOT/'build-special-probe-v6.ps1').write_text(script,encoding='utf-8',newline='\n')
