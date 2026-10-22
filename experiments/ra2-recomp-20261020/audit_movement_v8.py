"""保留原有实景门槛，并分别记录新增分支命中与尚未命中的目标。"""
from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parent
STAGE=ROOT/'evidence/movement-state-v8'

# 沿用第七批十五场景的效果检查，重新读取本批实际轨迹，不复制旧结论。
source=(ROOT/'audit_movement_v7.py').read_text(encoding='utf-8')
source=source[:source.index("investigation = read(STAGE/")]
source=source.replace('movement-state-v7','movement-state-v8').replace("'c-","'g-")
source=source.replace('runs/c-','runs/g-')
scope={'__file__':str(ROOT/'audit_movement_v7.py'),'__name__':'audit_base'}
exec(compile(source,str(ROOT/'audit_movement_v7.py'),'exec'),scope)
effect,budget=scope['effect'],scope['budget']
read,rows,audits,samples=scope['read'],scope['rows'],scope['audits'],scope['samples']
matrix=read(STAGE/'g-matrix.json'); additional=read(STAGE/'g-additional-matrix.json')
assert matrix['passed'] and additional['passed'] and len(additional['results'])==8
tags=[r['tag'] for r in matrix['results']+additional['results']]
counts=Counter()
for tag in tags: counts.update(r['value'] for r in audits(rows(tag),19))
assert all(counts[n]>0 for n in (0,1,2,7))
turn=rows('g-tc1'); events=audits(turn,19)
assert len(events)==1 and events[0]['value']==1 and events[0]['frame']==197
enemy=samples(turn,1022580)
assert next(o for f,o in enemy if f==197)['cloak_state']==2
assert {0,3}.intersection({o['cloak_state'] for f,o in enemy if 197<f<250})
effect['late_preparation']['turn_passage_counts']=dict(counts)
effect['late_preparation']['naturally_unobserved_turn_passages']=[p for p in range(8) if not counts[p]]
effect['turn_cloaked_obstacle']=dict(tag='g-tc1',frame=197,passage=1,cell=events[0]['cell'],
    candidate=events[0]['candidate'],enemy_id=1022580,cloaked_before=True,revealed_after=True,paired_frames=401)
hard=[r for r in audits(rows('g-ur3'),19) if r['value']==7]
assert len(hard)==1 and hard[0]['frame']==52
effect['turn_hard_blocked']=dict(tag='g-ur3',frame=52,passage=7,cell=hard[0]['cell'],candidate=hard[0]['candidate'],paired_frames=351)
advance={tag:len(audits(rows(tag),20)) for tag in tags}
assert advance['g-standard-01']>0 and advance['g-congestion-01']>0 and advance['g-tc1']>0
effect['path_advance']=dict(audit_stage=20,sample_entries_by_scene=advance,total_entries=sum(advance.values()))
investigations={}
for tag,expected in [('g-ur2',16),('g-ur3',24)]:
    records=rows(tag)
    placed=[r for r in records if r['kind'] in ('fixture-wall','fixture-unit')]
    assert len(placed)==expected,(tag,len(placed))
    assert [r for r in records if r['kind']=='fixture-constraints'][0]['explicit_rebuild_result']==0xFFFFFFFF
    budget_entries=audits(records,3)
    second_failures=audits(records,18)
    values=sorted({o['ground_drive']['path_failure_counter'] for _,o in samples(records,1022579)})
    investigations[tag]=dict(real_objects_created=expected,failure_budget_values=values,
        second_failure_events=second_failures,budget_events=budget_entries,
        primary_failed_rebuilds=[r for r in audits(records,6) if not r['value']])
budget['additional_scene_investigations']=investigations
natural=[tag for tag in tags if tag not in ('g-budget-entry','g-budget-natural')]
budget['second_search_failure_events']=[dict(scene=tag,**r) for tag in natural for r in audits(rows(tag),18)]
budget['second_search_failure_naturally_observed']=bool(budget['second_search_failure_events'])
budget['natural_budget_entries']=[dict(scene=tag,**r) for tag in natural for r in audits(rows(tag),3)]
budget['all_natural_scenes_no_budget_entry']=[tag for tag in natural if not audits(rows(tag),3)]
budget['natural_exhaustion_verified']=False
budget['unsupported_action_excluded']=read(STAGE/'action-bounds.json')
budget['unresolved']=[
    '尚未找到合法玩法中重建失败后仍保留调用者目标并通过可达性复核、最后自然耗尽预算的实景。',
    '已验证两/三格动态包围及转弯隐形揭露，分支命中以逐帧事件为准；片段测试不等同自然命中。',
    '本机原版动作分发上限为 117；128 号 TeleportAll 超出范围，不能拿其它版本的动作作本机合法证明。',
    '仍需检查本机原版支持的超时空/入格回调与旧 Drive 调用栈的交界。未证明整个游戏预算分支不可达。']
effect['budget_conditions']=str(STAGE/'budget-conditions.json')
effect['additional_scenes']=dict(paired_scenes=8,paired_frames=sum(r['frames'] for r in additional['results']),
    static_ring_rejection_observed=all(not audits(rows(tag),6) for tag in ('g-ring2','g-ring3')),
    dynamic_rings=investigations)
effect['passed']=True
for name,value in [('effects.json',effect),('budget-conditions.json',budget)]:
    p=STAGE/name; assert not p.exists(); p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,turn_counts=dict(counts),advance_entries=sum(advance.values()),
    second_failures=len(budget['second_search_failure_events']),natural_budget_entries=len(budget['natural_budget_entries'])),indent=2))
