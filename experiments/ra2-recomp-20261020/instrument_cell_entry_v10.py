from pathlib import Path
ROOT=Path(__file__).resolve().parent; S=ROOT/'evidence/movement-state-v10'
p=ROOT/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8')
(S/'diagnostic-current/state_trace.c').write_text(t,encoding='utf-8')
text='''
void ra2_state_cell_entry_diag(uint32_t actor,uint32_t cell,uint32_t caller)
{
    if (!movement_audit_enabled || !state_file || !started || U32(FRAME_ADDRESS)!=52
        || (int16_t)U16(cell+0x24)!=69 || (int16_t)U16(cell+0x26)!=113) return;
    fprintf(state_file,"{\\"kind\\":\\"cell-entry-detail\\",\\"frame\\":52,\\"id\\":%u,\\"caller\\":%u,\\"cw\\":%u}\\n",U32(actor+0x10),caller,original_mode ? original_cw : g_fpu_cw);
}
static uint32_t cell_entry_diag_trampoline;
'''
start=t.index('static __declspec(naked) void object_filter_audit_hook')
template=t[start:t.index('\n}\n',start)+3]
template=template.replace('object_filter_audit_hook','cell_entry_diag_hook').replace('object_filter_trampoline','cell_entry_diag_trampoline')
a=template.index('        push dword ptr [ebp + 4]');b=template.index('        fxrstor',a)
template=template[:a]+'''        push dword ptr [ebp + 36]
        push dword ptr [ebp + 40]
        push dword ptr [ebp + 24]
        call ra2_state_cell_entry_diag
        add esp,12
'''+template[b:]
t=t.replace('static __declspec(naked) void object_filter_audit_hook',text+template+'\nstatic __declspec(naked) void object_filter_audit_hook',1)
pos=t.index('        static const unsigned char allied_entry_bytes[]')
t=t[:pos]+'''        static const unsigned char cell_entry_diag_bytes[]={0x83,0xEC,0x68,0x53,0x8B,0x5C,0x24,0x70};
        install_hook(0x703040,cell_entry_diag_bytes,sizeof(cell_entry_diag_bytes),cell_entry_diag_hook,&cell_entry_diag_trampoline);
'''+t[pos:]
p.write_text(t,encoding='utf-8')
p=ROOT/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_text(encoding='utf-8')
if 'ra2_state_cell_entry_diag(ecx' in t: raise SystemExit(0)
t='void ra2_state_cell_entry_diag(uint32_t actor,uint32_t cell,uint32_t caller);\n'+t
# uint32_t 已由原文件头中的头文件引入，声明放在第一个函数之前。
t=t.replace('void ra2_state_cell_entry_diag(uint32_t actor,uint32_t cell,uint32_t caller);\n','',1)
pos=t.index('void sub_');t=t[:pos]+'void ra2_state_cell_entry_diag(uint32_t actor,uint32_t cell,uint32_t caller);\n'+t[pos:]
t=t.replace('L_00703040:\n','''L_00703040:
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    ra2_state_cell_entry_diag(ecx,MEM32(esp+4),g_cur_func);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
''')
p.write_text(t,encoding='utf-8')
