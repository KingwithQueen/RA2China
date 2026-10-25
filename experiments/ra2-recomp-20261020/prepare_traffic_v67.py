"""Native-terrain-checked reverse queue and opposing bridge/Tube requests."""
from run_batch_v67 import *
import re
def section(t,key,value):
 pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new='['+key+']\n'+value+'\n'
 return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new
if sys.argv[1]=='maps':
 for name in ['initial-checker-lineage.json','checker-lineage.json']:shutil.copy2(R/'lineage_v67.json',S/name)
 for name in ['make_channel_observer_v66.py','run_channel_observer_v66.py','build-channel-observer-v66.ps1']:
  (R/name.replace('v66','v67')).write_text((R/name).read_text(encoding='utf-8').replace('v66','v67').rstrip()+'\n',encoding='utf-8',newline='\n')
 entries=[]
 for name in ['channel_observer.c','channel-observer.exe']:
  d=S/'baseline-channel-observer'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d);shutil.copy2(O/name,S/name);entries.append(dict(path=name,sha256=sha(d)))
 write(S/'baseline-channel-observer/manifest.json',entries)
 shutil.copy2(O/'community-current-use.json',S/'community-current-use.json')
 write(S/'prior-explorations.json',dict(passed=True,path=str(O/'current-explorations.json'),sha256=sha(O/'current-explorations.json'),rerun=False,scope='Retain prior invalid targets, unresolved stationary start and explicitly invalidated overlap snapshot by hash. No current positive claims for them.'))
 definitions=[]
 starts=[(x,y) for y in [112,114] for x in [80,81,82,83]]+[(80,116),(81,116),(82,116),(79,114)]
 blockers=[(68,114),(67,114),(67,115)];goals=[(63,112),(64,112),(65,112),(66,112),(63,114),(64,114),(66,114),(63,116),(64,116),(65,116),(66,116)]
 events=[dict(frame=5,slot=11,cell=[65,114],stage='request')]+[dict(frame=100+200*i,slot=i,cell=list(p),stage='request') for i,p in enumerate(goals)]+[dict(frame=1600+100*j,slot=12+j,cell=[63+j,110],stage='release') for j in range(3)]
 definitions.append(dict(kind='reverse',tag='traffic-rq',source=O/'fixtures/traffic-cq2.MAP',catalog=O/'runs/id-cq3/original/cells.json',starts=starts+blockers,actor_slots=list(range(12)),blocker_slots=[12,13,14],events=events,route_slots={1:list(range(12))},oldest_slot=11,arrival_period=200,min_actual={1:4},long_wait_required=True))
 starts=[(60,60),(61,60),(59,60),(62,60),(60,58),(61,58),(59,58),(62,58)]+[(77,76),(78,76),(77,74),(78,74),(77,78),(78,78),(77,80),(78,80)]
 events=[]
 for i in range(8):
  for f,p,stage in [(5+300*i,(60+i%2,79-2*((i//2)%3)),'bridge'),(450+300*i,(59-i%4,76),'approach'),(800+300*i,(73+i%4,76 if i<4 else 74),'request')]:events.append(dict(frame=f,slot=i,cell=list(p),stage=stage))
 for i in range(8):events.append(dict(frame=900+300*i,slot=8+i,cell=[56+i%4,76 if i<4 else 78],stage='request'))
 definitions.append(dict(kind='mixed',tag='traffic-bm',source=O/'fixtures/traffic-cm5.MAP',catalog=O/'runs/id-cm5/original/cells.json',starts=starts,actor_slots=list(range(16)),blocker_slots=[],events=events,route_slots={0:list(range(8)),1:list(range(8,16))},oldest_slot=0,arrival_period=300,min_actual={0:2,1:2},long_wait_required=False))
 items=[];provenance=[];terrain=[]
 for d in definitions:
  cells={tuple(c['cell']):c for c in read(d['catalog'])['cells']};checked=[]
  assert len(d['starts'])==len(set(d['starts']))
  for stage,points in [('start',d['starts']),('ordinary-move-goal',[e['cell'] for e in d['events']])]:
   for p in points:
    c=cells[tuple(p)];assert c['land'] in [0,1,6,7] and c['level']==4,(d['tag'],stage,p,c);checked.append(dict(stage=stage,cell=list(p),land=c['land'],level=c['level'],overlay=c['overlay'],bridge=c['bridge']))
  text=d['source'].read_text(encoding='ascii');unit_rows=''.join(f'{i}=Player House,TRUCKA,256,{p[0]},{p[1]},0,{"Sleep" if i in d["blocker_slots"] else "Guard"},None,0,-1,0,-1,1,1\n' for i,p in enumerate(d['starts']))
  out=section(section(text,'Units',unit_rows),'Infantry','');strip=lambda t:section(section(t,'Units',''),'Infantry','');assert strip(out)==strip(text)
  p=S/'fixtures'/(d['tag']+'.MAP');assert not p.exists();p.write_text(out,encoding='ascii',newline='\n')
  item={k:v for k,v in d.items() if k not in ['source','catalog']};item.update(source=str(d['source']),source_sha256=sha(d['source']),path=p.relative_to(R).as_posix(),sha256=sha(p),starts=[list(p) for p in d['starts']],last=5400,seconds=600,cell_catalog=True,capture_host=False,tube_steps=10,scope='Ordinary reverse queue or opposing bridge/Tube requests, finite flow windows and per-vehicle outcomes. No memory/path injection or FIFO/infinite-load guarantee.')
  items.append(item);provenance.append(dict(path=item['path'],sha256=item['sha256'],source=item['source'],source_sha256=item['source_sha256'],only_units_and_infantry_changed=True));terrain.append(dict(tag=item['tag'],map_sha256=item['sha256'],catalog=str(d['catalog']),catalog_sha256=sha(d['catalog']),checked=checked))
 write(S/'traffic-pending.json',dict(passed=True,fixtures=items));write(S/'traffic-map-provenance.json',dict(passed=True,maps=provenance));write(S/'traffic-goal-terrain-validation.json',dict(passed=True,scenes=terrain,scope='Every start, waypoint and final goal checked against the locked original native catalog before game execution; occupancy and routing still require natural acceptance.'))
 print(dict(passed=True,recipes=2,all_starts_and_goals_prechecked=True))
elif sys.argv[1]=='bind':
 items=read(S/'traffic-pending.json')['fixtures'];catalogs=[]
 for x in items:
  tag='id-rq' if x['kind']=='reverse' else 'id-bm';p=S/'runs'/tag/'comparison.json';proof=read(p);assert proof['passed'] and proof['comparison']['frames_compared']==2
  rs=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];state=next(r for r in rs if r['kind']=='state');by_cell={tuple(v//256 for v in o['position'][:2]):o for o in state['objects'] if o.get('ground_drive')};ids=[by_cell[tuple(c)]['id'] for c in x['starts']]
  assert len(set(ids))==len(ids);x.update(slot_ids=ids,actor_ids=[ids[i] for i in x['actor_slots']],blocker_ids=[ids[i] for i in x['blocker_slots']],baseline_tag='b-'+x['tag'],observer_tag=x['tag']+'-obs',observer_baseline_tag='b-'+x['tag']+'-obs',oldest_id=ids[x['oldest_slot']],route_for_id={str(ids[i]):int(route) for route,slots in x['route_slots'].items() for i in slots})
  for e in x['events']:e['id']=ids[e['slot']]
  x.update(orders=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']],goals={str(e['id']):e['cell'] for e in x['events']},request_frames={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='request'},release_frames={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='release'})
  catalogs.append(dict(tag=tag,comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True))
 write(S/'actor-catalog-validation.json',dict(passed=True,catalogs=catalogs,setup_only=True));write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=2,rules_overrides=False,engine_state_or_path_injection=False))
 print(dict(passed=True,recipes=2,actors=[len(x['actor_ids']) for x in items]))
else:raise ValueError(sys.argv[1])
