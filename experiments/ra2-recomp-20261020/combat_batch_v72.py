"""Combat batch4 / formal71 / verification72: protected fixed-frame acceptance."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent
S=R/'evidence/combat-state-v4';O=R/'evidence/combat-state-v3'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','-c','core.quotepath=false',*args],cwd=P)
def run(args,name,codes=(0,)):
    p=S/(name+'.log');assert not p.exists(),p;print('Starting '+name,flush=True)
    with p.open('x',encoding='utf-8') as f:q=subprocess.run([str(a) for a in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if q.returncode not in codes:
        print(p.read_text(encoding='utf-8',errors='replace')[-4500:],flush=True);raise RuntimeError(name)
    return p
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def fixture(tag,x,last=1500,observer=True):
    args=py('run_combat_observer_v72.py' if observer else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','480','--range','0:'+str(last),'--scenario-map',R/x['path'])
    if x.get('rules'):args+=['--scenario-rules',R/x['rules']]
    if x.get('art'):args+=['--scenario-art',R/x['art']]
    for a in x.get('orders',[]):args+=['--order',a]
    return args
