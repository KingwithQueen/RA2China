from pathlib import Path
ROOT=Path(__file__).resolve().parent
STAGE=ROOT/'evidence/movement-state-v6'
text=(ROOT/'evidence/movement-state-v5/reaction_probe.c').read_text(encoding='utf-8')
text=text.replace('RECURSE, OP_COUNT','RECURSE, NEIGHBOR, ACCEPT_CELL, START_SEGMENT, ZERO_SPEED, OP_COUNT')
text=text.replace('2,2,3,3 };','2,2,3,3,1,1,2,2 };')
text=text.replace('        default: exit(2);','''        case NEIGHBOR:
            record[1]=arguments[0];
            return fixture & 8 ? POINTER(cell_data) : 0;
        case ACCEPT_CELL:
            record[1]=arguments[0]==POINTER(owner);
            if (fixture & 16) owner[0x7D]=0;
            if (fixture & 32) owner[0x76]=1;
            return fixture & 64 ? 1 : 0;
        case START_SEGMENT:
            memcpy(record+1,(void *)(uintptr_t)arguments[0],12);
            drive[0x61]=1; FIELD32(owner,0x4D0)=3;
            return 1;
        case ZERO_SPEED:
            record[1]=arguments[0]; record[2]=arguments[1];
            FIELD32(owner,0x468)=FIELD32(owner,0x46C)=0;
            return 0;
        default: exit(2);''')
text=text.replace('static recomp_func_t lifted[OP_COUNT]','LIFTED(l_neighbor,NEIGHBOR) LIFTED(l_cell_accept,ACCEPT_CELL) LIFTED(l_start,START_SEGMENT) LIFTED(l_zero,ZERO_SPEED)\nstatic recomp_func_t lifted[OP_COUNT]')
text=text.replace('l_sound,l_find,l_attack,l_recurse };','l_sound,l_find,l_attack,l_recurse,l_neighbor,l_cell_accept,l_start,l_zero };')
text=text.replace('        case 0x713DB0:','''        case 0x476AC0: return l_neighbor;
        case 0x476CC0: return l_cell_accept;
        case 0x4A0BC0: return l_start;
        case 0x713DB0:''')
text=text.replace('    patch_jump(0x713DB0,','''    patch_jump(0x476AC0,stub_base+NEIGHBOR*16);
    patch_jump(0x476CC0,stub_base+ACCEPT_CELL*16);
    patch_jump(0x4A0BC0,stub_base+START_SEGMENT*16);
    owner_vtable[0x4C8/4]=stub_base+ZERO_SPEED*16;
    patch_jump(0x713DB0,''')
text=text.replace('    unsigned boundary_count = 0;', '    boundaries[0]=0x4A4015; boundaries[1]=0x4A45B7;\n    unsigned boundary_count=(phase==0 || phase>=3) ? 2 : 0;')
text=text.replace('if (phase > 3)','if (phase > 4)')
text=text.replace('const uint32_t entries[] = { 0x4A3A8E,0x4A3A98,0x4A3ACF,0x4A3BFD };','const uint32_t entries[] = { 0x4A3F8B,0x4A45B7,0x4A45D0,0x4A3F9F,0x4A3FA1 };')
start=text.index('        mov esi, 0FFFFFFFFh')
end=text.index('        jmp entry_address',start)
text=text[:start]+'''        mov eax, fixture_number
        and eax, 7
        mov ebx, eax
        mov esi, dword ptr [esp + 24h]
'''+text[end:]
text=text.replace('    FIELD32(drive, 0x58) = 5;','''    FIELD32(drive,0x58)=5;
    for (unsigned i=0;i<24;++i) FIELD32(owner,0x4D0+i*4)=i ^ fixture;
    MEM32(frame_stack+0x2C)=POINTER(cell_data);
    const int32_t second[]={-1,0,1,2,3,4,5,6,7,8};
    MEM32(frame_stack+0x24)=(uint32_t)second[(number/8)%10];
    MEM32(frame_stack+0x68)=(fixture>>9)&1;
    const int32_t candidates[4][3]={{0,0,0},{128,-257,416},{INT32_MIN,INT32_MAX,0},{17280,29312,416}};
    memcpy((void *)(uintptr_t)(frame_stack+0x38),candidates[(fixture>>10)&3],12);
    owner[0x76]=(uint8_t)((fixture>>12)&1);''')
start=text.index('            g_esi = UINT32_MAX;')
end=text.index('            uint32_t flags = recomp_eflags',start)
text=text[:start]+'''            g_ebx=number&7; g_esi=MEM32(frame_stack+0x24);
            uint32_t resume=0;
            if (phase==0 || phase>=3) resume=ra2_ground_template_select_bridge(phase==0 ? 0 : phase==3 ? 1 : 2);
            else ra2_ground_template_commit_bridge(phase==2);
'''+text[end:]
text=text.replace('|| (phase != 2 && (g_ebx != native_head || g_esi != native_cell || (resume != 0x4A3C9B && g_edi != native_level)))','|| g_ebx != native_head || g_esi != native_cell')
text=text.replace('            int locals_diff = MEM8(frame_stack + 0x13) != expected_crush || MEM32(frame_stack + 0x28) != expected_level;',
    '            int locals_diff=MEM8(frame_stack+0x13)!=expected_crush || MEM32(frame_stack+0x28)!=expected_level;')
text=text.replace('reaction_cases','template_cases')
text=text.replace('unsigned outcome_counts[4][6]','unsigned outcome_counts[5][6]')
(STAGE/'template_probe.c').write_text(text,encoding='utf-8',newline='\n')
script=(ROOT/'build-special-probe-v6.ps1').read_text(encoding='utf-8').replace('special_probe','template_probe')
if 'ground_template.c' not in script:
    script=script.replace(' /Fe:',' ..\\..\\ra2\\src\\gameplay\\ground_template.c /Fe:')
(ROOT/'build-template-probe-v6.ps1').write_text(script,encoding='utf-8',newline='\n')
