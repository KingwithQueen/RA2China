"""Two ordinary sustained-arrival inputs on frozen parent maps; no terrain or path injection."""
from run_batch_v66 import *
import re

def section(t,key,value):
 pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new='['+key+']\n'+value+'\n'
 return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new

def body(t,key):
 m=re.search(rf'(?ms)^\[{key}\]\n(.*?)(?=^\[|\Z)',t);return m[1] if m else None

if sys.argv[1]=='maps':
 shutil.copy2(R/'lineage_v66.json',S/'initial-checker-lineage.json');shutil.copy2(R/'lineage_v66.json',S/'checker-lineage.json')
 for name in ['make_channel_observer_v65.py','run_channel_observer_v65.py','build-channel-observer-v65.ps1']:
  (R/name.replace('v65','v66')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v65','v66').rstrip()+'\n',encoding='utf-8',newline='\n')
 entries=[]
 for name in ['channel_observer.c','channel-observer.exe']:
  d=S/'baseline-channel-observer'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d);shutil.copy2(O/name,S/name);entries.append(dict(path=name,sha256=sha(d)))
 write(S/'baseline-channel-observer/manifest.json',entries)
 definitions=[('queue','traffic-cq','traffic-q.MAP',24,7600),('mixed','traffic-cm','traffic-m3.MAP',16,7200)]
 items=[];provenance=[]
 for kind,tag,filename,count,last in definitions:
  source=O/'fixtures'/filename;t=source.read_text(encoding='ascii');cells={tuple(c['cell']):c for c in read(O/'runs'/('traffic-q' if kind=='queue' else 'traffic-m3')/'original/cells.json')['cells']}
  def legal(p):return p in cells and cells[p]['land'] in [0,1,6,7] and cells[p]['level']==4 and not cells[p]['bridge']
  if kind=='queue':
   candidates=[(x,y) for y in [112,116,110,118,114] for x in range(60,67) if legal((x,y))];starts=candidates[:count-1]+[(67,114)];blockers=[(78,114),(79,114),(79,115)]
  else:
   candidates=[(x,y) for y in [60,58,56,54] for x in [60,61,59,62] if legal((x,y))];starts=candidates[:count];blockers=[(70,76),(71,76),(71,77)]
  assert len(starts)==count and len(set(starts+blockers))==count+3 and all(legal(p) for p in starts+blockers),(tag,starts,blockers)
  units=''.join(f'{i}=Player House,TRUCKA,256,{p[0]},{p[1]},0,{"Sleep" if i>=count else "Guard"},None,0,-1,0,-1,1,1\n' for i,p in enumerate(starts+blockers))
  out=section(section(t,'Units',units),'Infantry','')
  # No other section changes, including the bounded LCW bridge/Tube patch accepted by the parent.
  strip=lambda text:section(section(text,'Units',''),'Infantry','')
  assert strip(out)==strip(t)
  p=S/'fixtures'/(tag+'.MAP');assert not p.exists();p.write_text(out,encoding='ascii',newline='\n')
  item=dict(kind=kind,tag=tag,path=p.relative_to(R).as_posix(),sha256=sha(p),source=str(source),source_sha256=sha(source),starts=[list(p) for p in starts+blockers],actor_slots=list(range(count)),blocker_slots=list(range(count,count+3)),last=last,seconds=600,cell_catalog=True,capture_host=False,tube_steps=10,scope='Finite sustained arrivals on the unchanged accepted parent terrain/overlays, with ordinary Move commands and staggered stationary-blocker release; per-request recovery and throughput, not arbitrary-load starvation freedom.')
  items.append(item);provenance.append(dict(path=item['path'],sha256=item['sha256'],source=str(source),source_sha256=sha(source),only_units_and_infantry_changed=True,terrain_overlay_tubes_unchanged=True))
 write(S/'traffic-pending.json',dict(passed=True,fixtures=items))
 write(S/'traffic-map-provenance.json',dict(passed=True,maps=provenance,parent_mixed_patch=str(O/'mixed-relocation-rle.json'),parent_mixed_patch_sha256=sha(O/'mixed-relocation-rle.json'),ordinary_map_only=True,rules_or_resources_changed=False))
 write(S/'prior-explorations.json',dict(passed=True,path=str(O/'current-explorations.json'),sha256=sha(O/'current-explorations.json'),rerun=False,scope='All parent rejected route/map inputs and calibration/checker corrections retained without reclassifying them as successful traffic.'))
 print(dict(passed=True,prepared=[(x['tag'],len(x['actor_slots']),x['last']) for x in items]))
elif sys.argv[1]=='bind':
 items=read(S/'traffic-pending.json')['fixtures'];catalogs=[]
 for x in items:
  tag='id-cq' if x['kind']=='queue' else 'id-cm';p=S/'runs'/tag/'comparison.json';proof=read(p);assert proof['passed'] and proof['comparison']['frames_compared']==2
  rs=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];state=next(r for r in rs if r['kind']=='state');by_cell={tuple(v//256 for v in o['position'][:2]):o for o in state['objects'] if o.get('ground_drive')}
  ids=[by_cell[tuple(point)]['id'] for point in x['starts']];assert len(set(ids))==len(ids)
  x.update(slot_ids=ids,actor_ids=[ids[i] for i in x['actor_slots']],ground_vehicle_ids=[ids[i] for i in x['actor_slots']],blocker_ids=[ids[i] for i in x['blocker_slots']],actor_health={str(u):200 for u in ids},baseline_tag='b-'+x['tag'],observer_tag=x['tag']+'-obs',observer_baseline_tag='b-'+x['tag']+'-obs',observer_required=True)
  orders=[];events=[];requests={};releases={};goals={}
  def add(f,slot,point,stage):
   orders.append(f'{f}:{ids[slot]}:2:{point[0]}:{point[1]}');events.append(dict(frame=f,slot=slot,id=ids[slot],cell=list(point),stage=stage));goals[str(ids[slot])]=list(point)
   if stage=='request':requests[str(ids[slot])]=f
   if stage=='release':releases[str(ids[slot])]=f
  count=len(x['actor_ids'])
  if x['kind']=='queue':
   add(5,count-1,(94,116),'request')
   for i in range(count-1):add(100+180*i,i,(82+i%12,112+2*(i//12)),'request')
   for j,slot in enumerate(x['blocker_slots']):add(2200+100*j,slot,(96+j,114),'release')
   oldest=ids[-4]
  else:
   for i in x['actor_slots']:
    add(5+180*i,i,(60+i%2,79-2*((i//2)%3)),'bridge')
    add(450+180*i,i,(59-i%4,76),'approach')
    add(800+180*i,i,(77+i%8,74+2*(i//8)),'request')
   for j,slot in enumerate(x['blocker_slots']):add(2600+100*j,slot,(88+j,78),'release')
   oldest=ids[0]
  assert all(list(by_cell[tuple(x['starts'][i])]['position']) for i in range(len(ids)))
  x.update(orders=orders,events=events,goals=goals,oldest_id=oldest,request_frames=requests,release_frames=releases,arrival_period=180,arrival_start=min(requests.values()),arrival_end=max(requests.values()),release_start=min(releases.values()),release_end=max(releases.values()),ordinary_commands_only=True,replacement_queue_requests=False)
  catalogs.append(dict(tag=tag,comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True))
 write(S/'actor-catalog-validation.json',dict(passed=True,catalogs=catalogs,setup_only=True))
 write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=2,ordinary_map_and_move_events=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False))
 print(dict(passed=True,recipes=2,actors=[len(x['actor_ids']) for x in items],ids=[x['slot_ids'] for x in items]))
else:raise ValueError(sys.argv[1])
