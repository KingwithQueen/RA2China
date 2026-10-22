from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8')
assert '\\"schema\\":11' in t
t=t.replace('\\"schema\\":11','\\"schema\\":12')
t=t.replace('    else if (stage == 24)\n','    else if (stage == 24 || stage == 25 || stage == 26)\n')
needle='    else if (stage == 7)\n';assert needle in t
t=t.replace(needle,'''    else if (stage == 27)
    {
        auxiliary=U8(object+0x11);
        value=auxiliary ? 0 : I32(0x850EA0+(U32(cell+0xEC)*9u+U32(U32(actor+0x5AC)+0x5A4))*4u);
    }
'''+needle)
hook=t[t.index('static __declspec(naked) void object_filter_audit_hook'):t.index('static __declspec(naked) void advance_sample_audit_hook')]
new=''
for name,stage in [('allied_entry',25),('allied_geometry',26),('terrain_tail',27)]:
    h=hook.replace('object_filter',name).replace('push 24',f'push {stage}')
    if stage==26:
        h=h.replace('push dword ptr [ebp + 16]','push dword ptr [ebp + 160]').replace('push dword ptr [ebp + 8]','push dword ptr [ebp + 56]')
    if stage==27:
        h=h.replace('push dword ptr [ebp + 4]','lea eax,[ebp + 36]\n        push eax')
    new+=f'static uint32_t {name}_trampoline;\n'+h
t=t.replace('static __declspec(naked) void advance_sample_audit_hook',new+'static __declspec(naked) void advance_sample_audit_hook',1)
needle='        static const uint8_t object_filter_bytes[]';pos=t.index(needle)
new='''        static const unsigned char allied_entry_bytes[]={0x8B,0x55,0x00,0x8B,0xCD};
        install_hook(0x703693,allied_entry_bytes,sizeof(allied_entry_bytes),allied_entry_audit_hook,&allied_entry_trampoline);
        static const unsigned char allied_geometry_bytes[]={0x8B,0x5C,0x24,0x14,0x8D,0x54,0x24,0x34};
        install_hook(0x703748,allied_geometry_bytes,sizeof(allied_geometry_bytes),allied_geometry_audit_hook,&allied_geometry_trampoline);
        static const unsigned char terrain_tail_bytes[]={0x8A,0x44,0x24,0x11,0x84,0xC0};
        install_hook(0x703905,terrain_tail_bytes,sizeof(terrain_tail_bytes),terrain_tail_audit_hook,&terrain_tail_trampoline);
'''
t=t[:pos]+new+t[pos:];p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_allied_bridge.c';t=p.read_text(encoding='utf-8').replace('#include "ground_allied.h"','#include "state_trace.h"\n#include "ground_allied.h"')
t=t.replace('    AlliedContext *c=opaque; uint32_t arg=c->frame+0x34;','    AlliedContext *c=opaque; uint32_t arg=c->frame+0x34;\n    ra2_state_movement_audit(26,c->owner,c->cell,c->object);')
t=t.replace('    Ra2AlliedServices services={&c,','    ra2_state_movement_audit(25,c.owner,c.cell,c.object);\n    Ra2AlliedServices services={&c,')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_collision_bridge.c';t=p.read_text(encoding='utf-8')
t=t.replace('    unsigned upper_layer=MEM8(g_esp+0x11);','    ra2_state_movement_audit(27,g_ebp,g_ebx,g_esp);\n    unsigned upper_layer=MEM8(g_esp+0x11);')
p.write_text(t,encoding='utf-8',newline='\n')
