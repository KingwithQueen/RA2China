"""Bind the nearby ordinary bridge/Tube map; retain the remote candidate as excluded evidence."""
from run_batch_v65 import *
p=S/'runs/id-m3/comparison.json';c=read(p);assert c['passed'] and c['comparison']['frames_compared']==2
rows=[json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8')];first=next(r for r in rows if r['kind']=='state');objects={tuple(v//256 for v in o['position'][:2]):o for o in first['objects'] if o.get('ground_drive')}
ids=[objects[point]['id'] for point in [(60,61),(61,60),(60,59),(61,58)]]
fixtures=read(S/'traffic-fixtures.json');old=next(x for x in fixtures['fixtures'] if x['kind']=='mixed');assert old['tag']=='traffic-m'
shutil.copy2(S/'traffic-fixtures.json',S/'traffic-fixtures-initial.json')
evidence=[]
for tag in [old['baseline_tag'],old['observer_baseline_tag']]:
 q=S/'runs'/tag/'comparison.json';x=read(q);assert x['passed'];evidence.append(dict(path=str(q),sha256=sha(q),raw_strict=True))
write(S/'mixed-remote-exclusion.json',dict(passed=True,accepted_as_positive_scene=False,old_recipe=old,comparisons=evidence,reason='Remote ordinary ground detour did not complete intermediate waypoints before later orders; no actual Tube progression was observed. Retained as a failed recipe, not attributed to a proved original Tube bug.',production_or_rules_changed=False))
relocation=read(S/'mixed-relocation-rle.json');item=dict(old);item.update(tag='traffic-m3',baseline_tag='b-traffic-m3',observer_tag='traffic-m3-obs',observer_baseline_tag='b-traffic-m3-obs',path=relocation['path'],sha256=relocation['sha256'],slot_ids=ids,actor_ids=ids,ground_vehicle_ids=ids,actor_health={str(u):200 for u in ids},last=3500,seconds=300,scope='Four ordinary trucks cross the original bridge, use a nearby translated legal curved Tube in both directions, then return across the bridge. A 189-cell terrain/overlay patch is copied from the validated Tube map; original bridge bytes remain unchanged.')
orders=[];events=[];goals={}
for f in [5,450,800,1500,2200,2600]:
 for i,u in enumerate(ids):
  point={5:(60+i%2,79-2*(i//2)),450:(59-i,76),800:(76-i,76),1500:(56+i,76),2200:(60+i%2,75+2*(i//2)),2600:(59+2*(i%2),55+2*(i//2))}[f]
  orders.append(f'{f}:{u}:2:{point[0]}:{point[1]}');events.append(dict(frame=f,slot=i,id=u,cell=list(point)));goals[str(u)]=list(point)
item.update(orders=orders,events=events,goals=goals)
fixtures['fixtures']=[item if x['kind']=='mixed' else x for x in fixtures['fixtures']]
(S/'traffic-fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog=read(S/'actor-catalog-validation.json');catalog['catalogs'].append(dict(tag='id-m3',comparison_sha256=sha(p),actor_ids=ids,frames=2,excluded_from_movement_acceptance=True));(S/'actor-catalog-validation.json').write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,ids=ids,last=3500,original_remote_recipe_retained=True))
