"""Native world commands, fixed simulation frames, strict comparisons retained."""
from combat_batch_v69 import *
from concurrent.futures import ThreadPoolExecutor
def execute(tag,x,last,observer=True):
    run(fixture(tag,x,last,observer),'scene-'+tag,codes=(0,1));p=S/'runs'/tag/'comparison.json';d=read(p)
    assert all(a['passed'] and a['exit_code']==0 for a in d['runs']),tag
    assert d['comparison']['negative_control']['passed']
    return dict(tag=tag,frames=d['comparison']['frames_compared'],strict=d['passed'],comparison_sha256=sha(p),exe_sha256=d['exe_sha256'])
if sys.argv[1]=='baseline':
    items=read(S/'scene-pending.json')['fixtures']
    for x in items:
        execute('id-'+x['tag'],x,1)
        p=S/'runs'/('id-'+x['tag'])/'original/state.jsonl';a=next(json.loads(l) for l in p.open(encoding='utf-8') if json.loads(l)['kind']=='state')
        by_cell={tuple(v//256 for v in z['position'][:2]):z for z in a['objects']}
        if x['tag']=='repair':
            vehicle=by_cell[80,112]['id'];target=by_cell[85,112]['id'];engineer=by_cell[80,113]['id']
            x.update(attacker_id=vehicle,target_id=target,engineer_id=engineer,orders=[f'5:{engineer}:7:{vehicle}:0',f'200:{vehicle}:1:{target}:0'])
        else:
            attacker=by_cell[80,112]['id'];target=by_cell[86,112]['id'];x.update(attacker_id=attacker,target_id=target,orders=[f'5:{attacker}:1:{target}:0'])
    write(S/'scene-recipes.json',dict(passed=True,fixtures=items,calibration_excluded=True))
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(lambda x:execute('b-'+x['tag'],x,x['last']),items))
    write(S/'baseline-scenes.json',dict(passed=True,results=values,strict_all=all(x['strict'] for x in values)))
    traces=[dict(tag=v['tag'],mode=m,path=str(S/'runs'/v['tag']/m/'state.jsonl'),sha256=sha(S/'runs'/v['tag']/m/'state.jsonl')) for v in values for m in ['original','generated-c']]
    write(S/'baseline-contract.json',dict(passed=True,traces=traces,scope='Frozen before attaching the new health service; raw strict results stay explicit.'))
elif sys.argv[1]=='final':
    run(py('make_combat_observer_v69.py','--relink'),'make-final-observer');run(['pwsh','-NoProfile','-File',R/'build-combat-observer-v69.ps1'],'build-final-observer')
    items=read(S/'scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']]
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(lambda x:execute('f-'+x['tag'],x,x['last']),items))
    write(S/'final-scenes.json',dict(passed=True,results=values,strict_all=all(x['strict'] for x in values)))
else:raise ValueError(sys.argv[1])
