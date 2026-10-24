"""Wait for both complete scene lanes and the full current native suite."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
required=[S/n for n in ['core-scenes-complete.json','bridge-scenes-complete.json','native-gates.json']]
while not all(p.exists() for p in required):time.sleep(3)
assert all(json.loads(p.read_text(encoding='utf-8'))['passed'] for p in required)
jobs=['audit_overlap_callers','audit_movement','audit_default_budget','audit_connection','audit_internal_scenes','audit_combined_routes','record_connection_regression','audit_bridge_scenes','audit_bridge_mixed','audit_bridge_hostile','audit_scene_totals','audit_bridge_infantry','audit_alias_runtime']
if not (S/'new-fragment-contract.json').exists():jobs.insert(0,'audit_fragment_contract')
jobs+=['record_remaining','finalize_movement']
if '--resume-after-overlap' in sys.argv:
    assert json.loads((S/'overlap-caller-identity.json').read_text(encoding='utf-8'))['passed']
    jobs.remove('audit_overlap_callers')
for name in jobs:
    print('Starting '+name,flush=True)
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/(name+'_v38.py'))],cwd=R,check=True)
print('Generation37 accepted; local commit remains',flush=True)
