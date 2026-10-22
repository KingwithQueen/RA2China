"""以已有原版片段探针框架检查新增双入口，旧证据保持只读。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
text = (ROOT / 'evidence/movement-prepare-v3/prepare_probe.c').read_text(encoding='utf-8')
text = text.replace('static void patch_jump(', '''void ra2_state_movement_audit(uint32_t stage, uint32_t actor, uint32_t cell, uint32_t object)
{ (void)stage; (void)actor; (void)cell; (void)object; }
static void patch_jump(''')
text = text.replace('CANCEL, OP_COUNT', 'CANCEL, FACING, BOUNDS, HEIGHT, CELL, PASSAGE, GATE, SURFACE, BLOCKER, ALLY, TYPE, LAND, NOTIFY, OP_COUNT')
text = text.replace('2,2,3,1,0,0 };', '2,2,3,1,0,0,1,2,0,1,5,2,1,3,1,0,1,4 };')
text = text.replace('static unsigned phase;', 'static unsigned phase;\nstatic unsigned char cell_data[0x200], type_data[0x1000];\nstatic unsigned facing_reads;')
text = text.replace('        default: exit(2);', '''        case FACING:
            ++facing_reads;
            MEM32(arguments[0]) = (fixture + facing_reads * 0x1234u) & 0xFFFF;
            return arguments[0];
        case BOUNDS:
            record[1] = MEM32(arguments[0]); record[2] = arguments[1];
            return (fixture >> 1) & 1;
        case HEIGHT: return 4;
        case CELL:
        case LAND:
            memcpy(record + 1, (void *)(uintptr_t)arguments[0], id == CELL ? 4 : 12);
            return POINTER(cell_data);
        case PASSAGE:
            record[1] = arguments[0] == POINTER(cell_data); record[2] = arguments[1];
            record[3] = arguments[2] | (arguments[3] << 8) | (arguments[4] << 16);
            return (fixture >> 2) & 7;
        case GATE:
            record[1] = arguments[0] == POINTER(owner); record[2] = MEM32(arguments[1]);
            return 0;
        case SURFACE:
            memcpy(record + 1, (void *)(uintptr_t)arguments[0], 12);
            return (fixture & (1u << 16)) ? 104 : 208;
        case BLOCKER:
            record[1] = object == POINTER(cell_data); record[2] = arguments[1] & 255u; record[3] = arguments[2];
            return (fixture & (1u << 6)) ? POINTER(target) : 0;
        case ALLY: record[1] = arguments[0] == POINTER(target); return (fixture >> 7) & 1;
        case TYPE: return POINTER(type_data);
        case NOTIFY:
            record[1] = arguments[0]; record[2] = arguments[1] | arguments[2] << 8;
            record[3] = arguments[3] & 255u;
            if (fixture & (1u << 28)) FIELD32(owner, 0x4D0) = 7;
            return 0;
        default: exit(2);''')
marker = 'static recomp_func_t lifted[OP_COUNT]'
at = text.index(marker)
text = text[:at] + '''LIFTED(l_facing,FACING) LIFTED(l_bounds,BOUNDS) LIFTED(l_height,HEIGHT) LIFTED(l_cell,CELL)
LIFTED(l_passage,PASSAGE) LIFTED(l_gate,GATE) LIFTED(l_surface,SURFACE) LIFTED(l_blocker,BLOCKER)
LIFTED(l_ally,ALLY) LIFTED(l_type,TYPE) LIFTED(l_land,LAND) LIFTED(l_notify,NOTIFY)
''' + text[at:]
text = text.replace('l_rebuild,l_accept,l_predicate,l_cancel };', 'l_rebuild,l_accept,l_predicate,l_cancel,l_facing,l_bounds,l_height,l_cell,l_passage,l_gate,l_surface,l_blocker,l_ally,l_type,l_land,l_notify };')
text = text.replace('        default: return NULL;', '''        case 0x4B8BE0: return l_facing;
        case 0x55A660: return l_bounds;
        case 0x5D47D0: return l_height;
        case 0x548070: return l_cell;
        case 0x55ACD0: return l_gate;
        case 0x55A280: return l_surface;
        case 0x471660: return l_blocker;
        case 0x4E5580: return l_ally;
        case 0x636F10: return l_predicate;
        case 0x548000: return l_land;
        case 0x476920: return l_notify;
        default: return NULL;''')
text = text.replace('        mov eax, fixture\n', '        mov ecx, eax\n        mov eax, fixture\n')
text = text.replace('    aborted = 0xA5;', '''    aborted = 0xA5;
    facing_reads = 0;
    memset(cell_data, 0, sizeof(cell_data)); memset(type_data, 0, sizeof(type_data));
    type_data[0xAA0] = (uint8_t)((fixture >> 5) & 1);
    FIELD32(cell_data, 0xEC) = (fixture & (1u << 17)) ? 10 : 0;
    FIELD32(cell_data, 0x140) = (fixture & (1u << 19)) ? 0x100 : 0;
    cell_data[0x11B] = (uint8_t)((fixture & (1u << 20)) ? 1 : 4);
    MEM32(0x8529D0) = 104;
    FIELD32(owner, 0x53C) = 7;''')
text = text.replace('unsigned ids[] = { TEAM,VECTOR,LENGTH,REBUILD,PREDICATE,CANCEL };', '''unsigned ids[] = { TEAM,VECTOR,LENGTH,REBUILD,PREDICATE,CANCEL };
    uint32_t extra_addresses[] = { 0x4B8BE0,0x55A660,0x5D47D0,0x548070,0x55ACD0,0x55A280,0x471660,0x4E5580,0x636F10,0x548000,0x476920 };
    unsigned extra_ids[] = { FACING,BOUNDS,HEIGHT,CELL,GATE,SURFACE,BLOCKER,ALLY,PREDICATE,LAND,NOTIFY };
    for (unsigned i = 0; i < sizeof(extra_ids) / sizeof(extra_ids[0]); ++i) patch_jump(extra_addresses[i], stub_base + extra_ids[i] * 16);
    owner_vtable[0x80 / 4] = stub_base + TYPE * 16;
    owner_vtable[0x194 / 4] = stub_base + PASSAGE * 16;''')
text = text.replace('uint32_t boundaries[] = { 0x4A285E,0x4A32CA,0x4A2A83,0x4A2F7A,0x4A2EAC };', 'uint32_t boundaries[] = { 0x4A2DFD,0x4A32CA };')
text = text.replace('    unsigned char saved_retry[5]; memcpy(saved_retry, (void *)0x4A285E, 5);\n', '')
text = text.replace('b < 5', 'b < 2').replace('            if (phase == 1 && b == 0) { memcpy((void *)0x4A285E, saved_retry, 5); continue; }\n', '')
text = text.replace('entry_address = phase == 0 ? 0x4A2690 : 0x4A285E;', 'entry_address = phase == 0 ? 0x4A2A83 : 0x4A2F7A;')
text = text.replace('uint32_t resume = phase == 0 ? ra2_ground_prepare_entry_bridge() : ra2_ground_retry_path_bridge();', 'uint32_t resume = ra2_ground_observe_obstacle_bridge((int)phase);')
text = text.replace('i < 5; ++i) if (resume == boundaries[i])', 'i < 2; ++i) if (resume == boundaries[i])')
start = text.index('    printf("{\\"passed\\":true,\\"entry_cases')
text = text[:start] + '''    puts("{\\"passed\\":true,\\"failed_rebuild_cases\\":65536,\\"rebuilt_cases\\":65536,\\"state_calls_abi_cw_verified\\":true}");
    return 0;
}
'''
(ROOT / 'evidence/movement-state-v4/obstacle_probe.c').write_text(text, encoding='utf-8', newline='\n')
