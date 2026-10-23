"""Record completed entries and remaining work; do not manufacture a new percentage."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'evidence/movement-state-v36/progress-estimate.json';v=read(old)
paths=[S/n for n in ['new-fragment-contract.json','bridge-lane-release-real-scenes.json','production-scene-totals.json','alias-natural-scenes.json','alias-occupied-natural-scenes.json','internal-alias-sources.json','native-gates.json']]
assert all(read(p)['passed'] for p in paths)
assert read(S/'native-gates.json')['groups']==123 and read(S/'production-scene-totals.json')['production_scenes']==69
v.update(passed=True,historical_only=True,reestimated_this_round=False,previous_estimate=str(old),completed_entries_this_round=['004A24F0','00703A53','004A25E8'],completed_entry_does_not_prove_natural_C_dispatch=True)
v['remaining_internal_entry_candidates']=[e for e in v['remaining_internal_entry_candidates'] if e['address'] not in v['completed_entries_this_round']]
v['summary_zh']='沿用第三十五批的历史工程估算，本轮没有重新计算百分比。'+v['summary_zh']
v['remaining_zh']='本轮已整理4A24F0、703A53、4A25E8；仍有其他载入坐标、目标选择、格切换及桥层写回，更多对象/移动器/碾压毁桥和递归服务组合，以及29个非主C副本自然来源待核。原8–15批仅是上批规划区间，不是本轮重新估时。'
v['inputs']=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),old]+paths]
(S/'progress-estimate.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(v['remaining_zh'])
