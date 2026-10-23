"""Serial probe compilation and at most two scene lanes, with separate final audit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import os,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
jobs=[('preparation',['prepare_final_v36.py']),('core',['run_final_scenes_v36.py','core']),('bridge',['run_final_scenes_v36.py','bridge']),('acceptance',['finish_acceptance_v36.py'])]
def run(job):
    name,args=job
    with (S/('queue-'+name+'.log')).open('x',encoding='utf-8') as out:
        p=subprocess.run([sys.executable,'-X','utf8','-B',str(R/args[0]),*args[1:]],cwd=R,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:
        print((S/('queue-'+name+'.log')).read_text(encoding='utf-8',errors='replace')[-5000:],flush=True)
    print(name+' finished '+str(p.returncode),flush=True)
    return name,p.returncode
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,jobs))
assert all(code==0 for _,code in results),results
print('All acceptance queues complete; local commit remains',flush=True)
