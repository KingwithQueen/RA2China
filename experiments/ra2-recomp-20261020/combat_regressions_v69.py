"""Finite affected regressions through the unchanged production recorder."""
from combat_batch_v69 import *
from concurrent.futures import ThreadPoolExecutor
p=R/'run_skirmish_v69.py'
t=(R/'run_skirmish_v68.py').read_text(encoding='utf-8').replace('evidence/movement-state-v68','evidence/combat-state-v1')
assert not p.exists();p.write_text(t,encoding='utf-8',newline='\n')
jobs=[('default',py(p.name,'--tag','default','--range','0:300'))]
parent=R/'evidence/movement-state-v67'
for name in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json']:
    for x in read(parent/name)['fixtures']:
        if 'control' not in x['name']:jobs.append(('reg-'+x['name'],fixture('reg-'+x['name'],x,500,False)))
orders=read(O/'stop-command-acceptance.json')['orders'];x=dict(path=(O/'fixtures/stop-free.MAP').relative_to(R).as_posix(),orders=orders)
jobs.append(('reg-stop',fixture('reg-stop',x,1800,False)))
def execute(job):
    tag,args=job;run(args,'scene-'+tag,codes=(0,1));p=S/'runs'/tag/'comparison.json';d=read(p)
    assert d['passed'] and d['comparison']['negative_control']['passed'] and all(a['passed'] and a['exit_code']==0 for a in d['runs']),(tag,d.get('comparison',{}).get('first_difference'))
    return dict(tag=tag,frames=d['comparison']['frames_compared'],strict=True,comparison_sha256=sha(p),exe_sha256=d['exe_sha256'])
with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(execute,jobs))
write(S/'regressions.json',dict(passed=True,results=values,production_recorder_unchanged=True,scope='Default skirmish, two bridge crossings, train/crush contact, ordinary Stop and new Move. Earlier movement evidence inherited, not re-counted.'))
