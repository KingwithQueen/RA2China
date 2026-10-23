"""All28 aliases across six ordinary north/south staggered-exit traffic scene pairs."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36';items=json.loads((S/'bridge-staggered-fixtures.json').read_text(encoding='utf-8'))['fixtures']
for group in range(6):
    item=items[group%2];tag='ao-'+str(group);args=[sys.executable,'-X','utf8','-B',str(R/'run_occupied_alias_probe_v36.py'),'--tag',tag,'--evidence-stage','movement-state-v36','--movement-audit','--seconds','240','--range','0:900','--scenario-map',str(R/item['path'])]
    for order in item['orders']:args+=['--order',order]
    with (S/(tag+'.log')).open('x',encoding='utf-8') as f:subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
    assert json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'))['passed']
    print(dict(passed=True,tag=tag,frames=901),flush=True)
subprocess.run([sys.executable,'-X','utf8','-B',str(R/'audit_occupied_alias_v36.py')],cwd=R,check=True)
