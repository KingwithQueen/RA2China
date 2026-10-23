"""Test ordinary-map candidates; matching traces alone do not prove the target query."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
recipes=json.loads((S/'north-query-candidates.json').read_text(encoding='utf-8'))['fixtures'];results=[]
for item in recipes:
    tag='trial-'+item['name'];args=[sys.executable,'-B',str(R/'run_fixture_comparison.py'),'--tag',tag,'--evidence-stage','movement-state-v34','--movement-audit','--seconds','240','--range','0:300','--scenario-map',str(R/item['path'])]
    for order in item['orders']:args+=['--order',order]
    with (S/(tag+'.log')).open('x',encoding='utf-8') as f:p=subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT)
    report=json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'));assert p.returncode==0 and report['passed'],tag
    modes={}
    for mode in ['original','generated-c']:
        rs=[json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
        history={r['frame']:{o['id']:o['position'] for o in r['objects']} for r in rs if r['kind']=='state'};qualified=[]
        for r in rs:
            if r['kind']!='movement-audit' or r['stage'] not in [25,26] or r['id']!=1023362 or r['value']!=1023367 or r['frame']<=item['query_after_frame']:continue
            f=r['frame']
            if not all(u in history.get(f,{}) and u in history.get(f-1,{}) for u in [1023362,1023367]):continue
            a,b=history[f][1023362],history[f][1023367];pa,pb=history[f-1][1023362],history[f-1][1023367]
            if a[2]==b[2]==416 and a[1]>pa[1] and b[1]<pb[1] and abs(a[1]-b[1])<=1024:qualified.append(r)
        modes[mode]=dict(relationship_queries=sum(r['stage']==25 for r in qualified),geometry_queries=sum(r['stage']==26 for r in qualified),samples=qualified[:8])
    assert modes['original']==modes['generated-c'];result=dict(name=item['name'],tag=tag,paired_frames=301,acceptance_frames=0,positive=modes['original']['relationship_queries']>0 and modes['original']['geometry_queries']>0,modes=modes);results.append(result);print(json.dumps(result),flush=True)
(S/'north-query-trials.json').write_text(json.dumps(dict(passed=True,results=results,acceptance_frames=0),indent=2)+'\n',encoding='utf-8')
positive=[r for r in results if r['positive']];assert positive,'No legal moving northbound meeting query yet; keep all trials and investigate'
selected=[r for r in recipes if r['name']==positive[0]['name']]
(S/'north-query-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=selected,ordinary_move_orders=True,raw_state_writes=False),indent=2)+'\n',encoding='utf-8')
