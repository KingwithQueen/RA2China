"""Finite per-vehicle mixed-channel and exit-queue recovery; preserve all raw comparisons."""
from run_batch_v65 import R,S,read,sha
import json
def longest(frames):
 best=run=0;previous=None
 for f in frames:
  run=run+1 if previous is not None and f==previous+1 else 1;best=max(best,run);previous=f
 return best
def analyze(tag):
 recipe=next(x for x in read(S/'traffic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag'],x['observer_tag'],x['observer_baseline_tag']])
 observed=tag in [recipe['observer_tag'],recipe['observer_baseline_tag']];baseline=tag.startswith('b-');folder=S/'runs'/tag;comparison=read(folder/'comparison.json')
 assert comparison['passed'] and comparison['cell_catalog_equal'] and comparison['comparison']['negative_control']['passed']
 modes={};frozen_hashes={}
 for mode in ['original','generated-c']:
  path=folder/mode/'state.jsonl';rs=[json.loads(l) for l in path.open(encoding='utf-8')]
  if not baseline:
   frozen=S/'runs'/recipe['observer_baseline_tag' if observed else 'baseline_tag']/mode/'state.jsonl';assert sha(path)==sha(frozen),(tag,mode,'Complete baseline changed');frozen_hashes[mode]=sha(frozen)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'};assert list(h)==list(range(recipe['last']+1))
  actors=recipe['actor_ids'];all_ids=recipe['slot_ids'];cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert all(all(u in frame and frame[u]['health']==200 for u in all_ids) for frame in h.values())
  goals={}
  for u in all_ids:
   last=h[recipe['last']][u];assert list(cell(last))==recipe['goals'][str(u)] and last['mission'][0] in [0,5],(tag,mode,u,'Goal/Guard',last['position'],last['mission'])
   goals[str(u)]=dict(final_cell=list(cell(last)),final_position=last['position'],final_mission=last['mission'])
  moves={f:[u for u in actors if h[f][u]['position']!=h[f-1][u]['position']] for f in range(1,recipe['last']+1)}
  assert sum(len(ids)>=2 for ids in moves.values())>=20
  paths={str(u):sum(bool(frame[u]['ground_drive']['path_directions']) for frame in h.values()) for u in actors};assert all(paths.values())
  expected=sorted(tuple(map(int,o.split(':'))) for o in recipe['orders']);submissions=sorted((r['frame'],r['id'],r['mission'],*r['cell']) for r in rs if r['kind']=='submit');assert expected==submissions
  executions=[r for r in rs if r['kind']=='execute']
  for f,u,m,x,y in expected:assert m==2 and any(r['event_frame']==f and r['id']==u and r['mission']==m and f<=r['frame']<=f+2 for r in executions),(tag,mode,f,u)
  audit=[r for r in rs if r['kind']=='movement-audit' and r['stage']==6 and r['id'] in actors];assert audit and any(r['value'] for r in audit)
  effect={};snapshots={}
  if observed:
   snapshots={u:{r['frame']:r for r in rs if r['kind']=='fixture-tube-snapshot' and r['id']==u} for u in actors}
   assert all(len(v)==recipe['last']+1 for v in snapshots.values())
  if recipe['kind']=='mixed':
   for u in actors:
    flags=[frame[u]['ground_drive']['owner_flags_74_79'][1] for frame in h.values()]
    before=[f for f in range(650) if flags[f]];after=[f for f in range(2600,recipe['last']+1) if flags[f]];assert before and after,(tag,mode,u,'Missing ordered bridge use')
    directions=[f for f in range(450,2600) if 8 in h[f][u]['ground_drive']['path_directions']];assert directions
    entry=dict(first_bridge_frame=before[0],return_bridge_frame=after[0],unit_layer_transitions=sum(a!=b for a,b in zip(flags,flags[1:])),direction8_frames=len(directions))
    if observed:
     data=snapshots[u];forward=[f for f,r in data.items() if r['route']==0 and r['steps']==10 and 0<r['waypoint']<10];reverse=[f for f,r in data.items() if r['route']==1 and r['steps']==10 and 0<r['waypoint']<10]
     assert forward and reverse and before[0]<min(forward)<min(reverse)<after[0],(tag,mode,u,'No ordered bridge/tube recovery',entry)
     entry.update(first_forward_tube=min(forward),first_reverse_tube=min(reverse),forward_waypoints=sorted({data[f]['waypoint'] for f in forward}),reverse_waypoints=sorted({data[f]['waypoint'] for f in reverse}))
    effect[str(u)]=entry
  else:
   arrivals={str(u):next(f for f in h if list(cell(h[f][u]))==recipe['goals'][str(u)]) for u in actors};effect=dict(actor_count=len(actors),oldest_request_id=recipe['oldest_id'],final_arrivals=arrivals,all_requests_recovered=True)
   if observed:
    waits={};exits={};waiting_by_frame={f:0 for f in h}
    for u in actors:
     data=snapshots[u];active=[f for f,r in data.items() if r['route']==0 and r['steps']==10 and 0<r['waypoint']<=10]
     if not active:
      waits[str(u)]=dict(request_frame=recipe['request_frames'][str(u)],route='ground_bypass',arrival_frame=arrivals[str(u)],request_to_arrival=arrivals[str(u)]-recipe['request_frames'][str(u)])
      continue
     first=active[0];exit_frame=next((f for f in range(first+1,recipe['last']+1) if data[f]['route']==255),None);assert exit_frame is not None,(tag,mode,u,'No observed exit')
     hold=[f for f in active if data[f]['waypoint']==10 and f>0 and h[f][u]['position']==h[f-1][u]['position']]
     for f in hold:waiting_by_frame[f]+=1
     waits[str(u)]=dict(request_frame=recipe['request_frames'][str(u)],first_active_tube=first,exit_publish_frame=exit_frame,terminal_stationary_frames=len(hold),longest_terminal_wait=longest(hold),arrival_frame=arrivals[str(u)],request_to_exit=exit_frame-recipe['request_frames'][str(u)])
     exits[str(u)]=exit_frame
    peak=max(waiting_by_frame.values());old=str(recipe['oldest_id']);assert len(exits)>=8 and peak>=8 and waits[old]['longest_terminal_wait']>=120,(tag,mode,'Insufficient larger queue/old request wait',peak,waits[old])
    effect.update(per_vehicle=waits,peak_terminal_waiters=peak,oldest_later_requests_exited_first=sum(exits[str(u)]<exits[old] and recipe['request_frames'][str(u)]>5 for u in actors if str(u) in exits),last_exit_publish_frame=max(exits.values()),maximum_request_to_exit=max(x['request_to_exit'] for x in waits.values() if 'request_to_exit' in x),actual_tube_actors=len(exits),ground_bypass_actors=len(actors)-len(exits),finite_recovery_verified=True,unbounded_starvation_freedom_proved=False)
  modes[mode]=dict(goals=goals,health_preserved=True,reconstructed_path_frames=paths,simultaneous_two_or_more_frames=sum(len(v)>=2 for v in moves.values()),existing_stage6_observations=len(audit),effects=effect)
 result=dict(passed=True,recipe=recipe['tag'],baseline=baseline,observer=observed,comparison_sha256=sha(folder/'comparison.json'),strict_trace_equal=True,per_mode_traces_equal_prechange=not baseline,baseline_traces=frozen_hashes,modes=modes,ordinary_move_events=True,no_memory_or_path_result_injection=True,scope=recipe['scope'])
 p=folder/'traffic-acceptance.json'
 if p.exists():assert read(p)==result
 else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 print(json.dumps(analyze(sys.argv[1]),ensure_ascii=False))
