"""Ordinary Stop cancels active navigation; only a later Move starts it again."""
from run_batch_v68 import *
x=next(z for z in read(S/'scene-recipes.json')['fixtures'] if z['tag']=='stop-free');i=x['actor_ids'][0]
x=dict(x,orders=[f'5:{i}:2:57:76',f'100:{i}:13:0:0',f'350:{i}:2:57:76'])
for label in ['b','f']:
    tag,args=fixture(label+'-stopcmd',x,1800)
    if label=='b':args[4]=R/'run_baseline_fixture_v68.py'
    if not (S/'runs'/tag/'comparison.json').exists():run(args,'scene-'+tag)
    d=read(S/'runs'/tag/'comparison.json');assert d['passed']
    c=next(o for o in d['comparison']['controlled_objects'] if o['id']==i)
    assert c['stop_queued'] and c['stop_executed'] and c['stop_completed'],c
    assert [p//256 for p in c['final_position'][:2]]==[57,76]
for mode in ['original','generated-c']:
    assert sha(S/'runs/b-stopcmd'/mode/'state.jsonl')==sha(S/'runs/f-stopcmd'/mode/'state.jsonl')
    selected={}
    for l in (S/'runs/f-stopcmd'/mode/'state.jsonl').open(encoding='utf-8'):
        d=json.loads(l)
        if d['kind']=='state' and d['frame'] in [200,300,351,1800]:selected[d['frame']]=next(a for a in d['objects'] if a['id']==i)
    assert selected[200]['position']==selected[300]['position']
    assert selected[300]['ground_drive']['destination']==[0,0,0] and selected[300]['ground_drive']['path_directions']==[]
    assert selected[351]['ground_drive']['destination']!=[0,0,0]
write(S/'stop-command-acceptance.json',dict(passed=True,id=i,orders=x['orders'],pairs=2,frames=3602,strict=True,stationary_after_stop_before_new_move=True,queue_and_destination_cleared=True,per_mode_parent_trace_unchanged=True,scope='Ordinary Stop at100 while moving; stationary at200/300, new Move at350, reaches requested cell. No direct state, path or budget manipulation.'))
print(dict(passed=True,stop_cancel_and_new_move=True,pairs=2,frames=3602))
