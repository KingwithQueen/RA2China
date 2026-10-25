"""Per-request sustained-arrival metrics; strict raw comparisons and immutable pre-change traces."""
from run_batch_v66 import R,S,read,sha
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
 recipe=next(x for x in read(S/'traffic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag'],x['observer_tag'],x['observer_baseline_tag']])
 observed=tag in [recipe['observer_tag'],recipe['observer_baseline_tag']];baseline=tag.startswith('b-');folder=S/'runs'/tag;comparison=read(folder/'comparison.json')
 assert comparison['passed'] and comparison['cell_catalog_equal'] and comparison['comparison']['negative_control']['passed']
 modes={};frozen={};actors=recipe['actor_ids'];all_ids=recipe['slot_ids'];last=recipe['last']
 for mode in ['original','generated-c']:
  path=folder/mode/'state.jsonl'
  if not baseline:
   before=S/'runs'/recipe['observer_baseline_tag' if observed else 'baseline_tag']/mode/'state.jsonl';assert sha(path)==sha(before),(tag,mode,'Complete baseline changed');frozen[mode]=sha(before)
  h,snap,submissions,executions,audit=compact(path,set(all_ids));assert list(h)==list(range(last+1))
  cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert all(all(u in frame and frame[u]['health']==200 for u in all_ids) for frame in h.values())
  goals={};arrivals={};paths={};bridge={}
  for u in all_ids:
   target=tuple(recipe['goals'][str(u)]);o=h[last][u]
   assert cell(o)==target and o['mission'][0] in [0,5],(tag,mode,u,'Goal/Guard',o)
   goals[str(u)]=dict(final_cell=list(cell(o)),final_position=list(o['position']),final_mission=o['mission'])
   if u in actors:
    request=recipe['request_frames'][str(u)];arrivals[u]=next(f for f in range(request,last+1) if cell(h[f][u])==target)
    paths[str(u)]=sum(frame[u]['has_path'] for frame in h.values());assert paths[str(u)]
    bridge[u]=[f for f in h if h[f][u]['bridge'] and cell(h[f][u])[0] in [60,61] and 63<=cell(h[f][u])[1]<=70]
  expected=sorted(tuple(map(int,o.split(':'))) for o in recipe['orders']);assert sorted(submissions)==expected
  for f,u,m,x,y in expected:assert m==2 and any(ef==f and v==u and mission==m and f<=actual<=f+2 for ef,actual,v,mission in executions),(tag,mode,f,u)
  assert audit and recipe['arrival_end']-recipe['arrival_start']>=2000 and recipe['arrival_end']>recipe['release_end']
  assert max(b-a for a,b in zip(sorted(recipe['request_frames'].values()),sorted(recipe['request_frames'].values())[1:]))==recipe['arrival_period']
  effect=dict(actor_count=len(actors),oldest_request_id=recipe['oldest_id'],arrival_window=[recipe['arrival_start'],recipe['arrival_end']],arrival_period=recipe['arrival_period'],blocker_release_window=[recipe['release_start'],recipe['release_end']],all_requests_recovered=True,arrivals={str(u):f for u,f in arrivals.items()},replacement_queue_requests=False)
  if observed:
   assert all(len(snap[u])==last+1 for u in actors)
   waits={};exits={};waiting_by_frame={f:0 for f in h};tube_participants=[]
   for u in actors:
    data=snap[u];request=recipe['request_frames'][str(u)];active=[f for f,r in data.items() if f>=request and r['route']==0 and r['steps']==10 and 0<r['waypoint']<=10]
    entry=dict(request_frame=request,arrival_frame=arrivals[u],request_to_arrival=arrivals[u]-request,bridge_frames=len(bridge[u]))
    if not active:entry['route']='ground_bypass';waits[str(u)]=entry;continue
    first=active[0];exit_frame=next((f for f in range(first+1,last+1) if data[f]['route']==255),None);assert exit_frame is not None,(tag,mode,u,'No exit')
    hold=[f for f in active if data[f]['waypoint']==10 and f>0 and h[f][u]['position']==h[f-1][u]['position']]
    for f in hold:waiting_by_frame[f]+=1
    if recipe['kind']=='mixed':assert bridge[u] and min(bridge[u])<first,(tag,mode,u,'No same-vehicle bridge-before-Tube witness')
    entry.update(route='tube',first_active_tube=first,exit_publish_frame=exit_frame,terminal_stationary_frames=len(hold),longest_terminal_wait=longest(hold),request_to_exit=exit_frame-request,first_bridge_frame=min(bridge[u]) if bridge[u] else None)
    waits[str(u)]=entry;exits[u]=exit_frame;tube_participants.append(u)
   oldest=recipe['oldest_id'];assert oldest in exits,(tag,mode,'Oldest request bypassed Tube')
   minimum=8 if recipe['kind']=='queue' else 4
   assert len(exits)>=minimum and max(waiting_by_frame.values())>=minimum and waits[str(oldest)]['longest_terminal_wait']>=600,(tag,mode,'Insufficient queue or long wait',len(exits),max(waiting_by_frame.values()),waits[str(oldest)])
   during=[u for u,f in exits.items() if recipe['release_start']<=f<=recipe['arrival_end']];assert len(during)>=4,(tag,mode,'No sustained-arrival service',during)
   for u in exits:
    waits[str(u)]['later_requests_exited_first']=sum(recipe['request_frames'][str(v)]>recipe['request_frames'][str(u)] and exits[v]<exits[u] for v in exits)
   backlog=[]
   for f in range(0,last+1,100):
    pending=[u for u in actors if recipe['request_frames'][str(u)]<=f<arrivals[u]]
    backlog.append(dict(frame=f,pending=len(pending),oldest_pending_age=max((f-recipe['request_frames'][str(u)] for u in pending),default=0),terminal_waiters=waiting_by_frame[f]))
   bins=[dict(first=f,last=min(f+499,last),tube_exits=sum(f<=x<=min(f+499,last) for x in exits.values()),goal_arrivals=sum(f<=x<=min(f+499,last) for x in arrivals.values())) for f in range(0,last+1,500)]
   by_exit=sorted(exits,key=lambda u:(exits[u],u));inversions=sum(recipe['request_frames'][str(a)]>recipe['request_frames'][str(b)] for i,a in enumerate(by_exit) for b in by_exit[i+1:])
   width=last-recipe['release_start']+1
   effect.update(per_vehicle=waits,actual_tube_actors=len(exits),ground_bypass_actors=len(actors)-len(exits),peak_terminal_waiters=max(waiting_by_frame.values()),tube_exits_during_arrivals=len(during),oldest_exit_during_arrivals=exits[oldest]<=recipe['arrival_end'],oldest_later_requests_exited_first=waits[str(oldest)]['later_requests_exited_first'],maximum_request_to_exit=max(exits[u]-recipe['request_frames'][str(u)] for u in exits),maximum_terminal_wait=max(x.get('longest_terminal_wait',0) for x in waits.values()),last_exit_publish_frame=max(exits.values()),last_goal_arrival=max(arrivals.values()),request_exit_order_inversions=inversions,exit_order=by_exit,backlog_samples=backlog,throughput_500_frame_windows=bins,post_release_measurement_frames=width,post_release_tube_exits_per_1000_frames=1000*sum(f>=recipe['release_start'] for f in exits.values())/width,finite_recovery_verified=True,unbounded_starvation_freedom_proved=False,fifo_guarantee=False)
  modes[mode]=dict(goals=goals,health_preserved=True,reconstructed_path_frames=paths,existing_successful_stage6_observations=audit,effects=effect)
 result=dict(passed=True,recipe=recipe['tag'],baseline=baseline,observer=observed,comparison_sha256=sha(folder/'comparison.json'),strict_trace_equal=True,per_mode_traces_equal_prechange=not baseline,baseline_traces=frozen,modes=modes,ordinary_move_events=True,no_memory_or_path_result_injection=True,scope=recipe['scope'])
 p=folder/'traffic-acceptance.json'
 if p.exists():assert read(p)==result
 else:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result

if __name__=='__main__':
 import sys
 x=analyze(sys.argv[1]);print(json.dumps(dict(passed=x['passed'],recipe=x['recipe'],observer=x['observer']),ensure_ascii=False))
