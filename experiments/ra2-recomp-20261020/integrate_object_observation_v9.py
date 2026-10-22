from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8');assert 'object_filter_trampoline' not in t
t=t.replace('static void *advance_sample_trampoline;','static void *advance_sample_trampoline;\nstatic void *object_filter_trampoline;')
t=t.replace('    else if (stage == 7)\n','    else if (stage == 24)\n    {\n        /* Only the two classification bits tested in this scan. */\n        value=(int32_t)U32(object+0x10);auxiliary=U8(object+0x14)&0x05;\n    }\n    else if (stage == 7)\n',1)
start=t.index('static __declspec(naked) void advance_sample_audit_hook')
hook='''static __declspec(naked) void object_filter_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 24
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [object_filter_trampoline]
    }
}

'''
t=t[:start]+hook+t[start:]
t=t.replace('        static const uint8_t advance_sample_bytes[]','        static const uint8_t object_filter_bytes[]={0x8B,0x85,0x88,0x05,0x00,0x00};\n        install_hook(0x703473,object_filter_bytes,sizeof(object_filter_bytes),object_filter_audit_hook,&object_filter_trampoline);\n        static const uint8_t advance_sample_bytes[]')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_objects_bridge.c';t=p.read_text(encoding='utf-8').replace('#include "ground_objects_bridge.h"','#include "ground_objects_bridge.h"\n#include "state_trace.h"')
t=t.replace('    g_esp=c.frame-0x100;','    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit(24,c.owner,c.cell,c.object);\n    g_esp=c.frame-0x100;')
p.write_text(t,encoding='utf-8',newline='\n')
for name in ('objects_probe.c',):
    p=ROOT/'evidence/movement-state-v9'/name;t=p.read_text(encoding='utf-8')
    t+='\nvoid ra2_state_movement_audit(uint32_t a,uint32_t b,uint32_t c,uint32_t d) { (void)a;(void)b;(void)c;(void)d; }\n'
    p.write_text(t,encoding='utf-8',newline='\n')
