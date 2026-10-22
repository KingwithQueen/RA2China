from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/runtime/state_trace.c'
t=p.read_text(encoding='utf-8')
assert 'advance_sample_trampoline' not in t
t=t.replace('static void *speed_prepare_trampoline,','static void *advance_sample_trampoline;\nstatic void *speed_prepare_trampoline,')
t=t.replace('\\"schema\\":9','\\"schema\\":10')
t=t.replace('    uint32_t caller_drive = actor;','    uint32_t caller_drive = actor, observation_frame = stage==19 ? cell : 0;\n    if (stage==19) cell=0;')
t=t.replace('stage <= 19','stage <= 20')
t=t.replace('value = stage==16 || stage==19 ?', 'value = stage==16 || stage==19 || stage==20 ?')
t=t.replace('auxiliary = stage==16 || stage==17 ?', 'auxiliary = stage==16 || stage==17 || stage==20 ?')
needle='    if (cell)\n    {\n        x = (int16_t)U16(cell + 0x24);'
assert needle in t
t=t.replace(needle,'''    if (observation_frame)
    {
        x=(int16_t)U16(observation_frame+0x14);
        y=(int16_t)U16(observation_frame+0x16);
    }
'''+needle)
needle='    if (stage == 6 || stage == 18)\n'
t=t.replace(needle,'''    if (observation_frame)
    {
        fprintf(state_file, ",\\\"candidate\\\":[%d,%d,%d],\\\"next_direction\\\":%d,\\\"allow_recursive\\\":%u",
            I32(observation_frame+0x38),I32(observation_frame+0x3C),I32(observation_frame+0x40),
            I32(observation_frame+0x24),U32(observation_frame+0x64));
    }
'''+needle)
start=t.index('static __declspec(naked) void turn_classified_audit_hook')
end=t.index('static void install_hook',start)
block=t[start:end]
assert '        push 0\n' in block
block=block.replace('        push 0\n','        mov eax, dword ptr [ebp + 12]\n        add eax, 4\n        push eax\n',1)
newhook='''static __declspec(naked) void advance_sample_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov eax, dword ptr [ebp + 8]
        push dword ptr [eax + 5Ch]
        push 0
        push eax
        push 20
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [advance_sample_trampoline]
    }
}

'''
t=t[:start]+newhook+block+t[end:]
needle='        static const uint8_t speed_prepare_bytes[]'
t=t.replace(needle,'''        static const uint8_t advance_sample_bytes[] = { 0x8b,0x4d,0xc,0x8b,0x11 };
        install_hook(0x4A16A6, advance_sample_bytes, sizeof(advance_sample_bytes), advance_sample_audit_hook, &advance_sample_trampoline);
'''+needle)
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_followup_bridge.c'; t=p.read_text(encoding='utf-8')
t=t.replace('ra2_state_movement_audit(19, context->base.drive, 0,','ra2_state_movement_audit(19, context->base.drive, context->base.frame,')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_advance_bridge.c'; t=p.read_text(encoding='utf-8').replace('#include "ground_advance_bridge.h"','#include "ground_advance_bridge.h"\n#include "state_trace.h"')
t=t.replace('    AdvanceContext context={g_ebp,g_esp,0,0,0};','    AdvanceContext context={g_ebp,g_esp,0,0,0};\n    ra2_state_movement_audit(20,context.drive,0,MEM32(context.drive+0x5C));')
p.write_text(t,encoding='utf-8',newline='\n')
