"""可选实景覆盖记录：仅观察实际墙体/闸门/失败分支，不改变世界查询。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/runtime/state_trace.c'
text = path.read_text(encoding='utf-8')
assert 'movement_audit_enabled' not in text
text = text.replace('static int original_mode;', 'static int original_mode;\nstatic int movement_audit_enabled;\nstatic void *wall_trampoline, *gate_trampoline, *failure_trampoline;')
text = text.replace('    const char *name = argv[i];', '''    const char *name = argv[i];
    if (!strcmp(name, "--state-movement-audit"))
    {
        movement_audit_enabled = 1;
        return 1;
    }''')
text = text.replace('    if (order_count && !state_path[0])', '    if (movement_audit_enabled && !state_path[0]) fail("movement audit requires --state-log");\n    if (order_count && !state_path[0])')
idx = text.index('void ra2_state_tick(void)')
text = text[:idx] + '''/* 显式启用后才记录；该函数不调用游戏服务、不写游戏内存。 */
void ra2_state_movement_audit(uint32_t stage, uint32_t actor, uint32_t cell, uint32_t object)
{
    if (!movement_audit_enabled || !state_file || !started) return;
    int32_t x = 0, y = 0, value = 0, auxiliary = 0;
    if (stage == 1)
    {
        int32_t overlay = I32(cell + 0x44);
        if (overlay < 0) return;
        uint32_t type = U32(U32(0xA35DEC) + (uint32_t)overlay * 4);
        if (!U8(type + 0x278)) return;
        value = overlay;
        auxiliary = I32(cell + 0x50);
    }
    else if (stage == 2)
    {
        if (!U8(U32(object + 0x418) + 0x1351)) return;
        value = (int32_t)U32(object + 0x10);
        auxiliary = I32(object + 0x98);
    }
    else
    {
        actor = U32(actor + 0x0C);
        value = I32(actor + 0x53C);
        auxiliary = I32(actor + 0x98);
    }
    if (cell)
    {
        x = (int16_t)U16(cell + 0x24);
        y = (int16_t)U16(cell + 0x26);
    }
    fprintf(state_file, "{\\"kind\\":\\"movement-audit\\",\\"frame\\":%u,\\"stage\\":%u,\\"id\\":%u,"
        "\\"cell\\":[%d,%d],\\"value\\":%d,\\"auxiliary\\":%d}\\n", U32(FRAME_ADDRESS), stage, U32(actor + 0x10), x, y, value, auxiliary);
}

''' + text[idx:]
idx = text.index('static void install_hook(')
hooks = ''
for name, stage in [('wall', 1), ('gate', 2), ('failure', 3)]:
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
        push {'dword ptr [ebp + 4]' if stage == 2 else '0'}
        push {'dword ptr [ebp + 16]' if stage != 3 else '0'}
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
text = text[:idx] + hooks + text[idx:]
idx = text.index('    if (detail_id) install_hook(')
text = text[:idx] + '''    if (movement_audit_enabled)
    {
        static const uint8_t wall_bytes[] = { 0x8B, 0x43, 0x44, 0x83, 0xF8, 0xFF };
        static const uint8_t gate_bytes[] = { 0x8B, 0x86, 0x18, 0x04, 0x00, 0x00 };
        static const uint8_t failure_bytes[] = { 0x8B, 0x4D, 0x0C, 0x8B, 0x81, 0x3C, 0x05, 0x00, 0x00 };
        install_hook(0x703331, wall_bytes, sizeof(wall_bytes), wall_audit_hook, &wall_trampoline);
        install_hook(0x703536, gate_bytes, sizeof(gate_bytes), gate_audit_hook, &gate_trampoline);
        install_hook(0x4A2DFD, failure_bytes, sizeof(failure_bytes), failure_audit_hook, &failure_trampoline);
    }
''' + text[idx:]
path.write_text(text, encoding='utf-8', newline='\n')
for filename in ['recomp_0010.c', 'recomp_0046.c']:
    path = ROOT / 'ra2/src/recomp/gen_game' / filename
    text = path.read_text(encoding='utf-8')
    if '#include "state_trace.h"' not in text:
        text = '#include "state_trace.h"\n' + text
    for marker, statement in [('    ra2_ground_recover_path_bridge(0);', 'ra2_state_movement_audit(3, g_ebp, 0, 0);'),
        ('    uint32_t overlay_resume =', ''), ('    uint32_t gate_resume =', '')]:
        if marker in text and statement:
            text = text.replace(marker, '    ' + statement + '\n' + marker)
    # C 翻译器的原有局部变量名在上一轮生成脚本中固定。
    for bridge, stage in [('ra2_ground_overlay_bridge()', 1), ('ra2_ground_gate_bridge()', 2)]:
        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if bridge in line:
                lines[i] = f'    ra2_state_movement_audit({stage}, g_ebp, g_ebx, {"g_esi" if stage == 2 else "0"});\n' + line
        text = ''.join(lines)
    path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'run_fixture_comparison.py'
text = path.read_text(encoding='utf-8')
text = text.replace("ap.add_argument('--tag', required=True)", "ap.add_argument('--tag', required=True)\n    ap.add_argument('--movement-audit', action='store_true')")
text = text.replace("        if args.cell_catalog:", "        if args.movement_audit:\n            cmd += ['--state-movement-audit']\n        if args.cell_catalog:", 1)
text = text.replace("('submit', 'execute')", "('submit', 'execute', 'movement-audit')")
path.write_text(text, encoding='utf-8', newline='\n')
print('Integrated optional real-world audit')
