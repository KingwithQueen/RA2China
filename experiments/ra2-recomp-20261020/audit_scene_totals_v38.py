"""Reconcile the formal production count against actual completed final-executable pairs."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=sha(R/'ra2/build-original-c/ra2.exe')
groups={
    'main_matrix':[v['tag'] for n in ['t-matrix.json','u-additional-matrix.json'] for v in read(S/n)['results']],
    'final_checkpoint_production':['c-final-default','c-final-tube-east','c-final-tube-west','c-final-tube-blocked'],
    'additional_tube_production':['z-tube-production-uphill','z-tube-production-downhill','z-ce','z-cw','z-cu','z-cd','z-cb','z-tu','z-td'],
    'combined_production':['x-ub','x-db','x-mu','x-md'],
}
for key,metadata,prefix in [('bridge_chain','bridge-fixtures.json','b-'),('bridge_mixed','bridge-mixed-fixtures.json','mp-'),('bridge_hostile','bridge-hostile-fixtures.json','ep-'),('bridge_infantry','bridge-infantry-fixtures.json','ip-'),('north_query','north-query-fixtures.json','np-'),('occupied_bridge','bridge-occupied-fixtures.json','op-'),('held_exit_detour','bridge-detour-fixtures.json','dp-'),('staggered_exit','bridge-staggered-fixtures.json','sp-'),('main_lane_release','bridge-lane-release-fixtures.json','lp-'),('neighbor_lane_release','bridge-neighbor-release-fixtures.json','nr-')]:
    groups[key]=[prefix+v['name'] for v in read(S/metadata)['fixtures']]
tags=[t for ts in groups.values() for t in ts];assert len(tags)==len(set(tags))==71
totals={};inputs=[Path(__file__)];total=0
for name,scene_tags in groups.items():
    frames=0
    for tag in scene_tags:
        p=S/'runs'/tag/'comparison.json';v=read(p);c=v['comparison']
        assert v['passed'] and v['exe_sha256']==digest,tag
        assert c['equal_frames']==c['consecutive_equal_frames']==c['frames_compared'] and c['rng_equal_all_frames'],tag
        assert c['first_difference'] is None and c['command_difference'] is None,tag
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected'],tag
        frames+=c['frames_compared'];inputs.append(p)
    totals[name]=dict(scenes=len(scene_tags),frames=frames,tags=scene_tags);total+=frames
assert total==49241
excluded=[]
for p in sorted((S/'runs').glob('*/comparison.json')):
    v=read(p);tag=p.parent.name
    if v.get('exe_sha256')!=digest or tag in tags:continue
    assert v['passed'] and (tag=='c-final-ur3' or tag.startswith('trial-')),tag
    excluded.append(dict(tag=tag,frames=v['comparison']['frames_compared'],formal_count=0,reason='Short part-checkpoint regression retained separately' if tag=='c-final-ur3' else 'Exploration trial retained separately'))
value=dict(passed=True,production_scenes=len(tags),production_frames=total,production_executable_sha256=digest,
    groups=totals,excluded_final_executable_runs=excluded,
    observer_budget_not_counted_as_production=True,part_checkpoint_short_regression_not_double_counted=True,
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'production-scene-totals.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,production_scenes=len(tags),production_frames=total,excluded_runs=len(excluded))))
