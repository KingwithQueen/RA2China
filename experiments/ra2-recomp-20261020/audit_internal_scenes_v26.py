from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');helper=sha(S/'connection-fixture-probe.exe');scenes={};stages=Counter()
for name,plain,frames in [('default','c-final-default',901),('long','u-long',1501),('tc1','u-tc1',401),('repeat-failure','u-repeat-failure',1251)]:
 tag='i-'+('fail' if name=='repeat-failure' else name);x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];p=read(S/'runs'/plain/'comparison.json')
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
assert all(stages[i]>0 for i in range(10,16)),stages
assert any(h['stage']==11 and h['sample']>0 for scene in scenes.values() for h in scene['modes']['original']['hits'])
value=dict(passed=True,production_executable_sha256=production,observer_executable_sha256=helper,independent_scenes=4,independent_frames=4054,stages=dict(stages),scenes=scenes,
 scope='Read-only native hooks at 4A17A2/4A1725/4A17D5, 4A3486, 70323E and 4A263A matched to C service boundaries. Natural current/previous sample selection, transformed coordinates, prepare entry, object entry and shared return; no raw state/path/budget injection. Ordinary default and three fixed-map movement/turn/recovery scenes. Not complete coverage of every overlapping entry.',all_rare_branches_verified=False,previous_sample_real_scene_verified=True,
 sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [R/'make_connection_fixture_v26.py',S/'connection_observer.c',S/'connection_advance_bridge.c',S/'connection_joint_bridge.c',R/'run_internal_scenes_v26.py',R/'audit_internal_scenes_v26.py']])
for scene in scenes.values():
 for mode in scene['modes'].values():
  full=mode.pop('hits');mode['ordered_hits_sha256']=hashlib.sha256(json.dumps(full,separators=(',',':')).encode('utf-8')).hexdigest()
  mode['sample_hits']=[next(h for h in full if h['stage']==stage) for stage in sorted({h['stage'] for h in full})]+full[-3:]
(S/'internal-real-scenes.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=True,scenes=4,frames=4054,stages=dict(stages))))
