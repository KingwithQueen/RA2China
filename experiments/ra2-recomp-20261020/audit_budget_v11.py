"""将合法设置实景、受控摆放、主动寻路和未通过尝试分开记账。"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v11'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
result={}
for tag,radius in [('l-sk-ai-ring',1),('m-sk-ai-ring',2),('n-sk-zero-close',2)]:
    x=read(S/'runs'/tag/'comparison.json');details={}
    for mode in ['original','generated-c']:
        p=S/'runs'/tag/mode/'state.jsonl';seq=[]
        for line in p.open(encoding='utf-8'):
            try:seq.append(json.loads(line))
            except json.JSONDecodeError:pass # 失败退出的半行只作调查记录，绝不通过验收。
        ev=[r for r in seq if r['kind']=='movement-audit' and r['id']==1032258]
        samples=[(r['frame'],o) for r in seq if r['kind']=='state' for o in r['objects'] if o['id']==1032258]
        details[mode]=dict(real_units_placed=sum(r['kind']=='fixture-unit' for r in seq),
            failed_rebuilds=[r for r in ev if r['stage']==6 and not r['value']],
            budget_events=[r for r in ev if r['stage']==3],
            budget_values=sorted({o['ground_drive']['path_failure_counter'] for _,o in samples if 'ground_drive' in o}),
            fixture_constraints=[r for r in seq if r['kind']=='fixture-constraints'])
        if tag=='n-sk-zero-close':
            terminal=next(o for frame,o in samples if frame==69)
            details[mode]['zero_stop_goal_cleared']=terminal['ground_drive']['destination']==[0,0,0] and terminal['ground_drive']['path_failure_counter']==0
    result[tag]=dict(passed=x['passed'],exe_sha256=x['exe_sha256'],frames_compared=x.get('comparison',{}).get('frames_compared',0),
        first_difference=x.get('comparison',{}).get('first_difference'),command_difference=x.get('comparison',{}).get('command_difference'),
        radius=radius,explicit_rebuild_requested=radius==1,modes=details,
        default_original_rules=False,legal_rule_changes=['E1.Speed=0','E2.Speed=0','MTNK.Primary=none','HTNK.Primary=none']+(['CloseEnough=0'] if tag=='n-sk-zero-close' else []),
        budget_queue_goal_fields_written=False)
natural=result['n-sk-zero-close'];entries=natural['modes']['original']['budget_events']
assert all(x['passed'] for x in result.values())
assert all(not x['budget_queue_goal_fields_written'] for x in result.values())
assert all(c['explicit_rebuild_result']==0xFFFFFFFF for tag in ['m-sk-ai-ring','n-sk-zero-close'] for mode in ['original','generated-c'] for c in result[tag]['modes'][mode]['fixture_constraints'])
assert [r['value'] for r in result['m-sk-ai-ring']['modes']['original']['budget_events']]==[10,9,8]
exhausted=natural['passed'] and len(entries)==11 and [r['value'] for r in entries]==list(range(10,-1,-1)) and [r['frame'] for r in entries]==list(range(58,69)) and all(d['zero_stop_goal_cleared'] for d in natural['modes'].values())
assert exhausted
out=dict(natural_exhaustion_verified=bool(exhausted),scenes=result,
    independent_probe_not_formal_executable=True,formal_executable_sha256=hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest(),
    static_callback_lead='4C3895 -> Unit.SetDestination 7053F0 -> Foot.SetDestination 4C8030 -> locomotor.MoveTo 4C8165, after Stop at 4C371A; exact legal entry conditions remain to be observed.',
    default_rules_full_exhaustion_verified=False,natural_deduction_with_original_close_enough_verified=True,
    rejected_attempts={'h-sk-zero':'range 0:0 rejected by logger','i-sk-ai-ring':'AI did not accept player Move before placement','j-sk-ai-ring':'original fixture only allowed house 1 as blocker','k-sk-ai-ring':'isolated build compiled original fixture path; retained, corrected in build 02','o-sk-ai-far':'ring intersects an occupied cell; no accepted scene'})
(S/'budget-real-scenes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
