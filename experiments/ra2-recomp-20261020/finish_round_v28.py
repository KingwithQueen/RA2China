"""Complete the final integration before running independent acceptance suites."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v28'
def python(name,*args):return [sys.executable,'-B',str(R/name),*args]
def shell(name):return ['pwsh','-NoProfile','-File',str(R/name)]
def run(label,command):
 print(json.dumps(dict(starting=label)),flush=True)
 with (S/(label+'.log')).open('x',encoding='utf-8') as out:
  p=subprocess.run(command,cwd=R,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING="utf-8"))
 if p.returncode:
  print((S/(label+'.log')).read_text(encoding='utf-8',errors='replace')[-6000:],flush=True)
  raise RuntimeError(label+' failed')
 print(json.dumps(dict(passed=True,completed=label)),flush=True)
assert json.loads((S/'parts/passage-verified/validation.json').read_text(encoding='utf-8'))['passed']
assert json.loads((S/'parts/returns-verified/validation.json').read_text(encoding='utf-8'))['passed']
run('build-content-noop',shell('build-faithful.ps1'))
run('structure-preflight',python('preflight_movement_v28.py'))
run('production-matrix',python('run_movement_v28_matrix.py','t-'))
run('additional-scenes',python('run_scenes_v28.py','u-'))
run('auxiliary-gates',python('run_movement_v28_auxiliary.py'))
print(json.dumps(dict(passed=True,production_gates_passed=True,strict_audits_pending=True)),flush=True)
