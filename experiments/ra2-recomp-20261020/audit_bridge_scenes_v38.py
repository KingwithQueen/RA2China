"""Require real layer chains, actual ordered visits and observer/production identity."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
recipes=read(S/'bridge-fixtures.json')['fixtures']
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe')
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
scenes={};complete=Counter();probes=[]
for item in recipes:
 name=item['name'];plain='b-'+name;tag='h3-'+name
 reports=[read(S/'runs'/t/'comparison.json') for t in [plain,tag]]
 for report,digest in zip(reports,[production,observer]):
  c=report['comparison'];assert report['passed'] and report['exe_sha256']==digest
  assert all(r['passed'] and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256']=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b' for r in report['runs'])
  assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
  assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
  assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
 original=rows(tag,'original');generated=rows(tag,'generated-c');assert ordered(original)==ordered(generated)
 modes={}
 for mode,observed in [('original',original),('generated-c',generated)]:
  base=rows(plain,mode)
  states=[r for r in observed if r['kind']=='state'];assert states==[r for r in base if r['kind']=='state']
  assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(base)
  actor=[next(o for o in r['objects'] if o['id']==item['id']) for r in states]
  assert len({tuple(o['position']) for o in actor})>1
  first=states[0]['objects'];lower={o['id'] for o in first if o['id'] in range(1023363,1023366)};upper={o['id'] for o in first if o['id'] in range(1023366,1023369)}
  assert len(lower)==len(upper)==3
  assert all(o['position'][2]==(416 if o['id'] in upper else 0) for o in first if o['id'] in lower|upper)
  hits=[r for r in observed if r['kind']=='fixture-internal-hit' and r['id']==item['id']]
  groups=[];current=None
  for hit in hits:
   stage=hit['stage']
   if stage==18:
    if current:groups.append(current)
    current=dict(frame=hit['frame'],upper=bool(hit['value'][0]),head=hit['value'][1],visits=[])
   elif current and stage==23:current['lengths']=hit['value']
   elif current and stage==22:current['visits'].append(hit['value'])
  if current:groups.append(current)
  full=[];additional=[]
  for group in groups:
   ids=upper if group['upper'] else lower
   visits=group['visits'];visited=[v[0] for v in visits]
   if group['head'] not in ids or set(visited)!=ids or len(visits)!=3:continue
   assert visited[0]==group['head'] and [v[1] for v in visits]==visited[1:]+[0]
   if group['lengths']!=[3,3]:additional.append(group);continue
   assert set(visited).isdisjoint(lower if group['upper'] else upper)
   full.append(group)
  assert full,name
  modes[mode]=dict(ordered_hits_sha256=hashlib.sha256(json.dumps(hits,separators=(',',':')).encode()).hexdigest(),
   full_chains=len(full),additional_noncooccupied_chains=additional,upper_full_chains=sum(g['upper'] for g in full),lower_full_chains=sum(not g['upper'] for g in full),
   sample_full_chains=full[:3],upper_drive_frames=sum(bool(o['ground_drive']['owner_flags_74_79'][1]) for o in actor),
   other_layer_positions_unchanged=all(next(o for o in state['objects'] if o['id']==uid)['position']==next(o for o in first if o['id']==uid)['position'] for state in states for uid in (upper if name.startswith('lower-') else lower)),final_position=actor[-1]['position'],final_destination=actor[-1]['ground_drive']['destination'],reached_goal=(actor[-1]['position']==[item['goal'][0]*256+128,item['goal'][1]*256+128,0 if name.startswith('lower-') else 416] and actor[-1]['ground_drive']['destination']==[0,0,0]))
  if name.startswith('lower-'):assert modes[mode]['lower_full_chains']>0 and modes[mode]['upper_drive_frames']==0
  else:assert modes[mode]['upper_full_chains']>0 and modes[mode]['upper_drive_frames']>0 and modes[mode]['reached_goal']
  if mode=='original':complete.update('upper' if g['upper'] else 'lower' for g in full)
 text=(S/'runs'/tag/'generated-c/run.log').read_text(encoding='utf-8',errors='replace')
 command=read(S/'runs'/tag/'generated-c/command.json')
 counters={f'{int(command[i+1],0):08X}':0 for i,value in enumerate(command) if value=='--probe'}
 for address in re.findall(r'^\[probe\] sub_([0-9A-F]{8}) from ',text,re.M):
  assert address in counters;counters[address]+=1
 assert len(counters) in [7,8] and counters['00703040']>0,counters
 aliases={k:v for k,v in counters.items() if k not in ['004A1000','004A2670','00703040']}
 assert aliases and all(v==0 for v in aliases.values()),aliases
 probes.append(dict(scene=tag,first_call_record_counts=counters,primary_record_limit=5))
 scenes[name]=dict(passed=True,frames=901,modes=modes)
assert complete['upper']>0 and complete['lower']>0,complete
assert set(k for p in probes for k in p['first_call_record_counts'])=={'004A1000','004A2670','00703040','004A12F1','004A134F','004A161D','004A166A','004A17A2','004A32B4','0070346B','0070372C','007038EF'}
inputs=[R/'make_bridge_scenes_v38.py',R/'run_bridge_scenes_v38.py',R/'extend_observer_v38_chain.py',R/'run_connection_v38.py',R/'ra2/src/runtime/host.c',Path(__file__)]+[R/e['path'] for e in recipes]
value=dict(passed=True,production_scenes=4,production_frames=3604,independent_scenes=4,independent_frames=3604,
 production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,full_chains=dict(complete),
 completed_crossings=sum(s['modes']['original']['reached_goal'] for s in scenes.values()),actual_ordered_three_object_traversal_verified=True,other_layer_excluded=True,private_saves=True,
 resolver_probes=probes,nonprimary_natural_entry_proved=False,
 scope='Legal original bridge overlays and map-object placement; both layers contain three infantry. Ordinary moves naturally select and traverse real chains. Native 703473 observer records each actual nonowner visit. The existing host logs each target first five indirect resolutions. Configured nine aliases produce no first-call record; primary entries are positive controls. Complete counters are unavailable because fixed-frame completion uses ExitProcess. No absence claim outside these runs.',
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
(S/'bridge-real-scenes.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,production_frames=3604,full_chains=dict(complete),nonprimary_natural_entry_proved=False)))
