from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
assert 'turn_resume_v7' not in text
needle = 'L_004A4015:\n'
assert text.count(needle)>0
print('turn entries:',text.count(needle))
text = text.replace(needle,needle+'''    /* 可读 C：转弯模板第二格、全通行码响应及双方向消耗。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t turn_resume_v7 = ra2_ground_turn_prepare_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!turn_resume_v7) return;
    goto L_004A45D0;
''')
path.write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8').replace('  src/gameplay/ground_followup.c\n',
    '  src/gameplay/ground_followup.c\n  src/gameplay/ground_turn.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_turn.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'ra2/src/runtime/state_trace.c'
text = path.read_text(encoding='utf-8')
assert 'speed_prepare_audit_hook' not in text
text = text.replace('static int movement_audit_enabled;',
    'static int movement_audit_enabled;\nstatic void *speed_prepare_trampoline, *followup_prepare_trampoline, *followup_failure_trampoline, *turn_classified_trampoline;')
text = text.replace('stage >= 11 && stage <= 15','stage >= 11 && stage <= 19')
text = text.replace('        else\n        {\n            value = stage == 11', '''        else if (stage>=16)
        {
            value = stage==16 || stage==19 ? (int32_t)object : stage==17 ? I32(actor+0x4D4) : 0;
            auxiliary = stage==16 || stage==17 ? I32(drive+0x58) : I32(actor+0x4D0);
        }
        else
        {
            value = stage == 11''')
text = text.replace('if (stage == 6)\n', 'if (stage == 6 || stage == 18)\n')
text = text.replace('schema\\\":8', 'schema\\\":9')
hooks = ''
installs = ''
for name,stage,address,signature,operand in [
    ('speed_prepare',16,0x4A3C9B,'8b4d0c8b11','push dword ptr [ebp + 4]'),
    ('followup_prepare',17,0x4A3E35,'8b4424388b4d0c','push 0'),
    ('followup_failure',18,0x4A3F4E,'8b4d0c85c9','push 0'),
    ('turn_classified',19,0x4A413D,'8b4d0c8a417d','push dword ptr [ebp + 4]')]:
    hooks += f'''static __declspec(naked) void {name}_audit_hook(void)
{{
    __asm
    {{
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        {operand}
        push 0
        push dword ptr [ebp + 8]
        push {stage}
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [{name}_trampoline]
    }}
}}

'''
    values = ','.join(hex(byte) for byte in bytes.fromhex(signature))
    installs += f'        static const uint8_t {name}_bytes[] = {{ {values} }};\n'
    installs += f'        install_hook(0x{address:X}, {name}_bytes, sizeof({name}_bytes), {name}_audit_hook, &{name}_trampoline);\n'
text = text.replace('static void install_hook(',hooks+'static void install_hook(')
text = text.replace('        static const uint8_t special_temporary_bytes[]',installs+'        static const uint8_t special_temporary_bytes[]')
assert 'schema\\\":9' in text
path.write_text(text,encoding='utf-8',newline='\n')
