"""Naturally exercise additional alias candidates without any forced target calls."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
recipes={r['name']:r for r in json.loads((S/'bridge-mixed-fixtures.json').read_text(encoding='utf-8'))['fixtures']}
for group,name in [('a','traffic-north'),('b','traffic-south'),('c','mixed-north')]:
    tag='al-'+group;item=recipes[name]
    args=[sys.executable,'-X','utf8','-B',str(R/'run_alias_probe_v30.py'),'--tag',tag,'--evidence-stage','movement-state-v30',
        '--movement-audit','--seconds','240','--range','0:900','--scenario-map',str(R/item['path'])]
    for order in item['orders']:args+=['--order',order]
    with (S/(tag+'.log')).open('x',encoding='utf-8') as output:result=subprocess.run(args,cwd=R,stdout=output,stderr=subprocess.STDOUT)
    value=json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'));assert result.returncode==0 and value['passed'],tag
    print(json.dumps(dict(passed=True,tag=tag,frames=901)),flush=True)
