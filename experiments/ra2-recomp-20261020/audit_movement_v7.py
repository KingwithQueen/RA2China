"""正式实景须同时满足逐帧相等和实际分支/效果；未命中项如实保留。"""
from pathlib import Path
from collections import Counter
import json
import struct

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v7'
PREFIX = 'c-'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def rows(tag):
    return [json.loads(line) for line in (STAGE/'runs'/tag/'original/state.jsonl').open(encoding='utf-8')]


def states(records):
    return [r for r in records if r['kind']=='state']


def audits(records, stage):
    return [r for r in records if r['kind']=='movement-audit' and r['stage']==stage]


def samples(records, uid):
    return [(s['frame'],o) for s in states(records) for o in s['objects'] if o['id']==uid]


def write(name, data):
    path = STAGE/name
    assert not path.exists()
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


matrix = read(STAGE/'c-matrix.json')
assert matrix['passed'] and len(matrix['results'])==15
source = (ROOT/'audit_movement_v4.py').read_text(encoding='utf-8')
source = source.replace("'evidence/movement-state-v4'","'evidence/movement-state-v7'").replace("'final-","'c-")
source = source[:source.index('with (STAGE /')]
scope = {'__file__':str(ROOT/'audit_movement_v4.py'),'__name__':'audit_base'}
exec(compile(source,str(ROOT/'audit_movement_v4.py'),'exec'),scope)
effect = scope['effect']

congestion = rows('c-congestion-01')
waits = audits(congestion,8)
assert waits and {r['value'] for r in waits}=={0,1}
temporary = audits(congestion,11)
assert temporary and all(r['value']==6 for r in temporary)
effect['traffic_wait'] = dict(entries=len(waits),start_and_continue_observed=True)
effect['temporary_obstacle'] = dict(entries=len(temporary),real_branch_observed=True)
cloaked = rows('c-cloaked-corridor')
assert len(audits(cloaked,12))==1 and audits(cloaked,12)[0]['frame']==197
enemy = samples(cloaked,1022580)
assert next(o for f,o in enemy if f==197)['cloak_state']==2
assert {0,3}.issubset({o['cloak_state'] for f,o in enemy if 197<f<=220})
effect['cloaked_obstacle'] = dict(reveal_frame=197,real_cloak_and_reveal_observed=True,stock_truck_cloak=False)
for tag,value in [('c-restricted-clear',0),('c-restricted-rock',3)]:
    events = audits(rows(tag),7)
    assert events and all(r['value']==value for r in events)
effect['terrain_restrictions_retained'] = True
zero_waits = audits(rows('c-zero-delay'),8)
assert zero_waits and all(r['auxiliary']==0 for r in zero_waits)
effect['zero_delay'] = dict(real_entries=len(zero_waits),independent_full_rules_ini=True)

turn_counts = Counter()
followup_counts = {}
for tag in ('c-standard-01','c-congestion-01','c-slope-healthy','c-slope-damaged'):
    records = rows(tag)
    counts = Counter(r['value'] for r in audits(records,19))
    turn_counts.update(counts)
    assert audits(records,16) and audits(records,17)
    followup_counts[tag] = dict(speed_entries=len(audits(records,16)),followup_entries=len(audits(records,17)),
        absent_second_direction_entries=sum(r['value']==-1 for r in audits(records,17)),
        turn_passages=dict(counts),second_search_failure_entries=len(audits(records,18)))
assert turn_counts[0]>0 and turn_counts[2]>0
effect['late_preparation'] = dict(scenes=followup_counts,turn_passage_counts=dict(turn_counts),
    all_eight_turn_passages_verified_by_native_fragments=True,
    all_eight_turn_passages_naturally_observed=False,
    naturally_unobserved_turn_passages=[p for p in range(8) if not turn_counts[p]])

speed_scenes = {}
for label,health,base in [('healthy',400,1.0),('damaged',100,0.75)]:
    tag = 'c-slope-'+label
    units = samples(rows(tag),1022579)
    values = sorted({struct.unpack('<d',bytes.fromhex(o['ground_drive']['drive_speed_bits']))[0] for _,o in units})
    heights = [o['position'][2] for _,o in units]
    assert min(heights)==416 and max(heights)==520 and units[-1][1]['position']==[24192,30848,416]
    assert units[0][1]['health']==health and base in values
    assert all(o['stop_completed'] for o in read(STAGE/'runs'/tag/'comparison.json')['comparison']['controlled_objects'])
    speed_scenes[label] = dict(health=health,drive_speed_values=values,z_min=min(heights),z_max=max(heights),
        returned_to_start=True,stop_completed=True)
assert speed_scenes['healthy']['drive_speed_values']==[0.0,1.0,1.2000000476837158]
assert speed_scenes['damaged']['drive_speed_values']==[0.0,0.75,0.9000000357627869]
effect['speed'] = speed_scenes

budget = read(ROOT/'evidence/movement-state-v6/budget-conditions.json')
budget['real_scene_evidence'] = []
for suffix in ('budget-natural','restricted-clear','restricted-rock','cloaked-corridor'):
    tag = PREFIX+suffix
    records = rows(tag)
    failures = [r for r in audits(records,6) if r['value']==0]
    assert failures and all(r['active_is_caller'] and not r['caller_goal_valid'] for r in failures)
    counters = sorted({o['ground_drive']['path_failure_counter'] for _,o in samples(records,1022579)})
    assert counters==[10] and not audits(records,3)
    budget['real_scene_evidence'].append(dict(tag=tag,failed_rebuilds=failures,failure_budget_values=counters))
natural_tags = [r['tag'] for r in matrix['results'] if r['tag']!='c-budget-entry']
for tag in natural_tags:
    assert not audits(rows(tag),3),tag
    assert not audits(rows(tag),15),tag
budget['all_natural_scenes_no_budget_entry'] = natural_tags
budget['second_search_failure_events'] = [r for tag in natural_tags for r in audits(rows(tag),18)]
budget['second_search_failure_naturally_observed'] = bool(budget['second_search_failure_events'])

chrono = {}
for tag in ('c-chrono-team-reference','c-chrono-seam-budget'):
    records = rows(tag)
    unit = samples(records,1022584)
    assert unit and unit[0][0]==1
    counts = Counter(hex(o['locomotor_vtable']) for _,o in unit)
    assert counts['0x7ad1a8']>0 and counts['0x7a04cc']>0
    counters = sorted({o['ground_drive']['path_failure_counter'] for _,o in unit if 'ground_drive' in o})
    assert counters==[10]
    chrono[tag] = dict(unit_id=1022584,first_observed_frame=unit[0][0],frames_by_vtable=dict(counts),
        failure_budget_values=counters,old_drive_prepare_while_other_locomotor_active=len(audits(records,15)),
        natural_budget_entries=len(audits(records,3)))
seam = rows('c-chrono-seam-budget')
assert len([r for r in seam if r['kind']=='fixture-wall'])==8
commands = read(STAGE/'runs/c-chrono-seam-budget/comparison.json')['comparison']['controlled_objects']
assert commands and commands[0]['movement_observed'] and commands[0]['first_observed_frame']==1
chrono['c-chrono-seam-budget']['real_walls_created'] = 8
chrono['c-chrono-seam-budget']['unit_movement_observed'] = True
effect['chrono'] = chrono
budget['locomotor_investigation']['chrono_trigger'] = chrono
budget['locomotor_investigation']['real_save'] = {}
for tag in ('c-standard-01','c-congestion-01'):
    unit = samples(rows(tag),1032341)
    counts = Counter(hex(o['locomotor_vtable']) for _,o in unit)
    assert counts['0x7ad1a8']>0 and counts['0x7a04cc']>0
    budget['locomotor_investigation']['real_save'][tag] = dict(unit_id=1032341,frames_by_vtable=dict(counts),
        prepare_with_different_active_locomotor_entries=len(audits(rows(tag),15)))
budget['locomotor_investigation']['evidence'] = [str(ROOT/'evidence/movement-state-v6'/name)
    for name in ('locomotor-layout.json','teleport-process.asm','teleport-stop.asm','teleport-begin-end.asm')]
budget['locomotor_investigation']['action_reference_fix'] = dict(
    before='107,0,TeamID',after='107,1,TeamID',native_campaign_reference_examples=[5272,5280,5286,5288,5290],
    zero_selector_no_spawn_retained='final-chrono-immediate',actual_reinforcement_verified=True)
budget['additional_static_analysis'] = dict(
    destination_acceptance='4C2EF0 examines x/y cells, destination bridge flag, moving zone and owner queries; does not read destination z.',
    z_difference_alone_explains_early_rejection_mismatch=False,
    direct_prepare_call_candidates='8 call sites, all within the Drive routine family; see drive-entry-references.json.',
    process_pointer_candidate='7A050C only, the Drive interface Process slot; no direct CALL candidate.',
    all_indirect_flows_proven=False,
    evidence=['destination-acceptance.asm','path-rebuild-early.asm','drive-entry-references.json'])
budget['unresolved'] = [
    '仍未找到原版合法玩法中重建失败后保留有效调用者目标并通过二次可达性复核的自然耗尽场景。',
    '普通包装生命周期已实景覆盖；尚未观察到包装期间旧 Drive Prepare 被调用。',
    '后续可检查入格触发器/世界服务在同一旧 Drive 调用栈中替换移动器的瞬间；这是待验证假设。',
    '第二次路径补建失败已由原版片段覆盖；若实景没有 stage 18，不能宣称自然命中。',
    '不能把带前提的控制流分析扩大成整个游戏预算分支不可达证明。']
budget['natural_exhaustion_verified'] = False
budget['controlled_entry_is_natural'] = False

investigation = read(STAGE/'runs/verified-chrono-seam-02/comparison.json')
assert investigation['frame_comparison_passed'] and not investigation['scene_expectations_passed']
assert investigation['comparison']['equal_frames']==601
effect['retained_stop_investigation'] = dict(tag='verified-chrono-seam-02',paired_equal_frames=601,
    final_mission=investigation['comparison']['controlled_objects'][0]['final_mission'],
    stop_completed=False,classified_as_formal_stop_acceptance=False)
effect['budget_conditions'] = str(STAGE/'budget-conditions.json')
effect['passed'] = True
write('budget-conditions.json',budget)
write('effects.json',effect)
print(json.dumps(dict(passed=True,speed=speed_scenes,turn_counts=dict(turn_counts),chrono=chrono,
    natural_budget_exhaustion=False),ensure_ascii=False,indent=2))
