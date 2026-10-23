"""Use the bridge lane only after all alias observations have completed."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
parser=argparse.ArgumentParser();parser.add_argument('--only',choices=['combined-scenes']);selection=parser.parse_args()
if selection.only:
    required=[S/'core-scenes-complete.json',S/'alias-occupied-natural-scenes.json']
    while not all(p.exists() for p in required):time.sleep(3)
    assert all(json.loads(p.read_text(encoding='utf-8'))['passed'] for p in required)
assert json.loads((S/'alias-occupied-natural-scenes.json').read_text(encoding='utf-8'))['passed']
for label,script,args in [('combined-scenes','run_combined_routes_v36.py',[]),('bridge-observer','run_bridge_scenes_v36.py',['observer'])]:
    if selection.only and label!=selection.only:continue
    receipt=S/('delegated-'+label+'.json');assert not receipt.exists()
    print('Starting '+label+' on freed '+('core' if selection.only else 'bridge')+' lane',flush=True)
    with (S/('accept-'+label+'.log')).open('x',encoding='utf-8') as output:
        subprocess.run([sys.executable,'-X','utf8','-B',str(R/script),*args],cwd=R,stdout=output,stderr=subprocess.STDOUT,check=True,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    receipt.write_text(json.dumps(dict(passed=True,job=label,runner=script,runner_sha256=hashlib.sha256((R/script).read_bytes()).hexdigest(),completed_on_freed_bridge_lane=not bool(selection.only),completed_on_freed_core_lane=bool(selection.only),max_scene_lanes=2,max_game_processes=4),indent=2)+'\n',encoding='utf-8')
    print('Completed delegated '+label,flush=True)
