"""只读诊断：记录寻路候选与节点评分；正式归档前恢复，绝不放宽比较器。"""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent; S=R/'evidence/movement-state-v11'
p=R/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8')
backup=S/'diagnostic-current'; backup.mkdir(exist_ok=True)
for rel in ['ra2/src/runtime/state_trace.c','ra2/src/recomp/gen_game/recomp_0003.c']:
    target=backup/Path(rel).name
    if target.exists(): assert target.read_bytes()==(R/rel).read_bytes(),rel
    else: shutil.copy2(R/rel,target)
text=r'''
void ra2_path_diag(uint32_t stage,uint32_t frame,uint32_t context,uint32_t value)
{
    uint32_t node,cell,parent,index;
    if (!movement_audit_enabled || !state_file || !started || U32(FRAME_ADDRESS)!=52) return;
    if(stage==1) {
        cell=value; node=U32(frame+0x14);
        index=(uint32_t)(int32_t)(int16_t)U16(cell+0x24)+(uint32_t)(int32_t)(int16_t)U16(cell+0x26)*U32(0x84E804);
        fprintf(state_file,"{\"kind\":\"path-detail\",\"stage\":1,\"cell\":[%d,%d],\"dir\":%u,\"g\":%u,\"f\":%u,\"cache\":[%u,%u],\"mark\":[%u,%u],\"epoch\":%u}\n",
            (int16_t)U16(cell+0x24),(int16_t)U16(cell+0x26),U32(frame+0x18),U32(node+4),U32(node+8),
            U32(U32(context+0x20)+index*4),U32(U32(context+0x24)+index*4),
            U32(U32(context+0x18)+index*4),U32(U32(context+0x1c)+index*4),U32(context+0x28));
    } else {
        node=value; cell=U32(U32(U32(node))); parent=U32(frame+0x14);
        fprintf(state_file,"{\"kind\":\"path-detail\",\"stage\":2,\"cell\":[%d,%d],\"dir\":%u,\"g\":%u,\"f\":%u,\"edge\":%u,\"parent_g\":%u}\n",
            (int16_t)U16(cell+0x24),(int16_t)U16(cell+0x26),U32(frame+0x18),U32(node+4),U32(node+8),U32(frame+0x34),U32(parent+4));
    }
}
'''
start=t.index('static __declspec(naked) void object_filter_audit_hook')
template=t[start:t.index('\n}\n',start)+3]
hooks=''
for stage,name in [(1,'candidate'),(2,'score')]:
    hook=template.replace('object_filter_audit_hook',f'path_{name}_diag_hook').replace('object_filter_trampoline',f'path_{name}_diag_trampoline')
    a=hook.index('        push dword ptr [ebp + 4]');b=hook.index('        fxrstor',a)
    offset=16 if stage==1 else 28
    hook=hook[:a]+f'''        push dword ptr [ebp + {offset}]
        push dword ptr [ebp + 4]
        lea eax,[ebp + 36]
        push eax
        push {stage}
        call ra2_path_diag
        add esp,16
'''+hook[b:]
    hooks+=f'static void *path_{name}_diag_trampoline;\n'+hook+'\n'
t=t[:start]+text+hooks+t[start:]
pos=t.index('        static const unsigned char allied_entry_bytes[]')
t=t[:pos]+'''        static const unsigned char path_candidate_diag_bytes[]={0x8B,0x44,0x24,0x18,0x8D,0x4B,0x24};
        static const unsigned char path_score_diag_bytes[]={0x8B,0xD8,0x8B,0x44,0x24,0x1C};
        install_hook(0x427704,path_candidate_diag_bytes,sizeof(path_candidate_diag_bytes),path_candidate_diag_hook,&path_candidate_diag_trampoline);
        install_hook(0x427912,path_score_diag_bytes,sizeof(path_score_diag_bytes),path_score_diag_hook,&path_score_diag_trampoline);
'''+t[pos:]
p.write_text(t,encoding='utf-8')
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
pos=t.index('void sub_');t=t[:pos]+'void ra2_path_diag(uint32_t,uint32_t,uint32_t,uint32_t);\n'+t[pos:]
for addr,stage,value in [('00427704',1,'ebx'),('00427912',2,'eax')]:
    # 这些地址并非每处都有标签，按唯一指令注释覆盖每个重复函数体。
    lines=t.splitlines(keepends=True);count=0;out=[]
    for line in lines:
        if f'/* 0x{addr}: ' in line:
            out.append(f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_diag({stage},esp,esi,{value}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n');count+=1
        out.append(line)
    assert count=={'00427704':4,'00427912':7}[addr],(addr,count)
    t=''.join(out)
p.write_text(t,encoding='utf-8')
print('diagnostic installed in all copies of each generated location')
