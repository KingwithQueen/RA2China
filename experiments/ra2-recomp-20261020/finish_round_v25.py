"""Complete the final integration before running independent acceptance suites."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v25'
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
assert json.loads((S/'parts/internal-verified/validation.json').read_text(encoding='utf-8'))['passed']
run('integrate-passage',python('integrate_travel_v25.py','passage'))
run('build-passage',shell('build-faithful.ps1'))
run('part-passage-scenes',python('run_lifecycle_part_v25.py','passage'))
run('build-content-noop',shell('build-faithful.ps1'))
run('make-observer',python('make_connection_fixture_v25.py'))
run('build-observer',shell('build-connection-fixture-v25.ps1'))
run('structure-preflight',python('preflight_movement_v25.py'))
jobs=[('production-matrix',python('run_movement_v25_matrix.py','t-')),
 ('additional-scenes',python('run_scenes_v25.py','u-')),
 ('tube-observer-scenes',python('run_tube_scenes_v25.py'))]
with ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(lambda item:run(*item),jobs):pass
run('auxiliary-gates',python('run_movement_v25_auxiliary.py'))
for label,script in [('strict-audit','audit_movement_v25.py'),('budget-audit','audit_default_budget_v25.py'),('tube-audit','audit_connection_v25.py'),('tube-regression-origin','record_connection_regression_v25.py')]:run(label,python(script))
print(json.dumps(dict(passed=True,final_gates_passed=True,promotion_pending=True)),flush=True)
