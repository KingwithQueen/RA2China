"""严格核对完整有序轨迹、实际分支、片段与构建身份，不接受旧批次的两条例外。"""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v13'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=S/name;assert not p.exists(),p;p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
matrices=[read(S/'f-matrix.json'),read(S/'g-additional-matrix.json')]
assert all(m['passed'] for m in matrices)
cases=[r for m in matrices for r in m['results']];assert len(cases)==27 and sum(r['frames'] for r in cases)==14897
exe=R/'ra2/build-original-c/ra2.exe';fingerprint=sha(exe)
assert all(m['exe_sha256']==fingerprint for m in matrices)
def rows(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def events(tag,stage):return [r for r in rows(tag) if r['kind']=='movement-audit' and r['stage']==stage]
for row in cases:
    x=read(S/'runs'/row['tag']/'comparison.json');c=x['comparison']
    assert x['passed'] and row['passed'] and x['exe_sha256']==fingerprint and x['seed']==12345
    assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==row['frames']
    assert c['command_difference'] is None and c['first_difference'] is None and c['rng_equal_all_frames']
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
    assert all(r['passed'] and r['exit_code']==0 and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
    a=rows(row['tag']);b=rows(row['tag'],'generated-c')
    assert a[0]['schema']==b[0]['schema']==12
    select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
    assert select(a)==select(b),row['tag']
    assert not any(r['kind'] in ('path-detail','cell-entry-detail') for r in a+b)
previous={e['path']:e['sha256'] for e in read(S/'baseline/source-manifest.json')}
for rel in ['run_fixture_comparison.py','run_state_comparison.py']:
    assert sha(R/rel)==previous[rel],rel
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['executable_sha256']==fingerprint and receipt['source_count']==118
for p,digest in receipt['inputs'].items():assert sha(Path(p))==digest,p
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
assert 'ra2_path_diag' not in (R/'ra2/src/recomp/gen_game/recomp_0003.c').read_text(encoding='utf-8')
probes={p.name:read(p) for p in S.glob('*-verified-01.json')}
assert len(probes)==44 and all(p['passed'] for p in probes.values())
assert probes['path-cost-probe-verified-01.json']['cases']==786432
aux=read(S/'auxiliary-final-01/validation.json');assert aux['passed'] and aux['exe_sha256']==fingerprint

# 原有十五场景的效果门槛读取本轮实际轨迹，保留墙、门、临时/隐形障碍、模板、二次路径等检查。
source=(R/'audit_movement_v7.py').read_text(encoding='utf-8')
source=source[:source.index('investigation = read(STAGE/')]
source=source.replace('movement-state-v7','movement-state-v13').replace("'c-","'f-").replace('runs/c-','runs/f-')
scope={'__file__':str(R/'audit_movement_v7.py'),'__name__':'audit_effects_only'}
exec(compile(source,str(R/'audit_movement_v7.py'),'exec'),scope)
effect,budget=scope['effect'],scope['budget']
tags=[r['tag'] for r in cases]
allied={tag:len(events(tag,25)) for tag in tags};geometry={tag:len(events(tag,26)) for tag in tags}
zero=[dict(scene=tag,**r) for tag in tags for r in events(tag,27) if not r['auxiliary'] and (r['value']&0x7FFFFFFF)==0]
assert geometry['f-congestion-01']>0 and zero
effect['allied_motion']=dict(entries=allied,geometry_entries=geometry,total_entries=sum(allied.values()),total_geometry_entries=sum(geometry.values()))
effect['terrain_tail']=dict(zero_speed_events=zero,total_entries=sum(len(events(tag,27)) for tag in tags))
turn=events('g-tc1',19);assert len(turn)==1 and turn[0]['frame']==197 and turn[0]['value']==1
hard=events('g-ur3',19);assert any(r['frame']==52 and r['value']==7 for r in hard)
for tag in ['g-second-failure','g-repeat-failure']:
    ev=events(tag,18);assert len(ev)==1 and ev[0]['frame']==399 and not ev[0]['caller_goal_valid']
failed=[r for r in events('g-repeat-failure',6) if not r['value']]
assert [r['frame'] for r in failed]==list(range(451,1112,60))
assert all(r['active_is_caller'] and not r['caller_goal_valid'] for r in failed)
natural=[tag for tag in tags if tag not in ['f-budget-entry','f-budget-natural']]
budget['natural_budget_entries']=[dict(scene=tag,**r) for tag in natural for r in events(tag,3)]
assert not budget['natural_budget_entries']
budget['natural_exhaustion_verified']=False
budget['new_static_followup']='4C371A Stop is followed by callbacks; 4C3895 may set a new destination via Unit 7053F0 -> 4C8030 -> locomotor MoveTo 4C8165. Requires a legal scene showing goal restored before failed Prepare returns.'
budget['repeated_failure']=dict(frames=[r['frame'] for r in failed],same_drive_goal_cleared=True,natural_exhaustion_verified=False)
effect['passed']=True
write('effects.json',effect);write('budget-conditions.json',budget)
write('strict-acceptance.json',dict(passed=True,exe_sha256=fingerprint,paired_scenes=27,paired_frames=14897,
    strict_ordered_audit_passed=True,frame_comparison_passed=True,probes=probes,comparator_unchanged=True,
    source_content_verified=True,diagnostics_removed=True,natural_budget_exhaustion_verified=False,
    full_original_equivalence_verified=False))
print(json.dumps(dict(passed=True,scenes=27,frames=14897,probes=len(probes),allied_entries=sum(allied.values()),geometry_entries=sum(geometry.values()),zero_speed_entries=len(zero))))
