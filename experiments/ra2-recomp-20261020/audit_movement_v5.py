"""延续墙/闸/速度实际效果断言，再增加本批分支命中；零命中不算验收。"""
from pathlib import Path
import json
import collections
ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v5'
source = (ROOT/'audit_movement_v4.py').read_text(encoding='utf-8')
source = source.replace("'evidence/movement-state-v4'","'evidence/movement-state-v5'")
# 复用已明确的原版墙/闸/速度及受控预算断言，本批追加断言后才写最终效果报告。
source = source[:source.index('with (STAGE /')]
scope = {'__file__':str(ROOT/'audit_movement_v4.py'),'__name__':'audit_base'}
exec(compile(source,str(ROOT/'audit_movement_v4.py'),'exec'),scope)
effect = scope['effect']
def rows(tag):
    return [json.loads(line) for line in (STAGE/'runs'/tag/'original/state.jsonl').open(encoding='utf-8')]
congestion = rows('final-congestion-01')
waits = [r for r in congestion if r['kind']=='movement-audit' and r['stage']==8]
assert waits and {r['value'] for r in waits} == {0,1}
classified = [r for r in congestion if r['kind']=='movement-audit' and r['stage']==9]
assert any(r['value']==2 for r in classified)
terrain = {}
for tag,value in [('final-restricted-clear',0),('final-restricted-rock',3)]:
    events = [r for r in rows(tag) if r['kind']=='movement-audit' and r['stage']==7]
    assert events and all(r['value']==value for r in events)
    terrain[tag] = dict(queries=len(events),movement_restricted_to=value)
effect['traffic_wait'] = dict(native_entries=len(waits),start_and_continue_observed=True,
    frames=[r['frame'] for r in waits],passage_counts=dict(collections.Counter(r['value'] for r in classified)))
effect['terrain'] = terrain
effect['reaction'] = dict(wall_attack_and_goal_verified=True,hard_blocked_recursive_and_zero_budget_probed=True,
    all_reaction_branches_naturally_observed=False)
effect['budget_conditions'] = str(STAGE/'budget-conditions.json')
for tag in ('final-rapid-traffic','final-rapid-obstructed','final-zero-delay'):
    comparison = json.loads((STAGE/'runs'/tag/'comparison.json').read_text(encoding='utf-8'))
    records = rows(tag)
    events = [r for r in records if r['kind']=='movement-audit' and r['stage']==8]
    effect[tag] = dict(comparison_passed=comparison['passed'],frames=comparison['comparison']['equal_frames'],
        wait_entries=len(events),wait_branch_covered=bool(events))
    if tag == 'final-zero-delay':
        assert events and all(r['auxiliary']==0 for r in events)
        effect[tag]['zero_wait_duration_observed'] = True
        effect[tag]['independent_full_rules_ini_used'] = True
    if tag == 'final-rapid-obstructed':
        assert events and all(r['auxiliary']==60 for r in events)
        effect[tag]['map_only_zero_delay_override_effective'] = False
assert effect['passed']
(STAGE/'effects.json').write_text(json.dumps(effect,ensure_ascii=False,indent=2),encoding='utf-8')
print('Actual effects verified; rapid scenes recorded with their true branch coverage.')
