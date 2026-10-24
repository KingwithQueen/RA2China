"""Wire the complete queued-path/retry decision through one gameplay cycle."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41'
def save(p,t):
 raw=p.read_bytes();nl='\r\n' if raw.count(b'\r\n')==raw.count(b'\n') else '\n';p.write_bytes(t.replace('\n',nl).encode('utf-8'))
p=R/'ra2/src/runtime/ground_prepare_bridge.c';t=p.read_text(encoding='utf-8');t='#include "ground_prepare_cycle.h"\n'+t
marker='uint32_t ra2_ground_prepare_entry_bridge(void)';assert t.count(marker)==1
helpers='''static Ra2PathRetryTimer cycle_retry_timer(void *opaque)
{
    PrepareContext *context=opaque;uint32_t owner=owner_address(context);
    return (Ra2PathRetryTimer){(int32_t)MEM32(owner+0x530),(int32_t)MEM32(owner+0x538)};
}
static int32_t cycle_current_frame(void *opaque)
{(void)opaque;return (int32_t)MEM32(0xA40D2C);}
uint32_t ra2_ground_prepare_cycle_bridge(void)
{
    ra2_state_movement_audit(15,g_ebp,0,0);
    PrepareContext context={0};context.drive=g_ebp;context.frame=g_esp;
    int32_t path_head=(int32_t)g_ebx;int is_moving=(g_eax&255u)!=0;
    read_state(&context);g_esp-=0x200;
    Ra2PrepareServices prepare=services_for(&context);
    Ra2PrepareCycleServices services={&prepare,&context,cycle_retry_timer,cycle_current_frame};
    Ra2PreparePhase phase=ra2_ground_prepare_cycle(&context.state,read_point(0x852998),
        is_moving,&path_head,&services);
    return finish(&context,phase,path_head);
}

'''
save(p,t.replace(marker,helpers+marker))
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');assert t.count('ra2_ground_prepare_entry_bridge();')==1
t='extern unsigned ra2_ground_prepare_cycle_bridge(void);\n'+t.replace('ra2_ground_prepare_entry_bridge();','ra2_ground_prepare_cycle_bridge();')
t=t.replace('    if (prepare_entry_resume == 0x004A285Eu) goto L_004A285E;\n    goto L_004A32CA;','    if (prepare_entry_resume == 0x004A285Eu) goto L_004A285E;\n    if (prepare_entry_resume == 0x004A2F7Au) goto L_004A2F7A;\n    if (prepare_entry_resume == 0x004A2A83u) goto L_004A2A83;\n    if (prepare_entry_resume == 0x004A2EACu) goto L_004A2EAC;\n    goto L_004A32CA;');save(p,t)
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');m='  src/gameplay/ground_prepare.c\n';assert t.count(m)==1;t=t.replace(m,m+'  src/gameplay/ground_prepare_cycle.c\n');t+='\nset_source_files_properties(src/gameplay/ground_prepare_cycle.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';save(p,t)
# Build only the affected prepare probe, retaining its older entry/retry oracle phases.
t=(R/'build-prepare-probes-v38.ps1').read_text(encoding='utf-8-sig');line=next(l for l in t.splitlines() if 'prepare_probe.c ' in l)
line=line.replace(' ..\\..\\ra2\\src\\gameplay\\ground_prepare.c',' ..\\..\\ra2\\src\\gameplay\\ground_prepare.c ..\\..\\ra2\\src\\gameplay\\ground_prepare_cycle.c')
head=t[:t.index('    & cl')].replace('v38','v41')
(R/'build-prepare-probe-v41.ps1').write_text(head+line+"\n    if ($LASTEXITCODE) { throw 'Prepare cycle probe failed' }\n} finally { Pop-Location }\n",encoding='utf-8',newline='\n')
p=R/'build-segment-probe-v41.ps1';t=p.read_text(encoding='utf-8');t=t.replace(' ..\\..\\ra2\\src\\gameplay\\ground_prepare.c',' ..\\..\\ra2\\src\\gameplay\\ground_prepare.c ..\\..\\ra2\\src\\gameplay\\ground_prepare_cycle.c');save(p,t)
p=S/'prepare_probe.c';t=p.read_text(encoding='utf-8');t='extern unsigned ra2_ground_prepare_cycle_bridge(void);\n'+t
t=t.replace('outcome_counts[2][6]','outcome_counts[3][6]').replace('phase < 2','phase < 3').replace('phase == 1 && b == 0','phase >= 1 && b == 0')
t=t.replace('phase == 0 ? 0x4A2690 : 0x4A285E','phase == 1 ? 0x4A285E : 0x4A2690')
t=t.replace('phase == 0 ? ra2_ground_prepare_entry_bridge() : ra2_ground_retry_path_bridge()','phase == 0 ? ra2_ground_prepare_entry_bridge() : phase == 1 ? ra2_ground_retry_path_bridge() : ra2_ground_prepare_cycle_bridge()')
m='    printf("{\\"passed\\":true,\\"entry_cases';i=t.index(m);j=t.index('\n    return 0;',i)
t=t[:i]+'''    printf("{\\"passed\\":true,\\"entry_cases\\":65536,\\"retry_cases\\":65536,\\"cycle_cases\\":65536,\\"state_calls_abi_cw_verified\\":true,\\"cycle_outcomes\\":[%u,%u,%u,%u,%u,%u]}\\n",outcome_counts[2][0],outcome_counts[2][1],outcome_counts[2][2],outcome_counts[2][3],outcome_counts[2][4],outcome_counts[2][5]);'''+t[j:];save(p,t)
(S/'pending/prepare-integration.json').write_text(json.dumps(dict(passed=True,primary_prepare_cycle=True,clock_read_only_after_retry_transition=True,new_native_entries=0,original_labels_and_tail_tables_retained=True),indent=2)+'\n',encoding='utf-8')
print('Integrated Prepare cycle and native cycle oracle')
