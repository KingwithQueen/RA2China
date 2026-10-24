"""Freeze qualifying inputs and add normal rules-only negative controls."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'))
v=read(S/'collision-fixtures-02.json');items=[]
for item in v['fixtures']:
 x=read(S/'runs'/('baseline02-'+item['name'])/'comparison.json');assert x['passed'] and x['exe_sha256']=='66fe7d46d772694f735e643284ca5c821f9d27936226fa119384ea466176b72d'
 items.append(dict(item))
 control=dict(item);control['name']=item['name']+'-control'
 text=(R/item['rules']).read_bytes().decode('latin1');key='IsTrain' if item['name']=='train' else 'Crusher'
 m=re.search(r'(?ms)^\[TRUCKA\]\r?\n.*?(?=^\[|\Z)',text);assert m
 body=re.sub(r'(?mi)^'+key+r'\s*=.*$',key+'=no',m[0]);text=text[:m.start()]+body+text[m.end():]
 p=S/'fixtures'/('rules-'+control['name']+'.ini');assert not p.exists();p.write_bytes(text.encode('latin1'))
 control.update(rules=p.relative_to(R).as_posix(),rules_sha256=sha(p),negative_control=key+'=no');items.append(control)
v['fixtures']=items;v['initial_trials_qualify']=False;v['qualified_baseline_runs']=['baseline02-train','baseline02-crush']
(S/'collision-acceptance-fixtures.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
(S/'collision-trial-status.json').write_text(json.dumps(dict(passed=True,initial_trials=['baseline-train','baseline-crush'],initial_pair_frame_conformance=True,initial_pair_effects_qualified=False,reason='Train player Move was cancelled by original; targets were on lower layer. No such trial is counted as collision proof.',qualified_trials=v['qualified_baseline_runs'],positive_effects=['Two non-crushable vehicles removed, train health200->160, crushable infantry remains125','Two enemy infantry removed by crusher, vehicle remains200; held bridge exit and later release remain ordinary orders'],all_input_variants_preserved=True,initial_preflight='Preparation first rejected an allowlist that omitted the second newly created recipe; no baseline/state mutation occurred.'),indent=2)+'\n',encoding='utf-8')
print('Qualified two real scenes and prepared two flag-off controls')
