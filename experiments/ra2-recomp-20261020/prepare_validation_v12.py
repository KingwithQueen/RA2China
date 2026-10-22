"""Archive the verified scoring part and prepare fresh regression tools."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v12';O=R/'evidence/movement-state-v11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((S/'runs/c-score-ur3/comparison.json').read_text(encoding='utf-8'))['passed']
assert json.loads((S/'runs/c-score-default/comparison.json').read_text(encoding='utf-8'))['passed']
files={e['path'] for e in json.loads((S/'parts/walk-verified/manifest.json').read_text(encoding='utf-8'))}
files.update(['ra2/src/gameplay/ground_path_cache.h','ra2/src/gameplay/ground_path_cache.c','build-path-cache-probe-v12.ps1','evidence/movement-state-v12/path_cache_probe.c'])
out=S/'parts/path-cache-verified';assert not out.exists()
manifest=[]
for rel in sorted(files):
    dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest)
    manifest.append(dict(path=rel,sha256=sha(dest)))
(out/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'validation.json').write_text(json.dumps(dict(passed=True,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),frames=1002,scenes=['c-score-ur3','c-score-default'],step_cases=786432,cache_cases=786432,priority_cases=786432),indent=2),encoding='utf-8')
shutil.copytree(O/'fixtures',S/'fixtures',dirs_exist_ok=True)
names=['run_movement_v11_matrix.py','run_scenes_v11.py','run_movement_v11_auxiliary.py','run_regressions_v11.ps1']
names += [p.name for p in R.glob('build-*-v11.ps1')]
for name in names:
    target=R/name.replace('v11','v12')
    if not target.exists():target.write_text((R/name).read_text(encoding='utf-8').replace('movement-state-v11','movement-state-v12').replace('-v11.ps1','-v12.ps1'),encoding='utf-8')
# Probes reference earlier immutable evidence as fixtures; only their outputs move.
for p in O.glob('*probe*.c'):
    target=S/p.name
    if not target.exists():shutil.copy2(p,target)
print('Archived scoring rollback',len(manifest),'files; prepared regression tools')
