"""Run the not-yet-started infantry suites at the end of the owned core lane."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert read(S/'observer-lane-assignment.json')['bridge_infantry_on_core_lane']
out=S/'delegated-bridge-infantry-scenes.json';assert not out.exists()
prerequisites=[S/'runs'/('h3-'+e['name'])/'comparison.json' for e in read(S/'bridge-fixtures.json')['fixtures']]
assert len(prerequisites)==4 and all(read(p)['passed'] and read(p)['exe_sha256']==sha(S/'connection-fixture-probe.exe') for p in prerequisites)
for mode in ['production','observer']:
 with (S/('core-infantry-'+mode+'.log')).open('x',encoding='utf-8') as log:
  subprocess.run([sys.executable,'-X','utf8','-B',str(R/'run_bridge_infantry_v38.py'),mode],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True,env=dict(os.environ,RA2_V38_CORE_INFANTRY='1',PYTHONIOENCODING='utf-8'))
paths=list(prerequisites)
for item in read(S/'bridge-infantry-fixtures.json')['fixtures']:
 for prefix,exe in [('ip-',R/'ra2/build-original-c/ra2.exe'),('ih-',S/'connection-fixture-probe.exe')]:
  p=S/'runs'/(prefix+item['name'])/'comparison.json';v=read(p)
  assert v['passed'] and v['exe_sha256']==sha(exe) and v['comparison']['frames_compared']==901
  paths.append(p)
value=dict(passed=True,job='bridge-infantry-scenes',production_scenes=4,observer_scenes=4,frames=7208,completed_on_owned_core_lane=True,starts_after_core_bridge_observer=True,max_scene_lanes=2,max_game_processes=4,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'run_bridge_infantry_v38.py',S/'observer-lane-assignment.json']+paths])
out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,core_infantry_scenes=8))
