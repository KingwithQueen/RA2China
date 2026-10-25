"""Ordinary map placement and Move events; no runtime state injection."""
from run_batch_v64 import *
import re
def section(t,k,body):
 pattern=rf'(?ms)^\[{k}\]\n.*?(?=^\[|\Z)';value='['+k+']\n'+body+'\n'
 return re.sub(pattern,lambda _:value,t) if re.search(pattern,t) else t+'\n'+value
def unit(i,x,y,upper=0,mission='Guard'):
 return f'{i}=Player House,TRUCKA,256,{x},{y},0,{mission},None,0,-1,{upper},-1,1,1\n'
def foot(i,x,y,upper=0):return f'{i}=Player House,E2,256,{x},{y},2,Sleep,0,None,0,-1,{upper},1,1\n'
def moves(f,goals):return [f'{f}:{u}:2:{x}:{y}' for u,(x,y) in goals.items()]
items=[]
source=R/'evidence/movement-state-v38/fixtures/bridge-chain-lower-west.MAP';old=source.read_text(encoding='ascii')
t=section(old,'Units',unit(0,60,61)+unit(1,61,73)+unit(2,55,66)+unit(3,64,66));t=section(t,'Infantry',foot(0,60,60)+foot(1,55,65))
orders=[]
for f,g in [(5,{1023362:(60,75),1023363:(61,59),1023364:(65,66),1023365:(54,66),1023366:(61,75),1023367:(65,65)}),(650,{1023362:(60,59),1023363:(61,75),1023364:(54,66),1023365:(65,66),1023366:(61,59),1023367:(54,65)}),(1300,{1023362:(60,75),1023363:(61,59),1023364:(65,66),1023365:(54,66),1023366:(61,75),1023367:(65,65)}),(1950,{1023362:(60,59),1023363:(61,75),1023364:(54,66),1023365:(65,66),1023366:(61,59),1023367:(54,65)})]:orders+=moves(f,g)
items.append(dict(kind='bridge',tag='traffic-two-plane',source=str(source),text=t,last=2400,actor_ids=list(range(1023362,1023368)),ground_vehicle_ids=list(range(1023362,1023366)),actor_health={**{str(u):200 for u in range(1023362,1023366)},'1023366':125,'1023367':125},upper_ids=[1023362,1023363],lower_ids=[1023364,1023365],goals={str(u):list(x) for u,x in g.items()},orders=orders,scope='Ordinary opposing traffic on original bridge upper plane and previously validated clear underdeck corridor. Only Units/Infantry sections changed.'))
source=R/next(x for x in read(O/'bridge-cross-release-fixtures.json')['fixtures'] if x['name']=='north')['path'];old=source.read_text(encoding='ascii')
t=section(old,'Units',unit(0,60,62)+unit(1,59,70,1,'Sleep')+unit(2,60,70,1,'Sleep')+unit(3,61,70,1,'Sleep'));t=section(t,'Infantry',foot(0,61,74))
orders=moves(5,{1023362:(60,75),1023366:(61,61)})
for f,g in [(1200,{1023363:(59,79)}),(1300,{1023365:(61,79)}),(1400,{1023364:(60,79)}),(1500,{1023362:(60,75)}),(1800,{1023366:(61,78)}),(2000,{1023362:(60,61)}),(2050,{1023363:(59,59),1023364:(60,59),1023365:(61,59)}),(2800,{1023362:(60,76),1023363:(59,79),1023364:(60,79),1023365:(61,79),1023366:(61,59)})]:orders+=moves(f,g)
items.append(dict(kind='congestion',tag='traffic-long-block',source=str(source),text=t,last=3600,actor_ids=list(range(1023362,1023367)),ground_vehicle_ids=list(range(1023362,1023366)),actor_health={**{str(u):200 for u in range(1023362,1023366)},'1023366':125},main_id=1023362,blocker_ids=[1023363,1023364,1023365],release_frames={'1023363':1200,'1023365':1300,'1023364':1400},explicit_recovery_order=1500,goals={str(u):list(x) for u,x in g.items()},orders=orders,scope='Ordinary Sleep placement across bridge exit, staggered Move releases and one documented same-goal recovery order; no claim of autonomous recovery until raw positions prove it.'))
source=R/'evidence/movement-state-v38/fixtures/tube-curved-east.MAP';old=source.read_text(encoding='ascii')
t=section(old,'Units',unit(0,67,114)+unit(1,65,114)+unit(2,79,114)+unit(3,82,114));t=section(t,'Infantry','')
orders=[]
for f,g in [(5,{1022581:(80,114)}),(100,{1022582:(81,114)}),(350,{1022583:(66,114)}),(450,{1022584:(65,114)}),(800,{1022581:(66,114),1022582:(65,114),1022583:(80,114),1022584:(81,114)}),(1600,{1022581:(80,114),1022582:(81,114),1022583:(66,114),1022584:(65,114)})]:orders+=moves(f,g)
items.append(dict(kind='tube',tag='traffic-tu',tube_steps=10,source=str(source),text=t,last=2400,actor_ids=list(range(1022581,1022585)),ground_vehicle_ids=list(range(1022581,1022585)),actor_health={str(u):200 for u in range(1022581,1022585)},goals={str(u):list(x) for u,x in g.items()},orders=orders,observer_tag='traffic-tu-obs',observer_baseline_tag='b-traffic-tu-obs',scope='Four ordinary trucks on existing flat bidirectional ten-step curved Tubes; staggered starts and three rounds. Only unit placement changes; no engine state, exit constructor or route/queue injection.'))
for item in items:
 p=S/'fixtures'/(item['tag']+'.MAP');assert not p.exists();t=item.pop('text');p.write_text(t,encoding='ascii',newline='\n')
 source=Path(item['source']);before=source.read_text(encoding='ascii')
 strip=lambda text:section(section(text,'Units',''),'Infantry','')
 assert strip(t)==strip(before)
 item.update(path=p.relative_to(R).as_posix(),sha256=sha(p),source_sha256=sha(source),baseline_tag='b-'+item['tag'],cell_catalog=True,capture_host=False,stationary_health={},map_bytes_unchanged=False,unchanged_outside_units_infantry=True,seconds=300)
write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=3,ordinary_map_and_move_events=True,terrain_and_tubes_and_overlays_unchanged=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False))
print(dict(passed=True,recipes=3,production_frames_each=[x['last']+1 for x in items]))
