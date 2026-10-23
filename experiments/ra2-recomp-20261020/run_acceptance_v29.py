"""Keep shared native compilers serial; execute independent scene suites separately."""
from pathlib import Path
import argparse, json, os, subprocess, sys
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
ap=argparse.ArgumentParser();ap.add_argument('suite',choices=['production','observer','native']);a=ap.parse_args()
jobs = {
    'production': [                   ('production-matrix',[sys.executable,'-B',str(R/'run_movement_v29_matrix.py'),'t-']),
                   ('additional-matrix',[sys.executable,'-B',str(R/'run_scenes_v29.py'),'u-']),
                   ('auxiliary',[sys.executable,'-B',str(R/'run_movement_v29_auxiliary.py')])],
    'native': [('native-all',[sys.executable,'-B',str(R/'run_native_gates_v29.py')])],
    'observer': [                 ('internal-scenes',[sys.executable,'-B',str(R/'run_internal_scenes_v29.py')]),
                 ('tube-scenes',[sys.executable,'-B',str(R/'run_tube_scenes_v29.py')]),
                 # The old tall runner expects both routes to complete, but the original west route stalls.
                 # This runner preserves that distinction and leaves the old investigation unchanged.
                 ('tall-scenes',[sys.executable,'-B',str(R/'run_tall_equivalence_v29.py')]),
                 ('combined-scenes',[sys.executable,'-B',str(R/'run_combined_routes_v29.py')])]
}[a.suite]
for label, command in jobs:
    print(json.dumps(dict(starting=label)),flush=True)
    path=S/('accept-'+label+'.log')
    with path.open('x',encoding='utf-8') as output:
        p=subprocess.run(command,cwd=R,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:
        print(path.read_text(encoding='utf-8',errors='replace')[-7000:],flush=True)
        raise RuntimeError(label)
    print(json.dumps(dict(passed=True,completed=label)),flush=True)
