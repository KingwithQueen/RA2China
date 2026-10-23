"""Keep shared native compilers serial; execute independent scene suites separately."""
from pathlib import Path
import argparse, json, os, subprocess, sys, time
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v35'
ap=argparse.ArgumentParser();ap.add_argument('suite',choices=['production','observer','native']);ap.add_argument('--only',nargs='+');a=ap.parse_args()
if a.suite=='observer' and a.only==['tall-scenes'] and (S/'observer-lane-assignment.json').exists():
    assignment=json.loads((S/'observer-lane-assignment.json').read_text(encoding='utf-8'))
    if assignment.get('free_bridge_jobs'):
        subprocess.run([sys.executable,'-X','utf8','-B',str(R/'complete_freed_bridge_v35.py')],cwd=R,check=True)
jobs = {
    'production': [                   ('production-matrix',[sys.executable,'-B',str(R/'run_movement_v35_matrix.py'),'t-']),
                   ('additional-matrix',[sys.executable,'-B',str(R/'run_scenes_v35.py'),'u-']),
                   ('auxiliary',[sys.executable,'-B',str(R/'run_movement_v35_auxiliary.py')]),('bridge-production',[sys.executable,'-B',str(R/'run_bridge_scenes_v35.py'),'production'])],
    'native': [('native-all',[sys.executable,'-B',str(R/'run_native_gates_v35.py')])],
    'observer': [                 ('internal-scenes',[sys.executable,'-B',str(R/'run_internal_scenes_v35.py')]),
                 ('tube-scenes',[sys.executable,'-B',str(R/'run_tube_scenes_v35.py'),'--serial']),
                 # The old tall runner expects both routes to complete, but the original west route stalls.
                 # This runner preserves that distinction and leaves the old investigation unchanged.
                 ('tall-scenes',[sys.executable,'-B',str(R/'run_tall_equivalence_v35.py')]),
                 ('combined-scenes',[sys.executable,'-B',str(R/'run_combined_routes_v35.py')]),('bridge-observer',[sys.executable,'-B',str(R/'run_bridge_scenes_v35.py'),'observer'])]
}[a.suite]
if a.only:
    assert set(a.only)<=set(label for label,_ in jobs)
    jobs=[job for job in jobs if job[0] in a.only]
for label, command in jobs:
    assignment=S/'observer-lane-assignment.json'
    if a.suite=='observer' and assignment.exists() and label in json.loads(assignment.read_text(encoding='utf-8'))['delegated_jobs']:
        receipt=S/('delegated-'+label+'.json')
        while not receipt.exists():time.sleep(3)
        value=json.loads(receipt.read_text(encoding='utf-8'));assert value['passed'] and value['job']==label
        print(json.dumps(dict(passed=True,completed=label,completed_on_delegated_lane=True)),flush=True)
        continue
    print(json.dumps(dict(starting=label)),flush=True)
    path=S/('accept-'+label+'.log')
    with path.open('x',encoding='utf-8') as output:
        p=subprocess.run(command,cwd=R,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:
        print(path.read_text(encoding='utf-8',errors='replace')[-7000:],flush=True)
        raise RuntimeError(label)
    print(json.dumps(dict(passed=True,completed=label)),flush=True)
