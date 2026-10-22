"""只读记录 Walk 坐标计算；浮点、寄存器及标志全部恢复。"""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v12'
p=R/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8');assert t==(S/'baseline/ra2/src/runtime/state_trace.c').read_text(encoding='utf-8')
extra=r'''
void ra2_walk_diag(uint32_t stage,uint32_t stack,uint32_t walk,uint32_t x,uint32_t y,const unsigned char *fx)
{
    uint32_t actor=U32(walk+0xC),frame=U32(FRAME_ADDRESS);
    if(!movement_audit_enabled || !state_file || !started || frame<26 || frame>28 || U32(actor+0x10)!=1032262) return;
    uint64_t top=0; uint16_t exponent=0,control=g_fpu_cw;
    if(fx) {memcpy(&control,fx,2);memcpy(&top,fx+32,8);memcpy(&exponent,fx+40,2);}
    else {extern double g_st[8];memcpy(&top,&g_st[0],8);}
    fprintf(state_file,"{\"kind\":\"walk-detail\",\"stage\":%u,\"frame\":%u,\"id\":1032262,\"x\":%d,\"y\":%d,\"cw\":%u,\"top\":\"%016llx\",\"exp\":%u,\"local\":[%d,%d,%d,%d]}\n",stage,frame,(int32_t)x,(int32_t)y,control,(unsigned long long)top,exponent,I32(stack+0x14),I32(stack+0x3C),I32(stack+0x40),I32(stack+0x24));
}
'''
start=t.index('static __declspec(naked) void object_filter_audit_hook');template=t[start:t.index('\n}\n',start)+3];hooks=''
for stage in [1,2,3]:
    hook=template.replace('object_filter_audit_hook',f'walk_diag_{stage}_hook').replace('object_filter_trampoline',f'walk_diag_{stage}_trampoline')
    a=hook.index('        push dword ptr [ebp + 4]');b=hook.index('        fxrstor',a)
    hook=hook[:a]+f'''        push esp
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 28]
        push dword ptr [ebp + 8]
        lea eax,[ebp+36]
        push eax
        push {stage}
        call ra2_walk_diag
        add esp,24
'''+hook[b:]
    hooks+=f'static void *walk_diag_{stage}_trampoline;\n'+hook+'\n'
t=t[:start]+extra+hooks+t[start:]
pos=t.index('        static const unsigned char allied_entry_bytes[]')
t=t[:pos]+'''        static const unsigned char walk_diag_1_bytes[]={0x0F,0xBF,0xCE,0x81,0xE9,0xFF,0x3F,0,0};
        static const unsigned char walk_diag_2_bytes[]={0x83,0xC4,0x10,0xDA,0x44,0x24,0x3C};
        static const unsigned char walk_diag_3_bytes[]={0x89,0x44,0x24,0x30,0x89,0x74,0x24,0x34};
        install_hook(0x71F3B8,walk_diag_1_bytes,sizeof(walk_diag_1_bytes),walk_diag_1_hook,&walk_diag_1_trampoline);
        install_hook(0x71F410,walk_diag_2_bytes,sizeof(walk_diag_2_bytes),walk_diag_2_hook,&walk_diag_2_trampoline);
        install_hook(0x71F41C,walk_diag_3_bytes,sizeof(walk_diag_3_bytes),walk_diag_3_hook,&walk_diag_3_trampoline);
'''+t[pos:];p.write_text(t,encoding='utf-8')
p=R/'ra2/src/recomp/gen_game/recomp_0048.c';t=p.read_text(encoding='utf-8');pos=t.index('void sub_');t=t[:pos]+'void ra2_walk_diag(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,const unsigned char *);\n'+t[pos:]
for addr,stage in [('0071F3B8',1),('0071F410',2),('0071F41C',3)]:
    lines=t.splitlines(keepends=True);out=[];count=0
    for line in lines:
        # add esp 指令产生三行同地址注释，故只匹配其实际赋值；在该块首行插入。
        match=f'/* 0x{addr}: ' in line and (stage!=2 or 'esp = esp +' in line)
        if match:
            out.append(f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_walk_diag({stage},esp,ebp,eax,esi,0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n');count+=1
        out.append(line)
    assert count==1,(addr,count);t=''.join(out)
p.write_text(t,encoding='utf-8')
