"""Finite normal traffic effects, preserving raw original/C differences and exact pre-change traces."""
from run_batch_v61 import R,S,read,sha
import json
def analyze(tag):
 recipe=next(x for x in read(S/'traffic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']])
 baseline=tag==recipe['baseline_tag'];folder=S/'runs'/tag;comparison=read(folder/'comparison.json')
 assert all(x['passed'] and x['exit_code']==0 for x in comparison['runs']) and comparison['comparison']['negative_control']['passed']
 assert comparison['cell_catalog_equal']
 modes={};baseline_traces={}
 for mode in ['original','generated-c']:
  path=folder/mode/'state.jsonl';rows=[json.loads(l) for l in path.open(encoding='utf-8')]
  if not baseline:
   frozen=S/'runs'/recipe['baseline_tag']/mode/'state.jsonl';assert sha(path)==sha(frozen),('Changed complete pre-edit traffic trace',tag,mode)
   baseline_traces[mode]=sha(frozen)
  states={r['frame']:{o['id']:o for o in r['objects']} for r in rows if r['kind']=='state'};assert len(states)==recipe['last']+1
  cells={tuple(x['cell']):x for x in read(folder/mode/'cells.json')['cells']}
  actors=recipe['actor_ids'];health={**recipe['actor_health'],**recipe['stationary_health']};cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert all(all(int(u) in frame and frame[int(u)]['health']==v for u,v in health.items()) for frame in states.values())
  assert all(cells[cell(frame[u])]['land'] in [0,6,7] and frame[u]['position'][2]==0 for frame in states.values() for u in actors)
  goals={};path_frames={}
  for u in actors:
   last_order=max(int(s.split(':')[0]) for s in recipe['orders'] if int(s.split(':')[1])==u)
   arrived=[f for f,h in states.items() if f>=last_order and list(cell(h[u]))==recipe['goals'][str(u)]]
   assert arrived and list(cell(states[recipe['last']][u]))==recipe['goals'][str(u)] and states[recipe['last']][u]['mission'][0] in [0,5],(tag,mode,u,'Goal/Guard')
   goals[str(u)]=dict(first_arrival_after_final_order=arrived[0],final_cell=list(cell(states[recipe['last']][u])),final_mission=states[recipe['last']][u]['mission'])
  for u in recipe['ground_vehicle_ids']:
   samples=[f for f,h in states.items() if h[u].get('ground_drive',{}).get('path_directions')]
   assert samples,(tag,mode,u,'No reconstructed route observed');path_frames[str(u)]=len(samples)
  moving={f:[u for u in actors if states[f][u]['position']!=states[f-1][u]['position']] for f in range(1,recipe['last']+1)}
  simultaneous=[f for f,ids in moving.items() if len(ids)>=3]
  close=[f for f,ids in moving.items() if any(max(abs(states[f][a]['position'][i]-states[f][b]['position'][i]) for i in [0,1])<=768 for j,a in enumerate(ids) for b in ids[j+1:])]
  assert len(simultaneous)>=10 and len(close)>=5,(tag,mode,'No substantial concurrent nearby traffic',len(simultaneous),len(close))
  expected=sorted(tuple(map(int,s.split(':'))) for s in recipe['orders'])
  submissions=sorted((r['frame'],r['id'],r['mission'],*r['cell']) for r in rows if r['kind']=='submit')
  assert submissions==expected
  reroutes=[];previous={}
  for f,u,mission,x,y in expected:
   assert mission==2
   executions=[r for r in rows if r['kind']=='execute' and r['id']==u and r['mission']==2 and r['event_frame']==f and f<=r['frame']<=f+2]
   assert executions,(tag,mode,'Order not executed',f,u)
   if u in previous:
    recent=[q for q in range(max(1,f-8),f) if u in moving[q]]
    unfinished=list(cell(states[f-1][u]))!=previous[u]
    reroutes.append(dict(id=u,submit_frame=f,execute_frame=executions[0]['frame'],was_moving=states[f-1][u]['position']!=states[f-2][u]['position'],recent_motion_in_eight_frames=bool(recent),old_goal_unfinished=unfinished))
   previous[u]=[x,y]
  assert any(x['was_moving'] and x['old_goal_unfinished'] for x in reroutes),(tag,mode,'No moving unfinished goal replacement')
  requests=[r for r in rows if r['kind']=='movement-audit' and r['stage']==6 and r['id'] in actors]
  assert requests and any(r['value'] for r in requests)
  activity=[]
  for start,end in recipe['activity_windows']:
   multi=[f for f in range(max(1,start),end+1) if len(moving[f])>=3]
   active={str(u):sum(u in moving[f] for f in range(max(1,start),end+1)) for u in actors}
   assert len(multi)>=8 and all(n>=5 for n in active.values()),(tag,mode,'Insufficient later traffic',start,end,multi,active)
   activity.append(dict(window=[start,end],simultaneous_three_or_more_frames=len(multi),actor_moving_frames=active))
  modes[mode]=dict(activity_windows=activity,goals=goals,health_preserved=True,legal_land_and_zero_height=True,simultaneous_three_or_more_frames=len(simultaneous),nearby_simultaneous_motion_frames=len(close),moving_reissues=reroutes,reconstructed_route_frames=path_frames,existing_stage6_observations=len(requests),existing_stage6_positive_results=sum(bool(r['value']) for r in requests))
 result=dict(passed=True,recipe=recipe['tag'],baseline=baseline,comparison_sha256=sha(folder/'comparison.json'),strict_trace_equal=comparison['passed'],strict_failure_preserved=not comparison['passed'],baseline_traces=baseline_traces,per_mode_traces_equal_prechange=not baseline,modes=modes,all_final_goals_equal=True,ordinary_move_events=True,no_memory_or_path_result_injection=True,scope='Two new ordinary traffic recipes on unchanged original map. Observable route buffers and existing audit results do not prove every internal consumer/queue branch or optimal routes.')
 out=folder/'traffic-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 print(json.dumps(analyze(sys.argv[1]),ensure_ascii=False))
