"""重读本批实跑轨迹，分别验收二次补建失败、对象碰撞与仍未命中的预算。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v9'
OLD = ROOT/'evidence/movement-state-v8'

# 动作范围的原始输入未变化，沿用有指纹的静态证据，而不是重新声称实景命中。
action = json.loads((OLD/'action-bounds.json').read_text(encoding='utf-8'))
assert hashlib.sha256((ROOT/'ra2/game/game.exe').read_bytes()).hexdigest() == action['input_exe_sha256']
if (STAGE/'action-bounds.json').exists():
    assert (OLD/'action-bounds.json').read_bytes() == (STAGE/'action-bounds.json').read_bytes()
else:
    shutil.copy2(OLD/'action-bounds.json', STAGE/'action-bounds.json')

# 旧验收规则仍然运行在本批 25 个实际轨迹上；不复制旧 effects 的通过结论。
source = (ROOT/'audit_movement_v8.py').read_text(encoding='utf-8')
source = source[:source.index("effect['passed']=True")]
source = source.replace('movement-state-v8', 'movement-state-v9')
source = source.replace("'g-", "'i-").replace('runs/g-', 'runs/i-')
source = source.replace("len(additional['results'])==8", "len(additional['results'])==10")
source = source.replace('paired_scenes=8,', 'paired_scenes=10,')
scope = {'__file__': str(ROOT/'audit_movement_v8.py'), '__name__': 'audit_base'}
exec(compile(source, str(ROOT/'audit_movement_v8.py'), 'exec'), scope)
effect, budget = scope['effect'], scope['budget']
rows, audits, samples = scope['rows'], scope['audits'], scope['samples']
tags = scope['tags']

continuation = {tag: len(audits(rows(tag), 21)) for tag in tags}
continuation_passages = Counter(r['value'] for tag in tags for r in audits(rows(tag),21))
objects = {tag: len(audits(rows(tag), 24)) for tag in tags}
candidate = {tag: len(audits(rows(tag), 22)) for tag in tags}
secondary = [dict(scene=tag, **r) for tag in tags for r in audits(rows(tag), 23)]
assert sum(objects.values()) > 0 and sum(candidate.values()) > 0
effect['turn_continuation'] = dict(
    audit_stage=21, classified_entries_by_scene=continuation,
    total_classified_entries=sum(continuation.values()),
    passage_counts=dict(continuation_passages),
    natural_classification_observed=bool(sum(continuation.values())),
    all_eight_passages_naturally_observed=False,
    native_fragment_cases=65536, all_eight_passages_verified_by_native_fragments=True)
effect['object_collision'] = dict(audit_stage=24, entries_by_scene=objects,
    total_entries=sum(objects.values()), native_fragment_cases=4*65536,
    observed_flag_mask='0x05', raw_unused_high_flags_compared=False)
effect['secondary_preparation'] = dict(candidate_entries_by_scene=candidate,
    rebuild_requests=secondary, audit_stages=[22,23,18])

def unit_at(records, frame):
    return next(o for f,o in samples(records,1022579) if f == frame)

long = rows('i-long')
failed = rows('i-second-failure')
for records in (long, failed):
    requested = audits(records,23)
    assert len(requested)==1 and requested[0]['frame']==399
    assert requested[0]['value']==2560 and requested[0]['auxiliary']==2
    candidate_at_399 = [r for r in audits(records,22) if r['frame']==399]
    assert len(candidate_at_399)==1 and candidate_at_399[0]['value']==-1
    assert unit_at(records,398)['ground_drive']['path_directions']==[2]
assert not audits(long,18)
failure = audits(failed,18)
assert len(failure)==1 and failure[0]['frame']==399 and failure[0]['value']==0
assert failure[0]['active_is_caller'] and failure[0]['active_ground_drive']
assert not failure[0]['caller_goal_valid'] and not failure[0]['active_goal_valid']
placed = [r for r in failed if r['kind']=='fixture-unit']
assert len(placed)==16 and all(r['frame']==398 for r in placed)
constraints = [r for r in failed if r['kind']=='fixture-constraints']
assert len(constraints)==1 and constraints[0]['explicit_rebuild_result']==0xFFFFFFFF
assert constraints[0]['accepted_before']==constraints[0]['accepted_after']==1
assert constraints[0]['path_head']==2
assert unit_at(failed,400)['ground_drive']['destination']==[0,0,0]
assert unit_at(failed,400)['ground_drive']['path_directions']==[]
counter_values = sorted({o['ground_drive']['path_failure_counter'] for _,o in samples(failed,1022579)})
assert counter_values==[10] and not audits(failed,3)

effect['natural_secondary_failure'] = dict(
    tag='i-second-failure', reference_tag='i-long', paired_frames=651,
    reference_paired_frames=1501, order_frame=5, order_cell=[100,114],
    obstacle_frame=398, actual_obstacles=16, radius=2,
    explicit_fixture_rebuild=False, path_queue_or_budget_injected=False,
    pre_failure_direction_queue=[2], missing_second_direction=-1,
    distance=2560, secondary_request_frame=399, failure_frame=399,
    failure_event=failure[0], following_frame_goal_cleared=True,
    following_frame_queue_empty=True, failure_budget_values=counter_values,
    natural_budget_entry=False)
budget['natural_secondary_failure'] = effect['natural_secondary_failure']
assert budget['second_search_failure_naturally_observed']
assert len(budget['second_search_failure_events'])==1
assert not budget['natural_budget_entries']
budget['unresolved'] = [
    '二次补建失败已在合法长路线与真实障碍中自然命中；同一 Drive 的目标随失败清空，预算保持 10。',
    '仍需找到失败后保留调用者目标并通过可达性复核、反复扣减预算的合法实景，不能把二次失败等同预算耗尽。',
    '本机支持的超时空/入格回调是否会在旧 Drive 调用栈中替换活动移动器，仍是待验证假设。',
    '动作 128 不在本机原版 1.006 的 1..117 动作分发范围内；不能据此排除其它合法途径。',
    f'25 个实景接续分类 stage 21 共 {sum(continuation.values())} 次，分类计数 {dict(continuation_passages)}；八种通行码仍主要由 65536 组原版片段验证，不能写成实景全覆盖。',
    '上述带前提分析不是整个游戏预算分支不可达的证明。']
effect['diagnostic_investigation'] = dict(
    retained_run='h-fail', all_game_states_and_rng_equal=True,
    strict_command_audit_passed=False, first_mismatch_stage=24,
    original_raw_flags=31, generated_raw_flags=7, used_mask='0x05',
    resolution='记录对象分类实际检查的位 0 和位 2，保留失败轨迹；正式 25 场景以 schema 11 完整重新配对。',
    replay='i-second-failure', replay_passed=True,
    unused_high_bit_cause_proven=False)
effect['passed'] = True
for name, value in [('effects.json',effect), ('budget-conditions.json',budget)]:
    p = STAGE/name
    assert not p.exists()
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True, paired_scenes=len(tags),
    secondary_failures=len(budget['second_search_failure_events']),
    natural_budget_entries=len(budget['natural_budget_entries']),
    continuation_classifications=sum(continuation.values()),
    object_entries=sum(objects.values())),indent=2))
