"""Distinct flat and elevated traffic channels, with ordinary arrival/reissue orders."""
from run_batch_v62 import *
old=next(x for x in read(O/'traffic-fixtures.json')['fixtures'] if x['tag']=='traffic-long-cross')
source=R/old['path'];flat=S/'fixtures/traffic-channel-flat.MAP';assert not flat.exists();shutil.copy2(source,flat)
item=dict(old);orders=list(old['orders'])
for f,goals in [(900,{1023363:(139,102),1023366:(139,103),1023367:(143,99),1023368:(141,104)}),(1450,{1023363:(140,104),1023366:(144,100),1023367:(145,99),1023368:(139,104)}),(2150,{1023363:(139,102),1023366:(139,105),1023367:(145,99),1023368:(140,105)})]:
 for u,(x,y) in goals.items():orders.append(f'{f}:{u}:2:{x}:{y}')
item.update(path=flat.relative_to(R).as_posix(),sha256=sha(flat),source=str(source),source_sha256=sha(source),tag='traffic-channel-flat',baseline_tag='b-traffic-channel-flat',channel_kind='flat',expected_height=0,orders=orders,arrival_reissue_required=True,scope='Flat coastal channel with four active rounds and added ordinary same-goal orders after arrival.')
parent=read(O/'bridge-cross-release-fixtures.json')['fixtures'][0];source=R/parent['path'];deck=S/'fixtures/traffic-channel-deck.MAP';assert not deck.exists();shutil.copy2(source,deck)
orders=list(parent['orders'])
for f,goals in [(600,{1023362:(60,61),1023363:(61,63),1023364:(60,64),1023367:(61,76)}),(700,{1023362:(61,72),1023367:(61,74)}),(800,{1023363:(61,65)}),(1100,{1023362:(60,78),1023363:(61,77),1023364:(60,76),1023367:(61,61)}),(1200,{1023362:(60,71),1023364:(61,75)}),(1600,{1023362:(60,75),1023363:(61,79),1023364:(60,79),1023367:(61,72)}),(1750,{1023367:(61,61)}),(2200,{1023362:(60,75),1023363:(61,79),1023364:(60,79),1023367:(61,61)})]:
 for u,(x,y) in goals.items():orders.append(f'{f}:{u}:2:{x}:{y}')
bridge=dict(path=deck.relative_to(R).as_posix(),sha256=sha(deck),source=str(source),source_sha256=sha(source),last=2400,tag='traffic-channel-deck',baseline_tag='b-traffic-channel-deck',capture_host=False,cell_catalog=True,channel_kind='deck',expected_height=416,actor_ids=[1023362,1023363,1023364,1023367],ground_vehicle_ids=[1023362,1023363,1023364],actor_health={'1023362':200,'1023363':200,'1023364':200,'1023367':125},stationary_health={'1023365':125,'1023366':125,'1023368':125,'1023369':125},orders=orders,goals={'1023362':[60,75],'1023363':[61,79],'1023364':[60,79],'1023367':[61,61]},activity_windows=[[0,550],[600,1050],[1100,1550],[1600,2250]],arrival_reissue_required=True,scope='Elevated channel: original waiting/release prefix, counterflow and repeated rounds, then same-goal arrival reissue.')
for x in [item,bridge]:assert x['sha256']==x['source_sha256']
write(S/'traffic-fixtures.json',dict(passed=True,fixtures=[item,bridge],new_unique_recipes=2,distinct_channels=['flat','deck'],ordinary_map_and_move_events=True,map_bytes_unchanged=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False,frames_each=2401,activity_rounds=4))
print(dict(passed=True,channels=['flat','deck'],frames_each=2401))
