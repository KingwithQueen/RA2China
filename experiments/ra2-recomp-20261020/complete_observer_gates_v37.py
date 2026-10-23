from pathlib import Path
import os,subprocess,sys,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
jobs=[('caller-audit','audit_overlap_callers_v37.py'),('strict-audit','audit_movement_v37.py'),('budget-audit','audit_default_budget_v37.py'),('tube-audit','audit_connection_v37.py'),('internal-audit','audit_internal_scenes_v37.py'),('tube-regression-origin','record_connection_regression_v37.py')]
if '--remaining' in sys.argv:jobs=jobs[3:]
for label,name in jobs:
 print(json.dumps(dict(starting=label)),flush=True)
 with (S/(label+('-03.log' if '--remaining' in sys.argv else '-02.log'))).open('x',encoding='utf-8') as out:p=subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if p.returncode:
  print((S/(label+('-03.log' if '--remaining' in sys.argv else '-02.log'))).read_text(encoding='utf-8',errors='replace')[-5000:],flush=True);raise RuntimeError(label)
 print(json.dumps(dict(passed=True,completed=label)),flush=True)
