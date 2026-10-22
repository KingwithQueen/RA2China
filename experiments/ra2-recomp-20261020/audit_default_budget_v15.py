"""Strict default-rule real-object budget gate, separate from the production matrix."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v15'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
receipt=read(S/'truck-actor-fixture-receipt.json')
assert receipt['production_exe_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
assert receipt['fixture_exe_sha256']==sha(S/'truck-actor-fixture-probe.exe')
assert receipt['fixture_source_sha256']==sha(S/'truck_actor_movement_fixture.c')
assert receipt['object_count']==126
for x in receipt['objects']:assert sha(Path(x['path']))==x['sha256']
scenes={}
for tag,last in [('h-default-budget',900)]:
    x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
    assert x['passed'] and x['exe_sha256']==receipt['fixture_exe_sha256']
    assert x['scenario_rules_sha256'] is None and x['starting_units'] is None and x['seed']==12345
    assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==last+1
    assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
    for run in x['runs']:assert run['passed'] and run['exit_code']==0 and run['save_before']==run['save_after']
    a=rows(tag,'original');b=rows(tag,'generated-c')
    select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
    assert select(a)==select(b)
    modes={}
    for mode,records in [('original',a),('generated-c',b)]:
        actor=next(r for r in records if r['kind']=='fixture-actor');uid=actor['id'];assert actor['type']=='TRUCKA'
        placed=[r for r in records if r['kind']=='fixture-unit'];assert len(placed)==16
        assert not any(r['kind']=='fixture-occupied' for r in records)
        constraints=next(r for r in records if r['kind']=='fixture-constraints')
        assert constraints['close_enough']==576 and constraints['accepted_before']==constraints['accepted_after']==1
        assert constraints['explicit_rebuild_result']==0xFFFFFFFF
        events=[r for r in records if r.get('kind')=='movement-audit' and r['id']==uid]
        budget=[r for r in events if r['stage']==3]
        assert [r['frame'] for r in budget]==list(range(27,38))
        assert [r['value'] for r in budget]==list(range(10,-1,-1))
        failed=[r for r in events if r['stage']==6 and not r['value'] and r['frame']<=37]
        assert [r['frame'] for r in failed]==list(range(27,38))
        assert all(r['active_is_caller'] and r['caller_goal_valid'] and r['active_ground_drive'] for r in failed)
        samples={r['frame']:next(o for o in r['objects'] if o['id']==uid) for r in records if r['kind']=='state' and r['frame']>=27}
        for frame in range(28,38):assert samples[frame]['ground_drive']['path_failure_counter']==37-frame
        stopped=samples[38]['ground_drive']
        assert stopped['path_failure_counter']==0 and stopped['destination']==stopped['segment_end']==[0,0,0]
        assert all(samples[f]['ground_drive']['destination']==[0,0,0] for f in range(38,241))
        distances=[]
        for f in range(27,38):
            o=samples[f];d=o['ground_drive']['destination'];p=o['position']
            distances.append((d[0]-p[0])**2+(d[1]-p[1])**2)
        assert min(distances)>576**2
        modes[mode]=dict(actor=actor,real_units_placed=16,constraints=constraints,budget_events=budget,failed_rebuilds=failed,
            stop_frame=38,stopped_through_frame=240,post_stop=stopped,minimum_goal_distance_squared=min(distances),
            last_state=samples[last]['ground_drive'])
    scenes[tag]=dict(passed=True,frames_compared=last+1,exe_sha256=x['exe_sha256'],modes=modes)
result=dict(passed=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
    formal_executable_sha256=receipt['production_exe_sha256'],fixture_executable_sha256=receipt['fixture_exe_sha256'],
    scope='Unmodified default rules in the original skirmish map, with an explicitly created and initially ordered real AI TRUCKA plus 16 real enemy TRUCKA blockers. Natural subsequent search/recovery; no explicit search or direct state/budget/path writes. Not an untouched random match.',
    callback_scope='Same Drive and restored valid goal observed after failed Prepare; exact 4C3895 callback site remains static/state evidence, not separately hooked.',
    scenes=scenes,independent_long_scene='h-default-budget',independent_long_frames=901,
    incomplete_heap_checkpoint=str(R/'evidence/movement-state-v13/investigations/heap-before-inc-rule'),
    necessary_conditions=['AI owner can restore a destination after failed search','Unarmed actor avoids combat overriding the move','All fallback goals remain beyond default CloseEnough=576','Closed boundary is placed through normal services, retaining the terrain zone','Failed Prepare returns with the same Drive and a valid goal; the subsequent recovery consumes the normal budget'])
(S/'budget-real-scenes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=True,default_rules_exhaustion=True,frames=901,budget_frames=[27,37],stop_frame=38)))
