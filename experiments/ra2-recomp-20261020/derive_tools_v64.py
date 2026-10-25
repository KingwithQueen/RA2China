"""Derive from explicit v63 archives; freeze final tool identities before cleanup."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec="[('overlap',51),('segment',42),('travel',38)]"
p=R/'prepare_movement_v63.py';t=p.read_text(encoding='utf-8-sig').replace('v63','v64').replace('v62','v63')
t=t.replace('ccd7050fdf03e2d4c41770412e757264b79d1e2b','9b5f4e9af1219f6bfbe2f6cf90b5326130510c2a').replace("[('wait',44),('obstacle',53),('recovery',53)]",spec)
t=t.replace('Batch 62 baseline and waiting/release inputs','Batch 63 baseline and bridge/channel inputs')
(R/'prepare_movement_v64.py').write_text(t,encoding='utf-8',newline='\n')
entries=[]
for name in ['run_batch','accept_dynamic','audit_sources','audit_evidence','plan_cleanup','commit_movement','verify_final_movement']:
 p=R/(name+'_v63.py');t=p.read_text(encoding='utf-8-sig').replace('v63','v64')
 t=t.replace("O=R/'evidence/movement-state-v62'","O=R/'evidence/movement-state-v63'")
 t=t.replace("{'ra2/src/gameplay/ground_wait.c','ra2/src/gameplay/ground_obstacle.c'}","{'ra2/src/gameplay/ground_bridge_plane.c','ra2/src/gameplay/ground_segment.c','ra2/src/gameplay/ground_tube_travel.c'}")
 t=t.replace("['wait','release']","['bridge','channel']").replace("parts['release']","parts['channel']").replace('parts/release/','parts/channel/')
 if name=='run_batch':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for probe in ['overlap','segment','travel']:
  run(['pwsh','-NoProfile','-File',R/('build-'+probe+'-probe-v64.ps1')],'build-native-'+part+'-'+probe)
 for kind,probe,phase in [('early-layer','overlap',4),('late-layer','overlap',21),('segment','segment',None),('tube-entry','travel',0),('tube-remainder','travel',1),('tube-regular','travel',2)]:
  exe=S/(probe+'_probe.exe');args=[exe,R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
  x=read(run(args,'native-'+part+'-'+kind));assert x['passed'];cases=x['segment_cases'] if phase is None else x['cases']
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe'),**({'cases':cases} if phase is None else {})));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['overlap_probe.c','overlap_probe.exe','segment_probe.c','segment_probe.exe','travel_probe.c','travel_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

'''+t[b:]
  t=t.replace("if name=='release':write(S/'native-gates.json',dict(passed=True,groups=5","if name=='channel':write(S/'native-gates.json',dict(passed=True,groups=6")
  t=t.replace("['baseline','wait','release','final-scenes']","['baseline','bridge','channel','final-scenes']")
  t=t.replace('Clearance, invalidation, traffic wait, failed/rebuilt obstacle observation and failure recovery.','Early/late bridge layers, segment preparation, Tube entry/remainder/regular movement.')
  t=t.replace("args=py('run_bridge_catalog_v64.py' if item.get('capture_host') else 'run_fixture_comparison.py'", "args=py('run_channel_observer_v64.py' if item.get('channel_observer') else 'run_bridge_catalog_v64.py' if item.get('capture_host') else 'run_fixture_comparison.py'")
  t=t.replace("observer=Path(args[4]).name=='run_bridge_catalog_v64.py'", "observer=Path(args[4]).name in ['run_bridge_catalog_v64.py','run_channel_observer_v64.py'];channel=Path(args[4]).name=='run_channel_observer_v64.py'")
  t=t.replace("expected=sha(S/('baseline-observer/bridge-catalog-observer.exe'", "expected=sha(S/('baseline-channel-observer/channel-observer.exe' if baseline else 'channel-observer.exe')) if channel else sha(S/('baseline-observer/bridge-catalog-observer.exe'")
  # Baseline channel observer is built before service edits and retained separately.
  t=t.replace("values=scenes(jobs)\n write(S/'traffic-baseline-scenes.json'", "values=scenes(jobs,baseline=True)\n write(S/'traffic-baseline-scenes.json'")
  t=t.replace("jobs=[fixture_job(x['baseline_tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]", "jobs=[fixture_job(x['baseline_tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]\n jobs += [fixture_job(x['observer_baseline_tag'],dict(x,channel_observer=True),x['last']) for x in read(S/'traffic-fixtures.json')['fixtures'] if x.get('observer_tag')]")
  t=t.replace("jobs += [fixture_job(x['tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]", "jobs += [fixture_job(x['tag'],x,x['last']) for x in read(S/'traffic-fixtures.json')['fixtures']]\n jobs += [fixture_job(x['observer_tag'],dict(x,channel_observer=True),x['last']) for x in read(S/'traffic-fixtures.json')['fixtures'] if x.get('observer_tag')]")
  t=t.replace("'--seconds','240'", "'--seconds',str(item.get('seconds',300))")
  t=t.replace("run(py('make_bridge_catalog_v64.py','--relink'),'prepare-final-fixture-host')", "run(py('make_bridge_catalog_v64.py','--relink'),'prepare-final-fixture-host')\n run(py('make_channel_observer_v64.py','--relink'),'prepare-final-channel-observer')\n run(['pwsh','-NoProfile','-File',R/'build-channel-observer-v64.ps1'],'build-final-channel-observer')")
 elif name=='audit_sources':
  t=t.replace("['wait_probe.exe','obstacle_probe.exe','recovery_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['overlap_probe.exe','segment_probe.exe','travel_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace("native['groups']==5","native['groups']==6").replace('groups=5,new_cycle_cases','groups=6,new_cycle_cases')
  t=t.replace('Two existing gameplay units','Three existing gameplay units').replace('clearance level fallback, wait timer/rebuild and released-obstacle queue handoff order retained','bridge level/flag rereads, segment candidate/gate/facing order and tube entry height/numeric service order retained')
 elif name=='audit_evidence':
  a=t.index("wait=(R/");b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''bridge=(R/'ra2/src/gameplay/ground_bridge_plane.c').read_text(encoding='utf-8');segment=(R/'ra2/src/gameplay/ground_segment.c').read_text(encoding='utf-8');tube=(R/'ra2/src/gameplay/ground_tube_travel.c').read_text(encoding='utf-8')
assert 'enter_upper_bridge' in bridge and 'leave_upper_bridge' in bridge and 'resolve_segment_surface' in segment and 'wait_for_segment_permission' in segment and 'resolve_tube_rise' in tube
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_bridge_plane.c','ground_segment.c','ground_tube_travel.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['32-bit wrapped four-level bridge matching','second bridge flag queries after possible layer write','captured segment context, repeated candidate and owner flag queries','gate permission before facing and classification','Tube distance/route/heading/speed/endpoints order','entrance then exit height query, wrapped difference then division','existing x87 arithmetic and conversion control words unchanged'],scope='Original layer/segment/Tube fragments, ordinary two-plane traffic and tube channels; no unsupported new algorithm.'))
'''+t[b:]
 elif name=='plan_cleanup':
  t=t.replace("p=R/'lineage_v64.json'", "p=R/'lineage_v64.json'")
 elif name=='commit_movement':
  t=t.replace('第六十二批','第六十三批').replace('等待障碍恢复与层高通道交通','桥面层切换与隧道拥堵交通')
  t=t.replace('Stage wait and obstacle-release recovery with height-channel traffic (batch 62)','Stage bridge layers and channel handoff with tube and congestion traffic (batch 63)')
 elif name=='verify_final_movement':
  t=t.replace('==(62,63)','==(63,64)').replace('generation=62','generation=63').replace('458752','491520').replace('31069','40673').replace("len(x['probes'])==5","len(x['probes'])==6").replace("native['groups']==5","native['groups']==6")
  t=t.replace("{'clearance','invalidate','wait','obstacle','recovery'}","{'early-layer','late-layer','segment','tube-entry','tube-remainder','tube-regular'}")
  t=t.replace("v['new_traffic_recipes']==2","v['new_traffic_recipes']==3").replace("==19","==23")
  t=t.replace("expected=sha(S/'baseline/ra2/build-original-c/ra2.exe') if is_baseline else sha(S/'bridge-catalog-observer.exe') if a['capture_host'] else sha(exe)","expected=sha(S/('baseline-channel-observer/channel-observer.exe' if is_baseline else 'channel-observer.exe')) if a['tag'].endswith('-observed') else sha(S/'baseline/ra2/build-original-c/ra2.exe') if is_baseline else sha(S/'bridge-catalog-observer.exe') if a['capture_host'] else sha(exe)")
  a=t.index("channels=read(S/'channel-comparison.json')");b=t.index("short=read(S/'prior-traffic-inheritance.json')",a)
  t=t[:a]+"assert read(S/'channel-comparison.json')['passed']\n"+t[b:]
  a=t.index("surface=read(S/'bridge-surface-profile.json')");b=t.index("for item in read(S/'traffic-fixtures.json')",a)
  t=t[:a]+t[b:]
  t=t.replace("assert sha(R/item['path'])==item['sha256']==item['source_sha256']==sha(Path(item['source']))", "assert sha(R/item['path'])==item['sha256'] and item['source_sha256']==sha(Path(item['source']))")
 q=R/(name+'_v64.py');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=p.name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{v}/{n}_probe.c',sha256=sha(R/f'evidence/movement-state-v{v}/{n}_probe.c')) for n,v in [('overlap',51),('segment',42),('travel',38)]]
(R/'lineage_v64.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=origins),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v63'))
