"""Current heap/node harness, categorized original differences and bounded search witness."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v59'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();entries=[]
for name in ['run_batch_v58.py','accept_dynamic_v58.py','audit_scenes_v58.py','audit_sources_v58.py','plan_cleanup_v58.py','commit_movement_v58.py','audit_evidence_v58.py','verify_final_movement_v58.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v58','v59')
 if name=='run_batch_v58.py':
  t=t.replace("O=R/'evidence/movement-state-v57'","O=R/'evidence/movement-state-v58'").replace("'turns'","'heap'").replace("'segments'","'nodes'")
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for kind in ['heap','nodes']:
  run(['pwsh','-NoProfile','-File',R/('build-path-'+kind+'-probe-v59.ps1')],'build-native-'+part+'-'+kind)
  exe=S/('path_'+kind+'_probe.exe');args=[exe,R/'ra2/game/game.exe']
  if kind=='heap':args.append('0' if part=='baseline' else '1')
  log=run(args,'native-'+part+'-'+kind);x=read(log);assert x['passed']
  cases=sum(x[k] for k in (['offer_cases','take_cases','tail_cases'] if kind=='heap' else ['node_cases','publish_cases','reset_cases']))
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,cases=cases,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 run(['pwsh','-NoProfile','-File',R/'build-capacity-witness-v59.ps1'],'build-model-'+part)
 log=run([S/'capacity_witness.exe','0' if part=='baseline' else '1'],'model-'+part);x=read(log);assert x['passed']
 name='part-'+part+'-model.json';write(S/name,dict(**x,kind='model',probe_exe_sha256=sha(S/'capacity_witness.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['path_heap_probe.c','path_heap_probe.exe','path_nodes_probe.c','path_nodes_probe.exe','capacity_witness.c','capacity_witness.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts
''' +t[b:]
  a=t.index(" if name=='nodes':write(S/'native-gates.json'");b=t.index('\ndef baseline_scenes():',a)
  t=t[:a]+" if name=='nodes':write(S/'native-gates.json',dict(passed=True,groups=2,cases=sum(read(S/n)['cases'] for n in probes[:2]),receipts=probes[:2],functional_receipt=probes[2],expected_capacity_changes=read(S/probes[0])['intentional_capacity_changes'],scope='Original heap and node/cache fragments. Only categorized full-capacity pending selection may differ; original states/samples retained. Synthetic complete-search and quality/guard witness reported separately.'))\n"+t[b:]
 elif name=='audit_scenes_v58.py':t=t.replace("'segments-cross-'","'nodes-cross-'").replace('local-path','heap-node')
 elif name=='audit_sources_v58.py':
  t=t.replace('local-path service phases','heap/node service phases')
  t=t.replace("assert set(changed)=={'ra2/src/gameplay/'+n+'.c' for n in ['ground_path_local']},changed", "assert set(changed)=={'ra2/src/gameplay/ground_path_heap.c','ra2/src/gameplay/ground_path_heap.h','ra2/src/gameplay/ground_path_nodes.c'},changed")
  t=t.replace("['turns','segments']","['heap','nodes']").replace("parts['segments']","parts['nodes']")
  t=t.replace("['path_local','capture_packet','transport_packet']","['path_heap','path_nodes','capacity_witness','capture_packet','transport_packet']")
  t=t.replace("[S/(name+'_probe.exe') for name in ['path_heap','path_nodes','capacity_witness','capture_packet','transport_packet']]", "[S/name for name in ['path_heap_probe.exe','path_nodes_probe.exe','capacity_witness.exe','capture_packet_probe.exe','transport_packet_probe.exe']]")
  t=t.replace('One existing gameplay unit reorganized into service phases;', 'Existing heap and node gameplay units reorganized into service phases;')
  t=t.replace("native['groups']==3","native['groups']==2").replace('groups=3,new_cycle_cases=32768',"groups=2,new_cycle_cases=native['cases']")
  t=t.replace('anchor reverse scan, turn corridor queries, threat checks, post-block height lookahead and validate-before-publish segment ordering retained','bounded capacity selection improved; node/link allocation, state initialization and generation publication ordering retained')
 elif name=='commit_movement_v58.py':
  t=t.replace('第五十七批','第五十八批').replace('局部路径与锚点及段改写','堆容量与节点分配发布')
  t=t.replace('Stage local turn, anchor and segment rewriting services (batch 57)','Improve bounded frontier selection and stage heap/node services (batch 58)')
  t=t.replace("root_files={'README.md'", "root_files={'docs/寻路机制改进验收补充-20261025.txt','README.md'")
 elif name=='audit_evidence_v58.py':
  a=t.index('source=(R/');b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''heap=(R/'ra2/src/gameplay/ground_path_heap.c').read_text(encoding='utf-8');nodes=(R/'ra2/src/gameplay/ground_path_nodes.c').read_text(encoding='utf-8')
assert 'has_free_slot' in heap and 'try_push' in heap and 'initialize_node_state' in nodes and 'clear_wrapped_generation' in nodes
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_path_heap.c','ground_path_heap.h','ground_path_nodes.c'],new_headers_or_build_sources=False,intentional_mechanism_change='Full-capacity offer retains lower-priority pending/candidate, ties choose candidate; fixed memory budget.',retained=['under-capacity publication order and heap tie behavior','shared tail prepared-slot ABI','node counter before link counter; both advance at address selection','root/successor bridge height and x87 accumulation','priority is not initialized by node allocation','node path_link published after state','cache generation stamp before cost','reset reuses pools/heaps, clears only generation stamps on wrap'],node_storage_capacity_checked_here=False,node_storage_capacity_contract='Supplied by original search context; no new pool layout fields.',scope='Original comparison plus authorized bounded improvement. Not an all-map optimal-path guarantee.'))
''' +t[b:]
 elif name=='verify_final_movement_v58.py':
  t=t.replace('==(57,58)','==(58,59)').replace("['turns','segments']","['heap','nodes']").replace('parts/segments/','parts/nodes/')
  a=t.index(" assert len(x['probes'])==3");b=t.index(" for a in x['scenes']:",a)
  t=t[:a]+''' assert len(x['probes'])==3 and {read(S/n)['kind'] for n in x['probes']}=={'heap','nodes','model'}
 for e in read(root/'manifest.json'):assert sha(root/e['path'])==e['sha256']
 for name in x['probes']:
  proof=read(S/name);assert proof['passed'];kind=proof['kind'];exe_name={'heap':'path_heap_probe.exe','nodes':'path_nodes_probe.exe','model':'capacity_witness.exe'}[kind]
  assert proof['probe_exe_sha256']==sha(root/S.relative_to(R)/exe_name)
  if kind=='heap':assert proof['intentional_capacity_changes']>0 and proof['unexpected_differences']==0
  if kind=='model':assert proof['zero_slot_heap_reached_goal'] and proof['goal_cost']==1
''' +t[b:]
  a=t.index("native=read(S/'native-gates.json')");b=t.index("selected=read(S/'selected-baseline-scenes.json')",a)
  t=t[:a]+'''native=read(S/'native-gates.json');assert native['passed'] and native['groups']==2
assert native['cases']==sum(read(S/n)['cases'] for n in native['receipts'])
for name in native['receipts']:
 q=read(S/name);assert q['passed'] and q['original_sha256']==sha(R/'ra2/game/game.exe')
 assert q['probe_exe_sha256']==sha(S/('path_'+q['kind']+'_probe.exe'))
model=read(S/native['functional_receipt']);assert model['passed'] and model['expect_improvement'] and model['zero_slot_heap_reached_goal']
assert model['probe_exe_sha256']==sha(S/'capacity_witness.exe')
identity=read(S/'native-input-identity.json')
for item in identity['inputs']+identity['probe_executables']:assert sha(R/item['path'])==item['sha256']
baseline=read(S/'baseline-native-identity.json');assert baseline['passed']
for e in baseline['files']:assert sha(R/e['path'])==e['sha256']
old_heap=read(S/'part-baseline-heap.json');old_model=read(S/'part-baseline-model.json')
assert old_heap['intentional_capacity_changes']==0 and not old_model['zero_slot_heap_reached_goal'] and old_model['passed']
''' +t[b:]
  t=t.replace("assert read(S/'preservation.json')['changed_compile_inputs']==['ra2/src/gameplay/ground_path_local.c']", "assert set(read(S/'preservation.json')['changed_compile_inputs'])=={'ra2/src/gameplay/ground_path_heap.c','ra2/src/gameplay/ground_path_heap.h','ra2/src/gameplay/ground_path_nodes.c'}")
  t=t.replace(",'environment-note.json'",'')
  t=t.replace('generation=57','generation=58').replace('native_cases=32768',"native_cases=native['cases']")
 q=R/name.replace('v58','v59');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
# Preserve the original heap oracle. Categorize only the explicitly authorized
# return-value change; all heap arrays/counters and other operations stay exact.
p=S/'path_heap_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('if(argc!=2)return 2;','if(argc!=3)return 2;int improved=atoi(argv[2]);')
t=t.replace('unsigned offers=0,takes=0,tails=0;', 'unsigned offers=0,takes=0,tails=0,changes=0,sample_count=0;\n    struct {uint32_t n,count,capacity;float old_score,new_score;} samples[8];')
old='if(frame[0x1C/4]!=(uint32_t)(uintptr_t)actual){printf("offer return mismatch case=%u expected=%x actual=%p best=%p\\n",n,frame[0x1C/4],(void *)actual,(void *)best);return 1;}'
new='''if(frame[0x1C/4]!=(uint32_t)(uintptr_t)actual){
            if(!improved || !best || c_heap.count+1u<c_heap.capacity || frame[0x1C/4]!=(uint32_t)(uintptr_t)&nodes[128] || actual!=best || !(best->priority<nodes[128].priority)){puts("unexpected offer difference");return 1;}
            if(sample_count<8){samples[sample_count].n=n;samples[sample_count].count=c_heap.count;samples[sample_count].capacity=c_heap.capacity;samples[sample_count].old_score=nodes[128].priority;samples[sample_count].new_score=best->priority;++sample_count;}
            ++changes;
        }'''
assert old in t;t=t.replace(old,new)
a=t.index('    printf("{\\"passed\\":true,\\"offer_cases');b=t.index('return 0;',a)
t=t[:a]+'''    if(improved && !changes)return 1;
    printf("{\\"passed\\":true,\\"offer_cases\\":%u,\\"take_cases\\":%u,\\"tail_cases\\":%u,\\"intentional_capacity_changes\\":%u,\\"unexpected_differences\\":0,\\"mapped_original_fragments\\":true,\\"finite_scores\\":true,\\"samples\\":[",offers,takes,tails,changes);
    for(unsigned i=0;i<sample_count;++i)printf("%s{\\"case\\":%u,\\"count\\":%u,\\"capacity\\":%u,\\"original_selected_priority\\":%g,\\"new_selected_priority\\":%g}",i?",":"",samples[i].n,samples[i].count,samples[i].capacity,(double)samples[i].old_score,(double)samples[i].new_score);
    puts("]}");''' +t[b:]
p.write_text(t,encoding='utf-8',newline='\n')
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=entries,heap_probe_origin_sha256=sha(R/'evidence/movement-state-v38/path_heap_probe.c'),nodes_probe_origin_sha256=sha(S/'path_nodes_probe.c')),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v58'))
