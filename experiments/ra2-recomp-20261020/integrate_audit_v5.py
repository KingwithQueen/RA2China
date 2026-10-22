from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/runtime/state_trace.c'
text = path.read_text(encoding='utf-8')
assert 'traffic_audit_hook' not in text
text = text.replace('static int movement_audit_enabled;', 'static int movement_audit_enabled;\nstatic void *terrain_trampoline, *clearance_trampoline, *traffic_trampoline;')
start = text.index('static __declspec(naked) void wall_audit_hook')
end = text.index('static __declspec(naked) void gate_audit_hook')
template = text[start:end]
hooks = ''
for name, stage, cell, obj in [('terrain',7,'dword ptr [ebp + 16]','0'),
        ('clearance',9,'dword ptr [ebp + 4]','eax'), ('traffic',8,'0','0')]:
    hook = template.replace('wall_', name + '_').replace('push 1\n', f'push {stage}\n')
    hook = hook.replace('        push 0\n        push dword ptr [ebp + 16]', f'        push {obj}\n        push {cell}')
    if name == 'clearance':
        hook = hook.replace('        push eax', '        mov eax, dword ptr [ebp + 12]\n        mov eax, dword ptr [eax + 1Ch]\n        push eax')
    hooks += hook
idx = text.index('static void install_hook(')
text = text[:idx] + hooks + text[idx:]
needle = '        static const uint8_t wall_bytes[]'
idx = text.index(needle)
text = text[:idx] + '''        static const uint8_t terrain_bytes[] = { 0x8B,0x81,0x94,0x0B,0,0 };
        static const uint8_t clearance_bytes[] = { 0x8B,0x46,0x44,0x8B,0x4C,0x24,0x18 };
        static const uint8_t traffic_bytes[] = { 0x8B,0x45,0x0C,0x8A,0x88,0xA1,0x05,0,0 };
        install_hook(0x7030B6, terrain_bytes, sizeof(terrain_bytes), terrain_audit_hook, &terrain_trampoline);
        install_hook(0x4A3550, clearance_bytes, sizeof(clearance_bytes), clearance_audit_hook, &clearance_trampoline);
        install_hook(0x4A364F, traffic_bytes, sizeof(traffic_bytes), traffic_audit_hook, &traffic_trampoline);
''' + text[idx:]
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/src/runtime/ground_prepare_bridge.c'
text = path.read_text(encoding='utf-8')
text = text.replace('    context.obstacle_cell = g_esi;\n', '    context.obstacle_cell = g_esi;\n    if (!clear_only) ra2_state_movement_audit(9, context.drive, context.obstacle_cell, MEM32(context.frame + 0x18));\n')
needle = 'uint32_t ra2_ground_traffic_wait_bridge(void)\n{\n'
text = text.replace(needle, needle + '    ra2_state_movement_audit(8, g_ebp, 0, 0);\n')
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/src/runtime/ground_collision_bridge.c'
text = path.read_text(encoding='utf-8').replace('#include "ground_terrain.h"', '#include "ground_terrain.h"\n#include "state_trace.h"')
needle = 'int ra2_ground_terrain_bridge(void)\n{\n'
text = text.replace(needle, needle + '    ra2_state_movement_audit(7, g_ebp, g_ebx, 0);\n')
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'run_state_comparison.py'
text = path.read_text(encoding='utf-8')
text = text.replace("ap.add_argument('--tag', required=True)", "ap.add_argument('--tag', required=True)\n    ap.add_argument('--movement-audit', action='store_true')")
text = text.replace('        if args.cell_catalog:', "        if args.movement_audit:\n            cmd += ['--state-movement-audit']\n        if args.cell_catalog:", 1)
text = text.replace("('submit', 'execute')", "('submit', 'execute', 'movement-audit')")
path.write_text(text, encoding='utf-8', newline='\n')
