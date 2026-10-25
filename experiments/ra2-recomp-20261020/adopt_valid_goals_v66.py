"""Correct the interpretation using native terrain data; keep every rejected input and trace."""
from run_batch_v66 import *
current=read(S/'traffic-fixtures.json');old=next(x for x in current['fixtures'] if x['kind']=='mixed');assert old['tag']=='traffic-cm3'
catalog=S/'runs/id-cm/original/cells.json';cells={tuple(c['cell']):c for c in read(catalog)['cells']};review=[]
for name in ['traffic-fixtures-initial.json']:
 recipe=next(x for x in read(S/name)['fixtures'] if x['kind']=='mixed')
 review.append(dict(tag=recipe['tag'],unusable_goals=[dict(id=int(u),cell=p,terrain=cells[tuple(p)]) for u,p in recipe['goals'].items() if cells[tuple(p)]['land'] not in [0,1,6,7] or cells[tuple(p)]['level']!=4]))
for recipe in [next(e['recipe'] for e in read(S/'traffic-exclusions.json')['records'] if e['kind']=='mixed-dense-centerline-unfinished'),old]:
 review.append(dict(tag=recipe['tag'],unusable_goals=[dict(id=int(u),cell=p,terrain=cells[tuple(p)]) for u,p in recipe['goals'].items() if cells[tuple(p)]['land'] not in [0,1,6,7] or cells[tuple(p)]['level']!=4]))
assert all(r['unusable_goals'] for r in review)
comparisons=[]
for tag in [old['baseline_tag'],old['observer_baseline_tag']]:
 p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed'];comparisons.append(dict(path=str(p),sha256=sha(p),strict_original_c_equal=True,frames=q['comparison']['frames_compared']))
excluded=read(S/'traffic-exclusions.json');excluded['records'].append(dict(kind='mixed-lower-rate-invalid-goals',recipe=old,map_path=str(R/old['path']),map_sha256=sha(R/old['path']),comparisons=comparisons,accepted_as_positive_fairness_scene=False,all_goals_reached=False,actual_tube_actors=6,completed_requests=6,uncompleted_requests=10,arrival_period=300,interpretation_corrected_by=str(S/'mixed-target-terrain-review.json')))
for e in excluded['records']:
 if e['kind'].startswith('mixed-'):
  e['original_queue_bug_proved']=False;e['load_boundary_proved']=False;e['current_interpretation']='Invalid rock/water goals are present in these rejected ordinary inputs. Earlier congestion/load wording is superseded by the native terrain review; no supported saturation or starvation conclusion follows.'
(S/'traffic-exclusions.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'mixed-target-terrain-review.json',dict(passed=True,catalog=str(catalog),catalog_sha256=sha(catalog),review=review,prior_load_interpretation_withdrawn=True,original_queue_bug_proved=False,scope='Native cell land/height data establishes invalid goals. Strict original/C equality and unfinished goals are retained facts; their cause cannot be labeled a queue load boundary from these recipes.'))
x=dict(old);p=S/'fixtures/traffic-cm4.MAP';assert not p.exists();shutil.copy2(R/old['path'],p);assert sha(p)==old['sha256']
x.update(tag='traffic-cm4',path=p.relative_to(R).as_posix(),baseline_tag='b-traffic-cm4',observer_tag='traffic-cm4-obs',observer_baseline_tag='b-traffic-cm4-obs',arrival_period=180,arrival_end=3500)
x['events']=[dict(e) for e in old['events']]
for e in x['events']:
 if e['stage'] in ['bridge','approach','request']:e['frame']={'bridge':5,'approach':450,'request':800}[e['stage']]+180*e['slot']
 if e['stage']=='request':
  i=e['slot'];e['cell']=[73+i,76] if i<6 else [73+i-6,78] if i<12 else [73+i-12,74]
 if e['stage']=='release':e['cell']=[[74,80],[76,80],[78,80]][e['slot']-16]
x['orders']=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']]
x['request_frames']={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='request'};x['goals']={str(e['id']):e['cell'] for e in x['events']}
assert len(set(tuple(p) for p in x['goals'].values()))==19
for e in x['events']:
 c=cells[tuple(e['cell'])];assert c['land'] in [0,1,6,7] and c['level']==4,(e,c)
current['fixtures']=[x if r['kind']=='mixed' else r for r in current['fixtures']]
(S/'traffic-fixtures.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
provenance=read(S/'traffic-map-provenance.json')
for e in provenance['maps']:
 if e['path'].endswith('/traffic-cm3.MAP'):e['path']=x['path']
(S/'traffic-map-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proof=S/'runs/id-cm/comparison.json';assert read(proof)['scenario_sha256']==sha(p)
write(S/'mixed-valid-goal-adoption.json',dict(passed=True,map_bytes_identical_to_calibration=True,calibration=str(proof),calibration_sha256=sha(proof),map_sha256=sha(p),ordinary_goal_commands_changed=True,arrival_period=180,arrival_window=[800,3500],all_final_and_intermediate_goal_cells_terrain_checked=True))
print(dict(passed=True,tag=x['tag'],goals_validated=19,all_move_targets_validated=True,prior_load_interpretation_withdrawn=True))
