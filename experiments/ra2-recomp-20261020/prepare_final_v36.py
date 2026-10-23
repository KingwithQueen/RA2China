"""Wait for immutable part checkpoints, then build observers and all native gates serially."""
from pathlib import Path
import json,os,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
while not (S/'parts/returns-verified/validation.json').exists():time.sleep(3)
assert json.loads((S/'parts/returns-verified/validation.json').read_text(encoding='utf-8'))['passed']
def run(command,log):
    print('Starting '+log,flush=True)
    with (S/log).open('x',encoding='utf-8') as f:p=subprocess.run(command,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:print((S/log).read_text(encoding='utf-8',errors='replace')[-5000:],flush=True);raise RuntimeError(log)
run(['pwsh','-NoProfile','-File',str(R/'build-faithful.ps1')],'build-final-noop.log')
for n in ['extend_observer','make_connection_fixture']:
    run([sys.executable,'-X','utf8','-B',str(R/(n+'_v36.py'))],n+'-final.log')
run(['pwsh','-NoProfile','-File',str(R/'build-connection-fixture-v36.ps1')],'build-final-observer.log')
for n in ['audit_legal_sources','audit_alias_routes','audit_internal_alias_sources','audit_recipe_replay','preflight_movement','audit_inherited_fixtures','audit_fragment_contract']:
    run([sys.executable,'-X','utf8','-B',str(R/(n+'_v36.py'))],n+'-preparation.log')
(S/'final-build-ready.json').write_text(json.dumps(dict(passed=True,all_parts_and_observers_ready=True),indent=2)+'\n',encoding='utf-8')
run([sys.executable,'-X','utf8','-B',str(R/'run_native_gates_v36.py')],'all-native-final.log')
print('Native and build preparation complete',flush=True)
