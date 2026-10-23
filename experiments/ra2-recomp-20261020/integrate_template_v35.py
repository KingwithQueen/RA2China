"""Continue from the incoming table pointer and scaled sample offset."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
p=R/'ra2/src/runtime/ground_tube_state_bridge.c';t=p.read_text(encoding='utf-8')
mark='uint32_t ra2_ground_internal_handoff_bridge(unsigned entry)'
new='static void retain_loaded_table(void *opaque,int32_t table){(void)opaque;(void)table;}\nstatic Ra2PathSample loaded_sample(void *opaque,int32_t index)\n{\n    TubeContext *c=opaque;(void)index;Ra2PathSample value;\n    memcpy(&value,(void *)(uintptr_t)ADDR(c->table+c->vector*4u),sizeof(value));return value;\n}\n'
assert t.count(mark)==1;t=t.replace(mark,new+mark)
a='int32_t index=entry==3?(int32_t)g_edx:';assert a in t
b='if(entry==4){c.table=g_eax;c.vector=g_ecx;services.select_table=retain_loaded_table;services.sample_at=loaded_sample;}\n    int32_t index=entry>=3?(int32_t)g_edx:'
t=t.replace(a,b.replace('\\n','\n'));p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A2320:\n';n=t.count(m);assert n==8
code='    /* 已载入表和缩放偏移来自入口寄存器，保留原终止样本判定。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned loaded_sample_resume_v35=ra2_ground_internal_handoff_bridge(4);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(loaded_sample_resume_v35==0x4A263A)goto L_004A263A;\n    goto L_004A237D;\n'
t=t.replace(m,m+code);p.write_bytes(t.encode('utf-8'))
(S/'pending/loaded-sample-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2320',copies=n,index_source='incoming EDX; table EAX; scaled offset ECX',new_native_entries=0),indent=2)+'\n',encoding='utf-8')
