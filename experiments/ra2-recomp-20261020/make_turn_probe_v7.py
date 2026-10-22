from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v7'
text = (STAGE/'followup_probe.c').read_text(encoding='utf-8')
text = text.replace('SLOW_RATIO, OP_COUNT','SLOW_RATIO, REVEAL, OP_COUNT').replace('2,2,1,2,0,0 };','2,2,1,2,0,0,0 };')
text = text.replace('FIELD32(drive, 0x58) = 7; drive[0x61] = 0;',
    'FIELD32(drive, 0x58) = 7; drive[0x61] = 0;\n            if(fixture & (1u<<26)) FIELD32(drive,0xC)=0;')
text = text.replace('if (fixture & 16) owner[0x7D]=0;', 'if (fixture & (1u<<24)) owner[0x7D]=0;')
text = text.replace('if (fixture & 32) owner[0x76]=1;', 'if (fixture & (1u<<25)) owner[0x76]=1;')
text = text.replace('            return (fixture >> 2) & 7;',
    '            if (fixture & (1u<<23)) owner[0x7D]=0;\n            return (fixture >> 2) & 7;')
text = text.replace('        default: exit(2);', '        case REVEAL: owner[0x57B]=1; return 0;\n        default: exit(2);')
text = text.replace('static recomp_func_t lifted[OP_COUNT]', 'LIFTED(l_reveal,REVEAL)\nstatic recomp_func_t lifted[OP_COUNT]')
text = text.replace('l_target_position,l_prepare_candidate,l_owner_kind,l_ratio };','l_target_position,l_prepare_candidate,l_owner_kind,l_ratio,l_reveal };')
text = text.replace('        case 0x475D60:', '        case 0x478740: return l_reveal;\n        case 0x475D60:')
text = text.replace('    patch_jump(0x475D60,','    patch_jump(0x478740,stub_base+REVEAL*16);\n    patch_jump(0x475D60,')
text = text.replace('if (phase > 1)','if (phase > 0)')
text = text.replace('boundaries[0]=phase==0 ? 0x4A3E35 : 0x4A3F8B; boundaries[1]=0x4A3F9F;',
    'boundaries[0]=0x4A45D0;')
text = text.replace('unsigned boundary_count=phase==0 ? 1 : 2;', 'unsigned boundary_count=1;')
text = text.replace('const uint32_t entries[] = { 0x4A3C9B,0x4A3E35 };','const uint32_t entries[] = { 0x4A4015 };')
text = text.replace('        and esi, 3','        and esi, 7')
text = text.replace('    FIELD32(owner,0x4D4)=number&1 ? UINT32_MAX : number&7;', '''    FIELD32(owner,0x4D4)=number&1 ? UINT32_MAX : number&7;
    const uint32_t recursive_flags[]={0,1,0x100,0x101,0x80000001};
    MEM32(frame_stack+0x64)=recursive_flags[(number/11)%5];''')
text = text.replace('            unsigned expected_crush = MEM8(frame_stack + 0x13);',
    '            unsigned expected_crush = MEM8(frame_stack + 0x13);\n            unsigned char expected_candidate[12]; memcpy(expected_candidate,(void *)(uintptr_t)(frame_stack+0x38),12);')
start = text.index('            g_ebx=number&7;')
end = text.index('            uint32_t flags = recomp_eflags',start)
text = text[:start]+'''            g_ebx=number&7; g_esi=number&7;
            uint32_t resume=ra2_ground_turn_prepare_bridge();
'''+text[end:]
text = text.replace('|| g_ebx != native_head || (phase==1 && resume!=0x4A3F9F && g_esi!=native_cell))',
    '|| g_edi!=native_level)')
text = text.replace('|| (phase==0 && actual_factor!=expected_factor)',
    '|| memcmp(expected_candidate,(void *)(uintptr_t)(frame_stack+0x38),12)')
text = text.replace('followup_cases','turn_cases')
text = text.replace('static unsigned surface_reads;', 'static unsigned surface_reads;\nstatic unsigned classified_counts[8], owner_removed_cases;')
text = text.replace('            unsigned outcome = 0;', '            if(!FIELD32(drive,0xC)) ++owner_removed_cases;\n            unsigned outcome = 0;')
text = text.replace('{ (void)stage; (void)actor; (void)cell; (void)object; }',
    '{ if(stage==19 && object<8) ++classified_counts[object]; (void)actor; (void)cell; }')
start = text.rindex('    printf(')
text = text[:start]+'''    for(unsigned i=0;i<8;++i) if(!classified_counts[i]) { fprintf(stderr,"uncovered passage %u\\n",i); return 1; }
    if(!owner_removed_cases) return 1;
    printf("{\\"phase\\":%u,\\"passed\\":true,\\"turn_cases\\":65536,\\"live_stack_locals_verified\\":true,\\"state_calls_abi_cw_verified\\":true,\\"classified_counts\\":[%u,%u,%u,%u,%u,%u,%u,%u],\\"owner_removed_cases\\":%u}\\n",phase,
        classified_counts[0],classified_counts[1],classified_counts[2],classified_counts[3],classified_counts[4],classified_counts[5],classified_counts[6],classified_counts[7],owner_removed_cases);
    return 0;
}
'''
(STAGE/'turn_probe.c').write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'build-followup-probe-v7.ps1'
script = path.read_text(encoding='utf-8')
if 'ground_turn.c' not in script:
    script = script.replace(' /Fe:', ' ..\\..\\ra2\\src\\gameplay\\ground_turn.c /Fe:')
    path.write_text(script,encoding='utf-8',newline='\n')
(ROOT/'build-turn-probe-v7.ps1').write_text(script.replace('followup_probe','turn_probe'),encoding='utf-8',newline='\n')
