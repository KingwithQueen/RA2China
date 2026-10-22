"""Direct original/C branch hits plus uninstrumented production parity; no inferred hit counts."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');helper=sha(S/'connection-fixture-probe.exe');scenes={}
for direction,index,entrance,exit,goal in [('east',0,[68,114],[78,114],[80,114]),('west',1,[78,114],[68,114],[66,114]),('blocked',0,[68,114],[78,114],None)]:
 tags=['w2-tube-hook-'+direction,'c-final-tube-'+direction]
 for tag in tags:
  x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
  assert x['passed'] and x['exe_sha256']==(helper if tag.startswith('w2-') else production)
  assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==501
  assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
  assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
  assert all(r['exit_code']==0 and r['passed'] and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
  assert ordered(rows(tag,'original'))==ordered(rows(tag,'generated-c'))
 x=read(S/'runs'/tags[0]/'comparison.json');modes={}
 for mode in ['original','generated-c']:
  diagnostic=rows(tags[0],mode);plain=rows(tags[1],mode)
  assert [r for r in diagnostic if r['kind']=='state']==[r for r in plain if r['kind']=='state']
  assert [r for r in ordered(diagnostic) if r['kind'] not in ['fixture-connection-hit','fixture-internal-hit']]==ordered(plain)
  all_hits=[r for r in diagnostic if r['kind']=='fixture-connection-hit']
  progress_hits=[h for h in all_hits if h['stage']>=4]
  assert all(any(h['stage']==stage for h in progress_hits) for stage in [4,5,6,7,8,9])
  hits=[h for h in all_hits if h['stage']<4]
  assert len(hits)>=3 and [r['stage'] for r in hits[:2]]==[0,1]
  assert hits[0]['frame']==hits[1]['frame'] and all(r['id']==1022581 for r in hits)
  assert all(r['connection']==index and r['tube_count']==2 and r['entrance']==entrance and r['exit']==exit and r['duration']==10 for r in hits)
  assert all(r['segment']==[exit[0]*256+128,exit[1]*256+128,0] and r['flags']==[index,0] and r['selector']==-1 for r in hits[:2])
  assert [r['driving'] for r in hits[:2]]==[0,1] and hits[1]['landing_height']==416
  if direction!='blocked':
   assert len(hits)==3 and hits[2]['stage']==2 and hits[2]['frame']>hits[1]['frame']
  else:
   occupied=[h for h in hits if h['stage']==3];assert [h['frame'] for h in occupied]==list(range(211,256))
   assert [h['frame'] for h in hits if h['stage']==2]==[256]
   assert all(h['stage'] in [2,3] for h in hits[2:])
   assert len({tuple(h['position']) for h in occupied})==1
   units=[r for r in plain if r['kind']=='fixture-unit'];constraints=[r for r in plain if r['kind']=='fixture-constraints']
   assert len(units)==16 and all(r['frame']==170 for r in units) and [78,114] in [r['cell'] for r in units]
   assert len(constraints)==1 and constraints[0]['explicit_rebuild_result']==4294967295
  states=[r for r in plain if r['kind']=='state'];last=next(o for o in states[-1]['objects'] if o['id']==1022581)
  if direction=='blocked':
   samples={r['frame']:next(o for o in r['objects'] if o['id']==1022581) for r in states}
   assert all(samples[f]['position']==[20096,29312,416] and samples[f]['ground_drive']['unit_speed_bits']=='0000000000000000' for f in range(212,257))
   assert samples[257]['ground_drive']['unit_speed_bits']=='000000000000f03f'
   assert last['position']==[20608,29312,416] and last['ground_drive']['destination']==[0,0,0]
  if goal:
   assert last['position']==[goal[0]*256+128,goal[1]*256+128,416]
   assert last['ground_drive']['destination']==[0,0,0]
  assert any(8 in o['ground_drive']['path_directions'] for r in states for o in r['objects'] if o['id']==1022581)
  modes[mode]=dict(hits=hits,progress_hits=progress_hits,final_position=last['position'],plain_state_identity=True)
 scenes[direction]=dict(passed=True,frames=501,fixture_sha256=sha(S/'fixtures'/('tube-'+('east' if direction=='blocked' else direction)+'.MAP')),modes=modes)
for name,direction,index,goal,target_height in [('uphill','east',0,80,624),('downhill','west',1,66,416)]:
 tags=['w2-tube-hook-'+name,'z-tube-production-'+name]
 for tag in tags:
  x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
  assert x['passed'] and x['exe_sha256']==(helper if tag.startswith('w2-') else production)
  assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==501
  assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
  assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
  assert all(r['exit_code']==0 and r['passed'] and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
  assert ordered(rows(tag,'original'))==ordered(rows(tag,'generated-c'))
 modes={}
 for mode in ['original','generated-c']:
  diagnostic=rows(tags[0],mode);plain=rows(tags[1],mode)
  assert [r for r in diagnostic if r['kind']=='state']==[r for r in plain if r['kind']=='state']
  assert [r for r in ordered(diagnostic) if r['kind'] not in ['fixture-connection-hit','fixture-internal-hit']]==ordered(plain)
  hits=[r for r in diagnostic if r['kind']=='fixture-connection-hit'];progress_hits=[r for r in hits if r['stage']>=4]
  assert all(any(h['stage']==stage for h in hits) for stage in [0,1,2,4,5,6,7,8,9])
  assert all(h['connection']==index and h['id']==1022581 for h in hits)
  landing=next(h for h in hits if h['stage']==1)
  assert landing['landing_height']==(436 if name=='uphill' else 604)
  heights=[h['position'][2] for h in progress_hits];assert max(heights)-min(heights)>=100
  last=next(o for r in reversed(plain) if r['kind']=='state' for o in r['objects'] if o['id']==1022581)
  assert last['position']==[goal*256+128,29312,target_height] and last['ground_drive']['destination']==[0,0,0]
  modes[mode]=dict(hits=[h for h in hits if h['stage']<4],progress_hits=progress_hits,final_position=last['position'],plain_state_identity=True,nonzero_height_range=[min(heights),max(heights)],initial_landing_height=landing['landing_height'])
 scenes[name]=dict(passed=True,frames=501,fixture_sha256=sha(S/'fixtures'/('tube-elevated-'+direction+'.MAP')),modes=modes)
for direction,index,goal in [('east',0,80),('west',1,66)]:
 tags=['w2-tube-hook-curved-'+direction,('z-ce' if direction=='east' else 'z-cw')];modes={}
 for tag in tags:
  x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];assert x['passed'] and x['exe_sha256']==(helper if tag.startswith('w2-') else production)
  assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==601 and c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
  assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
  assert ordered(rows(tag,'original'))==ordered(rows(tag,'generated-c'))
 for mode in ['original','generated-c']:
  observed=rows(tags[0],mode);plain=rows(tags[1],mode)
  assert [r for r in observed if r['kind']=='state']==[r for r in plain if r['kind']=='state']
  assert [r for r in ordered(observed) if r['kind'] not in ['fixture-connection-hit','fixture-internal-hit']]==ordered(plain)
  hits=[r for r in observed if r['kind']=='fixture-connection-hit'];progress=[r for r in hits if r['stage']>=4]
  assert all(any(h['stage']==stage for h in hits) for stage in [0,1,2,4,5,6,7,8,9])
  assert all(h['connection']==index for h in hits)
  assert any(h['position'][1]!=29312 for h in progress)
  assert len({h['flags'][1] for h in progress})>=8
  exits=[h for h in hits if h['stage']==2];assert len(exits)==1 and 211<exits[0]['frame']<550
  last=next(o for r in reversed(plain) if r['kind']=='state' for o in r['objects'] if o['id']==1022581)
  assert last['position']==[goal*256+128,29312,416] and last['ground_drive']['destination']==[0,0,0]
  modes[mode]=dict(hits=[h for h in hits if h['stage']<4],progress_hits=progress,exit_frame=exits[0]['frame'],final_position=last['position'],plain_state_identity=True,y_range=[min(h['position'][1] for h in progress),max(h['position'][1] for h in progress)])
 scenes['curved-'+direction]=dict(passed=True,frames=601,fixture_sha256=sha(S/'fixtures'/('tube-curved-'+direction+'.MAP')),modes=modes)
args=read(S/'connection-fixture-build-arguments.json')
objects=[Path(p) if Path(p).is_absolute() else R/'ra2/build-original-c'/p for p in args['link'] if p.endswith('.obj')]
assert len(objects)==168 and sum(p.name.startswith('connection_') for p in objects)==9
sources=[R/'make_connection_fixture_v26.py',R/'build-connection-fixture-v26.ps1',R/'run_connection_v26.py',R/'run_tube_scenes_v26.py',S/'connection_observer.c',S/'connection_movement_fixture.c',S/'connection_remainder_bridge.c',S/'connection_tube_state_bridge.c',S/'connection_progress_bridge.c',S/'connection_travel_bridge.c',S/'connection_advance_bridge.c',S/'connection_joint_bridge.c',S/'connection_entry_bridge.c',S/'connection_prepare_bridge.c',R/'run_fixture_comparison.py',R/'ra2/src/runtime/state_trace.c']
value=dict(passed=True,production_executable_sha256=production,observer_executable_sha256=helper,
 scope='Legal bidirectional map TubeClass connections with ordinary move orders, including ascent/descent between map height levels4/6; third scene places 16 real blockers through normal services at frame170 with radius2, without explicit rebuilding or raw state writes. Direct native 4A1470/4A1564/6FAFE1/6FAEB4/6FABAA/6FAD1C/6FAE1D/6FAA66/6FAC70/6FAD75 hits versus matching C service points. Test-only nine-object observer; complete production states and existing ordered events equal observer traces after excluding new observer records.',
 production_scenes=7,production_frames=3707,independent_observer_scenes=7,independent_observer_frames=3707,
 tube_approach_runtime_verified=True,tube_height_runtime_verified=True,curved_bidirectional_runtime_verified=True,tube_entry_runtime_verified=True,tube_horizontal_runtime_verified=True,nonzero_height_bidirectional_runtime_verified=True,normal_exit_runtime_verified=True,occupied_exit_runtime_verified=True,
 direct_runtime_hit_records_per_mode=sum(len(v['modes']['original']['hits'])+len(v['modes']['original']['progress_hits']) for v in scenes.values()),scenes=scenes,objects=[dict(path=str(p),sha256=sha(p)) for p in objects],
 sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],
 original_resources_unchanged=True,raw_movement_state_writes=False,production_recorder_comparator_unchanged=True,
 alternate_saved_segment_pointer_real_scene_verified=False,all_rare_branches_verified=False)
(S/'connection-real-scenes.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,production_frames=3707,observer_frames=3707,hit_stages={k:[(h['frame'],h['stage']) for h in v['modes']['original']['hits'][:5]] for k,v in scenes.items()})))
