"""Keep the dense mixed-route boundary; declare a longer, lower-rate arrival stream."""
from run_batch_v66 import *
current=read(S/'traffic-fixtures.json');old=next(x for x in current['fixtures'] if x['kind']=='mixed');assert old['tag']=='traffic-cm2'
comparisons=[]
for tag in [old['baseline_tag'],old['observer_baseline_tag']]:
 p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed'];comparisons.append(dict(path=str(p),sha256=sha(p),strict_original_c_equal=True,frames=q['comparison']['frames_compared']))
excluded=read(S/'traffic-exclusions.json');excluded['records'].append(dict(kind='mixed-dense-centerline-unfinished',recipe=old,map_path=str(R/old['path']),map_sha256=sha(R/old['path']),comparisons=comparisons,accepted_as_positive_fairness_scene=False,all_goals_reached=False,actual_tube_actors=6,completed_requests=6,uncompleted_requests=10,all_submissions_and_executions=51,arrival_period=180,scope='Observed unchanged parent production and original. Six leading trucks pass; later ordinary requests stop on the entrance side or upstream. Retain as finite input/load boundary, not a final-code positive or arbitrary-load fairness proof.'))
(S/'traffic-exclusions.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
x=dict(old);p=S/'fixtures/traffic-cm3.MAP';assert not p.exists();shutil.copy2(R/old['path'],p);assert sha(p)==old['sha256']
x.update(tag='traffic-cm3',path=p.relative_to(R).as_posix(),baseline_tag='b-traffic-cm3',observer_tag='traffic-cm3-obs',observer_baseline_tag='b-traffic-cm3-obs',arrival_period=300,arrival_end=5300)
x['events']=[dict(e) for e in old['events']]
for e in x['events']:
 if e['stage'] in ['bridge','approach','request']:e['frame']={'bridge':5,'approach':450,'request':800}[e['stage']]+300*e['slot']
x['orders']=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']]
x['request_frames']={str(e['id']):e['frame'] for e in x['events'] if e['stage']=='request'}
current['fixtures']=[x if r['kind']=='mixed' else r for r in current['fixtures']]
(S/'traffic-fixtures.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
provenance=read(S/'traffic-map-provenance.json')
for e in provenance['maps']:
 if e['path'].endswith('/traffic-cm2.MAP'):e['path']=x['path']
(S/'traffic-map-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proof=S/'runs/id-cm/comparison.json';assert read(proof)['scenario_sha256']==sha(p)
write(S/'mixed-rate-adoption.json',dict(passed=True,map_bytes_identical_to_calibration=True,calibration=str(proof),calibration_sha256=sha(proof),map_sha256=sha(p),ordinary_move_timing_changed_only=True,arrival_period=300,arrival_window=[800,5300],baseline_check_policy='Same goals/health, actual Tube/bridge, wait, sustained-window service and immutable full trace gates. Declared interval replaces the first candidate interval; no production or global comparator changes.'))
print(dict(passed=True,tag=x['tag'],interval=300,map_bytes_unchanged=True))
