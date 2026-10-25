"""Per-request sustained-arrival metrics; strict raw comparisons and immutable pre-change traces."""
from run_batch_v67 import R,S,read,sha
import json

def records(path):
 with path.open(encoding='utf-8') as f:
  for line in f:yield json.loads(line)

def longest(frames):
 best=run=0;previous=None
 for f in frames:
  run=run+1 if previous is not None and f==previous+1 else 1;best=max(best,run);previous=f
 return best

def compact(path,ids):
 h={};snapshots={u:{} for u in ids};submissions=[];executions=[];audit=0
 for r in records(path):
  kind=r['kind']
  if kind=='state':
   frame={}
   for o in r['objects']:
    if o['id'] not in ids:continue
    g=o['ground_drive'];frame[o['id']]=dict(position=tuple(o['position']),health=o['health'],mission=o['mission'],bridge=g['owner_flags_74_79'][1],has_path=bool(g['path_directions']))
   h[r['frame']]=frame
  elif kind=='fixture-tube-snapshot' and r['id'] in ids:
   snapshots[r['id']][r['frame']]={k:r[k] for k in ['route','waypoint','steps','entrance','exit']}
  elif kind=='submit':submissions.append((r['frame'],r['id'],r['mission'],*r['cell']))
  elif kind=='execute':executions.append((r['event_frame'],r['frame'],r['id'],r['mission']))
  elif kind=='movement-audit' and r['stage']==6 and r['id'] in ids and r['value']:audit+=1
 return h,snapshots,submissions,executions,audit

def analyze(tag):
 recipe=next(x for x in read(S/'traffic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag'],x['observer_tag'],x['observer_baseline_tag']]);observed=tag in [recipe['observer_tag'],recipe['observer_baseline_tag']];baseline=tag.startswith('b-');folder=S/'runs'/tag;comparison=read(folder/'comparison.json')
 assert comparison['passed'] and comparison['cell_catalog_equal'] and comparison['comparison']['negative_control']['passed']
 modes={};frozen={};actors=recipe['actor_ids'];all_ids=recipe['slot_ids'];last=recipe['last']
 for mode in ['original','generated-c']:
  path=folder/mode/'state.jsonl'
  if not baseline:
   before=S/'runs'/recipe['observer_baseline_tag' if observed else 'baseline_tag']/mode/'state.jsonl';assert sha(path)==sha(before),(tag,mode,'Complete baseline changed');frozen[mode]=sha(before)
  h,snap,submissions,executions,audit=compact(path,set(all_ids));assert list(h)==list(range(last+1));cell=lambda o:tuple(v//256 for v in o['position'][:2]);goals={};arrivals={};paths={}
  assert all(all(u in frame and frame[u]['health']==200 for u in all_ids) for frame in h.values())
  for u in all_ids:
   o=h[last][u];target=tuple(recipe['goals'][str(u)]);assert cell(o)==target and o['mission'][0] in [0,5],(tag,mode,u,'Goal/Guard',o,target)
   goals[str(u)]=dict(final_cell=list(cell(o)),final_mission=o['mission'])
   if u in actors:
    request=recipe['request_frames'][str(u)];arrivals[u]=next(f for f in range(request,last+1) if cell(h[f][u])==target);paths[str(u)]=sum(frame[u]['has_path'] for frame in h.values());assert paths[str(u)]
  expected=sorted(tuple(map(int,o.split(':'))) for o in recipe['orders']);assert sorted(submissions)==expected
  for f,u,m,x,y in expected:assert m==2 and any(ef==f and v==u and mission==m and f<=actual<=f+2 for ef,actual,v,mission in executions),(tag,mode,f,u)
  assert audit;effect=dict(actor_count=len(actors),oldest_request_id=recipe['oldest_id'],all_requests_recovered=True,last_goal_arrival=max(arrivals.values()),arrivals={str(u):f for u,f in arrivals.items()},ordinary_request_reissues=False)
  if observed:
   assert all(len(snap[u])==last+1 for u in actors);waits={};exits={};route_stats={};inflight={str(route):set() for route in recipe['min_actual']}
   for u in actors:
    request=recipe['request_frames'][str(u)];route=recipe['route_for_id'][str(u)];data=snap[u];active=[f for f,r in data.items() if f>=request and r['route']==route and r['steps']==10 and 0<r['waypoint']<=10]
    entry=dict(request_frame=request,arrival_frame=arrivals[u],request_to_arrival=arrivals[u]-request,requested_route=route)
    if not active:entry['route']='ground_bypass';waits[str(u)]=entry;continue
    first=active[0];exit_frame=next((f for f in range(first+1,last+1) if data[f]['route']==255),None);assert exit_frame is not None
    hold=[f for f in active if data[f]['waypoint']==10 and f>0 and h[f][u]['position']==h[f-1][u]['position']]
    inflight[str(route)].update(f for f in active if data[f]['waypoint']<10)
    bridge=[f for f in h if h[f][u]['bridge'] and cell(h[f][u])[0] in [60,61] and 63<=cell(h[f][u])[1]<=70]
    if recipe['kind']=='mixed' and route==0:assert bridge and min(bridge)<first,(tag,mode,u,'No bridge before forward Tube')
    entry.update(route='tube',first_active_tube=first,exit_publish_frame=exit_frame,terminal_stationary_frames=len(hold),longest_terminal_wait=longest(hold),terminal_wait_frames=hold,request_to_exit=exit_frame-request,first_bridge_frame=min(bridge) if bridge else None);waits[str(u)]=entry;exits[u]=exit_frame
   for key,minimum in recipe['min_actual'].items():
    route=int(key);ids=[u for u in actors if recipe['route_for_id'][str(u)]==route];actual=[u for u in ids if u in exits];assert len(actual)>=minimum,(tag,mode,route,'Insufficient actual Tube use',actual)
    by_frame={f:0 for f in h}
    for u in actual:
     waits[str(u)]['later_requests_exited_first']=sum(recipe['request_frames'][str(v)]>recipe['request_frames'][str(u)] and exits[v]<exits[u] for v in actual)
     for f in waits[str(u)]['terminal_wait_frames']:by_frame[f]+=1
    old=min(ids,key=lambda u:recipe['request_frames'][str(u)]);end=max(recipe['request_frames'][str(u)] for u in ids);start=min(recipe['request_frames'][str(u)] for u in ids)
    route_stats[key]=dict(requests=len(ids),actual_tube_actors=len(actual),ground_bypass_actors=len(ids)-len(actual),arrival_window=[start,end],oldest_id=old,oldest_observed=waits[str(old)],peak_terminal_waiters=max(by_frame.values()),exits_during_arrivals=sum(start<=exits[u]<=end for u in actual),maximum_request_to_exit=max(waits[str(u)]['request_to_exit'] for u in actual),maximum_terminal_wait=max(waits[str(u)]['longest_terminal_wait'] for u in actual),throughput_500_frame_windows=[dict(first=f,last=min(f+499,last),tube_exits=sum(f<=exits[u]<=min(f+499,last) for u in actual)) for f in range(0,last+1,500)])
   if recipe['kind']=='reverse':
    old=waits[str(recipe['oldest_id'])];assert old['route']=='tube' and old['longest_terminal_wait']>=600 and route_stats['1']['peak_terminal_waiters']>=4
   else:
    overlap=sorted(inflight['0']&inflight['1']);assert len(overlap)>=20,(tag,mode,'No simultaneous opposite Tube travel',len(overlap));effect.update(opposing_inflight_frames=len(overlap),first_opposing_inflight_frame=overlap[0],last_opposing_inflight_frame=overlap[-1])
   # Large raw frame lists are reduced after the exact metrics have been computed.
   for entry in waits.values():entry.pop('terminal_wait_frames',None)
   effect.update(per_vehicle=waits,by_direction=route_stats,actual_tube_actors=len(exits),ground_bypass_actors=len(actors)-len(exits),fifo_guarantee=False,unbounded_starvation_freedom_proved=False)
  modes[mode]=dict(goals=goals,health_preserved=True,reconstructed_path_frames=paths,effects=effect)
 result=dict(passed=True,recipe=recipe['tag'],baseline=baseline,observer=observed,comparison_sha256=sha(folder/'comparison.json'),strict_trace_equal=True,per_mode_traces_equal_prechange=not baseline,baseline_traces=frozen,modes=modes,ordinary_move_events=True,no_memory_or_path_result_injection=True,scope=recipe['scope']);p=folder/'traffic-acceptance.json'
 if p.exists():assert read(p)==result
 else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result

if __name__=='__main__':
 import sys
 result=analyze(sys.argv[1]);print(dict(passed=result['passed'],recipe=result['recipe'],observer=result['observer']))

