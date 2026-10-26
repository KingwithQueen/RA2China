"""Eight inherited battle scenes and six bounded production movement regressions."""
from combat_batch_v72 import *
from lifecycle_scenes_v72 import execute
from concurrent.futures import ThreadPoolExecutor
if sys.argv[1]=='combat':
    previous=R/'evidence/combat-state-v1';items=[]
    for x in read(previous/'scene-recipes.json')['fixtures']+[read(previous/'extra-scene.json')['fixture']]:items.append((x,previous,'f-'+x['tag']))
    for x in read((R/'evidence/combat-state-v2')/'scene-recipes.json')['fixtures']:items.append((x,R/'evidence/combat-state-v2','f-'+x['tag']))
    def one(item):
        x,parent,oldtag=item;value=execute('old-'+x['tag'],x,1500,True);value.update(parent_stage=str(parent),parent_tag=oldtag);return value
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,items))
    write(S/'combat-regressions.json',dict(passed=True,results=values,command_only_host=True))
elif sys.argv[1]=='movement':
    text=(R/'run_skirmish_v71.py').read_text(encoding='utf-8').replace('evidence/combat-state-v3','evidence/combat-state-v4');p=R/'run_skirmish_v72.py';assert not p.exists();p.write_text(text,encoding='utf-8',newline='\n')
    jobs=[('default',py(p.name,'--tag','default','--range','0:300'))];prior=R/'evidence/movement-state-v67'
    for name in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json']:
        for x in read(prior/name)['fixtures']:
            if 'control' not in x['name']:jobs.append(('reg-'+x['name'],fixture('reg-'+x['name'],x,500,False)))
    p=R/'evidence/movement-state-v68';x=dict(path=(p/'fixtures/stop-free.MAP').relative_to(R).as_posix(),orders=read(p/'stop-command-acceptance.json')['orders']);jobs.append(('reg-stop',fixture('reg-stop',x,1800,False)))
    def one(job):
        tag,args=job;run(args,'scene-'+tag,codes=(0,1));p=S/'runs'/tag/'comparison.json';d=read(p);assert d['passed'] and d['comparison']['negative_control']['passed'] and all(x['passed'] and x['exit_code']==0 for x in d['runs']),tag
        return dict(tag=tag,frames=d['comparison']['frames_compared'],strict=True,comparison_sha256=sha(p),exe_sha256=d['exe_sha256'])
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,jobs))
    write(S/'movement-regressions.json',dict(passed=True,results=values,production_recorder_unchanged=True))
else:raise ValueError(sys.argv[1])
