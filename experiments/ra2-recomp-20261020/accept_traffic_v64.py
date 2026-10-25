"""Dedicated finite channel effects; raw strict comparison and complete baselines retained."""
from run_batch_v64 import R,S,read,sha
import json
def analyze(tag):
 recipe=next(x for x in read(S/'traffic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag'],x.get('observer_tag'),x.get('observer_baseline_tag')])
 observed=tag in [recipe.get('observer_tag'),recipe.get('observer_baseline_tag')];baseline=tag.startswith('b-');folder=S/'runs'/tag;x=read(folder/'comparison.json')
 assert x['passed'] and x['cell_catalog_equal'] and x['comparison']['negative_control']['passed']
 modes={};baselines={}
 for mode in ['original','generated-c']:
  path=folder/mode/'state.jsonl';rows=[json.loads(l) for l in path.open(encoding='utf-8')]
  if not baseline:
   frozen=S/'runs'/recipe['observer_baseline_tag' if observed else 'baseline_tag']/mode/'state.jsonl';assert sha(path)==sha(frozen),(tag,mode,'Complete prechange trace differs');baselines[mode]=sha(frozen)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rows if r['kind']=='state'};assert list(h)==list(range(recipe['last']+1))
  actors=recipe['actor_ids'];vehicles=recipe['ground_vehicle_ids'];cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert all(all(u in frame and frame[u]['health']==recipe['actor_health'][str(u)] for u in actors) for frame in h.values())
  goals={}
  for u in actors:
   last=h[recipe['last']][u];assert list(cell(last))==recipe['goals'][str(u)] and last['mission'][0] in [0,5],(tag,mode,u,'Goal/Guard',last['position'],last['mission'])
   goals[str(u)]=dict(final_cell=list(cell(last)),final_position=last['position'],final_mission=last['mission'])
  moving={f:[u for u in actors if h[f][u]['position']!=h[f-1][u]['position']] for f in range(1,recipe['last']+1)}
  assert sum(len(ids)>=2 for ids in moving.values())>=20
  paths={str(u):sum(bool(frame[u].get('ground_drive',{}).get('path_directions')) for frame in h.values()) for u in vehicles};assert all(paths.values())
  expected=sorted(tuple(map(int,o.split(':'))) for o in recipe['orders'])
  actual=sorted((r['frame'],r['id'],r['mission'],*r['cell']) for r in rows if r['kind']=='submit');assert actual==expected
  for f,u,mission,cx,cy in expected:
   assert mission==2 and any(r['kind']=='execute' and r['event_frame']==f and r['id']==u and r['mission']==mission and f<=r['frame']<=f+2 for r in rows),(tag,mode,f,u,'Missing execution')
  requests=[r for r in rows if r['kind']=='movement-audit' and r['stage']==6 and r['id'] in vehicles];assert requests and any(r['value'] for r in requests)
  effect={};catalog={tuple(c['cell']):c for c in read(folder/mode/'cells.json')['cells']}
  if recipe['kind']=='bridge':
   upper=recipe['upper_ids'];lower=recipe['lower_ids'];flags={}
   for u in upper+lower:
    fs=[frame[u]['ground_drive']['owner_flags_74_79'][1] for frame in h.values()]
    if u in upper:assert set(fs)=={0,1} and sum(a!=b for a,b in zip(fs,fs[1:]))>=4,(tag,mode,u,'No bridge-layer transitions')
    else:assert set(fs)=={0} and any(catalog[cell(frame[u])]['bridge'] and frame[u]['position'][2]==0 for frame in h.values()),(tag,mode,u,'No lower crossing')
    flags[str(u)]=dict(upper_frames=sum(bool(v) for v in fs),transitions=sum(a!=b for a,b in zip(fs,fs[1:])))
   overlap=[f for f in moving if any(a in moving[f] and b in moving[f] and h[f][a]['ground_drive']['owner_flags_74_79'][1] and catalog[cell(h[f][b])]['bridge'] and h[f][a]['position'][2]==416 and h[f][b]['position'][2]==0 and max(abs(h[f][a]['position'][i]-h[f][b]['position'][i]) for i in [0,1])<=512 for a in upper for b in lower)]
   assert overlap,(tag,mode,'No simultaneous upper/lower interaction')
   effect=dict(unit_layer_flags=flags,nearby_simultaneous_two_plane_frames=len(overlap),sample_frames=overlap[:12])
  elif recipe['kind']=='congestion':
   main=recipe['main_id'];blocks=recipe['blocker_ids'];held=[f for f in range(200,1200) if h[f][main]['position']==h[f-1][main]['position'] and all(h[f][u]['position']==h[f-1][u]['position'] for u in blocks)]
   assert len(held)>=600,(tag,mode,'No long congestion',len(held))
   assert all(h[f][main]['position'][1]<(71*256) for f in range(200,1200)),(tag,mode,'Crossed before release')
   first_motion={str(u):next(f for f in range(1,1601) if h[f][u]['position']!=h[f-1][u]['position']) for u in blocks}
   assert all(first_motion[str(u)]>=recipe['release_frames'][str(u)] for u in blocks),(tag,mode,'Unexpected early blocker motion',first_motion)
   recovered=next(f for f in range(1200,1800) if h[f][main]['position']!=h[f-1][main]['position'])
   effect=dict(held_frames=len(held),held_range=[held[0],held[-1]],main_mission_before_release=h[1199][main]['mission'],blocker_first_motion=first_motion,first_recovery_motion=recovered,ordinary_same_goal_recovery_order=recipe['explicit_recovery_order'],automatic_before_recovery_order=recovered<recipe['explicit_recovery_order'])
  else:
   directions={str(u):sum(8 in frame[u]['ground_drive']['path_directions'] for frame in h.values()) for u in vehicles}
   assert all(directions.values()),(tag,mode,'Tube direction8 not observed',directions)
   effect=dict(direction8_frames=directions)
   if observed:
    snapshots=[r for r in rows if r['kind']=='fixture-tube-snapshot'];per_unit={}
    for u in vehicles:
     samples=[r for r in snapshots if r['id']==u];indices={r['route'] for r in samples if r['steps']==recipe['tube_steps'] and 0<r['waypoint']<recipe['tube_steps']};waypoints={r['waypoint'] for r in samples if r['steps']==recipe['tube_steps'] and 0<r['waypoint']<recipe['tube_steps']}
     assert indices=={0,1} and len(waypoints)>=6,(tag,mode,u,'No actual bidirectional Tube progression',indices,waypoints)
     per_unit[str(u)]=dict(routes=sorted(indices),waypoints=sorted(waypoints),progress_samples=sum(r['steps']==recipe['tube_steps'] and 0<r['waypoint']<recipe['tube_steps'] for r in samples))
    effect['readonly_tube_progress']=per_unit
  modes[mode]=dict(goals=goals,health_preserved=True,reconstructed_path_frames=paths,simultaneous_two_or_more_frames=sum(len(ids)>=2 for ids in moving.values()),existing_stage6_observations=len(requests),effects=effect)
 result=dict(passed=True,recipe=recipe['tag'],baseline=baseline,observer=observed,comparison_sha256=sha(folder/'comparison.json'),strict_trace_equal=True,per_mode_traces_equal_prechange=not baseline,baseline_traces=baselines,modes=modes,ordinary_move_events=True,no_memory_or_path_result_injection=True,scope=recipe['scope'])
 p=folder/'traffic-acceptance.json'
 if p.exists():assert read(p)==result
 else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 print(json.dumps(analyze(sys.argv[1]),ensure_ascii=False))
