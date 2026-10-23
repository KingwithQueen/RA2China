"""Promote only after both simulation lanes and the last strict audits finish."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
required=[S/'core-observers-complete.json']
required += [S/'runs'/('h3-'+r['name'])/'comparison.json' for r in json.loads((S/'bridge-fixtures.json').read_text(encoding='utf-8'))['fixtures']]
while True:
    ready=True
    for p in required:
        if not p.exists():ready=False;continue
        assert json.loads(p.read_text(encoding='utf-8-sig'))['passed'],str(p)
    if ready:break
    time.sleep(3)
commands=[['run_final_audits_v32.py','--only','audit_connection_v32.py','record_connection_regression_v32.py','audit_bridge_scenes_v32.py'],
          ['audit_inherited_fixtures_v32.py'],['finalize_movement_v32.py']]
for args in commands:
    print('Starting '+args[0],flush=True)
    subprocess.run([sys.executable,'-B',str(R/args[0]),*args[1:]],cwd=R,check=True)
print('Formal generation31 complete; staging and local commit remain separately audited',flush=True)
