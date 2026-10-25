"""Ordinary bridge/Tube map composition and twelve-vehicle exit queue; actor IDs calibrated at frame0."""
from run_batch_v65 import *
import re,struct
from map_codec_v65 import unpack
def section(t,k,body):
 pat=rf'(?ms)^\[{k}\]\n.*?(?=^\[|\Z)';v='['+k+']\n'+body+'\n'
 return re.sub(pat,lambda _:v,t) if re.search(pat,t) else t+'\n'+v
def body(t,k):
 m=re.search(rf'(?ms)^\[{k}\]\n(.*?)(?=^\[|\Z)',t);return m[1].rstrip() if m else None
def row(i,p,sleep=False):return f'{i}=Player House,TRUCKA,256,{p[0]},{p[1]},0,{"Sleep" if sleep else "Guard"},None,0,-1,0,-1,1,1\n'
if sys.argv[1]=='maps':
 items=[];tube_source=R/'evidence/movement-state-v38/fixtures/tube-curved-east.MAP'
 tube=tube_source.read_text(encoding='ascii');bridge_source=R/'evidence/movement-state-v38/fixtures/bridge-chain-lower-west.MAP';bridge=bridge_source.read_text(encoding='ascii')
 # These regions already share the original tunnel terrain; add only its legal Tubes records.
 records=lambda raw:{struct.unpack_from('<HH',raw,i):bytes(raw[i+4:i+11]) for i in range(0,len(raw)-4,11)}
 a=records(unpack(bridge)[1]);b=records(unpack(tube)[1]);region=[xy for xy in a if 64<=xy[0]<=84 and 108<=xy[1]<=120]
 assert region and all(a[xy]==b[xy] for xy in region)
 start=[(60,61),(61,60),(60,59),(61,58)];t=section(bridge,'Units',''.join(row(i,p) for i,p in enumerate(start)));t=section(t,'Infantry','');t=section(t,'Tubes',body(tube,'Tubes')+'\n')
 for k in ['IsoMapPack5','OverlayPack','OverlayDataPack']:assert body(t,k)==body(bridge,k)
 items.append(dict(kind='mixed',tag='traffic-m',source=str(bridge_source),secondary_source=str(tube_source),secondary_source_sha256=sha(tube_source),text=t,starts=[list(x) for x in start],actor_slots=list(range(4)),blocker_slots=[],last=5000,seconds=420,allowed_changed_sections=['Units','Infantry','Tubes'],tube_steps=10,scope='Four vehicles take ordinary waypoints across the same original bridge and existing flat curved Tubes, then return through both. Original terrain/overlays unchanged.'))
 source=R/'evidence/movement-state-v64/fixtures/traffic-tu.MAP';old=source.read_text(encoding='ascii');cells={tuple(c['cell']):c for c in read(O/'runs/traffic-tu/original/cells.json')['cells']}
 candidates=[(x,y) for y in [112,114,116,111,117] for x in [63,64,65,66] if cells[(x,y)]['land'] in [0,1,6,7] and cells[(x,y)]['level']==4 and not cells[(x,y)]['bridge']]
 start=candidates[:11]+[(67,114),(78,114),(79,114),(79,115)];assert len(start)==len(set(start))==15
 for x in range(80,95):assert cells[(x,114)]['land'] in [0,1,6,7] and cells[(x,114)]['level']==4
 t=section(old,'Units',''.join(row(i,p,i>=12) for i,p in enumerate(start)));t=section(t,'Infantry','')
 for k in ['IsoMapPack5','OverlayPack','OverlayDataPack','Tubes']:assert body(t,k)==body(old,k)
 items.append(dict(kind='queue',tag='traffic-q',source=str(source),text=t,starts=[list(x) for x in start],actor_slots=list(range(12)),blocker_slots=[12,13,14],oldest_slot=11,last=3600,seconds=360,allowed_changed_sections=['Units','Infantry'],tube_steps=10,scope='Twelve ordinary truck requests plus three stationary exit blockers. The highest actor ID receives the oldest request; later requests and staggered blocker releases test finite per-vehicle recovery and overtaking, not an unbounded starvation guarantee.'))
 for x in items:
  p=S/'fixtures'/(x['tag']+'.MAP');assert not p.exists();p.write_text(x.pop('text'),encoding='ascii',newline='\n');x.update(path=p.relative_to(R).as_posix(),sha256=sha(p),source_sha256=sha(Path(x['source'])),cell_catalog=True,capture_host=False)
 write(S/'traffic-pending.json',dict(passed=True,fixtures=items,terrain_and_overlays_unchanged=True,ordinary_map_and_move_events=True))
 print('Two ordinary map candidates prepared; calibrate actor IDs before movement orders.')
elif sys.argv[1]=='bind':
 items=read(S/'traffic-pending.json')['fixtures'];catalogs=[]
 for x in items:
  tag='id-m' if x['kind']=='mixed' else 'id-q';p=S/'runs'/tag/'comparison.json';proof=read(p);assert proof['passed'] and proof['comparison']['frames_compared']==2
  rs=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];state=next(r for r in rs if r['kind']=='state');by_cell={tuple(v//256 for v in o['position'][:2]):o for o in state['objects'] if o.get('ground_drive')}
  ids=[]
  for point in x['starts']:
   o=by_cell[tuple(point)];assert o['health']==200;ids.append(o['id'])
  x.update(slot_ids=ids,actor_ids=[ids[i] for i in x['actor_slots']],ground_vehicle_ids=[ids[i] for i in x['actor_slots']],blocker_ids=[ids[i] for i in x['blocker_slots']],actor_health={str(u):200 for u in ids},stationary_health={},baseline_tag='b-'+x['tag'],observer_tag=x['tag']+'-obs',observer_baseline_tag='b-'+x['tag']+'-obs',observer_required=True)
  orders=[];events=[]
  def add(f,slot,point):orders.append(f'{f}:{ids[slot]}:2:{point[0]}:{point[1]}');events.append(dict(frame=f,slot=slot,id=ids[slot],cell=list(point)))
  if x['kind']=='mixed':
   for f in [5,650,1800,2600,3400,4400]:
    for i in x['actor_slots']:
     point={5:(60+i%2,79-2*(i//2)),650:(67-i,114),1800:(83-i,114),2600:(62+i,114),3400:(60+i%2,75+2*(i//2)),4400:(59+2*(i%2),55+2*(i//2))}[f];add(f,i,point)
  else:
   add(5,11,(91,114))
   for i in range(11):add(100+35*i,i,(80+i,114))
   for f,i,point in [(1200,12,(92,114)),(1300,13,(93,114)),(1400,14,(94,114))]:add(f,i,point)
   x.update(oldest_id=ids[11],request_frames={str(ids[e['slot']]):e['frame'] for e in events if e['slot']<12},release_frames={str(ids[e['slot']]):e['frame'] for e in events if e['slot']>=12})
  x['orders']=orders;x['events']=events;x['goals']={}
  for e in events:x['goals'][str(e['id'])]=e['cell']
  catalogs.append(dict(tag=tag,comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True))
 write(S/'actor-catalog-validation.json',dict(passed=True,catalogs=catalogs,setup_only=True))
 write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=2,ordinary_map_and_move_events=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False))
 write(S/'prior-explorations.json',dict(passed=True,path=str(O/'current-explorations.json'),sha256=sha(O/'current-explorations.json'),rerun=False,scope='Retain all parent long-path startup, range-setup and elevated-cardinal stall records; not counted as current positive traffic.'))
 print(dict(passed=True,recipes=2,actor_counts=[len(x['actor_ids']) for x in items],ids=[x['slot_ids'] for x in items]))
else:raise ValueError(sys.argv[1])
