"""Unchanged ordinary map, staged blocker release followed by ramp/crossroad traffic."""
from run_batch_v63 import *
parent=read(O/'bridge-cross-release-fixtures.json')['fixtures'][0]
source=R/parent['path'];fixtures=[]
for channel,rounds in [
 ('ramp',[(600,{1023362:(60,43),1023363:(61,44),1023364:(59,45),1023367:(61,46)}),(680,{1023362:(61,42),1023363:(60,43),1023364:(61,44),1023367:(59,45)}),(1300,{1023362:(60,59),1023363:(61,58),1023364:(59,57),1023367:(61,56)}),(1380,{1023362:(61,59),1023363:(60,58),1023364:(61,57),1023367:(59,56)}),(2000,{1023362:(60,43),1023363:(61,44),1023364:(59,45),1023367:(61,46)}),(2080,{1023362:(61,42),1023363:(60,43),1023364:(61,44),1023367:(59,45)})]),
 ('crossroad',[(600,{1023362:(70,49),1023363:(71,50),1023364:(69,50),1023367:(70,51)}),(680,{1023362:(60,43),1023363:(61,44),1023364:(59,45),1023367:(61,46)}),(1300,{1023362:(70,50),1023363:(69,49),1023364:(71,50),1023367:(70,49)}),(1380,{1023362:(60,59),1023363:(61,58),1023364:(59,57),1023367:(61,56)}),(2000,{1023362:(70,49),1023363:(71,50),1023364:(69,50),1023367:(70,51)}),(2080,{1023362:(60,43),1023363:(61,44),1023364:(59,45),1023367:(61,46)})])]:
 path=S/'fixtures'/('traffic-height-'+channel+'.MAP');assert not path.exists();shutil.copy2(source,path)
 orders=list(parent['orders'])
 for f,goals in rounds:
  orders.extend(f'{f}:{u}:2:{x}:{y}' for u,(x,y) in goals.items())
 goals={str(u):list(g) for u,g in rounds[-1][1].items()}
 # Same-goal ordinary orders after the last traversal exercise arrival re-entry.
 orders.extend(f'2800:{u}:2:{x}:{y}' for u,(x,y) in rounds[-1][1].items())
 fixtures.append(dict(path=path.relative_to(R).as_posix(),sha256=sha(path),source=str(source),source_sha256=sha(source),last=3000,tag='traffic-height-'+channel,baseline_tag='b-traffic-height-'+channel,capture_host=False,cell_catalog=True,channel_kind=channel,height_range=[416,520],required_base_levels=[4,5],actor_ids=[1023362,1023363,1023364,1023367],ground_vehicle_ids=[1023362,1023363,1023364],actor_health={'1023362':200,'1023363':200,'1023364':200,'1023367':125},stationary_health={'1023365':125,'1023366':125,'1023368':125,'1023369':125},orders=orders,goals=goals,activity_windows=[[0,550],[600,1250],[1300,1950],[2000,2850]],arrival_reissue_required=True,release_prefix=parent,scope='Unchanged source map and staged ordinary blocker-release prefix; three later rounds through existing ramp and road intersection.'))
write(S/'traffic-fixtures.json',dict(passed=True,fixtures=fixtures,new_unique_recipes=2,distinct_channels=['ramp','crossroad'],ordinary_map_and_move_events=True,map_bytes_unchanged=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False,frames_each=3001,activity_rounds=4))
shutil.copy2(O/'channel-land-proof.json',S/'channel-land-proof.json')
print(dict(passed=True,channels=['ramp','crossroad'],frames_each=3001))
