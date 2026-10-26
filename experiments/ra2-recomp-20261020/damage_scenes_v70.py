"""Calibrate object IDs, run finite scenes, and freeze complete pre-attachment records."""
from combat_batch_v70 import *
from concurrent.futures import ThreadPoolExecutor
def execute(tag,x,last,command=False):
    args=fixture(tag,x,last)
    if command:args[4]=R/'run_combat_command_v70.py'
    run(args,'scene-'+tag,codes=(0,1));p=S/'runs'/tag/'comparison.json';d=read(p)
    assert all(a['passed'] and a['exit_code']==0 for a in d['runs']),(tag,d['runs'])
    assert d['comparison']['negative_control']['passed']
    return dict(tag=tag,frames=d['comparison']['frames_compared'],strict=d['passed'],comparison_sha256=sha(p),exe_sha256=d['exe_sha256'])
if __name__=='__main__':
    phase=sys.argv[1]
    if phase=='baseline':
        items=read(S/'scene-pending.json')['fixtures']
        for x in items:
            execute('id-'+x['tag'],x,1)
            a=next(json.loads(l) for l in (S/'runs'/('id-'+x['tag'])/'original/state.jsonl').open(encoding='utf-8') if json.loads(l)['kind']=='state')
            cells={tuple(v//256 for v in z['position'][:2]):z['id'] for z in a['objects']}
            x.update(attacker_id=cells[tuple(x['attacker_cell'])],target_id=cells[tuple(x['target_cell'])]);x['orders']=[f"5:{x['attacker_id']}:1:{x['target_id']}:0"]
        write(S/'scene-recipes.json',dict(passed=True,fixtures=items,calibration_excluded=True))
        with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(lambda x:execute('b-'+x['tag'],x,x['last']),items))
        write(S/'baseline-scenes.json',dict(passed=True,results=values))
        write(S/'baseline-contract.json',dict(passed=True,traces=[dict(tag=v['tag'],mode=m,path=str(S/'runs'/v['tag']/m/'state.jsonl'),sha256=sha(S/'runs'/v['tag']/m/'state.jsonl')) for v in values for m in ['original','generated-c']]))
    elif phase=='final':
        items=read(S/'scene-recipes.json')['fixtures']
        with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(lambda x:execute('f-'+x['tag'],x,x['last']),items))
        write(S/'final-scenes.json',dict(passed=True,results=values))
    elif phase in ['command-baseline','command-final']:
        phase='b' if phase=='command-baseline' else 'f';x=read(S/'scene-recipes.json')['fixtures'][0]
        value=execute(phase+'-rifle-command',x,1500,True);write(S/(phase+'-command-scenes.json'),dict(passed=True,result=value))
    else:raise ValueError(phase)
