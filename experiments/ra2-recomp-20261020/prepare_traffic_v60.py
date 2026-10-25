"""Two ordinary traffic recipes on the exact previously verified coastal map."""
from run_batch_v60 import *
old=next(x for x in read(O/'dynamic-fixtures.json')['fixtures'] if x['tag']=='sc')
source=R/old['path'];destination=S/'fixtures/traffic-coast-original.MAP';assert not destination.exists()
shutil.copy2(source,destination)
assert sha(source)==sha(destination)
common=dict(path=destination.relative_to(R).as_posix(),sha256=sha(destination),source=str(source),source_sha256=sha(source),terrain_pack_sha256=old['terrain_pack_sha256'],last=900,capture_host=False,cell_catalog=True,actor_ids=[1023363,1023366,1023367,1023368],ground_vehicle_ids=[1023363,1023366,1023367],actor_health={'1023363':200,'1023366':200,'1023367':200,'1023368':125},stationary_health={'1023362':300,'1023364':600,'1023369':125})
items=[dict(**common,tag='traffic-cross',baseline_tag='b-traffic-cross',orders=['5:1023363:2:145:98','5:1023366:2:141:105','5:1023367:2:144:100','5:1023368:2:141:99','35:1023363:2:140:104','45:1023367:2:139:105','80:1023368:2:144:99','140:1023366:2:143:101'],goals={'1023363':[140,104],'1023366':[143,101],'1023367':[139,105],'1023368':[144,99]},scope='Three trucks and one infantry cross nearby ordinary land; moving orders replace earlier destinations.'),
dict(**common,tag='traffic-convoy',baseline_tag='b-traffic-convoy',orders=['5:1023363:2:145:98','15:1023366:2:145:99','25:1023367:2:144:100','5:1023368:2:143:101','150:1023363:2:139:104','150:1023366:2:140:104','150:1023367:2:141:104','150:1023368:2:139:100','220:1023363:2:143:100'],goals={'1023363':[143,100],'1023366':[140,104],'1023367':[141,104],'1023368':[139,100]},scope='Staggered vehicle departures with infantry traffic, reversal orders and one later destination replacement.')]
write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=2,ordinary_map_and_move_events=True,map_bytes_unchanged=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False))
print(dict(passed=True,new_recipes=2,map_sha256=sha(destination)))
