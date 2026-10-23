"""Change only the ordinary infantry subcell, keeping all movement state natural."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34';out=S/'investigations/south-subcells';out.mkdir(parents=True,exist_ok=True)
item=next(x for x in json.loads((S/'bridge-occupied-fixtures.json').read_text(encoding='utf-8'))['fixtures'] if x['name']=='south');source=(R/item['path']).read_text(encoding='utf-8');results=[]
for slot in [4,3]:
    section=None;ls=[]
    for line in source.splitlines():
        if line.startswith('['):section=line
        if section=='[Infantry]' and line.startswith('2='):
            k,v=line.split('=',1);fs=v.split(',');assert fs[1]=='E2';fs[5]=str(slot);line=k+'='+','.join(fs)
        ls.append(line)
    p=out/('south-subcell-'+str(slot)+'.MAP');p.write_text('\n'.join(ls)+'\n',encoding='utf-8');tag='trial-os'+str(slot)+'b'
    args=[sys.executable,'-X','utf8','-B',str(R/'run_fixture_comparison.py'),'--tag',tag,'--evidence-stage','movement-state-v34','--movement-audit','--seconds','240','--range','0:300','--scenario-map',str(p)]
    for order in item['orders']:
        if int(order.split(':',1)[0])<300:args+=['--order',order]
    with (out/(tag+'.log')).open('x',encoding='utf-8') as f:subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
    report=json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'));assert report['passed'];modes={}
    for mode in ['original','generated-c']:
        rs=[json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')];h={r['frame']:{o['id']:o['position'] for o in r['objects']} for r in rs if r['kind']=='state'};qs=[]
        for r in rs:
            if r['kind']!='movement-audit' or r['stage'] not in [25,26] or r['id']!=1023362 or r['value']!=1023367 or r['frame']<=5:continue
            f=r['frame'];a,b=h[f][1023362],h[f][1023367];pa,pb=h[f-1][1023362],h[f-1][1023367]
            if a[2]==b[2]==416 and a[1]<pa[1] and b[1]>pb[1] and abs(a[1]-b[1])<=1024:qs.append(r)
        modes[mode]=dict(relationship_queries=sum(q['stage']==25 for q in qs),geometry_queries=sum(q['stage']==26 for q in qs),samples=qs[:8])
    assert modes['original']==modes['generated-c'];v=dict(slot=slot,paired_frames=301,formal_acceptance_frames=0,modes=modes,positive=all(modes['original'][k]>0 for k in ['relationship_queries','geometry_queries']));results.append(v);print(json.dumps(v),flush=True)
(out/'results.json').write_text(json.dumps(dict(passed=True,results=results,formal_acceptance_frames=0),indent=2)+'\n',encoding='utf-8')
positive=[r for r in results if r['positive']];assert positive,'Keep nonqualifying trials and continue ordinary map investigation'
(S/'south-subcell-selected.json').write_text(json.dumps(dict(passed=True,slot=positive[0]['slot'],trial_frames_not_admitted=True),indent=2)+'\n',encoding='utf-8')
