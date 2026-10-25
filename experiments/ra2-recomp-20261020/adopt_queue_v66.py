"""Retain the bypass-only candidate; bind a centerline sustained request input."""
from run_batch_v66 import *
import re
def section(t,key,value):
 pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new='['+key+']\n'+value+'\n'
 return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new

if sys.argv[1]=='map':
 current=read(S/'traffic-fixtures.json');old=next(x for x in current['fixtures'] if x['kind']=='queue');assert old['tag']=='traffic-cq'
 if not (S/'traffic-fixtures-initial.json').exists():write(S/'traffic-fixtures-initial.json',current)
 else:assert read(S/'traffic-fixtures-initial.json')==current
 comparisons=[]
 for tag in [old['baseline_tag'],old['observer_baseline_tag']]:
  p=S/'runs'/tag/'comparison.json';x=read(p);assert x['passed']
  comparisons.append(dict(path=str(p),sha256=sha(p),strict_original_c_equal=True,frames=x['comparison']['frames_compared']))
 exclusion=dict(passed=True,records=[dict(kind='queue-bypass-candidate',recipe=old,map_path=str(R/old['path']),map_sha256=sha(R/old['path']),comparisons=comparisons,accepted_as_positive_fairness_scene=False,all_goals_reached=True,actual_tube_actors=2,oldest_took_ground_bypass=True,reason='Offset goals and more distant starts chose legal ground bypasses; only two trucks used Tube after release. Not a proved original queue bug and not a Tube starvation witness. Keep both complete strict traces; revise ordinary starts/goals without changing game or rules.')])
 if not (S/'traffic-exclusions.json').exists():write(S/'traffic-exclusions.json',exclusion)
 else:assert read(S/'traffic-exclusions.json')==exclusion
 source=O/'fixtures/traffic-q.MAP';t=source.read_text(encoding='ascii')
 starts=[(63,112),(64,112),(65,112),(66,112),(63,114),(64,114),(65,114),(66,114),(63,116),(64,116),(65,116)]
 cells={tuple(c['cell']):c for c in read(O/'runs/traffic-q/original/cells.json')['cells']}
 extra=[(x,y) for y in [112,114,116,110,118] for x in range(60,67) if (x,y) in cells and (x,y) not in starts and cells[(x,y)]['land'] in [0,1,6,7] and cells[(x,y)]['level']==4 and not cells[(x,y)]['bridge']]
 starts += extra[:12]+[(67,114)]
 blockers=[(78,114),(79,114),(79,115)];assert len(starts)==24 and len(set(starts+blockers))==27
 assert all(cells[p]['land'] in [0,1,6,7] and cells[p]['level']==4 and not cells[p]['bridge'] for p in starts+blockers)
 units=''.join(f'{i}=Player House,TRUCKA,256,{p[0]},{p[1]},0,{"Sleep" if i>=24 else "Guard"},None,0,-1,0,-1,1,1\n' for i,p in enumerate(starts+blockers))
 out=section(section(t,'Units',units),'Infantry','');assert section(section(out,'Units',''),'Infantry','')==section(section(t,'Units',''),'Infantry','')
 p=S/'fixtures/traffic-cq2.MAP';assert not p.exists();p.write_text(out,encoding='ascii',newline='\n')
 pending=dict(old);pending.update(tag='traffic-cq2',path=p.relative_to(R).as_posix(),sha256=sha(p),starts=[list(p) for p in starts+blockers])
 write(S/'queue-centerline-pending.json',dict(passed=True,recipe=pending,source=str(source),source_sha256=sha(source)))
 print(dict(passed=True,map=str(p),ordinary_units_only=True))
elif sys.argv[1]=='bind':
 pending=read(S/'queue-centerline-pending.json');x=pending['recipe'];p=S/'runs/id-cq3/comparison.json';proof=read(p);assert proof['passed'] and proof['comparison']['frames_compared']==2
 rs=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];state=next(r for r in rs if r['kind']=='state');by_cell={tuple(v//256 for v in o['position'][:2]):o for o in state['objects'] if o.get('ground_drive')}
 ids=[by_cell[tuple(point)]['id'] for point in x['starts']];assert len(set(ids))==27
 orders=[];events=[];requests={};releases={};goals={}
 def add(f,slot,point,stage):
  orders.append(f'{f}:{ids[slot]}:2:{point[0]}:{point[1]}');events.append(dict(frame=f,slot=slot,id=ids[slot],cell=list(point),stage=stage));goals[str(ids[slot])]=list(point)
  if stage=='request':requests[str(ids[slot])]=f
  else:releases[str(ids[slot])]=f
 add(5,23,(91,114),'request')
 for i in range(23):add(100+180*i,i,(80+i,114),'request')
 # Keep every final cell unique while preserving the proven oldest goal.
 for e in events[1:]:
  if e['cell']==[91,114]:
   e['cell']=[103,114];goals[str(e['id'])]=e['cell'];orders[e['slot']+1]=f"{e['frame']}:{e['id']}:2:103:114"
 for j,slot in enumerate(x['blocker_slots']):add(2200+100*j,slot,(108+j,114),'release')
 assert len(set(tuple(v) for v in goals.values()))==27
 x.update(slot_ids=ids,actor_ids=ids[:24],ground_vehicle_ids=ids[:24],blocker_ids=ids[24:],actor_health={str(u):200 for u in ids},baseline_tag='b-'+x['tag'],observer_tag=x['tag']+'-obs',observer_baseline_tag='b-'+x['tag']+'-obs',orders=orders,events=events,goals=goals,oldest_id=ids[23],request_frames=requests,release_frames=releases)
 current=read(S/'traffic-fixtures.json');assert next(r for r in current['fixtures'] if r['kind']=='queue')['tag']=='traffic-cq';current['fixtures']=[x if r['kind']=='queue' else r for r in current['fixtures']]
 (S/'traffic-fixtures.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 provenance=read(S/'traffic-map-provenance.json');provenance['maps']=[dict(path=x['path'],sha256=x['sha256'],source=pending['source'],source_sha256=pending['source_sha256'],only_units_and_infantry_changed=True,terrain_overlay_tubes_unchanged=True) if r['path'].endswith('/traffic-cq.MAP') else r for r in provenance['maps']]
 (S/'traffic-map-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 catalog=read(S/'actor-catalog-validation.json');catalog['catalogs'].append(dict(tag='id-cq3',comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True));(S/'actor-catalog-validation.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(dict(passed=True,tag=x['tag'],oldest=ids[23],actors=24))
else:raise ValueError(sys.argv[1])
