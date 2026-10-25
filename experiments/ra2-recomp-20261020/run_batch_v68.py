"""Movement closeout: finite functional acceptance and explicit inherited limits."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent
S=R/'evidence/movement-state-v68';O=R/'evidence/movement-state-v67'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name,codes=(0,)):
    log=S/(name+'.log');assert not log.exists(),log
    print('Starting '+name,flush=True)
    with log.open('x',encoding='utf-8') as f:
        q=subprocess.run([str(a) for a in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if q.returncode not in codes:
        print(log.read_text(encoding='utf-8',errors='replace')[-5000:],flush=True)
        raise RuntimeError(name)
    return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def git(*args):return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','-c','core.quotepath=false',*args],cwd=P)
def fixture(tag,item,last,observer=False):
    args=py('run_bridge_catalog_v68.py' if observer else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','600','--range','0:'+str(last),'--scenario-map',R/item['path'])
    if item.get('rules'):args+=['--scenario-rules',R/item['rules']]
    for order in item.get('orders',[]):args+=['--order',order]
    return tag,args
