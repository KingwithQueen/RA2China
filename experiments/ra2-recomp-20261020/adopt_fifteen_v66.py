"""Keep the unresolved original stationary-start case; use fifteen proven moving starts."""
from run_batch_v66 import *
import re
if sys.argv[1]=='map':
 current=read(S/'traffic-fixtures.json');old=next(x for x in current['fixtures'] if x['kind']=='mixed');assert old['tag']=='traffic-cm4'
 comparisons=[]
 for tag in [old['baseline_tag'],old['observer_baseline_tag']]:
  p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed'];comparisons.append(dict(path=str(p),sha256=sha(p),strict_original_c_equal=True,frames=q['comparison']['frames_compared']))
 excluded=read(S/'traffic-exclusions.json');excluded['records'].append(dict(kind='mixed-legal-goals-stationary-start',recipe=old,map_path=str(R/old['path']),map_sha256=sha(R/old['path']),comparisons=comparisons,accepted_as_positive_fairness_scene=False,all_goals_reached=False,completed_requests=15,completed_release_vehicles=3,uncompleted_requests=1,uncompleted_actor=old['actor_ids'][15],initial_and_final_cell=[62,54],unreached_goal=[76,74],root_cause_proved=False,original_queue_bug_proved=False,scope='All goals have legal native land/height. One actor stays at its initial cell in both original and unchanged C; reason unresolved. Keep the full 16-request input and traces, and do not call this a proved queue load or starvation defect.'))
 (S/'traffic-exclusions.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 t=(R/old['path']).read_text(encoding='ascii');m=re.search(r'(?ms)^\[Units\]\n(.*?)(?=^\[|\Z)',t);lines=[l for l in m[1].splitlines() if l.strip()];assert len(lines)==19
 lines=[l for l in lines if int(l.split('=',1)[0])!=15];units=''.join(str(i)+'='+l.split('=',1)[1]+'\n' for i,l in enumerate(lines))+'\n';out=t[:m.start(1)]+units+t[m.end(1):]
 assert re.sub(r'(?ms)^\[Units\]\n.*?(?=^\[|\Z)','[Units]\n\n',out)==re.sub(r'(?ms)^\[Units\]\n.*?(?=^\[|\Z)','[Units]\n\n',t)
 p=S/'fixtures/traffic-cm5.MAP';assert not p.exists();p.write_text(out,encoding='ascii',newline='\n')
 pending=dict(old);pending.update(tag='traffic-cm5',path=p.relative_to(R).as_posix(),sha256=sha(p),starts=old['starts'][:15]+old['starts'][16:],actor_slots=list(range(15)),blocker_slots=[15,16,17],arrival_end=3320)
 pending['events']=[dict(e) for e in old['events'] if e['slot']!=15]
 for e in pending['events']:
  if e['stage']=='release':e['slot']-=1
 write(S/'mixed-fifteen-pending.json',dict(passed=True,recipe=pending,removed_unconfirmed_stationary_start=[62,54],source_input=str(R/old['path']),source_input_sha256=sha(R/old['path']),ordinary_units_only=True))
 print(dict(passed=True,map=str(p),requests=15,release_vehicles=3))
elif sys.argv[1]=='bind':
 x=read(S/'mixed-fifteen-pending.json')['recipe'];p=S/'runs/id-cm5/comparison.json';proof=read(p);assert proof['passed'] and proof['comparison']['frames_compared']==2
 rs=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];state=next(r for r in rs if r['kind']=='state');by_cell={tuple(v//256 for v in o['position'][:2]):o for o in state['objects'] if o.get('ground_drive')}
 ids=[by_cell[tuple(c)]['id'] for c in x['starts']];assert len(set(ids))==18
 for e in x['events']:e['id']=ids[e['slot']]
 x.update(slot_ids=ids,actor_ids=ids[:15],ground_vehicle_ids=ids[:15],blocker_ids=ids[15:],actor_health={str(u):200 for u in ids},oldest_id=ids[0],baseline_tag='b-'+x['tag'],observer_tag=x['tag']+'-obs',observer_baseline_tag='b-'+x['tag']+'-obs',orders=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']],goals={str(e['id']):e['cell'] for e in x['events']},request_frames={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='request'},release_frames={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='release'})
 current=read(S/'traffic-fixtures.json');assert next(r for r in current['fixtures'] if r['kind']=='mixed')['tag']=='traffic-cm4';current['fixtures']=[x if r['kind']=='mixed' else r for r in current['fixtures']]
 (S/'traffic-fixtures.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 provenance=read(S/'traffic-map-provenance.json')
 for e in provenance['maps']:
  if e['path'].endswith('/traffic-cm4.MAP'):e.update(path=x['path'],sha256=x['sha256'])
 (S/'traffic-map-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 catalog=read(S/'actor-catalog-validation.json');catalog['catalogs'].append(dict(tag='id-cm5',comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True));(S/'actor-catalog-validation.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 oldproof=S/'traffic-goal-terrain-validation.json';archived=S/'traffic-goal-terrain-validation-cm4.json';assert not archived.exists();oldproof.rename(archived)
 print(dict(passed=True,tag=x['tag'],actors=15,ids=ids))
else:raise ValueError(sys.argv[1])
