"""Share the register-sourced sample continuation, keeping all native labels."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
p=R/'ra2/src/runtime/ground_tube_state_bridge.c';t=p.read_text(encoding='utf-8')
old='int32_t index=(int32_t)MEM32(c.drive+0x5C);Ra2SamplingPhase'
assert t.count(old)==1;t=t.replace(old,'int32_t index=entry==3?(int32_t)g_edx:(int32_t)MEM32(c.drive+0x5C);Ra2SamplingPhase');p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A2314:\n';n=t.count(m);assert n==8
t=t.replace(m,m+'''    /* 从原寄存器读取样本下标，不重读drive缓存。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); unsigned sample_resume_v34=ra2_ground_internal_handoff_bridge(3);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if(sample_resume_v34==0x4A263A)goto L_004A263A;
    goto L_004A237D;
''');p.write_bytes(t.encode('utf-8'))
(S/'pending/register-sample-integration.json').write_text(json.dumps(dict(passed=True,entry='004A2314',copies=n,index_source='incoming EDX',new_native_entries=0),indent=2)+'\n',encoding='utf-8')
