from pathlib import Path
ROOT = Path(__file__).resolve().parent
NEW = ROOT / 'evidence/movement-state-v5'
source = (ROOT / 'evidence/movement-state-v4/segment_probe.c').read_text(encoding='utf-8')
source = source.replace('native_cell, native_level;', 'native_cell, native_level;\nstatic unsigned char overlay_data[0x300];\nstatic uint32_t overlays_table[27];')
source = source.replace('        mov ecx, eax\n        mov eax, fixture', '''        mov ecx, eax
        lea esi, cell_data
        mov edi, 4
        cmp phase, 2
        jne start_fragment
        lea ebx, drive + 40h
        xor edi, edi
    start_fragment:
        mov eax, fixture''')
source = source.replace('    MEM32(0x8529D0) = 104;', '''    MEM32(0x8529D0) = 104;
    MEM32(0xA35DEC) = POINTER(overlays_table);
    for (unsigned i = 0; i < 27; ++i) overlays_table[i] = POINTER(overlay_data);
    overlay_data[0x1FD] = (uint8_t)((fixture >> 8) & 1);
    owner[0x5A1] = (uint8_t)((fixture >> 1) & 1);
    FIELD32(owner, 0x558) = starts[(number / 7) % 6];
    FIELD32(owner, 0x560) = times[(number / 11) % 7];
    FIELD32(rules, 0x13D0) = times[(number / 13) % 7];
    MEM32(frame_stack + 0x14) = 0xFFF00010;
    MEM32(frame_stack + 0x18) = (fixture >> 2) & 7;
    MEM32(frame_stack + 0x28) = 0xA5A5A5A5;
    MEM8(frame_stack + 0x13) = (uint8_t)((fixture >> 7) & 1);''')
source = source.replace('if (argc != 2) return 2;', 'if (argc != 3) return 2;\n    phase = (unsigned)atoi(argv[2]);\n    if (phase > 2) return 2;')
source = source.replace('uint32_t boundaries[] = { 0x4A3550 };', '''uint32_t boundaries[4];
    unsigned boundary_count;
    if (phase == 0) { boundaries[0] = 0x4A3C9B; boundaries[1] = 0x4A36ED; boundaries[2] = 0x4A364F; boundaries[3] = 0x4A3A8E; boundary_count = 4; }
    else if (phase == 1) { boundaries[0] = 0x4A364F; boundaries[1] = 0x4A3A8E; boundary_count = 2; }
    else { boundaries[0] = 0x4A3A98; boundary_count = 1; }''')
source = source.replace('for (phase = 0; phase < 1; ++phase)', 'for (unsigned once = 0; once < 1; ++once)')
source = source.replace('unsigned b = 0; b < 1;', 'unsigned b = 0; b < boundary_count;')
source = source.replace('entry_address = 0x4A32CA;', 'entry_address = phase == 0 ? 0x4A3550 : phase == 1 ? 0x4A35FE : 0x4A364F;')
start = source.index('            uint32_t expected_locals[7]')
end = source.index('            initialize(number);', start)
source = source[:start] + '''            uint32_t expected_level = MEM32(frame_stack + 0x28);
            unsigned expected_crush = MEM8(frame_stack + 0x13);
''' + source[end:]
source = source.replace('uint32_t resume = ra2_ground_prepare_segment_bridge();', '''g_esi = POINTER(cell_data); g_edi = 4;
            if (phase == 2) { g_ebx = POINTER(drive + 0x40); g_edi = 0; }
            uint32_t resume = phase == 2 ? ra2_ground_traffic_wait_bridge() : ra2_ground_clearance_bridge(phase == 1);''')
source = source.replace('|| (resume == 0x4A3550 && (g_ebx != native_head || g_esi != native_cell || g_edi != native_level))',
    '|| (phase != 2 && (g_ebx != native_head || g_esi != native_cell || (resume != 0x4A3C9B && g_edi != native_level)))')
start = source.index('            uint32_t actual_locals[7]')
end = source.index('            if (locals_diff', start)
source = source[:start] + '''            int locals_diff = MEM8(frame_stack + 0x13) != expected_crush
                || (resume == 0x4A3C9B && MEM32(frame_stack + 0x28) != expected_level);
''' + source[end:]
source = source.replace('i < 1; ++i) if (resume == boundaries[i])', 'i < boundary_count; ++i) if (resume == boundaries[i])')
source = source.replace('unsigned outcome_counts[2][6]', 'unsigned outcome_counts[3][6]')
source = source.replace('    puts("{\\"passed', '    printf("{\\"phase\\":%u,\\"passed')
source = source.replace('state_calls_abi_cw_verified\\":true}");', 'state_calls_abi_cw_verified\\":true}\\n", phase);')
source = source.replace('segment_cases', 'fragment_cases')
(NEW / 'wait_probe.c').write_text(source, encoding='utf-8', newline='\n')
script = (ROOT / 'build-segment-probe.ps1').read_text(encoding='utf-8').replace('movement-state-v4', 'movement-state-v5')
script = script.replace('segment_probe', 'wait_probe')
script = script.replace('..\\..\\ra2\\src\\gameplay\\ground_segment.c ..\\..\\ra2\\src\\gameplay\\ground_segment.c',
    '..\\..\\ra2\\src\\gameplay\\ground_segment.c ..\\..\\ra2\\src\\gameplay\\ground_wait.c')
(ROOT / 'build-wait-probe-v5.ps1').write_text(script, encoding='utf-8', newline='\n')
import shutil
shutil.copy2(ROOT / 'evidence/movement-state-v4/native_probe_host.h', NEW / 'native_probe_host.h')
