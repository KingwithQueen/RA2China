from pathlib import Path
import os,subprocess,sys,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
jobs=[('tube-observer-r3','run_tube_scenes_v26.py'),('internal-observer-r4','run_internal_scenes_v26.py'),('auxiliary-gates','run_movement_v26_auxiliary.py'),('strict-audit','audit_movement_v26.py'),('budget-audit','audit_default_budget_v26.py'),('tube-audit','audit_connection_v26.py'),('internal-audit','audit_internal_scenes_v26.py'),('tube-regression-origin','record_connection_regression_v26.py')]
for label,name in jobs:
 print(json.dumps(dict(starting=label)),flush=True)
 with (S/(label+'.log')).open('x',encoding='utf-8') as out:p=subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if p.returncode:
  print((S/(label+'.log')).read_text(encoding='utf-8',errors='replace')[-5000:],flush=True);raise RuntimeError(label)
 print(json.dumps(dict(passed=True,completed=label)),flush=True)
