"""Five inherited combat effects and six bounded affected production regressions."""
from combat_batch_v70 import *
from concurrent.futures import ThreadPoolExecutor
from damage_scenes_v70 import execute
if sys.argv[1]=='combat':
    items=read(O/'scene-recipes.json')['fixtures']+[read(O/'extra-scene.json')['fixture']]
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(lambda x:execute('old-'+x['tag'],x,1500,True),items))
    write(S/'combat-regressions.json',dict(passed=True,results=values,health_observation_inherited=True,command_only_host=True))
elif sys.argv[1]=='movement':
    text=(R/'run_skirmish_v69.py').read_text(encoding='utf-8').replace('evidence/combat-state-v1','evidence/combat-state-v2');p=R/'run_skirmish_v70.py';assert not p.exists();p.write_text(text,encoding='utf-8',newline='\n')
    jobs=[('default',py(p.name,'--tag','default','--range','0:300'))]
    prior=R/'evidence/movement-state-v67'
    for name in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json']:
        for x in read(prior/name)['fixtures']:
            if 'control' not in x['name']:jobs.append(('reg-'+x['name'],fixture('reg-'+x['name'],x,500,False)))
    p=R/'evidence/movement-state-v68';x=dict(path=(p/'fixtures/stop-free.MAP').relative_to(R).as_posix(),orders=read(p/'stop-command-acceptance.json')['orders'])
    jobs.append(('reg-stop',fixture('reg-stop',x,1800,False)))
    def run_one(job):
        tag,args=job;run(args,'scene-'+tag,codes=(0,1));p=S/'runs'/tag/'comparison.json';d=read(p)
        assert d['passed'] and all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed'],tag
        return dict(tag=tag,frames=d['comparison']['frames_compared'],strict=True,comparison_sha256=sha(p),exe_sha256=d['exe_sha256'])
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(run_one,jobs))
    write(S/'movement-regressions.json',dict(passed=True,results=values,production_recorder_unchanged=True))
else:raise ValueError(sys.argv[1])
