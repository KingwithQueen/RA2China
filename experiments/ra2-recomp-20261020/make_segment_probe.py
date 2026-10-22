"""复用低地址原版对照执行框架，覆盖路径下一格和转向状态。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
text = (ROOT / 'evidence/movement-state-v4/obstacle_probe.c').read_text(encoding='utf-8')
text = text.replace('NOTIFY, OP_COUNT', 'NOTIFY, ALLOW_SEGMENT, OCCUPATION, TURN, OP_COUNT')
text = text.replace('1,0,1,4 };', '1,0,1,4,0,1,2 };')
text = text.replace('static unsigned facing_reads;', 'static unsigned facing_reads;\nstatic uint32_t locomotion_vtable[0x100 / 4];')
text = text.replace('            MEM32(arguments[0]) = (fixture + facing_reads * 0x1234u) & 0xFFFF;',
    '            MEM32(arguments[0]) = fixture_number & 1 ? ((FIELD32(owner, 0x4D0) << 13) & 0xFFFF) : fixture & 0xFFFF;')
text = text.replace('        case GATE:\n', '        case GATE:\n')
text = text.replace('record[2] = MEM32(arguments[1]);\n            return 0;', 'record[2] = MEM32(arguments[1]);\n            return (fixture >> 2) & 1;')
text = text.replace('        default: exit(2);', '''        case ALLOW_SEGMENT: return (fixture >> 1) & 1;
        case OCCUPATION:
            record[1] = arguments[0];
            drive[0x61] = (uint8_t)arguments[0];
            if (fixture & (1u << 20)) owner[0x57B] = (uint8_t)arguments[0];
            return 0;
        case TURN:
            record[1] = arguments[0] == POINTER(drive + 4); record[2] = arguments[1] & 0xFFFFu;
            return 0;
        default: exit(2);''')
text = text.replace('static recomp_func_t lifted[OP_COUNT]', 'LIFTED(l_allow,ALLOW_SEGMENT) LIFTED(l_occupation,OCCUPATION) LIFTED(l_turn,TURN)\nstatic recomp_func_t lifted[OP_COUNT]')
text = text.replace('l_land,l_notify };', 'l_land,l_notify,l_allow,l_occupation,l_turn };')
text = text.replace('    facing_reads = 0;', '''    facing_reads = 0;
    FIELD32(drive, 4) = POINTER(locomotion_vtable);
    owner[0x79] = (fixture >> 12) & 3;
    owner[0x57B] = (uint8_t)((fixture >> 14) & 1);''')
text = text.replace('type_data[0xAA0] = (uint8_t)((fixture >> 5) & 1);', '''type_data[0xAA0] = (uint8_t)((fixture >> 5) & 1);
    type_data[0xAF3] = (uint8_t)((fixture >> 6) & 1);
    const uint32_t overlays[] = { 0,1,26,UINT32_MAX };
    FIELD32(cell_data, 0x44) = overlays[(fixture >> 9) & 3];''')
text = text.replace('owner_vtable[0x194 / 4] = stub_base + PASSAGE * 16;', '''owner_vtable[0x194 / 4] = stub_base + PASSAGE * 16;
    owner_vtable[0x27C / 4] = stub_base + ALLOW_SEGMENT * 16;
    owner_vtable[0x11C / 4] = stub_base + OCCUPATION * 16;
    locomotion_vtable[0x4C / 4] = stub_base + TURN * 16;''')
text = text.replace('uint32_t boundaries[] = { 0x4A2DFD,0x4A32CA };', 'uint32_t boundaries[] = { 0x4A3550 };')
text = text.replace('b < 2', 'b < 1').replace('phase < 2', 'phase < 1')
text = text.replace('entry_address = phase == 0 ? 0x4A2A83 : 0x4A2F7A;', 'entry_address = 0x4A32CA;')
text = text.replace('uint32_t resume = ra2_ground_observe_obstacle_bridge((int)phase);', 'uint32_t resume = ra2_ground_prepare_segment_bridge();')
text = text.replace('            initialize(number);\n            g_esp', '''            uint32_t expected_locals[7] = { MEM32(frame_stack + 0x14),MEM32(frame_stack + 0x18),MEM32(frame_stack + 0x2C),
                MEM32(frame_stack + 0x38),MEM32(frame_stack + 0x3C),MEM32(frame_stack + 0x40),MEM8(frame_stack + 0x13) };
            initialize(number);
            g_esp''')
# 原版续接桩回收了 callee-saved 寄存器；补充保存待续接的分类格和高度。
text = text.replace('static uint32_t locomotion_vtable[0x100 / 4];', 'static uint32_t locomotion_vtable[0x100 / 4], native_cell, native_level;')
text = text.replace('        mov native_head, ebx', '        mov native_head, ebx\n        mov native_cell, esi\n        mov native_level, edi')
text = text.replace('(resume == 0x4A32CA && g_ebx != native_head)', '(resume == 0x4A3550 && (g_ebx != native_head || g_esi != native_cell || g_edi != native_level))')
text = text.replace('            if (state_diff || abi_diff', '''            uint32_t actual_locals[7] = { MEM32(frame_stack + 0x14),MEM32(frame_stack + 0x18),MEM32(frame_stack + 0x2C),
                MEM32(frame_stack + 0x38),MEM32(frame_stack + 0x3C),MEM32(frame_stack + 0x40),MEM8(frame_stack + 0x13) };
            int locals_diff = resume && memcmp(expected_locals, actual_locals, sizeof(expected_locals));
            if (locals_diff || state_diff || abi_diff''')
text = text.replace('i < 2; ++i) if (resume == boundaries[i])', 'i < 1; ++i) if (resume == boundaries[i])')
text = text.replace('failed_rebuild_cases\\":65536,\\"rebuilt_cases\\":65536', 'segment_cases\\":65536,\\"live_stack_locals_verified\\":true')
(ROOT / 'evidence/movement-state-v4/segment_probe.c').write_text(text, encoding='utf-8', newline='\n')
script = (ROOT / 'build-obstacle-probe.ps1').read_text(encoding='utf-8')
script = script.replace('obstacle_probe', 'segment_probe').replace('..\u005c..\u005cra2\u005csrc\u005cgameplay\u005cground_obstacle.c ', '..\u005c..\u005cra2\u005csrc\u005cgameplay\u005cground_obstacle.c ..\u005c..\u005cra2\u005csrc\u005cgameplay\u005cground_segment.c ')
(ROOT / 'build-segment-probe.ps1').write_text(script, encoding='utf-8', newline='\n')
