from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v27'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');helper=sha(S/'connection-fixture-probe.exe');scenes={};stages=Counter()
caller_identity=read(S/'overlap-caller-identity.json');assert caller_identity['passed'];routes=caller_identity['routes']
for name,plain,frames in [('default','c-final-default',901),('long','u-long',1501),('tc1','u-tc1',401),('repeat-failure','u-repeat-failure',1251)]:
 tag='j-'+('fail' if name=='repeat-failure' else name);x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];p=read(S/'runs'/plain/'comparison.json')
 assert x['passed'] and x['exe_sha256']==helper and p['passed'] and p['exe_sha256']==production
 assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==frames and c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
 assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
 original=rows(tag,'original');generated=rows(tag,'generated-c');assert ordered(original)==ordered(generated),tag
 modes={}
 for mode,observed in [('original',original),('generated-c',generated)]:
  plain_rows=rows(plain,mode);assert [r for r in observed if r['kind']=='state']==[r for r in plain_rows if r['kind']=='state']
  assert [r for r in ordered(observed) if r['kind'] not in ['fixture-connection-hit','fixture-internal-hit']]==ordered(plain_rows)
  hits=[r for r in observed if r['kind']=='fixture-internal-hit'];assert hits
  modes[mode]=dict(count=len(hits),stages=dict(Counter(h['stage'] for h in hits)),hits=hits,plain_state_identity=True)
 stages.update(h['stage'] for h in modes['original']['hits'])
 scenes[name]=dict(passed=True,frames=frames,production_scene=plain,modes=modes)
assert all(stages[i]>0 for i in range(10,20)),stages
assert any(h['stage']==11 and h['sample']>0 for scene in scenes.values() for h in scene['modes']['original']['hits'])
value=dict(passed=True,production_executable_sha256=production,observer_executable_sha256=helper,independent_scenes=4,independent_frames=4054,stages=dict(stages),scenes=scenes,
 scope='Read-only native hooks at ten boundaries, adding 4A17FE, 4A3502, 703439 and 7038EF. Natural current/previous samples, type gates, entry, object-chain initialization/continuation and shared return; no raw state/path/budget injection. Generated entry-route inventory distinguishes actual adapter use from matching high-level service observations; it is not complete coverage of every overlapping function.',all_rare_branches_verified=False,previous_sample_real_scene_verified=True,
 generated_entry_routes=routes,new_adapter_runtime_stages=sorted({r['stage'] for r in routes}),
 nonprimary_overlapping_adapter_naturally_observed=caller_identity['nonprimary_overlapping_adapter_naturally_observed'],
 sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [R/'make_connection_fixture_v27.py',R/'extend_overlap_observer_v27.py',S/'connection_observer.c',S/'connection_advance_bridge.c',S/'connection_joint_bridge.c',S/'connection_overlap_bridge.c',R/'run_internal_scenes_v27.py',R/'audit_internal_scenes_v27.py']])
assert {18,19}.issubset({r['stage'] for r in routes}),routes
for scene in scenes.values():
 for mode in scene['modes'].values():
  full=mode.pop('hits');mode['ordered_hits_sha256']=hashlib.sha256(json.dumps(full,separators=(',',':')).encode('utf-8')).hexdigest()
  mode['sample_hits']=[next(h for h in full if h['stage']==stage) for stage in sorted({h['stage'] for h in full})]+full[-3:]
(S/'internal-real-scenes.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=True,scenes=4,frames=4054,stages=dict(stages))))
