"""Direct original/C branch hits plus uninstrumented production parity; no inferred hit counts."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v22'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');helper=sha(S/'connection-fixture-probe.exe');scenes={}
for direction,index,entrance,exit,goal in [('east',0,[68,114],[78,114],[80,114]),('west',1,[78,114],[68,114],[66,114])]:
 tags=['w-tube-hook-'+direction,'z-tube-production-'+direction]
 for tag in tags:
  x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
  assert x['passed'] and x['exe_sha256']==(helper if tag.startswith('w-') else production)
  assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==501
  assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
  assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
  assert all(r['exit_code']==0 and r['passed'] and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
  assert ordered(rows(tag,'original'))==ordered(rows(tag,'generated-c'))
 x=read(S/'runs'/tags[0]/'comparison.json');modes={}
 for mode in ['original','generated-c']:
  diagnostic=rows(tags[0],mode);plain=rows(tags[1],mode)
  assert [r for r in diagnostic if r['kind']=='state']==[r for r in plain if r['kind']=='state']
  assert [r for r in ordered(diagnostic) if r['kind']!='fixture-connection-hit']==ordered(plain)
  hits=[r for r in diagnostic if r['kind']=='fixture-connection-hit']
  assert len(hits)==2 and [r['stage'] for r in hits]==[0,1]
  assert hits[0]['frame']==hits[1]['frame'] and all(r['id']==1022581 for r in hits)
  assert all(r['connection']==index and r['tube_count']==2 and r['entrance']==entrance and r['exit']==exit and r['duration']==10 for r in hits)
  assert all(r['segment']==[exit[0]*256+128,exit[1]*256+128,0] and r['flags']==[index,0] and r['selector']==-1 for r in hits)
  assert [r['driving'] for r in hits]==[0,1] and hits[1]['landing_height']==416
  states=[r for r in plain if r['kind']=='state'];last=next(o for o in states[-1]['objects'] if o['id']==1022581)
  assert last['position']==[goal[0]*256+128,goal[1]*256+128,416]
  assert last['ground_drive']['destination']==[0,0,0]
  assert any(8 in o['ground_drive']['path_directions'] for r in states for o in r['objects'] if o['id']==1022581)
  modes[mode]=dict(hits=hits,final_position=last['position'],plain_state_identity=True)
 scenes[direction]=dict(passed=True,frames=501,fixture_sha256=sha(S/'fixtures'/('tube-'+direction+'.MAP')),modes=modes)
args=read(S/'connection-fixture-build-arguments.json')
objects=[Path(p) if Path(p).is_absolute() else R/'ra2/build-original-c'/p for p in args['link'] if p.endswith('.obj')]
assert len(objects)==152 and sum(p.name.startswith('connection_') for p in objects)==2
sources=[R/'make_connection_fixture_v22.py',R/'build-connection-fixture-v22.ps1',R/'run_connection_v22.py',S/'connection_observer.c',S/'connection_movement_fixture.c',S/'connection_remainder_bridge.c',R/'run_fixture_comparison.py',R/'ra2/src/runtime/state_trace.c']
value=dict(passed=True,production_executable_sha256=production,observer_executable_sha256=helper,
 scope='Legal map TubeClass connections in both directions. Ordinary move order only; direct hits at native 4A1470/4A1564 and matching C service points. Test-only two-object observer; production traces match observer traces after excluding observer records.',
 production_scenes=2,production_frames=1002,independent_observer_scenes=2,independent_observer_frames=1002,
 direct_runtime_hit_records_per_mode=4,scenes=scenes,objects=[dict(path=str(p),sha256=sha(p)) for p in objects],
 sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],
 original_resources_unchanged=True,raw_movement_state_writes=False,production_recorder_comparator_unchanged=True,
 alternate_saved_segment_pointer_real_scene_verified=False,all_rare_branches_verified=False)
(S/'connection-real-scenes.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,production_frames=1002,observer_frames=1002,hit_frames={k:v['modes']['original']['hits'][0]['frame'] for k,v in scenes.items()})))
