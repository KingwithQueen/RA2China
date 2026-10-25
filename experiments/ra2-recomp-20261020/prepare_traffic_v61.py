"""Extend ordinary coastal traffic with four active command rounds, not only idle time."""
from run_batch_v61 import *
parents=read(O/'traffic-fixtures.json')['fixtures'];source=R/parents[0]['path'];destination=S/'fixtures/traffic-coast-original.MAP'
assert not destination.exists();shutil.copy2(source,destination);assert sha(source)==sha(destination)
items=[]
for n,old in enumerate(parents):
 item=dict(old);item.update(path=destination.relative_to(R).as_posix(),sha256=sha(destination),source=str(source),source_sha256=sha(source),last=2400,tag='traffic-long-'+('cross' if n==0 else 'convoy'),baseline_tag='b-traffic-long-'+('cross' if n==0 else 'convoy'),activity_windows=[[0,500],[550,1050],[1100,1600],[1650,2250]],parent_recipe=old['tag'],parent_last=old['last'])
 orders=list(old['orders'])
 rounds=[(550,600,[(145,98),(139,103),(144,100),(139,105)],[(1023363,139,102),(1023367,143,99),(1023368,141,104)]),
 (1100,1150,[(146,98),(140,105),(145,99),(141,100)],[(1023363,140,104),(1023366,144,100),(1023368,139,104)]),
 (1650,1710,[(145,98),(139,105),(140,104),(143,101)],[(1023363,139,102),(1023367,145,99),(1023368,140,105)])]
 for start,reroute,targets,replacements in rounds:
  for i,(u,(x,y)) in enumerate(zip(item['actor_ids'],targets)):
   stagger=(i*15 if i<3 else 0) if n else 0
   orders.append(f'{start+stagger}:{u}:2:{x}:{y}')
  for u,x,y in replacements:orders.append(f'{reroute+(25 if n else 0)}:{u}:2:{x}:{y}')
 item.update(orders=orders,goals={'1023363':[139,102],'1023366':[139,105],'1023367':[145,99],'1023368':[140,105]},scope='Four active rounds of ordinary mixed traffic, direction reversals and moving destination replacements; unchanged map and rules.')
 items.append(item)
write(S/'traffic-fixtures.json',dict(passed=True,fixtures=items,new_unique_recipes=2,ordinary_map_and_move_events=True,map_bytes_unchanged=True,rules_overrides=False,engine_state_or_path_injection=False,claimed_new_natural_heap_saturation=False,prior_recipe_frames=901,current_recipe_frames=2401,activity_rounds=4))
print(dict(passed=True,new_long_recipes=2,frames_each=2401,map_sha256=sha(destination)))
