"""Reuse a freed simulation lane only after every production prerequisite passes."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
required=[S/'t-matrix.json',S/'u-additional-matrix.json',S/'auxiliary-final-04/validation.json']
required += [S/'runs'/('b-'+r['name'])/'comparison.json' for r in json.loads((S/'bridge-fixtures.json').read_text(encoding='utf-8'))['fixtures']]
while True:
    ready=True
    for p in required:
        if not p.exists():ready=False;continue
        v=json.loads(p.read_text(encoding='utf-8-sig'));assert v['passed'],str(p)
    if ready:break
    time.sleep(3)
print('Production lane complete; starting internal and tube observers',flush=True)
subprocess.run([sys.executable,'-B',str(R/'run_acceptance_v33.py'),'observer','--only','internal-scenes','tube-scenes'],cwd=R,check=True)
(S/'core-observers-complete.json').write_text(json.dumps(dict(passed=True,internal_and_tube_suites=True),indent=2)+'\n',encoding='utf-8')
