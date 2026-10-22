"""将逐帧等价、新模块片段验证和未消除的旧查询差异分开记录。"""
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
S=ROOT/'evidence/movement-state-v10'
OLD=ROOT/'evidence/movement-state-v9'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def records(tag,mode='original'):
    return [json.loads(x) for x in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def events(tag,stage):
    return [r for r in records(tag) if r.get('stage')==stage and r['kind']=='movement-audit']
def samples(tag):
    return [(r['frame'],o) for r in records(tag) if r['kind']=='state'
        for o in r['objects'] if o['id']==1022579 and 'ground_drive' in o]
def write(name,value):
    p=S/name;assert not p.exists();p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

main=read(S/'m-matrix.json'); extra=read(S/'m-additional-matrix.json')
assert len(main['results'])==15 and len(extra['results'])==12
cases=main['results']+extra['results']
assert main['passed'] and not extra['passed']
assert [r['tag'] for r in cases if not r['passed']]==['m-ur3']
assert sum(r['frames'] for r in cases)==14897
fingerprint=hashlib.sha256((ROOT/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()
assert main['exe_sha256']==extra['exe_sha256']==fingerprint
for row in cases:
    report=read(S/'runs'/row['tag']/'comparison.json'); c=report['comparison']
    assert report['exe_sha256']==fingerprint
    assert c['equal_frames']==c['consecutive_equal_frames']==c['frames_compared']==row['frames']
    assert c['first_difference'] is None and c['rng_equal_all_frames']
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
    original=[r for r in records(row['tag']) if r['kind'] in ('submit','execute') or r['kind'].startswith('fixture-')]
    generated=[r for r in records(row['tag'],'generated-c') if r['kind'] in ('submit','execute') or r['kind'].startswith('fixture-')]
    assert original==generated

# 既有严格比较器及 comparison.json 不改动；精确核对仅有两条已定位的额外观测。
a=[[r for r in records('m-ur3',m) if r['kind']=='movement-audit'] for m in ('original','generated-c')]
delta=[]
for op,i,j,k,l in difflib.SequenceMatcher(None,*[[json.dumps(r,sort_keys=True) for r in v] for v in a],autojunk=False).get_opcodes():
    if op=='equal': continue
    assert op=='insert' and not a[0][i:j]
    delta+=a[1][k:l]
assert len(delta)==2 and all(r['frame']==52 and r['stage']==27 and r['cell']==[69,113] for r in delta)
assert all(r['value']==0x3F800000 and r['auxiliary']==0 for r in delta)
control=read(S/'pathfinder-investigation.json')
assert control['preexisting_difference_reproduced'] and control['both_new_ports_bypassed']
assert control['new_ports_vs_baseline_control_ordered_audits_equal']
baseline_source=(S/'baseline-control/recomp_0046.c').read_text(encoding='utf-8')
assert 'ra2_ground_allied_bridge()' not in baseline_source and 'ra2_ground_terrain_tail_bridge()' not in baseline_source
path_source=ROOT/'ra2/src/recomp/gen_game/recomp_0003.c'
before=S/'diagnostic-current/recomp_0003.c'
assert path_source.read_bytes()==before.read_bytes()
# 该文件不在旧批次的已修改文件清单内，另存试验前副本，不虚构第九批清单指纹。
extended=S/'baseline/ra2/src/recomp/gen_game/recomp_0003.c'
assert not extended.exists(); extended.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(before,extended)
write('extended-baseline.json',dict(path='ra2/src/recomp/gen_game/recomp_0003.c',
    sha256=hashlib.sha256(before.read_bytes()).hexdigest(),source='pre-scoring-experiment snapshot',
    listed_in_previous_536_file_manifest=False,restored_before_final_validation=True))

shutil.copy2(OLD/'action-bounds.json',S/'action-bounds.json')
# 旧效果门槛继续作用于本批轨迹。额外矩阵的唯一严格失败已在上面精确核对，
# 此处只验实际分支效果，不替换其 comparison.json 或把严格失败改成通过。
source=(ROOT/'audit_movement_v8.py').read_text(encoding='utf-8')
source=source[:source.index("effect['passed']=True")]
source=source.replace('movement-state-v8','movement-state-v10').replace("'g-","'m-").replace('runs/g-','runs/m-')
source=source.replace("assert matrix['passed'] and additional['passed'] and len(additional['results'])==8",
    "assert matrix['passed'] and len(additional['results'])==12")
source=source.replace('paired_scenes=8,','paired_scenes=12,')
scope={'__file__':str(ROOT/'audit_movement_v8.py'),'__name__':'audit_effects_only'}
exec(compile(source,str(ROOT/'audit_movement_v8.py'),'exec'),scope)
effect,budget=scope['effect'],scope['budget']
tags=[r['tag'] for r in cases]
allied={tag:len(events(tag,25)) for tag in tags}
geometry={tag:len(events(tag,26)) for tag in tags}
terrain={tag:len(events(tag,27)) for tag in tags}
zero=[r for tag in tags for r in events(tag,27) if not r['auxiliary'] and (r['value']&0x7FFFFFFF)==0]
assert geometry['m-congestion-01']>0 and zero
effect['allied_motion']=dict(entry_counts=allied,geometry_counts=geometry,
    total_entries=sum(allied.values()),total_geometry_entries=sum(geometry.values()),native_cases=65536)
effect['terrain_tail']=dict(entry_counts=terrain,total_entries=sum(terrain.values()),
    zero_speed_entries=len(zero),zero_speed_events=zero,zero_speed_scene='m-zero-road',
    zero_speed_scene_frames=301,native_cases=65536,nan_cases_are_synthetic_only=True)
repeat='m-repeat-failure'
failed=[r for r in events(repeat,6) if not r['value']]
assert [r['frame'] for r in failed]==list(range(451,1112,60))
assert all(r['active_is_caller'] and not r['caller_goal_valid'] for r in failed)
assert len(events(repeat,18))==1 and events(repeat,18)[0]['frame']==399
counters=sorted({o['ground_drive']['path_failure_counter'] for _,o in samples(repeat)})
assert counters==[10] and not events(repeat,3)
effect['repeated_failure']=dict(tag=repeat,paired_frames=1251,secondary_failure_frame=399,
    later_move_orders=12,primary_failure_frames=[r['frame'] for r in failed],
    all_failures_clear_same_drive_goal=True,budget_values=counters,natural_budget_entry=False)
budget['repeated_failure_investigation']=effect['repeated_failure']
budget['natural_exhaustion_verified']=False
budget['unresolved']=[
    '真实二次失败及随后 12 次普通移动命令均清空同一 Drive 目标，预算始终 10，未进入预算扣减。',
    '继续寻找失败后保留目标且通过可达性复核的合法途径，重点仍是移动器替换/世界回调的栈内交界。',
    'Infantry 虚表的停止槽 504AE0 两条尾路仍调用 Foot.Stop 4C4B60；不同虚表槽地址本身不能证明绕过清目标。',
    '三格包围第 52 帧有两次旧路径评分查询差异，已用未接入新模块的控制重现；数值根因尚未证明。',
    '预算自然耗尽及整个游戏预算分支不可达均未被证明。']
effect['strict_ordered_observation']=dict(passed=False,scene='m-ur3',
    extra_generated_records=delta,baseline_control=control,comparator_unchanged=True)
effect['frame_and_effect_checks_passed']=True
effect['passed']=True  # 仅为效果检查；整批严格门槛仍为 false。
write('effects.json',effect);write('budget-conditions.json',budget)
write('acceptance-boundary.json',dict(passed=False,refactor_checks_passed=True,
    frame_comparison_passed=True,external_commands_equal=True,rng_equal_all_frames=True,
    strict_ordered_audit_passed=False,strict_failed_scenes=['m-ur3'],
    paired_scenes=27,paired_frames=14897,previous_formal_baseline_retained=True,
    reason='既有路径评分查询差异未消除；不将严格比较失败改写为正式通过。'))
print(json.dumps(dict(frame_checks=True,strict_ordered_checks=False,scenes=27,frames=14897,
    allied_geometry_entries=sum(geometry.values()),zero_speed_entries=len(zero),
    repeated_primary_failures=12,natural_budget_exhaustion=False),indent=2))
