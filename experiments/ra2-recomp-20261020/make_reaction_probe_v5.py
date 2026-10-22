from pathlib import Path
ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v5'
text = (STAGE / 'wait_probe.c').read_text(encoding='utf-8')
text = text.replace('TURN, OP_COUNT', 'TURN, SOUND, FIND_OBJECT, ATTACK_OBJECT, RECURSE, OP_COUNT')
text = text.replace('1,4,0,1,2 };', '1,4,0,1,2,2,2,3,3 };')
text = text.replace('        default: exit(2);', '''        case SOUND:
            record[1] = object; record[2] = arguments[0]; record[3] = arguments[1];
            return 0;
        case FIND_OBJECT:
            record[1] = MEM32(arguments[0]); record[2] = MEM32(arguments[0] + 4); record[3] = arguments[1] & 255u;
            return (fixture & (1u << 6)) ? POINTER(target) : 0;
        case ATTACK_OBJECT:
            record[1] = arguments[0]; record[2] = arguments[1] == POINTER(cell_data) ? 1 : arguments[1] == POINTER(target) ? 2 : 3;
            record[3] = arguments[2]; owner[0x57A] = 1;
            return 0;
        case RECURSE:
            record[1] = arguments[0] == POINTER(&aborted); record[2] = arguments[1]; record[3] = arguments[2];
            FIELD32(drive, 0x58) = 7; drive[0x61] = 0;
            return (fixture >> 10) & 1;
        default: exit(2);''')
text = text.replace('static recomp_func_t lifted[OP_COUNT]', '''LIFTED(l_sound,SOUND) LIFTED(l_find,FIND_OBJECT) LIFTED(l_attack,ATTACK_OBJECT) LIFTED(l_recurse,RECURSE)
static recomp_func_t lifted[OP_COUNT]''')
text = text.replace('l_allow,l_occupation,l_turn };', 'l_allow,l_occupation,l_turn,l_sound,l_find,l_attack,l_recurse };')
text = text.replace('        case 0x68A680:', '''        case 0x713DB0: return l_sound;
        case 0x471830: return l_find;
        case 0x4A2670: return l_recurse;
        case 0x68A680:''')
start = text.index('        lea esi, cell_data')
end = text.index('        jmp entry_address', start)
text = text[:start] + '''        mov esi, 0FFFFFFFFh
        mov edi, fixture
        and edi, 1
        lea ebx, drive + 40h
        mov eax, dword ptr [esp + 18h]
''' + text[end:]
text = text.replace('if (phase > 2)', 'if (phase > 3)')
text = text.replace('    owner_vtable[0x80 / 4]', '''    patch_jump(0x713DB0, stub_base + SOUND * 16);
    patch_jump(0x471830, stub_base + FIND_OBJECT * 16);
    patch_jump(0x4A2670, stub_base + RECURSE * 16);
    owner_vtable[0x1DC / 4] = stub_base + ATTACK_OBJECT * 16;
    owner_vtable[0x80 / 4]''', 1)
start = text.index('    unsigned boundary_count;')
end = text.index('    unsigned outcome_counts', start)
text = text[:start] + '    unsigned boundary_count = 0;\n' + text[end:]
text = text.replace('unsigned outcome_counts[3][6]', 'unsigned outcome_counts[4][6]')
text = text.replace('uint32_t boundaries[4];', 'uint32_t boundaries[4] = { 0 };')
text = text.replace('entry_address = phase == 0 ? 0x4A3550 : phase == 1 ? 0x4A35FE : 0x4A364F;',
    'const uint32_t entries[] = { 0x4A3A8E,0x4A3A98,0x4A3ACF,0x4A3BFD };\n            entry_address = entries[phase];')
text = text.replace('            g_esi = POINTER(cell_data); g_edi = 4;\n            if (phase == 2) { g_ebx = POINTER(drive + 0x40); g_edi = 0; }\n            uint32_t resume = phase == 2 ? ra2_ground_traffic_wait_bridge() : ra2_ground_clearance_bridge(phase == 1);',
    '''            g_esi = UINT32_MAX; g_edi = fixture & 1; g_ebx = POINTER(drive + 0x40); g_eax = MEM32(frame_stack + 0x18);
            ra2_ground_reaction_bridge(phase);
            uint32_t resume = 0;''')
text = text.replace('    overlay_data[0x1FD]', '    overlay_data[0x278] = (uint8_t)((fixture >> 8) & 1);\n    overlay_data[0x1FD]', 1)
text = text.replace('    FIELD32(owner, 0x53C) = 7;', '''    FIELD32(owner, 0x53C) = 7;
    owner[0x57A] = (uint8_t)((fixture >> 7) & 1);
    MEM32(frame_stack + 0x64) = (fixture >> 9) & 1;
    FIELD32(rules, 0x620) = 123;
    FIELD32(drive, 0x58) = 5;''')
text = text.replace('            int locals_diff = MEM8(frame_stack + 0x13) != expected_crush\n                || (resume == 0x4A3C9B && MEM32(frame_stack + 0x28) != expected_level);',
    '            int locals_diff = MEM8(frame_stack + 0x13) != expected_crush || MEM32(frame_stack + 0x28) != expected_level;')
text = text.replace('fragment_cases', 'reaction_cases')
(STAGE / 'reaction_probe.c').write_text(text,encoding='utf-8',newline='\n')
script = (ROOT / 'build-wait-probe-v5.ps1').read_text(encoding='utf-8').replace('wait_probe', 'reaction_probe')
script = script.replace('..\\..\\ra2\\src\\gameplay\\ground_wait.c ', '..\\..\\ra2\\src\\gameplay\\ground_wait.c ..\\..\\ra2\\src\\gameplay\\ground_reaction.c ')
(ROOT/'build-reaction-probe-v5.ps1').write_text(script,encoding='utf-8',newline='\n')
