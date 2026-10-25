"""Retain the offset mixed-route failure and adopt centerline ordinary exit goals."""
from run_batch_v66 import *
current=read(S/'traffic-fixtures.json');x=next(r for r in current['fixtures'] if r['kind']=='mixed');assert x['tag']=='traffic-cm'
exclusions=read(S/'traffic-exclusions.json');comparisons=[]
for tag in [x['baseline_tag'],x['observer_baseline_tag']]:
 p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed'];comparisons.append(dict(path=str(p),sha256=sha(p),strict_original_c_equal=True,frames=q['comparison']['frames_compared']))
exclusions['records'].append(dict(kind='mixed-offset-unfinished',recipe=x,map_path=str(R/x['path']),map_sha256=sha(R/x['path']),comparisons=comparisons,accepted_as_positive_fairness_scene=False,all_goals_reached=False,example_actor=1023312,example_final_cell=[57,76],example_goal=[79,74],reason='Original and C both finish some offset-target requests on the west side without reaching the requested goals. Retain the complete strict traces; a failed ordinary route does not prove a Tube exit starvation defect.'))
p=S/'runs/id-cq2/comparison.json';q=read(p);assert not q['passed'] and all(r['exit_code']==7 and r['state_sha256'] is None for r in q['runs'])
exclusions['records'].append(dict(kind='calibration-order-range-error',comparisons=[dict(path=str(p),sha256=sha(p))],accepted_as_positive_fairness_scene=False,simulation_started=False,reason='The calibration helper carried movement orders outside its 0:1 trace range. Both modes rejected the setup before simulation. Repeat with orders cleared and a fresh tag, retaining this rejected receipt.'))
(S/'traffic-exclusions.json').write_text(json.dumps(exclusions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old_path=R/x['path'];p=S/'fixtures/traffic-cm2.MAP';assert not p.exists();shutil.copy2(old_path,p);assert sha(p)==x['sha256']
x=dict(x);x.update(tag='traffic-cm2',path=p.relative_to(R).as_posix(),baseline_tag='b-traffic-cm2',observer_tag='traffic-cm2-obs',observer_baseline_tag='b-traffic-cm2-obs')
for e in x['events']:
 if e['stage']=='request':e['cell']=[73+e['slot'],76];x['goals'][str(e['id'])]=e['cell']
x['orders']=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']]
current['fixtures']=[x if r['kind']=='mixed' else r for r in current['fixtures']]
(S/'traffic-fixtures.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
provenance=read(S/'traffic-map-provenance.json')
for e in provenance['maps']:
 if e['path'].endswith('/traffic-cm.MAP'):e['path']=x['path']
(S/'traffic-map-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proof=S/'runs/id-cm/comparison.json';assert read(proof)['scenario_sha256']==sha(p)
write(S/'mixed-centerline-adoption.json',dict(passed=True,map_bytes_identical_to_calibration=True,calibration=str(proof),calibration_sha256=sha(proof),map_sha256=sha(p),ordinary_goal_commands_changed_only=True,goals=[x['goals'][str(u)] for u in x['actor_ids']]))
print(dict(passed=True,tag=x['tag'],map_bytes_unchanged=True,calibration_reused_by_exact_hash=True))
