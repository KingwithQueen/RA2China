"""Strict audits read completed traces; failures never become acceptance by omission."""
from pathlib import Path
import argparse,json,os,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
jobs=['audit_overlap_callers_v29.py','audit_movement_v29.py','audit_default_budget_v29.py',
      'audit_connection_v29.py','audit_internal_scenes_v29.py','audit_combined_routes_v29.py','record_connection_regression_v29.py','audit_bridge_scenes_v29.py']
ap=argparse.ArgumentParser();ap.add_argument('--part',choices=['all','core','remaining'],default='all');args=ap.parse_args()
if args.part=='core':jobs=jobs[:5]
elif args.part=='remaining':jobs=jobs[5:]
for name in jobs:
    print(json.dumps(dict(starting=name)),flush=True)
    path=S/('final-'+name.removesuffix('.py')+'.log')
    with path.open('x',encoding='utf-8') as output:
        p=subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,stdout=output,stderr=subprocess.STDOUT,
                         env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:
        print(path.read_text(encoding='utf-8',errors='replace')[-7000:],flush=True)
        raise RuntimeError(name)
    print(json.dumps(dict(passed=True,completed=name)),flush=True)
