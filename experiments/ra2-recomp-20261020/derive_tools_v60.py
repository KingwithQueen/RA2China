"""Derive current lifecycle gates and ordinary traffic acceptance without changing global comparators."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v60'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();entries=[]
for name in ['run_batch_v59.py','accept_dynamic_v59.py','audit_scenes_v59.py','audit_sources_v59.py','plan_cleanup_v59.py','commit_movement_v59.py','audit_evidence_v59.py','verify_final_movement_v59.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v59','v60')
 t=t.replace("O=R/'evidence/movement-state-v58'","O=R/'evidence/movement-state-v59'")
 if name=='run_batch_v59.py':
  t=t.replace("['heap','nodes']","['completion','rebuild']")
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for kind,probe,phase in [('completion','local',3),('rebuild','lifecycle',2)]:
  run(['pwsh','-NoProfile','-File',R/('build-path-'+probe+'-probe-v60.ps1')],'build-native-'+part+'-'+kind)
  exe=S/('path_'+probe+'_probe.exe')
  log=run([exe,R/'ra2/game/game.exe',phase],'native-'+part+'-'+kind);x=read(log);assert x['passed']
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['path_local_probe.c','path_local_probe.exe','path_lifecycle_probe.c','path_lifecycle_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

''' +t[b:]
  a=t.index(" if name=='nodes':write(S/'native-gates.json'");b=t.index('\ndef baseline_scenes():',a)
  t=t[:a]+" if name=='rebuild':write(S/'native-gates.json',dict(passed=True,groups=2,cases=sum(read(S/n)['cases'] for n in probes),receipts=probes,scope='Completion callback/return/stack control and original complete path reconstruction. Exact fragment results; finite scope. Prior bounded heap improvement inherited separately.'))\n"+t[b:]
  t=t.replace("['baseline','heap','nodes','final-scenes']","['baseline','completion','rebuild','final-scenes']")
  t=t.replace("if x.action=='baseline':baseline_scenes()", "if x.action=='baseline':native('baseline');baseline_scenes();baseline_traffic()")
  t=t.replace("  x=read(p);c=x['comparison'];observer=", "  x=read(p);c=x['comparison'];traffic=tag.removeprefix('b-').startswith('traffic-');observer=")
  t=t.replace("tag in ['mi','sc','aw3','fm','b-fm']", "(tag in ['mi','sc','aw3','fm','b-fm'] or tag.removeprefix('b-').startswith('traffic-'))")
  a=t.index("  if not x['passed']:");b=t.index('  return dict(tag=',a)
  t=t[:a]+'''  if traffic:
   from accept_traffic_v60 import analyze
   assert analyze(tag)['passed']
  elif not x['passed']:
   assert tag in ['mi','sc','aw3','fm','b-fm']
   from accept_dynamic_v60 import analyze
   assert analyze(tag)['passed']
  if x['passed']:assert c['rng_equal_all_frames'] and c['equal_frames']==c['frames_compared']
''' +t[b:]
  a=t.index('def final_scenes():')
  t=t[:a]+'''def baseline_traffic():
 jobs=[fixture_job(x['baseline_tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]
 values=scenes(jobs)
 write(S/'traffic-baseline-scenes.json',dict(passed=True,results=values,scope='Two new ordinary-map traffic recipes executed against original and the unchanged parent production program before either service edit.'))

''' +t[a:]
  t=t.replace(" jobs=[fixture_job(x['tag'],x,x['last']) for x in read(S/'dynamic-fixtures.json')['fixtures']]", " jobs=[fixture_job(x['tag'],x,x['last']) for x in read(S/'dynamic-fixtures.json')['fixtures']]\n jobs += [fixture_job(x['tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]")
 elif name=='audit_sources_v59.py':
  t=t.replace("{'ra2/src/gameplay/ground_path_heap.c','ra2/src/gameplay/ground_path_heap.h','ra2/src/gameplay/ground_path_nodes.c'}", "{'ra2/src/gameplay/ground_path_completion.c','ra2/src/gameplay/ground_path_rebuild.c'}")
  t=t.replace("['heap','nodes']","['completion','rebuild']").replace("parts['nodes']","parts['rebuild']")
  t=t.replace("['path_heap_probe.exe','path_nodes_probe.exe','capacity_witness.exe','capture_packet_probe.exe','transport_packet_probe.exe']", "['path_local_probe.exe','path_lifecycle_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace('heap/node service phases','completion/rebuild service phases').replace('bounded capacity selection improved; node/link allocation, state initialization and generation publication ordering retained','completion gate, callback ordering, delayed obstacle restoration, metadata publication and reverse parent-chain reconstruction retained')
 elif name=='audit_scenes_v59.py':
  t=t.replace("'nodes-cross-'","'rebuild-cross-'").replace('heap-node','completion/rebuild')
  t += '''\nfrom accept_traffic_v60 import analyze as traffic_analyze
traffic={x['tag']:traffic_analyze(x['tag']) for x in read(S/'traffic-fixtures.json')['fixtures']}
write(S/'traffic-effects.json',dict(passed=True,scenes=traffic,ordinary_events=True,production_host=True,new_unique_recipes=2,baseline_pairs=2,final_pairs=2,memory_state_injection=False,path_result_injection=False))
'''
 elif name=='audit_evidence_v59.py':
  a=t.index("heap=(R/");b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''completion=(R/'ra2/src/gameplay/ground_path_completion.c').read_text(encoding='utf-8');rebuild=(R/'ra2/src/gameplay/ground_path_rebuild.c').read_text(encoding='utf-8')
assert 'can_publish_path' in completion and 'rebuild_and_finalize' in completion and 'initialize_result' in rebuild and 'reconstruct_steps' in rebuild
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_path_completion.c','ground_path_rebuild.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['invalid/already-there early returns','equality-only expansion limit gates before path length','rebuild then smooth then postprocess, even if rebuild returns null','shared obstacle flag read after callbacks','metadata before parent-chain reads','parent surface, parent point then child point, reverse slots','nonadjacent direction 8 and final -1 slot','root point read again after terminator; zero score corrected last'],scope='Finite original fragment equality and normal traffic effects. Existing bounded heap choice remains unchanged; no new mechanism change without evidence.'))
'''+t[b:]
 elif name=='commit_movement_v59.py':
  t=t.replace('第五十八批','第五十九批').replace('堆容量与节点分配发布','路径完成重建与自然交通')
  t=t.replace('Improve bounded frontier selection and stage heap/node services (batch 58)','Stage path completion and reconstruction with natural traffic (batch 59)')
 elif name=='verify_final_movement_v59.py':
  t=t.replace('==(58,59)','==(59,60)').replace('generation=58','generation=59')
  t=t.replace("['heap','nodes']","['completion','rebuild']").replace('parts/nodes/','parts/rebuild/')
  a=t.index(" assert len(x['probes'])==3");b=t.index(" for a in x['scenes']:",a)
  t=t[:a]+''' assert len(x['probes'])==2 and {read(S/n)['kind'] for n in x['probes']}=={'completion','rebuild'}
 for e in read(root/'manifest.json'):assert sha(root/e['path'])==e['sha256']
 for name in x['probes']:
  proof=read(S/name);assert proof['passed'];exe_name={'completion':'path_local_probe.exe','rebuild':'path_lifecycle_probe.exe'}[proof['kind']]
  assert proof['probe_exe_sha256']==sha(root/S.relative_to(R)/exe_name)
''' +t[b:]
  a=t.index("native=read(S/'native-gates.json')");b=t.index("selected=read(S/'selected-baseline-scenes.json')",a)
  t=t[:a]+'''native=read(S/'native-gates.json');assert native['passed'] and native['groups']==2 and native['cases']==24576
for name in native['receipts']:
 q=read(S/name);assert q['passed'] and q['original_sha256']==sha(R/'ra2/game/game.exe')
 assert q['probe_exe_sha256']==sha(S/({'completion':'path_local_probe.exe','rebuild':'path_lifecycle_probe.exe'}[q['kind']]))
identity=read(S/'native-input-identity.json')
for item in identity['inputs']+identity['probe_executables']:assert sha(R/item['path'])==item['sha256']
baseline=read(S/'baseline-native-identity.json');assert baseline['passed']
for e in baseline['files']:assert sha(R/e['path'])==e['sha256']
for name in baseline['receipts']:assert read(S/name)['passed']
lineage=read(S/'checker-lineage.json');assert lineage['passed']
for item in lineage['entries']:
 assert sha(R/item['derived'])==item['final_derived_sha256']
 assert sha(R/item['source'])==item['source_sha256']
for name,digest in lineage['native_origins'].items():assert sha(S/name)==digest==sha(R/'evidence/movement-state-v38'/name)
''' +t[b:]
  a=t.index('matrix=read(');b=t.index("assert read(S/'fixture-host-identity.json')",a)
  t=t[:a]+'''matrix=read(S/'final-scene-matrix.json');traffic_baseline=read(S/'traffic-baseline-scenes.json');assert traffic_baseline['passed']
from accept_traffic_v60 import analyze as traffic_analyze
frames=0;strict=6;pair_count=6
for a in matrix['results']+traffic_baseline['results']:
 p=S/'runs'/a['tag']/'comparison.json';x=read(p);c=x['comparison'];is_baseline=a in traffic_baseline['results']
 expected=sha(S/'baseline/ra2/build-original-c/ra2.exe') if is_baseline else sha(S/'bridge-catalog-observer.exe') if a['capture_host'] else sha(exe)
 assert sha(p)==a['comparison_sha256'] and x['exe_sha256']==expected
 for run in x['runs']:assert run['passed'] and sha(p.parent/run['mode']/'state.jsonl')==run['state_sha256']
 assert c['negative_control']['passed']
 if x['passed']:assert c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames'];strict+=1
 elif 'traffic-' not in a['tag']:
  assert a['tag'] in ['mi','sc','aw3','fm']
  from accept_dynamic_v60 import analyze
  assert analyze(a['tag'])['baseline_inherited_exactly']
 if 'traffic-' in a['tag']:assert traffic_analyze(a['tag'])['passed']
 frames+=c['frames_compared'];pair_count+=1
assert frames+2606==v['accepted_frames']==22669 and pair_count==v['accepted_game_pairs']==19
assert strict==v['strict_game_pairs'] and pair_count-strict==v['functional_game_pairs']
assert read(S/'traffic-effects.json')['passed']
''' +t[b:]
  t=t.replace("{'ra2/src/gameplay/ground_path_heap.c','ra2/src/gameplay/ground_path_heap.h','ra2/src/gameplay/ground_path_nodes.c'}", "{'ra2/src/gameplay/ground_path_completion.c','ra2/src/gameplay/ground_path_rebuild.c'}")
  t=t.replace('game_pairs=15,frames=19065',"game_pairs=v['accepted_game_pairs'],frames=v['accepted_frames']")
 q=R/name.replace('v59','v60');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins={n:sha(S/n) for n in ['path_local_probe.c','path_lifecycle_probe.c']}),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v59'))
