from pathlib import Path
ROOT=Path(__file__).resolve().parent
path=ROOT/'ra2/src/runtime/state_trace.c'
text=path.read_text(encoding='utf-8')
assert 'special_temporary_trampoline' not in text
text=text.replace('static int movement_audit_enabled;','static int movement_audit_enabled;\nstatic void *special_temporary_trampoline, *special_cloaked_trampoline, *template_select_trampoline, *template_commit_trampoline, *prepare_identity_trampoline;')
text=text.replace('    else if (stage == 7)', '''    else if (stage >= 11 && stage <= 15)
    {
        uint32_t drive = actor;
        actor = U32(drive + 0x0C);
        if (stage == 15)
        {
            uint32_t active = U32(actor + 0x564);
            if (active == drive + 4) return;
            value = active ? (int32_t)U32(active) : 0;
            auxiliary = I32(drive + 0x58);
        }
        else
        {
            value = stage == 11 ? 6 : stage == 12 ? 1 : stage == 13 ? (int32_t)object : I32(drive + 0x58);
            auxiliary = stage == 13 ? U8(drive + 0x64) : stage == 14 ? I32(drive + 0x5C) : I32(actor + 0x4D0);
        }
    }
    else if (stage == 7)''')
text=text.replace('    int32_t x = 0, y = 0, value = 0, auxiliary = 0;', '    uint32_t caller_drive = actor;\n    int32_t x = 0, y = 0, value = 0, auxiliary = 0;')
text=text.replace('        int active_drive = active && U32(active) == 0x7A04CC;', '''        int active_drive = active && U32(active) == 0x7A04CC;
        fprintf(state_file, ",\\"active_is_caller\\":%s,\\"caller_goal_valid\\":%s",
            active == caller_drive + 4 ? "true" : "false",
            U32(caller_drive+0x34)!=U32(0x852998) || U32(caller_drive+0x38)!=U32(0x85299C)
                || U32(caller_drive+0x3C)!=U32(0x8529A0) ? "true" : "false");''')
start=text.index('static __declspec(naked) void traffic_audit_hook')
end=text.index('static void install_hook(',start)
template=text[start:end]
hooks=''
for name,stage in [('special_temporary',11),('special_cloaked',12),('template_select',13),('template_commit',14),('prepare_identity',15)]:
    hook=template.replace('traffic_',name+'_').replace('push 8\n',f'push {stage}\n')
    if stage==13:
        hook=hook.replace('        push 0\n        push 0', '''        mov eax, dword ptr [ebp + 4]
        mov edx, dword ptr [ebp + 16]
        lea eax, [eax + edx*8]
        push eax
        push 0''')
    if stage==15:
        hook=hook.replace('push dword ptr [ebp + 8]','push dword ptr [ebp + 24]')
    hooks+=hook
text=text[:end]+hooks+text[end:]
idx=text.index('        static const uint8_t terrain_bytes[]')
block=''
for name,address,data in [
    ('special_temporary',0x4A36F6,[0x8B,0x4D,0x0C,0x8B,1]),
    ('special_cloaked',0x4A3944,[0x8D,0x4C,0x24,0x14,0x51]),
    ('template_select',0x4A3FE3,[0x8D,4,0xDE,0xC6,0x45,0x60,0]),
    ('template_commit',0x4A469E,[0x8B,0x55,0x0C,0x52,0x50]),
    ('prepare_identity',0x4A2670,[0x83,0xEC,0x4C,0x53,0x55])]:
    block+=f'        static const uint8_t {name}_bytes[] = {{ '+','.join(hex(x) for x in data)+' };\n'
    block+=f'        install_hook(0x{address:X}, {name}_bytes, sizeof({name}_bytes), {name}_audit_hook, &{name}_trampoline);\n'
text=text[:idx]+block+text[idx:]
path.write_text(text,encoding='utf-8',newline='\n')
path=ROOT/'ra2/src/runtime/ground_prepare_bridge.c'
text=path.read_text(encoding='utf-8')
text=text.replace('uint32_t ra2_ground_prepare_entry_bridge(void)\n{','uint32_t ra2_ground_prepare_entry_bridge(void)\n{\n    ra2_state_movement_audit(15,g_ebp,0,0);')
text=text.replace('    read_state(&context);\n    g_esp -= 0x200;\n    Ra2SpecialServices',
    '    read_state(&context);\n    if (passage==6 || passage==1) ra2_state_movement_audit(passage==6 ? 11 : 12,context.drive,0,0);\n    g_esp -= 0x200;\n    Ra2SpecialServices')
text=text.replace('    MEM8(context.drive+0x60) = 0;',
    '    ra2_state_movement_audit(13,context.drive,0,(uint32_t)result.next_direction+(uint32_t)direction*8u);\n    MEM8(context.drive+0x60) = 0;')
needle='static int commit_accepts(void *opaque, Ra2WorldPoint position)'
start=text.index(needle)
idx=text.index('    write_commit(context);',start)+len('    write_commit(context);')
text=text[:idx]+'\n    ra2_state_movement_audit(14,context->prepare.drive,0,0);'+text[idx:]
path.write_text(text,encoding='utf-8',newline='\n')
