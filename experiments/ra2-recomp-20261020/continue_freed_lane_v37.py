"""Reuse the core lane for the unchanged tall suite only after that lane finishes."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37';ready=S/'core-scenes-complete.json'
while not ready.exists():time.sleep(3)
assert json.loads(ready.read_text(encoding='utf-8'))['passed']
print('Starting delegated tall-scenes on freed core lane',flush=True)
with (S/'accept-tall-scenes.log').open('x',encoding='utf-8') as f:
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/'run_tall_equivalence_v37.py')],cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
(S/'delegated-tall-scenes.json').write_text(json.dumps(dict(passed=True,job='tall-scenes',runner='run_tall_equivalence_v37.py',runner_sha256=hashlib.sha256((R/'run_tall_equivalence_v37.py').read_bytes()).hexdigest(),two_lanes_max=True),indent=2)+'\n',encoding='utf-8')
print('Completed delegated tall-scenes',flush=True)
