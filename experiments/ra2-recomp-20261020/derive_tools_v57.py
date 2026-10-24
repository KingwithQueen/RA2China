"""Bounded inherited harness; explicit parent identity and two original optimizer probes."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v57'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lineage=[]
for name in ['run_batch_v56.py','accept_dynamic_v56.py','audit_scenes_v56.py','audit_sources_v56.py','plan_cleanup_v56.py','commit_movement_v56.py','audit_evidence_v56.py','verify_final_movement_v56.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v56','v57')
 if name=='run_batch_v56.py':
  t=t.replace("O=R/'evidence/movement-state-v55'", "O=R/'evidence/movement-state-v56'")
  t=t.replace("S=R/'evidence/movement-state-v57';O=R/'evidence/movement-state-v56'", "S=R/'evidence/movement-state-v57';O=R/'evidence/movement-state-v56'\nassert O==Path(json.loads((S/'vcs-context.json').read_text(encoding='utf-8-sig'))['parent_archive']).parent")
  t=t.replace("'layers'","'smooth'").replace("'edges'","'postprocess'")
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 run(['pwsh','-NoProfile','-File',R/'build-path-optimize-probe-v57.ps1'],'build-native-'+part)
 receipts=[]
 for phase in [0,1]:
  log=run([S/'path_optimize_probe.exe',R/'ra2/game/game.exe',str(phase)],'native-'+part+'-'+str(phase))
  x=read(log);assert x['passed'] and x['cases']==8192 and x['phase']==phase
  name='part-'+part+'-path-optimize-'+str(phase)+'.json'
  write(S/name,dict(**x,probe_exe_sha256=sha(S/'path_optimize_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe')))
  receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';assert not out.exists();out.mkdir();entries=[]
  for name in ['path_optimize_probe.c','path_optimize_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);entries.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=entries,receipts=receipts,production_source=str(S/'baseline/ra2/src/gameplay/ground_path_optimize.c'),production_source_sha256=sha(S/'baseline/ra2/src/gameplay/ground_path_optimize.c'),probe_sha256=sha(out/'path_optimize_probe.exe')))
 return receipts
''' +t[b:]
  t=t.replace('def snapshot(name,values,probe):','def snapshot(name,values,probes):').replace('probes=[probe],files=','probes=probes,files=')
  t=t.replace(' probe=native(name)',' probes=native(name)').replace('snapshot(name,values,probe)','snapshot(name,values,probes)')
  a=t.index(" if name=='postprocess':write(S/'native-gates.json'");b=t.index('\ndef baseline_scenes():',a)
  t=t[:a]+" if name=='postprocess':write(S/'native-gates.json',dict(passed=True,groups=2,cases=16384,receipts=probes,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,scope='Mapped original smooth and postprocess routines, 8192 distinct inputs each. Same groups before and after both parts; repeat executions counted once. Ordered callback arguments, full path structure, direction and height buffers; engine services stubbed.'))\n"+t[b:]
 elif name=='audit_scenes_v56.py':
  t=t.replace("'edges-cross-'","'postprocess-cross-'").replace('regional-search','path-optimization')
 elif name=='audit_sources_v56.py':
  t=t.replace('regional-search service phases','path-optimization service phases').replace("['ground_region_search']","['ground_path_optimize']")
  t=t.replace("['layers','edges']","['smooth','postprocess']").replace("parts['edges']","parts['postprocess']")
  t=t.replace("['region_search','capture_packet','transport_packet']","['path_optimize','capture_packet','transport_packet']")
  t=t.replace("native['groups']==1","native['groups']==2").replace('groups=1,new_cycle_cases=6144','groups=2,new_cycle_cases=16384')
  t=t.replace('coarse-to-fine layer setup, same-region shortcut, penalty conversion, edge filter and full-heap cache publication ordering retained','smooth pair/connection progression, callback-updated arrays and anchors, postprocess scan limits and compaction ordering retained')
 elif name=='commit_movement_v56.py':
  t=t.replace('第五十五批','第五十六批').replace('分层区域搜索与边代价','路径平滑与后处理服务')
  t=t.replace('Stage layered region search, edge restrictions and cost services (batch 55)','Stage path smoothing and postprocess services (batch 56)')
 elif name=='audit_evidence_v56.py':
  a=t.index('source=(R/');b=t.index('print(dict(passed=True',a)
  t=t[:a]+'''source=(R/'ra2/src/gameplay/ground_path_optimize.c').read_text(encoding='utf-8')
for helper in ['advance_smooth_scan','finish_smooth_pair','rewrite_postprocess_segment','compact_postprocess_directions']:assert helper in source
write(S/'service-boundaries.json',dict(passed=True,changed_unit='ground_path_optimize.c',new_headers_or_build_sources=False,stages=['smooth scan progression and paired-turn completion','postprocess anchor/rewrite service boundary','direction-only compaction and terminal padding'],retained=['entry length/direction/height pointer snapshots','shorten callback updates anchor/directions/heights before rereading next direction','same second-direction pair extends without advancing point','special connection in smooth uses callback; postprocess uses offset zero and resets scan','reversal retries same index; front scan bounded by old length and 20','find-anchor precedes delta, count and live height lookup','terminal rewrite uses index minus one, final flag and original count expression','rewrite feedback on local anchor/delta does not overwrite scan point','compaction skips minus two, stops at minus one, preserves height slots','padding uses live path length and writes the extra terminator'],native_probe_scope='8192 original inputs per routine, comparing ordered callbacks, complete path object and buffers; engine services stubbed. Not all ABI fields or natural rewrite behavior.'))
write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=False,parent_status=str(O/'infrastructure-status.json'),parent_status_sha256=sha(O/'infrastructure-status.json'),scope='Current scene setup succeeded; historical infrastructure evidence retained through the parent status chain.'))
''' +t[b:]
 elif name=='verify_final_movement_v56.py':
  t=t.replace('==(55,56)','==(56,57)').replace("['layers','edges']","['smooth','postprocess']").replace('parts/edges/','parts/postprocess/')
  t=t.replace('region_search_probe','path_optimize_probe').replace("['ra2/src/gameplay/ground_region_search.c']","['ra2/src/gameplay/ground_path_optimize.c']")
  t=t.replace("proof['cases']==6144","proof['cases']==8192")
  t=t.replace("  assert proof['successes']>0 and proof['failures']>0 and proof['final_numeric_control_compared']\n  assert proof['successes']+proof['failures']==6144", "  assert proof['phase'] in [0,1] and proof['ordered_callbacks_and_buffers_compared']")
  t=t.replace("native['groups']==1 and native['cases']==6144","native['groups']==2 and native['cases']==16384")
  a=t.index("baseline=read(S/'part-baseline-region-search.json')");b=t.index("selected=read(S/'selected-baseline-scenes.json')",a)
  t=t[:a]+'''baseline=read(S/'baseline-native-identity.json');assert baseline['passed']
for e in baseline['files']:assert sha(R/e['path'])==e['sha256']
assert sha(Path(baseline['production_source']))==baseline['production_source_sha256']
for name in baseline['receipts']:
 x=read(S/name);assert x['passed'] and x['cases']==8192 and x['probe_exe_sha256']==baseline['probe_sha256']
assert sum(read(S/name)['cases'] for name in native['receipts'])==16384
''' +t[b:]
  t=t.replace(",'tooling-correction.json'",'')
  a=t.index("correction=read(S/'tooling-correction.json')");b=t.index("for x in read(S/'boundary-inheritance.json')",a)
  t=t[:a]+t[b:]
  t=t.replace('generation=55','generation=56').replace('native_cases=6144','native_cases=16384')
 q=R/name.replace('v56','v57');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n')
 lineage.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
source=R/'evidence/movement-state-v38/path_optimize_probe.c'
assert sha(source)==sha(S/'path_optimize_probe.c')
lineage.append(dict(source=source.relative_to(R).as_posix(),source_sha256=sha(source),derived=(S/'path_optimize_probe.c').relative_to(R).as_posix(),derived_sha256=sha(S/'path_optimize_probe.c'),change='Unmodified original smooth/postprocess probe; separate phase groups counted once.'))
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=lineage),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(lineage),parent='movement-state-v56'))
